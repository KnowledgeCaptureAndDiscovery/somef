import logging
import re
import shlex
from ..process_results import Result
from ..utils import constants

def _split_docker_reference(ref):
    """Split a docker image reference into its components."""

    digest = None
    if "@" in ref:
        ref, digest = ref.split("@", 1)
    registry = None
    parts = ref.split("/")
    if len(parts) > 1 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost"):
        registry, ref = parts[0], "/".join(parts[1:])
    tag = None
    if ":" in ref.rsplit("/", 1)[-1]:
        ref, tag = ref.rsplit(":", 1)
    return ref, tag, registry, digest


def _find_docker_image_token(sub, tokens):
    """Find the token that holds the image in a tokenized docker command"""

    flags = constants.DOCKER_FLAGS_WITH_VALUE[sub]
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.startswith("-"):
            if sub == "build" and t.startswith("--tag="):
                return t.split("=", 1)[1]
            if "=" in t:
                i += 1
            elif t in flags:
                if sub == "build" and t in constants.DOCKER_BUILD_TAG_FLAGS:
                    return tokens[i + 1] if i + 1 < len(tokens) else None
                i += 2                            # skip the flag and its value
            else:
                i += 1
            continue
        if sub != "build":
            return t                              # run/pull: first non-flag token is the image
        i += 1                                    # build: the image comes from -t
    return None


def detect_docker_commands(readme_unfiltered_text):
    """
    Detect docker run/pull/build commands in the code blocks of a README.
    The result is an intermediate structure, independent of the output format.
    """
    found = []
    seen = set()
    # Join multi-line commands (trailing backslash) and scan every line,
    # not only fenced blocks: many READMEs use 4-space indented code blocks.
    text = re.sub(constants.REGEXP_LINE_CONTINUATION, " ", readme_unfiltered_text)
    for line in text.splitlines():
        m = re.match(constants.REGEXP_DOCKER_CLI_CMD, line, re.IGNORECASE)
        if not m:
            continue
        sub = m.group("sub").lower()
        raw = " ".join(m.group("cmd").split())
        if raw in seen:
            continue
        try:
            tokens = shlex.split(m.group("cmd"))[2:]
        except ValueError:
            continue
        ref = _find_docker_image_token(sub, tokens)
        if not ref or not re.match(constants.REGEXP_DOCKER_CLI_IMAGE_REF, ref, re.IGNORECASE):
            continue
        # Skip template commands (e.g. "docker run -it [container name]") whose
        # candidate image is a bare word: no namespace, no tag.
        if any(c in m.group("cmd") for c in "[<{$") and "/" not in ref and ":" not in ref:
            continue
        seen.add(raw)
        name, tag, registry, digest = _split_docker_reference(ref)
        found.append({
            "subcommand": sub,
            "raw_command": raw,
            "reference": ref,
            "name": name,
            "tag": tag,
            "registry": registry,
            "digest": digest,
        })
    return found


def extract_containers(unfiltered_text, repository_metadata: Result, readme_source) -> Result:
    """
    Add the container category from the docker commands found in the README.
    Commands are grouped by registry + name + tag. For each image, the first "run" and the first "build" command are kept
    """
    grouped = {}
    for cmd in detect_docker_commands(unfiltered_text):
        key = (cmd["registry"], cmd["name"], cmd["tag"])
        entry = grouped.setdefault(key, {
            "value": cmd["reference"],
            "image": f"{cmd['registry']}/{cmd['name']}" if cmd["registry"] else cmd["name"],
            "tag": cmd["tag"],
            "run": None,
            "build": None,
        })
        if cmd["subcommand"] == "run" and entry["run"] is None:
            entry["run"] = cmd["raw_command"]
        elif cmd["subcommand"] == "build" and entry["build"] is None:
            entry["build"] = cmd["raw_command"]

    for entry in grouped.values():
        result = {
            constants.PROP_TYPE: constants.STRING,
            constants.PROP_VALUE: entry["value"],
            constants.PROP_IMAGE: entry["image"],
        }
        if entry["tag"]:
            result[constants.PROP_TAG] = entry["tag"]
        if entry["run"]:
            result[constants.PROP_EXECUTION_COMMAND] = entry["run"]
        if entry["build"]:
            result[constants.PROP_BUILD_COMMAND] = entry["build"]
        repository_metadata.add_result(constants.CAT_CONTAINER, result, 1,
                                       constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
    logging.info(f"Extracted {len(grouped)} container image(s) from README")
    return repository_metadata