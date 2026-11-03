import json
import logging
from pathlib import Path
import re
from ..process_results import Result
from ..regular_expressions import detect_license_spdx
from ..utils import constants


def parse_zenodo_file(file_path, metadata_result: Result, source):
    """
    Parse a .zenodo.json file and extract relevant metadata.

    Parameters
    ----------
    file_path: path of the zenodo file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the package file (URL)

    Returns
    -------
    metadata_result
    """
    try:
        if Path(file_path).name.lower() in [".zenodo.json"]:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                return metadata_result

            def add(category, value_dict):
                metadata_result.add_result(category, value_dict, 1, constants.TECHNIQUE_CODE_CONFIG_PARSER, source)

            if isinstance(data.get("title"), str) and data["title"].strip():
                add(constants.CAT_NAME, {constants.PROP_VALUE: data["title"].strip(),constants.PROP_TYPE: constants.STRING})

            description = data.get("description")
            if isinstance(description, str):
                description = re.sub(constants.REGEXP_CLEAN_HTML_TAGS, '', description).strip()
                if description:
                    add(constants.CAT_DESCRIPTION, {constants.PROP_VALUE: description,constants.PROP_TYPE: constants.STRING})

            if data.get("version"):
                add(constants.CAT_VERSION, {constants.PROP_VALUE: str(data["version"]).strip(), constants.PROP_TYPE: constants.STRING})

            keywords = data.get("keywords")
            if isinstance(keywords, str):
                keywords = keywords.split(",")
            if isinstance(keywords, list):
                for kw in keywords:
                    if isinstance(kw, str) and kw.strip():
                        add(constants.CAT_KEYWORDS, {constants.PROP_VALUE: kw.strip(), constants.PROP_TYPE: constants.STRING})

            license_info = parse_zenodo_license(data.get("license"))
            if license_info:
                license_data = {
                    constants.PROP_VALUE: license_info["value"],
                    constants.PROP_TYPE: constants.LICENSE,
                }
                if license_info.get("spdx_id"):
                    license_data[constants.PROP_NAME] = license_info["name"]
                    license_data[constants.PROP_SPDX_ID] = license_info["spdx_id"]
                    license_data[constants.PROP_IDENTIFIER] = license_info["identifier"]
                add(constants.CAT_LICENSE, license_data)

            if data.get("publication_date"):
                add(constants.CAT_DATE_PUBLISHED, {constants.PROP_VALUE: data["publication_date"], constants.PROP_TYPE: constants.STRING})

            for person in data.get("creators") or []:
                info = parse_zenodo_person(person)
                if info:
                    add(constants.CAT_AUTHORS, info)

            for person in data.get("contributors") or []:
                info = parse_zenodo_person(person)
                if info:
                    add(constants.CAT_CONTRIBUTORS, info)

    except Exception as e:
        logging.error(f"Error parsing zenodo.json from {file_path}: {str(e)}")

    return metadata_result


def clean_html(text):
    """Remove HTML tags from a string, keeping readable text. The description in zenodo is usually in HTML format."""
    if not isinstance(text, str):
        return ""
    soup = BeautifulSoup(text, "html.parser")
    for br in soup.find_all("br"):
        br.replace_with(" ")
    for tag in soup.find_all(["p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6"]):
        tag.append(" ")
    return " ".join(soup.get_text().split())


def parse_zenodo_license(license_data):
    """
    Parse the license field of a .zenodo.json file.
    Zenodo uses either {"id": "mit"} or a plain string id.

    Returns
    -------
    dict or None
        Always has "value". If the license is recognised, it also has
        name, spdx_id and identifier (SPDX URL).
    """
    if isinstance(license_data, dict):
        license_id = license_data.get("id") or license_data.get("name")
    elif isinstance(license_data, str):
        license_id = license_data
    else:
        return None

    if not isinstance(license_id, str) or not license_id.strip():
        return None
    license_id = license_id.strip()

    license_info = {"value": license_id}
    license_info_spdx = detect_license_spdx(license_id, "JSON")
    if license_info_spdx:
        license_info["name"] = license_info_spdx.get("name")
        license_info["spdx_id"] = license_info_spdx.get("spdx_id")
        license_info["identifier"] = license_info_spdx.get("identifier")
    return license_info


def parse_zenodo_person(person):
    """
    Parse an entry of 'creators' / 'contributors'.
    Zenodo names usually come as "Family, Given".
    """
    if isinstance(person, str):
        person = {"name": person}
    if not isinstance(person, dict):
        return None

    name = (person.get("name") or "").strip()
    if not name:
        return None

    info = {constants.PROP_TYPE: constants.AGENT}
    if "," in name:
        family, given = [p.strip() for p in name.split(",", 1)]
        info[constants.PROP_VALUE] = f"{given} {family}".strip()
        if given:
            info[constants.PROP_GIVEN_NAME] = given
        if family:
            info[constants.PROP_LAST_NAME] = family
    else:
        info[constants.PROP_VALUE] = name
    info[constants.PROP_NAME] = info[constants.PROP_VALUE]

    if person.get("affiliation"):
        info[constants.PROP_AFFILIATION] = person["affiliation"]
    if person.get("orcid"):
        orcid = person["orcid"].strip()
        info[constants.PROP_IDENTIFIER] = orcid if orcid.startswith("http") else f"https://orcid.org/{orcid}"
    return info


