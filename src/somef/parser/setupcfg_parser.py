import re
import os
import logging
import configparser
from pathlib import Path
from ..process_results import Result
from ..utils import constants
from ..regular_expressions import detect_license_spdx, detect_spdx_from_declared

def parse_setup_cfg(file_path, metadata_result: Result, source):
    """
    Parser for setup.cfg files. Very similar to the one for pyproject.toml, but using configparser instead of toml library.
    """

    try:
        metadata_result.add_result(
            constants.CAT_HAS_PACKAGE_FILE,
            {"value": source, "type": constants.URL},
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )

        config = configparser.ConfigParser()
        config.read(file_path, encoding="utf-8")

        metadata = dict(config["metadata"]) if "metadata" in config else {}
        options = dict(config["options"]) if "options" in config else {}

        if "name" in metadata:
            metadata_result.add_result(
                constants.CAT_PACKAGE_ID,
                {"value": metadata["name"], "type": constants.STRING},
                1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
            )

        if "version" in metadata:
            version_value = metadata["version"]
            if not version_value.startswith("attr:"):
                metadata_result.add_result(
                    constants.CAT_VERSION,
                    {"value": version_value, "type": constants.RELEASE, "tag": version_value},
                    1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
                )

        if "description" in metadata:
            metadata_result.add_result(
                constants.CAT_DESCRIPTION,
                {"value": metadata["description"], "type": constants.STRING},
                1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
            )

        if "author" in metadata or "author_email" in metadata:
            author_data = {
                "name": metadata.get("author"),
                "email": metadata.get("author_email"),
                "type": constants.AGENT,
                "value": metadata.get("author")
            }
            metadata_result.add_result(
                constants.CAT_AUTHORS, author_data,
                1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source

        if "license" in metadata:
            license_value = metadata["license"]
            license_info_spdx = detect_spdx_from_declared(license_value)
            if not license_info_spdx:
                license_info_spdx = detect_license_spdx(license_value, 'JSON')
            if license_info_spdx:
                license_data = {
                    "value": license_value,
                    "spdx_id": license_info_spdx.get('spdx_id'),
                    "name": license_info_spdx.get('name'),
                    "type": constants.LICENSE
                }
            else:
                license_data = {"value": license_value, "type": constants.LICENSE}

            metadata_result.add_result(
                constants.CAT_LICENSE, license_data,
                1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
            )
            
        if "keywords" in metadata:
            for kw in re.split(r'[,\n]', metadata["keywords"]):
                kw = kw.strip()
                if kw:
                    metadata_result.add_result(
                        constants.CAT_KEYWORDS,
                        {"value": kw, "type": constants.STRING},
                        1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
                    )

        if "url" in metadata:
            metadata_result.add_result(
                constants.CAT_HOMEPAGE,
                {"value": metadata["url"], "type": constants.URL},
                1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
            )

        if "install_requires" in options:
            for req in options["install_requires"].strip().splitlines():
                req = req.strip()
                if req:
                    name, version = parse_dependency(req)
                    if name:
                        metadata_result.add_result(
                            constants.CAT_REQUIREMENTS,
                            {
                                "value": req,
                                "name": name,
                                "version": version,
                                "type": constants.SOFTWARE_DEPENDENCY,
                                "dependency_type": constants.DEPENDENCY_TYPE_RUNTIME,
                                "dependency_resolver": "python"
                            },
                            1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
                        )

        if "setup_requires" in options:
                for req in options["setup_requires"].strip().splitlines():
                    req = req.strip()
                    if req:
                        name, version = parse_dependency(req)
                        if name:
                            metadata_result.add_result(
                                constants.CAT_REQUIREMENTS,
                                {
                                    "value": req,
                                    "name": name,
                                    "version": version,
                                    "type": constants.SOFTWARE_DEPENDENCY,
                                    "dependency_type": constants.DEPENDENCY_TYPE_DEVELOPMENT,
                                    "dependency_resolver": "python"
                                },
                                1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
                            )

        if "python_requires" in options:
            metadata_result.add_result(
                constants.CAT_RUNTIME_PLATFORM,
                {
                    "value": f"Python{options['python_requires']}",
                    "name": "Python",
                    "version": options["python_requires"],
                    "type": constants.STRING
                },
                1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
            )

        if "project_urls" in metadata:
            lines = metadata["project_urls"].split('\n')
            for line in lines:
                if '=' in line:
                    label, url_val = [part.strip() for part in line.split('=', 1)]
                    label_lower = label.lower()
                    
                    if label_lower in ["documentation", "docs", "doc"]:
                        metadata_result.add_result(
                            constants.CAT_DOCUMENTATION,
                            {"value": url_val, "type": constants.URL},
                            1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
                        )
                    
                    elif label_lower in ["repository", "source", "code"]:
                         metadata_result.add_result(
                            constants.CAT_CODE_REPOSITORY,
                            {"value": url_val, "type": constants.URL},
                            1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source
                        )

    except Exception as e:
        logging.error(f"Error parsing setup.cfg file {file_path}: {str(e)}")

    return metadata_result

def parse_dependency(dependency_str):
    """Parse a dependency string to extract name and version."""
    if not dependency_str:
        return None, None

    parts = re.split(r'(>=|<=|==|!=|>|<|~=)', dependency_str, 1)
    name = parts[0].strip()
    if len(parts) > 1:
        version = ''.join(parts[1:])
    else:
        version = ""

    version = re.sub(r'[\[\]]', '', version)

    return name, version