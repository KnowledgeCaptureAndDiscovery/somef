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


def parse_codeowners_file(file_path, metadata_result: Result, source, reconcile_authors=None) -> Result:
    try:
        print(f"Additional info flag: {reconcile_authors}")
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
                    # print(f"Adding maintainer: {owner}")

                    if owner in added_maintainers:
                        continue

                    added_maintainers.add(owner)

                    maintainer_data = {
                        "value": owner,
                        "username": owner,
                        "role": "Maintainer",
                        "type": "Person"
                    }

                    if reconcile_authors:
                        user_info = enrich_github_user(owner)
                        if user_info:
                            if user_info.get("name"):
                                maintainer_data["name"] = user_info.get("name")
                            if user_info.get("company"):
                                maintainer_data["affiliation"] = user_info.get("company")
                            if user_info.get("email"):
                                maintainer_data["email"] = user_info.get("email")

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

def enrich_github_user(username):
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "name": data.get("name"),
            "company": data.get("company"),
            "email": data.get("email")  
        }

    except Exception:
        return None

