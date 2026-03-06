import json
import logging
import os
import requests
from pathlib import Path
from ..process_results import Result
from ..utils import constants

def parse_codeowners_structured(dir_path, filename):
    codeowners = []

    with open(os.path.join(dir_path, filename), "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split()
                path = parts[0]
                owners = [o.lstrip("@") for o in parts[1:]]
                codeowners.append({"path": path, "owners": owners})

    return {"codeowners": codeowners}


def parse_codeowners_file(file_path, metadata_result: Result, source, reconcile_authors=None, repo_type=None, server_url=None) -> Result:
    try:
        logging.info(f"Reconcile authors flag: {reconcile_authors}")
        if Path(file_path).name.upper() == constants.CODEOWNERS_FILE:
            owners = parse_codeowners_structured(
                os.path.dirname(file_path),
                Path(file_path).name
            )

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

            added_maintainers = set()
            for entry in owners["codeowners"]:
                for owner in entry["owners"]:

                    if owner in added_maintainers:
                        continue

                    added_maintainers.add(owner)

                    maintainer_data = {
                        constants.PROP_VALUE: owner,
                        constants.PROP_USERNAME: owner,
                        constants.PROP_ROLE: "Maintainer",
                        constants.PROP_TYPE: "Person"
                    }

                    if reconcile_authors:
                        user_info = enrich_user(owner, repo_type, server_url)
                        if user_info:
                            if user_info.get(constants.PROP_CODEOWNERS_NAME):
                                maintainer_data[constants.PROP_NAME] = user_info.get(constants.PROP_CODEOWNERS_NAME)
                            if user_info.get(constants.PROP_CODEOWNERS_COMPANY):
                                maintainer_data[constants.PROP_AFFILIATION] = user_info.get(constants.PROP_CODEOWNERS_COMPANY)
                            if user_info.get(constants.PROP_CODEOWNERS_EMAIL):
                                maintainer_data[constants.PROP_EMAIL] = user_info.get(constants.PROP_CODEOWNERS_EMAIL)

                    metadata_result.add_result(
                        constants.CAT_MAINTAINER,
                        maintainer_data,
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )


    except Exception as e:
        logging.error(f"Error parsing CODEOWNERS: {e}")

    return metadata_result

# def enrich_github_user(username):
#     """ Enrich user metadata using the appropriate platform API. 
#     Currently only GitHub is supported. 
#     """
#     try:
#         url = f"https://api.github.com/users/{username}"
#         response = requests.get(url, timeout=5)

#         if response.status_code != 200:
#             return None

#         data = response.json()

#         return {
#             constants.PROP_CODEOWNERS_NAME: data.get("name"),
#             constants.PROP_CODEOWNERS_COMPANY: data.get("company"),
#             constants.PROP_CODEOWNERS_EMAIL: data.get("email"),
#         }


#     except Exception:
#         return None
    

def enrich_user(username, repo_type, server_url=None):
    """
    Enrich user metadata using the appropriate platform API.
    
    Parameters
    ----------
    username : str Username to enrich.
    repo_type : str "GITHUB" or "GITLAB"
    server_url : str, optional
        Base URL of GitLab instance if repo_type is "GITLAB"
    
    Returns
    -------
    dict or None
        Dictionary with available user info (name, company, email), or None if not found.
    """

    if repo_type == constants.RepositoryType.GITHUB:
        # logging.info(f"Enriching GitHub user {username}")
        try:
            url = f"https://api.github.com/users/{username}"
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return None
            data = response.json()
            return {
                constants.PROP_CODEOWNERS_NAME: data.get("name"),
                constants.PROP_CODEOWNERS_COMPANY: data.get("company"),
                constants.PROP_CODEOWNERS_EMAIL: data.get("email"),
            }
        except Exception as e:
            logging.warning(f"Error enriching GitHub user {username}: {e}")
            return None

    elif repo_type == constants.RepositoryType.GITLAB:
        try:
            if server_url is None:
                server_url = "https://gitlab.com"
            if not server_url.startswith("http"):
                server_url = "https://" + server_url
            api_url = f"{server_url.rstrip('/')}/api/v4/users?username={username}"
            response = requests.get(api_url, timeout=5)
            if response.status_code != 200:
                logging.warning(f"GitLab API request failed for {username}: {response.status_code}")
                return None
            data = response.json()
            if not data:
                return None
            user_info = data[0]
            return {
                constants.PROP_CODEOWNERS_NAME: user_info.get("name"),
                constants.PROP_CODEOWNERS_COMPANY: user_info.get("organization"),
                constants.PROP_CODEOWNERS_EMAIL: user_info.get("public_email"),
            }
        except Exception as e:
            logging.error(f"Error enriching GitLab user {username}: {e}")
            return None

    else:
        logging.warning(f"Unsupported repo_type {repo_type}")
        return None

