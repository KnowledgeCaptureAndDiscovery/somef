
import json
import yaml
import logging
from pathlib import Path
from ..process_results import Result
from ..utils import constants
import re

def parse_publiccode_file(file_path, metadata_result: Result, source):
    """
    Parse a publiccode.yml file and extract relevant metadata.
    
    Parameters
    ----------
    file_path: path of the publiccode.yml file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the package file (URL)

    Returns
    """
    print("file_path publiccode:", file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file)

    except Exception as e:
        logging.warning(f"Could not parse publiccode.yml {file_path}: {e}")
        return metadata_result

    if not isinstance(content, dict):
        return metadata_result
    
    if Path(file_path).name.lower() in {"publiccode.yml", "publiccode.yaml"}:
        print("Detected publiccode.yml file.")  
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

    if "url" in content:
        metadata_result.add_result(
            constants.CAT_CODE_REPOSITORY,
            {
                "value": content["url"],
                "type": constants.URL
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
    #application domain: Categories and description.[lang].genericName
    if "categories" in content:
        for category in content["categories"]:
            metadata_result.add_result(
                constants.CAT_APPLICATION_DOMAIN,
                {
                    "value": category,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    if "name" in content:
        metadata_result.add_result(
            constants.CAT_NAME,
            {
                "value": content["name"],
                "type": constants.STRING
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )

    if "description" in content:
        # this is the structure. But we don't need the language
        # description:
        #   en:
        #     genericName: Registry
        #   es:
        #     genericName: Registro
        description = content.get("description", {})

        generic_names = {
            lang_block["genericName"]
            for lang_block in description.values()
            if isinstance(lang_block, dict) and "genericName" in lang_block
        }
        for generic_name in generic_names:
            metadata_result.add_result(
                constants.CAT_APPLICATION_DOMAIN,
                {
                    "value": generic_name,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        short_descriptions = [
                lang_block.get("shortDescription")
                for lang_block in description.values()
                if isinstance(lang_block, dict)
            ]
        for short_desc in filter(None, short_descriptions):
            metadata_result.add_result(
                constants.CAT_DESCRIPTION,
                {
                    "value": short_desc.strip(),
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        long_descriptions = [
            lang_block.get("longDescription")
            for lang_block in description.values()
            if isinstance(lang_block, dict)
        ]
        for long_desc in filter(None, long_descriptions):
            metadata_result.add_result(
                constants.CAT_DESCRIPTION,
                {
                    "value": long_desc.strip(),
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        names = {
            lang_block.get("localisedName")
            for lang_block in description.values()
            if isinstance(lang_block, dict)
        }
        for name in filter(None, names):
            metadata_result.add_result(
                constants.CAT_NAME,
                {
                    "value": name.strip(),
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        keywords = []
        for lang_block in description.values():
            if not isinstance(lang_block, dict):
                continue

            features = lang_block.get("features", [])
            if isinstance(features, list):
                for feature in features:
                    if isinstance(feature, str):
                        keywords.append(feature)

        if keywords:
            metadata_result.add_result(
                constants.CAT_KEYWORDS,
                {
                    "value": keywords,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    if "platforms" in content:
        for platform in content["platforms"]:
            metadata_result.add_result(
                constants.CAT_RUNTIME_PLATFORM,
                {
                    "value": platform,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    depends_on = content.get("dependsOn", {})
#     dependsOn:
#       open: or propietary or hardware
#         - name: MySQL
#           versionMin: "1.1"
#           versionMax: "1.3"
#           optional: true
    for dep_type, dep_list in depends_on.items():  # dep_type = "open", "proprietary", "hardware"
        for dep in dep_list:
            name = dep.get("name")
            version = None
            version_str = None

            # complex version handling because sometimes is version and sometimes versionMin/versionMax
            if "version" in dep:
                version = dep["version"]
                version_str = f"=={version}"
            else:
                version_min = dep.get("versionMin")
                version_max = dep.get("versionMax")
                if version_min and version_max:
                    version = f">={version_min},<{version_max}"
                    version_str = version
                elif version_min:
                    version = f">={version_min}"
                    version_str = version
                elif version_max:
                    version = f"<{version_max}"
                    version_str = version


            metadata_result.add_result(
                constants.CAT_REQUIREMENTS,
                {
                    "value": f"{name}{version_str}" if version_str else name,
                    "name": name,
                    "version": version,
                    "type": constants.SOFTWARE_APPLICATION,
                    "dependency_type": "runtime" 
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    if "softwareVersion" in content:
        metadata_result.add_result(
            constants.CAT_VERSION,
            {
                "value": content["softwareVersion"],
                "type": constants.RELEASE,
                "tag": content["softwareVersion"]
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
        
    if "developmentStatus" in content:
        metadata_result.add_result(
            constants.CAT_DEV_STATUS,
            {
                "value": content["developmentStatus"],
                "type": constants.RELEASE,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
        
    if "legal" in content:
        legal = content["legal"]
        if "license" in legal:
            license_info_spdx = detect_license_spdx(legal["license"])
                    
            if license_info_spdx:
                license_data = {
                    "value": legal["license"],
                    "spdx_id": license_info_spdx.get('spdx_id'),
                    "name": license_info_spdx.get('name'),
                    "type": constants.LICENSE
                }
            else:
                license_data = {
                    "value": legal["license"],
                    "type": constants.LICENSE
                }
            metadata_result.add_result(
                constants.CAT_LICENSE,
                license_data,
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    if "releaseDate" in content:
        date_published = content["releaseDate"]
        # Add both date published and date updated with the same value
        if date_published:
            metadata_result.add_result(
                constants.CAT_DATE_PUBLISHED,
                {
                    "value": date_published,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            metadata_result.add_result(
                constants.CAT_DATE_UPDATED,
                {
                    "value": date_published,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    if "maintenance" in content:
        maintenance = content.get("maintenance", {})
        # maintenance_type = maintenance.get("type")

        # if maintenance_type == "contract":
        role_map = [
            ("contractors", "maintenance_contractor"),
            ("contacts", "maintenance_contact"),
        ]

        for key, role in role_map:
            for person in maintenance.get(key, []):
                author_data = {
                    "type": constants.AGENT,
                    "value": person.get("name", ""),
                    "name": person.get("name", ""),
                    "role": role
                }

                if "email" in person:
                    author_data["email"] = person["email"]

                if "website" in person:
                    author_data["url"] = person["website"]

                if "affiliation" in person:
                    author_data["affiliation"] = person["affiliation"]

                metadata_result.add_result(
                    constants.CAT_OWNER,
                    author_data,
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

    return metadata_result     


def detect_license_spdx(license_text):
    """
    Function that given a license text, infers the name and spdx id in a dockerfile
    Parameters
    ----------
    license_text

    Returns
    -------
    A JSON dictionary with name and spdx id
    """

    for license_name, license_info in constants.LICENSES_DICT.items():
        if re.search(license_info["regex"], license_text, re.IGNORECASE):
            return {
                "name": license_name,
                "spdx_id": f"{license_info['spdx_id']}",
                "@id": f"https://spdx.org/licenses/{license_info['spdx_id']}"
            }

    for license_name, license_info in constants.LICENSES_DICT.items():
        spdx_id = license_info["spdx_id"]
        if re.search(rf'\b{re.escape(spdx_id)}\b', license_text, re.IGNORECASE):
            return {
                "name": license_name,
                "spdx_id": spdx_id,
                "@id": f"https://spdx.org/licenses/{spdx_id}"
            }
    return None
