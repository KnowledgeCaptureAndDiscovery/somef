import ast
import os
import tomli
import logging
import re
from pathlib import Path
from ..process_results import Result
from ..utils import constants 
from ..regular_expressions import detect_license_spdx

def determine_dependency_type(info):
    """
    Determine the type of dependency and extract its version or URL.
    
    Parameters
    ----------
    info: The dependency information from Cargo.toml
    
    Returns
    -------
    version: The version string or URL
    dep_type: The type of dependency (version, url, path, other)
    req: The formatted requirement string
    """
    if isinstance(info, dict):
        if "version" in info:
            version = info["version"]
            req = f"version = {version}"
            dep_type = "version"
        elif "git" in info:
            version = info["git"]
            req = f"git = \"{version}\""
            dep_type = "url"
        elif "path" in info:
            version = info["path"]
            req = f"path = \"{version}\""
            dep_type = "path"
        else:
            version = str(info)
            req = f"other = {version}"
            dep_type = "other"
    else:
        version = info
        req = f"version = {version}"
        dep_type = "version"
    
    return version, dep_type, req

def parse_cargo_toml(file_path, metadata_result: Result, source):
    """
    Parse a Cargo.toml file to extract metadata.

    Parameters
    ----------
    file_path: path to the Cargo.toml file being analyzed
    metadata_result: Metadata object dictionary
    source: source of the package file (URL)

    Returns
    -------
    """
    try:
        if Path(file_path).name == "Cargo.toml":
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    "value": "Cargo.toml",
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            with open(file_path, "rb") as f:
                data = tomli.load(f)
                
                if "package" in data:
                    package = data["package"]
                    
                    if "name" in package:
                        metadata_result.add_result(
                            constants.CAT_PACKAGE_ID,
                            {
                                "value": package["name"], 
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                    
                    if "description" in package:
                        metadata_result.add_result(
                            constants.CAT_DESCRIPTION,
                            {
                                "value": package["description"], 
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                    
                    if "version" in package:
                        metadata_result.add_result(
                            constants.CAT_VERSION,
                            {
                                "value": package["version"],
                                "type": constants.RELEASE,
                                "tag": package["version"]
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                    
                    if "authors" in package:
                        for author_str in package["authors"]:
                            email_match = re.search(r'<([^>]+)>', author_str)
                            if email_match:
                                email = email_match.group(1)
                                name = author_str[:email_match.start()].strip()
                            else:
                                name = author_str
                                email = None
                                
                            metadata_result.add_result(
                                constants.CAT_AUTHORS,
                                {
                                    "name": name,
                                    "email": email,
                                    "type": constants.AGENT,
                                    "value": name
                                },
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                    if  "repository" in package:
                        metadata_result.add_result(
                            constants.CAT_CODE_REPOSITORY,
                            {
                                "value": package["repository"],
                                "type": constants.URL
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                
                    if "keywords" in package:
                        for keyword in package["keywords"]:
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
                    if "license" in package:
                        license_value = package["license"]
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
                        
                if "dependencies" in data:
                    dependencies = data["dependencies"]
                    for name, info in dependencies.items():
                        version, dep_type, req_details = determine_dependency_type(info)
                        req = f"{name} = {{ {req_details} }}"
                        
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
                
                # This for extracting target specific dependencies
                for key in data:
                    if key.startswith("target.") and isinstance(data[key], dict) and "dependencies" in data[key]:
                        target_deps = data[key]["dependencies"]
                        for name, info in target_deps.items():
                            version, dep_type, req_details = determine_dependency_type(info)
                            req = f"{name} = {{ {req_details} }} (target-specific)"
                            
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
            
    except Exception as e:
        logging.error(f"Error parsing Cargo.toml from {file_path}: {str(e)}")

    return metadata_result