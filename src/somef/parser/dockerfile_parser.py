import logging
import os
import re
from ..utils import constants
from ..process_results import Result

def parse_dockerfile(file_path, metadata_result: Result, source):

    print(f"Extracting properties from Dockerfile: {file_path}")

    try:
        with open(file_path, "rb") as file:
            raw_data = file.read()

        content = raw_data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as e:
        logging.warning(f"Could not process Dockerfile {file_path}: {e}")
        return None

    container = {}      
    # print(content)
    title_match = re.search(
        constants.REGEXP_DOCKER_TITLE,
        content,
        re.IGNORECASE
    )

    if title_match:
        title = title_match.group(1).strip()
        if title:
            metadata_result.add_result(
                constants.CAT_NAME,
                {
                    "value": title,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            container[constants.PROP_NAME] = title

    description_match = re.search(
        constants.REGEXP_DOCKER_DESCRIPTION,
        content,
        re.IGNORECASE
    )

    if description_match:
        description = description_match.group(1).strip()
        if description:
            metadata_result.add_result(
                constants.CAT_DESCRIPTION,
                {
                    "value": description,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            container[constants.PROP_DESCRIPTION] = description

    licenses_match = re.search(constants.REGEXP_DOCKER_LICENSES, content, re.IGNORECASE)
    if licenses_match:
        license_info_spdx = detect_license_spdx(licenses_match.group(1).strip())
                    
        if license_info_spdx:
            license_data = {
                "value": licenses_match.group(1).strip(),
                "spdx_id": license_info_spdx.get('spdx_id'),
                "name": license_info_spdx.get('name'),
                "type": constants.LICENSE
            }
        else:
            license_data = {
                "value": licenses_match.group(1).strip(),
                "type": constants.LICENSE
            }
        metadata_result.add_result(
            constants.CAT_LICENSE,
            license_data,
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
        container[constants.PROP_LICENSE] = license_data["value"]
        if license_data.get("spdx_id"):
            container[constants.PROP_SPDX_ID] = license_data["spdx_id"]


    # source_match = re.search(constants.REGEXP_DOCKER_SOURCE, content, re.IGNORECASE)
    # if source_match:
    #     properties[constants.PROP_SOURCE] = source_match.group(1).strip()

    url_match = re.search(constants.REGEXP_DOCKER_URL, content, re.IGNORECASE)
    if url_match:
        metadata_result.add_result(
            constants.CAT_CODE_REPOSITORY,
            {
                "value": url_match.group(1).strip(),
                "type": constants.URL
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
        container[constants.PROP_URL] = url_match.group(1).strip()

    version_match = re.search(constants.REGEXP_DOCKER_VERSION, content, re.IGNORECASE)
    if version_match:
        metadata_result.add_result(
            constants.CAT_VERSION,
            {
                "value": version_match.group(1).strip(),
                "type": constants.RELEASE,
                "tag": version_match.group(1).strip()
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
        container[constants.PROP_VERSION] = version_match.group(1).strip()
    
    documentation_match = re.search(constants.REGEXP_DOCKER_DOCUMENTATION, content, re.IGNORECASE)
    if documentation_match:
        metadata_result.add_result(
            constants.CAT_DOCUMENTATION,
            {
                "value": documentation_match.group(1).strip(),
                "type": constants.STRING
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
        container[constants.PROP_DOCUMENTATION] = documentation_match.group(1).strip()


    vendor_match = re.search(
        constants.REGEXP_DOCKER_VENDOR,
        content,
        re.IGNORECASE
    )

    if vendor_match:
        vendor = vendor_match.group(1).strip()
        if vendor:
            if vendor and re.search(constants.REGEXP_LTD_INC, vendor, re.IGNORECASE):
                type_vendor = "Organization"
            else:
                type_vendor = "Person"

            metadata_result.add_result(
                constants.CAT_OWNER,
                {
                    "value": vendor,
                    "type": type_vendor
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    # Extract maintainers
    maintainers = []
    unique_maintainers = [] 

    maintainer_oci_match = re.findall(
        constants.REGEXP_MAINTAINER_LABEL_OCI,
        content,
        re.IGNORECASE | re.MULTILINE
    )
    # LABEL maintainer free
    maintanainer_label_match = re.findall(
        constants.REGEXP_MAINTAINER_LABEL_FREE,
        content,
        re.IGNORECASE | re.MULTILINE
    )
    # Deprecated maintainer
    maintainer_match = re.findall(
        constants.REGEXP_MAINTAINER,
        content,
        re.IGNORECASE | re.MULTILINE
    )
    maintainers.extend(maintainer_oci_match)
    maintainers.extend(maintanainer_label_match)
    maintainers.extend(maintainer_match)

    unique_maintainers = list({m.strip() for m in maintainers if m.strip()})
    if unique_maintainers:
        container[constants.PROP_AUTHOR] = [
            {constants.PROP_TYPE: constants.AGENT, constants.PROP_VALUE: m} for m in unique_maintainers
        ]
    for maintainer in unique_maintainers:         
        metadata_result.add_result(
            constants.CAT_AUTHORS,
            {
                "type": constants.AGENT,
                "value": maintainer
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )

    if container:
        container_result = {
            constants.PROP_TYPE: constants.URL if str(source).startswith("http") else constants.STRING,
            constants.PROP_VALUE: source,
        }
        container_result.update(container)
        metadata_result.add_result(
            constants.CAT_CONTAINER,
            container_result,
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
    print("Detecting license from text:", license_text)
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

 