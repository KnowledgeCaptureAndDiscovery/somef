import json
import logging
import os
import re
from pathlib import Path
from ..process_results import Result
from ..utils import constants
from ..regular_expressions import detect_license_spdx

def parse_composer_json(file_path, metadata_result: Result, source):
    """
    Parse a composer.json file to extract metadata.

    Parameters
    ----------
    file_path: path to the composer.json file being analyzed
    metadata_result: Metadata object dictionary
    source: source of the package file (URL)

    Returns
    -------
    """
    try:

        if Path(file_path).name.lower() in ["composer.json"]:
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    "value": "composer.json",
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

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
                            "tag": data["version"]
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                if "authors" in data:
                    for author in data["authors"]:
                        author_data = {
                            "type": constants.AGENT,
                            "value": author.get("name", "")
                        }
                        
                        if "name" in author:
                            author_data["name"] = author["name"]
                        
                        if "email" in author:
                            author_data["email"] = author["email"]
                        
                        if "homepage" in author:
                            author_data["url"] = author["homepage"]
                        
                        if "role" in author:
                            author_data["role"] = author["role"]
                        
                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            author_data,
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                
                if "license" in data:
                    license_value = data["license"]
                    license_text = ""
                    
                    dir_path = os.path.dirname(file_path)
                    license_paths = [
                        os.path.join(dir_path, "LICENSE"),
                        os.path.join(dir_path, "LICENSE.txt"),
                        os.path.join(dir_path, "LICENSE.md")
                    ]
                    
                    for license_path in license_paths:
                        if os.path.exists(license_path):
                            with open(license_path, "r", encoding="utf-8") as lf:
                                license_text = lf.read()
                            break
                    
                    license_info_spdx = detect_license_spdx(license_text, 'JSON')
                    
                    if license_info_spdx:
                        license_data = {
                            "value": license_value,
                            "spdx_id": license_info_spdx.get('spdx_id'),
                            "name": license_info_spdx.get('name'),
                            "type": constants.LICENSE
                        }
                    else:
                        license_data = {
                            "value": license_value,
                            "type": constants.LICENSE
                        }
                    
                    metadata_result.add_result(
                        constants.CAT_LICENSE,
                        license_data,
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                dependency_sections = ["require", "require-dev"]
                for section in dependency_sections:
                    if section in data:
                        for name, version in data[section].items():
                            req = f"{name}: {version}"
                            if section == "require-dev":
                                dep_type = "dev"
                            else:
                                dep_type = "runtime"
                            
                            metadata_result.add_result(
                                constants.CAT_REQUIREMENTS,
                                {
                                    "value": req,
                                    "name": name,
                                    "version": version,
                                    "type": constants.SOFTWARE_APPLICATION,
                                    "dependency_type": dep_type
                                },
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                
                if "repository" in data:
                    repo_data = data["repository"]
                    if isinstance(repo_data, str):
                        repo_url = repo_data
                    elif isinstance(repo_data, dict) and "url" in repo_data:
                        repo_url = repo_data["url"]
                    else:
                        repo_url = None
                    
                    if repo_url:
                        metadata_result.add_result(
                            constants.CAT_CODE_REPOSITORY,
                            {
                                "value": repo_url,
                                "type": constants.URL
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
        logging.error(f"Error parsing composer.json from {file_path}: {str(e)}")
    
    return metadata_result