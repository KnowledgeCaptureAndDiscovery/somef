import json
import logging
import os
from pathlib import Path
from ..process_results import Result
from ..utils import constants
from ..regular_expressions import detect_license_spdx

def parse_bower_json_file(file_path, metadata_result: Result, source):
    """

    Parameters
    ----------
    file_path: path of the bower file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the package file (URL)

    Returns
    -------

    """
    try:
        if Path(file_path).name.lower() in ["bower.json"]:
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    "value": "bower.json",
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                if "name" in data:
                    metadata_result.add_result(
                        constants.CAT_NAME,
                        {
                            "value": data["name"],
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                if "description" in data:
                    metadata_result.add_result(
                        constants.CAT_DESCRIPTION,
                        {
                            "value": data["description"],
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                if "homepage" in data:
                    home = data["homepage"]
                    if home and home.strip():
                        metadata_result.add_result(
                            constants.CAT_HOMEPAGE,
                            {
                                "value": data["homepage"],
                                "type": constants.URL
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
                            "type": constants.RELEASE,
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                if "authors" in data:
                    authors_data = data["authors"]
                    if isinstance(authors_data, str):
                        authors_list = [a.strip() for a in authors_data.split(",") if a.strip()]
                    elif isinstance(authors_data, list):
                        authors_list = []
                        for a in authors_data:
                            if isinstance(a, str):
                                authors_list.extend([s.strip() for s in a.split(",") if s.strip()])
                            elif isinstance(a, dict):
                                name = a.get("name", "")
                                email = f" <{a['email']}>" if "email" in a else ""
                                authors_list.append(f"{name}{email}".strip())
                    else:
                        authors_list = []

                    for aut in authors_list:
                           # "value": data["authors"],
                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            {
                                "value": aut,
                                "type": constants.AGENT
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )

                if "license" in data:                   
                    metadata_result.add_result(
                        constants.CAT_LICENSE,
                        {
                            "value": data["license"],
                            "type": constants.LICENSE
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                
                if "dependencies" in data and isinstance(data["dependencies"], dict):
                    for name, version in data["dependencies"].items():
                        req = f"{name}: {version}"
                        
                        metadata_result.add_result(
                            constants.CAT_REQUIREMENTS,
                            {
                                "value": req,
                                "name": name,
                                "version": version,
                                "type": constants.SOFTWARE_APPLICATION,
                                "dependency_type": "runtime"
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                
                if "devDependencies" in data and isinstance(data["devDependencies"], dict):
                    for name, version in data["devDependencies"].items():
                        req = f"{name}: {version}"
                        
                        metadata_result.add_result(
                            constants.CAT_REQUIREMENTS,
                            {
                                "value": req,
                                "name": name,
                                "version": version,
                                "type": constants.SOFTWARE_APPLICATION,
                                "dependency_type": "dev"
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                
                if "keywords" in data:
                    for keyword in data["keywords"]:
                        metadata_result.add_result(
                            constants.CAT_KEYWORDS,
                            {
                                "value": keyword,
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                
    except Exception as e:
        logging.error(f"Error parsing bower.json from {file_path}: {str(e)}")
    
    return metadata_result