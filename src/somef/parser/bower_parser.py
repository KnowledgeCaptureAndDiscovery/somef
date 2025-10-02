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
                    metadata_result.add_result(
                        constants.CAT_AUTHORS,
                        {
                            "value": data["authors"],
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