import json
import logging
from ..process_results import Result
from ..utils import constants

"""
This code is inspired by Codemeta Project parsers, specifically nodejs.py
https://github.com/proycon/codemetapy/blob/master/codemeta/parsers/nodejs.py
"""

def parse_package_json_file(file_path, metadata_result: Result, source):
    """

    Parameters
    ----------
    file_path: path of the package file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the package file (URL)

    Returns
    -------

    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if "name" in data:
                metadata_result.add_result(
                    constants.CAT_PACKAGE_ID,
                    {
                        "value": data["name"], 
                        "type": constants.STRING},
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )
            
            if "description" in data:
                metadata_result.add_result(
                    constants.CAT_DESCRIPTION,
                    {
                        "value": data["description"], 
                        "type": constants.STRING},
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "homepage" in data:
                metadata_result.add_result(
                    constants.CAT_HOMEPAGE,
                    {
                        "value": data["homepage"], 
                        "type": constants.URL},
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

            repo_url = parse_repository(data.get("repository"))
            if repo_url:
                metadata_result.add_result(
                    constants.CAT_CODE_REPOSITORY,
                    {
                        "value": repo_url, 
                        "type": constants.URL},
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )
            
            parsed_bugs_url = parse_bugs(data.get("bugs"))
            if parsed_bugs_url:
                metadata_result.add_result(
                    constants.CAT_ISSUE_TRACKER,
                    {
                        "value": parsed_bugs_url, 
                        "type": constants.URL},
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            author_info = parse_author(data.get("author"))
            if author_info:
                if isinstance(author_info, dict):
                    result = {
                            "name": author_info.get("name"),
                            "email": author_info.get("email"),
                            "type": constants.AGENT,
                            "value": author_info.get("name")
                        }
                    if author_info.get("url") is not None:
                        result["url"] = author_info.get("url")
                    metadata_result.add_result(
                        constants.CAT_AUTHORS,
                        result,
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                else:
                    metadata_result.add_result(
                        constants.CAT_AUTHORS,
                        {
                            "name": author_info, 
                            "type": constants.AGENT,
                            "value": author_info},
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
            
            license_value = parse_license(data.get("license"))
            if license_value:
                metadata_result.add_result(
                    constants.CAT_LICENSE,
                    {
                        "value": license_value,
                        "type": constants.LICENSE
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )
            
            if "keywords" in data and isinstance(data["keywords"], list):
                for keyword in data["keywords"]:
                    metadata_result.add_result(
                        constants.CAT_KEYWORDS,
                        {
                            "value": keyword, 
                            "type": constants.STRING},
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            runtimes = parse_runtime_platform_from_package_json(data)
            if runtimes:
                for runtime in runtimes:
                    metadata_result.add_result(
                        constants.CAT_RUNTIME_PLATFORM,
                        runtime,
                        # {
                        #     "value": runtime["version"],
                        #     "version": runtime["version"],
                        #     "name": runtime["name"],
                        #     "type": constants.STRING
                        # },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
         
            deps = {}
            deps.update(data.get("dependencies", {}))
            deps.update(data.get("devDependencies", {}))
            
            for name, version in deps.items():
                req = f"{name}@{version}"
                metadata_result.add_result(
                    constants.CAT_REQUIREMENTS,
                    {
                        "value": req, 
                        "name": name, 
                        "version": version, 
                        "type": constants.SOFTWARE_APPLICATION
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    # "value": "package.json",
                    "value": source,
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in package.json: {str(e)}")
    except Exception as e:
        logging.error(f"Error parsing package.json: {str(e)}")
    
    return metadata_result

def parse_repository(repo_data):
    if isinstance(repo_data, dict):
        return repo_data.get("url", repo_data.get("directory"))
    return repo_data

def parse_author(author_data):
    if isinstance(author_data, dict):
        return {
            "name": author_data.get("name"),
            "email": author_data.get("email"),
            "url": author_data.get("url")
        }
    return author_data

def parse_license(license_data):
    if isinstance(license_data, dict):
        return license_data.get("type")
    return license_data

def parse_bugs(bugs_data):
    if isinstance(bugs_data, dict) and "url" in bugs_data:
        return bugs_data["url"]
    if isinstance(bugs_data, str):
        return bugs_data
    return None

def parse_runtime_platform_from_package_json(data):
    """
    Extract runtime information from a package.json dict.
    Returns a list of dicts with 'name' and 'version', e.g.:
    [{'name': 'Node.js', 'version': '18.x'}]
    """
    runtimes = []

    engines = data.get("engines", {})
    if isinstance(engines, dict):
        for runtime_name, version_value in engines.items():

            if version_value:
                value_str = f"{runtime_name}: {version_value}".strip()
            else:
                value_str = runtime_name

            run = {
                "value": value_str,
                "name": runtime_name.capitalize(),
                "type": constants.STRING
            }
            if version_value:
                run["version"] = version_value.strip()

            # if version_value:
            #     # runtimes.append({
            #     #     "name": runtime_name.capitalize(),
            #     #     "version": version_value.strip()
            #     # })
            #     run["version"]=  version_value.strip()
            
            runtimes.append(run)  
    
    return runtimes