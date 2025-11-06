# -*- coding: utf-8 -*-
import tomli
from pathlib import Path
import re
import logging
from somef.process_results import Result
from somef.utils import constants

def parse_project_toml(file_path, metadata_result: Result, source):
    """
    Parse a Project.toml file to extract metadata.

    Parameters
    ----------
    file_path: path to the Project.toml file being analyzed
    metadata_result: Metadata object dictionary
    source: source of the package file (URL)

    Returns
    -------
    """
    try:
        if Path(file_path).name in ["Project.toml"]:
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    "value": "Project.toml",
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        with open(file_path, "rb") as f:
            data = tomli.load(f)

            if "name" in data:
                metadata_result.add_result(
                    constants.CAT_PACKAGE_ID,
                    {
                        "value": data["name"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "compat" in data:
                compat = data["compat"]
                for package_name, version in compat.items():
                    metadata_result.add_result(
                        constants.CAT_RUNTIME_PLATFORM,
                        {
                            "value": f"{package_name}",
                            "package": package_name,
                            "version": version,
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "version" in data:
                metadata_result.add_result(
                    constants.CAT_VERSION,
                    {
                        "value": data["version"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "uuid" in data:
                metadata_result.add_result(
                    constants.CAT_IDENTIFIER,
                    {
                        "value": data["uuid"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "deps" in data:
                deps = data["deps"]
                for req in deps.keys():
                    metadata_result.add_result(
                        constants.CAT_REQUIREMENTS,
                        {
                            "value": req,
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "authors" in data:
                authors = data["authors"]
                for auth in authors:
                    match = re.match(r'^(.+?)\s*<(.+?)>$', auth.strip())

                    if match:
                        author_name = match.group(1).strip()
                        author_email = match.group(2).strip()

                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            {
                                "value": author_name,
                                "name": author_name,
                                "email": author_email,
                                "type": constants.AGENT
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                    else:
                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            {
                                "value": auth.strip(),
                                "name": auth.strip(),
                                "type": constants.AGENT
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )


    except Exception as e:
        logging.error(f"Error parsing Project.toml file {file_path}: {str(e)}")

    return metadata_result