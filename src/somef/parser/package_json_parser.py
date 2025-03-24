import json
import logging
from ..process_results import Result
from ..utils import constants

def parse_package_json_file(file_path, metadata_result: Result):
    """Function parses package.json file and extract Node.js project metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            project_data = {
                "name": data.get("name"),
                "version": data.get("version"),
                "description": data.get("description"),
                "repository": parse_repository(data.get("repository")),
                "author": parse_author(data.get("author")),
                "license": parse_license(data.get("license")),
                "keywords": data.get("keywords", []),
                "dependencies": list_dependencies(data),
                "scripts": data.get("scripts", {})
            }

            metadata_result.add_result(
                constants.CAT_PACKAGE_FILE,
                {
                    "value": file_path,
                    "type": "package.json",
                    "metadata": {k: v for k, v in project_data.items() if v}
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                file_path
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

def list_dependencies(data):
    """Combine dependencies and devDependencies (This is based on the methodology of Codemetapy)"""
    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))
    return [f"{name}@{version}" for name, version in deps.items()]