import json
import yaml
import logging
from pathlib import Path
from ..process_results import Result
from ..utils import constants
import re

def parse_conda_environment_file(file_path, metadata_result: Result, source):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logging.warning(f"Could not parse environment.yml {file_path}: {e}")
        return metadata_result

    # Validación mínima
    if not isinstance(data, dict) or "dependencies" not in data:
        return metadata_result

    if Path(file_path).name.lower() in {"environment.yml", "environment.yaml"}:
        metadata_result.add_result(
            constants.CAT_HAS_PACKAGE_FILE,
            {
                "value": source,
                "type": constants.URL,
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )

    name = data.get("name")
    # not sure about this channels. I doubt they are relevant for the metadata in somef. 
    channels = data.get("channels", [])
    dependencies = data.get("dependencies", [])

    conda_deps = []
    pip_deps = []

    for dep in dependencies:
        if isinstance(dep, str):
            conda_deps.append(dep)
        elif isinstance(dep, dict) and "pip" in dep:
            pip_deps.extend(dep["pip"])

    # conda dependencies
    for dep in conda_deps:
        dep_dict = {
            "value": dep,
            "name": re.split(r"[=<>!]", dep)[0],
            "type": constants.SOFTWARE_APPLICATION,
            "dependency_type": "conda"
        }

        match = re.search(r"[=<>!]+(.+)", dep)
        if match:
            dep_dict["version"] = match.group(1)

        metadata_result.add_result(
            constants.CAT_REQUIREMENTS,
            dep_dict,
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
    # pip dependdencies
    for dep in pip_deps:

        dep_dict = {
            "value": dep,
            "name": re.split(r"[=<>!~]", dep)[0],
            "type": constants.SOFTWARE_APPLICATION,
            "dependency_type": "pip"
        }

        match = re.search(r"[=<>!~]+(.+)", dep)
        if match:
            dep_dict["version"] = match.group(1)

        metadata_result.add_result(
            constants.CAT_REQUIREMENTS,
            dep_dict,
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
    
    return metadata_result
