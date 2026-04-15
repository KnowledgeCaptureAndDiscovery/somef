import json
import logging
from ..process_results import Result
from ..utils import constants
import re


def parse_keywords(keywords_data):
    """
    Parse keywords from codemeta.json file

    Parameters
    ----------
    keywords_data: str or list
    The keywords data from codemeta.json, can be a comma-separated string or a list

    Returns
    -------
    list
        List of processed keywords
    """
    processed_keywords = []
    if isinstance(keywords_data, str):
        for k in keywords_data.split(","):
            k = k.strip()
            if k:
                processed_keywords.append(k)
        return processed_keywords
    elif isinstance(keywords_data, list):
        for item in keywords_data:
            if isinstance(item, str):
                sub_parts = item.split(",")
                for sub_part in sub_parts:
                    processed_keywords.append(sub_part.strip())
            else:
                processed_keywords.append(str(item).strip())
        return processed_keywords
    return processed_keywords


def parse_license(license_data):
    """
    Parse license information from codemeta.json

    Parameters
    ----------
    license_data: dict or str
        The license data from codemeta.json

    Returns
    -------
    dict or None
        Processed license information with keys: name, url, identifier, spdx_id
    """
    license_info = {}
    if isinstance(license_data, dict):
        license_info["name"] = license_data.get("name")
        license_info["url"] = license_data.get("url")
        license_info["identifier"] = license_data.get("identifier")

        identifier = license_info.get("identifier", "")
        if "spdx.org/licenses/" in identifier:
            spdx_id = identifier.split("spdx.org/licenses/")[-1].split("/")[0]
            license_info["spdx_id"] = spdx_id
    elif isinstance(license_data, str):
        # license_info["name"] = license_data
        # license_info["identifier"] = f"https://spdx.org/licenses/{license_data}"
        # license_info["spdx_id"] = license_data
        license_str = license_data.strip()

        if "spdx.org/licenses/" in license_str:
            # Already a full SPDX URL
            license_info["identifier"] = license_str
            license_info["name"] = license_str.split("/")[-1]
            license_info["spdx_id"] = license_info["name"]
        else:
            # we assume it's an spdx id like "MIT"
            license_info["name"] = license_str
            license_info["identifier"] = f"https://spdx.org/licenses/{license_str}"
            license_info["spdx_id"] = license_str
    else:
        return None
    return license_info


def parse_software_requirements(requirements_data):
    """
    Parse software requirements information from codemeta.json

    Parameters
    ----------
    requirements_data: list or str
    The software requirements data from codemeta.json

    Returns
    -------
    list
    """
    requirements = []

    if isinstance(requirements_data, str):
        requirements_data = [requirements_data]

    if isinstance(requirements_data, list):
        for req in requirements_data:
            if isinstance(req, str):
                original = req.strip()

                match = re.match(r'^([a-zA-Z0-9_.\-]+)([<>=!~].*)?$', original)
                if match:
                    name = match.group(1)
                    version = match.group(2).strip() if match.group(2) else None
                    requirements.append({
                        "value": original,
                        # "name": name,
                        # "version": version
                        **({"name": name} if name else {}),
                        **({"version": version} if version else {})
                    })
                else:
                    requirements.append({
                        "value": original
                    })
            elif isinstance(req, dict):
                # Handle structured object format
                name = req.get("name") or req.get("identifier")
                version = req.get("version")
                identifier = req.get("identifier")

                if name:
                    requirement_dict = {
                        "value": name,
                        "name": name
                    }

                    if version:
                        requirement_dict["version"] = version
                        requirement_dict["value"] = f"{name}=={version}" if version else name

                    if identifier and identifier != name:
                        requirement_dict["identifier"] = identifier

                    requirements.append(requirement_dict)

    return requirements


def parse_referenced_publication(reference_data):
    """
    Parse referenced publication information from codemeta.json

    Parameters
    ----------
    reference_data: dict
    The reference publication data from codemeta.json

    Returns
    -------
    dict or None
    """
    if isinstance(reference_data, dict):
        return {
            "title": reference_data.get("name") or reference_data.get("title"),
            "author": reference_data.get("author"),
            "url": reference_data.get("url"),
            "date_published": reference_data.get("datePublished"),
            "identifier": reference_data.get("identifier")
        }
    return None


def parse_funding(funding_data):
    """
    Parse funding information from codemeta.json

    Parameters
    ----------
    funding_data: dict, str
    The funding data from codemeta.json

    Returns
    -------
    dict or None
    """
    if isinstance(funding_data, dict):
        funder_name = None
        if "funder" in funding_data:
            funder = funding_data["funder"]
            if isinstance(funder, dict):
                funder_name = funder.get("name")

        return {
            "funder": funder_name,
            "funding": funding_data.get("fundingIdentifier")
        }
    elif isinstance(funding_data, str):
        return {
            "funder": None,
            "funding": funding_data
        }

    return None

def parse_programming_language(language_data):
    """
    Parse programming language information from codemeta.json

    Parameters
    ----------
    language_data: dict or str
        The programming language data from codemeta.json

    Returns
    -------
    dict or None
        Processed programming language information
    """
    if isinstance(language_data, dict):
        name = language_data.get("name")
        version = language_data.get("version")
        url = language_data.get("url")

        if name:
            lang_info = {
                "name": name,
                "value": name,
                "type": constants.LANGUAGE
                # "version": version if version is not None else None 
            }
            if version:
                lang_info["version"] = version

            if url:
                lang_info["url"] = url

            return lang_info

    elif isinstance(language_data, str):
        return {
            "name": language_data,
            "value": language_data,
            "type": constants.LANGUAGE
            # ,
            # "version": None
        }

    return None

def parse_contributors(contributors_data):
    """
    Parse contributors from codemeta.json

    Parameters
    ----------
    contributors_data: list, dict
        Contributor data from codemeta.json

    Returns
    -------
    list
        List of contributor dictionaries
    """
    contributors_list = []

    if isinstance(contributors_data, dict):
        contributors_data = [contributors_data]

    if not isinstance(contributors_data, list):
        return contributors_list

    for contributor in contributors_data:

        if isinstance(contributor, dict):

            given = contributor.get(constants.PROP_CODEMETA_GIVENAME)
            family = contributor.get(constants.PROP_CODEMETA_FAMILYNAME)
            name = contributor.get(constants.PROP_NAME)

            if given and family:
                full_name = f"{given} {family}"
            elif name:
                full_name = name
            else:
                continue

            contributor_info = {
                constants.PROP_VALUE: full_name,
                constants.PROP_NAME: full_name,
                constants.PROP_TYPE: constants.AGENT
            }

            if given:
                contributor_info[constants.PROP_GIVEN_NAME] = given

            if family:
                contributor_info[constants.PROP_LAST_NAME] = family

            if "email" in contributor:
                contributor_info[constants.PROP_EMAIL] = contributor[constants.PROP_EMAIL]

            affil = contributor.get(constants.PROP_AFFILIATION)
            if affil:
                if isinstance(affil, dict) and affil.get(constants.PROP_NAME):
                    contributor_info[constants.PROP_AFFILIATION] = affil[constants.PROP_NAME]
                elif isinstance(affil, str):
                    contributor_info[constants.PROP_AFFILIATION] = affil

            identifier = contributor.get(constants.PROP_IDENTIFIER) or contributor.get(constants.PROP_CODEMETA_ID)
            if identifier:
                contributor_info[constants.PROP_IDENTIFIER] = identifier

            contributors_list.append(contributor_info)

        elif isinstance(contributor, str):
            name = contributor.strip()
            if name:
                contributors_list.append({
                    constants.PROP_VALUE: name,
                    constants.PROP_TYPE: constants.AGENT
                })

    return contributors_list


def parse_codemeta_json_file(file_path, metadata_result: Result, source):
    """

    Parameters
    ----------
    file_path: path of the package file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the codemeta file (URL)

    Returns
    -------

    """
    print(f"CODEMETA PARSER - Processing file: {file_path}")
    print(f"CODEMETA PARSER - Source: {source}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if "applicationCategory" in data:
                metadata_result.add_result(
                    constants.CAT_APPLICATION_DOMAIN,
                    {
                        "value": data["applicationCategory"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "softwareVersion" in data:
                metadata_result.add_result(
                    constants.CAT_VERSION,
                    {
                        "value": data["softwareVersion"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "codeRepository" in data:
                metadata_result.add_result(
                    constants.CAT_CODE_REPOSITORY,
                    {
                        "value": data["codeRepository"],
                        "type": constants.URL
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "contributor" in data:
                contributors = parse_contributors(data["contributor"])
                for contributor in contributors:
                    metadata_result.add_result(
                        constants.CAT_CONTRIBUTORS,
                        contributor,
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "issueTracker" in data:
                metadata_result.add_result(
                    constants.CAT_ISSUE_TRACKER,
                    {
                        "value": data["issueTracker"],
                        "type": constants.URL
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "dateCreated" in data:
                date_created = data["dateCreated"]
                if date_created:
                    metadata_result.add_result(
                        constants.CAT_DATE_CREATED,
                        {
                            "value": date_created,
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "dateModified" in data:
                date_modified = data["dateModified"]
                if date_modified:
                    metadata_result.add_result(
                        constants.CAT_DATE_UPDATED,
                        {
                            "value": date_modified,
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "datePublished" in data:
                date_published = data["datePublished"]
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

            if "downloadUrl" in data:
                metadata_result.add_result(
                    constants.CAT_DOWNLOAD_URL,
                    {
                        "value": data["downloadUrl"],
                        "type": constants.URL
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

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

            if "contIntegration" in data:
                metadata_result.add_result(
                    constants.CAT_CONTINUOUS_INTEGRATION,
                    {
                        "value": data["contIntegration"],
                        "type": constants.URL
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "keywords" in data:
                keywords = parse_keywords(data['keywords'])
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

            if "referencePublication" in data:
                ref_publications = data["referencePublication"]
                if isinstance(ref_publications, list):

                    for pub in ref_publications:
                        pub_data = parse_referenced_publication(pub)
                        result_dict = map_reference_publication(pub_data)
                        if result_dict:
                            metadata_result.add_result(
                                constants.CAT_CITATION,
                                result_dict,
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                elif isinstance(ref_publications, dict):
                
                    pub_data = parse_referenced_publication(ref_publications)
                    result_dict = map_reference_publication(pub_data)
                    if result_dict:
                        metadata_result.add_result(
                            constants.CAT_CITATION,
                            result_dict,
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                else:
                    metadata_result.add_result(
                        constants.CAT_CITATION,
                        {
                            "value": data["referencePublication"],
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "funding" in data:
                funding_data = data["funding"]
                if isinstance(funding_data, list):
                    for fund in funding_data:
                        fund_info = parse_funding(fund)
                        if fund_info:
                            metadata_result.add_result(
                                constants.CAT_FUNDING,
                                {
                                    "funder": fund_info.get("funder", ""),
                                    "funding": fund_info.get("funding", ""),
                                    "type": constants.STRING
                                },
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                elif isinstance(funding_data, dict):
                    fund_info = parse_funding(funding_data)
                    if fund_info:
                        metadata_result.add_result(
                            constants.CAT_FUNDING,
                            {
                                "funder": fund_info.get("funder", ""),
                                "funding": fund_info.get("funding", ""),
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )

            if "developmentStatus" in data:
                metadata_result.add_result(
                    constants.CAT_DEV_STATUS,
                    {
                        "value": data["developmentStatus"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "identifier" in data:
                metadata_result.add_result(
                    constants.CAT_IDENTIFIER,
                    {
                        "value": data["identifier"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "readme" in data:
                metadata_result.add_result(
                    constants.CAT_README_URL,
                    {
                        "value": data["readme"],
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

            if "version" in data:
                metadata_result.add_result(
                    constants.CAT_VERSION,
                    {
                        "value": data["version"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

            if "author" in data:
                authors = data["author"]
                if isinstance(authors, list):
                    for author in authors:
                        if isinstance(author, dict):
                            author_name = ""
                            if "givenName" in author and "familyName" in author:
                                author_name = f"{author['givenName']} {author['familyName']}"
                            elif "name" in author:
                                author_name = author["name"]

                            if author_name:
                                author_info = {
                                    "value": author_name,
                                    "type": constants.AGENT
                                }

                                if "email" in author:
                                    author_info["email"] = author["email"]

                                if "affiliation" in author:
                                    if isinstance(author["affiliation"], dict) and "name" in author["affiliation"]:
                                        author_info["affiliation"] = author["affiliation"]["name"]
                                    elif isinstance(author["affiliation"], str):
                                        author_info["affiliation"] = author["affiliation"]

                                identifier = author.get("identifier") or author.get("@id")
                                if identifier:
                                    author_info["identifier"] = identifier

                                metadata_result.add_result(
                                    constants.CAT_AUTHORS,
                                    author_info,
                                    1,
                                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                    source
                                )
                elif isinstance(authors, dict):
                    author = authors
                    author_name = ""
                    if "givenName" in author and "familyName" in author:
                        author_name = f"{author['givenName']} {author['familyName']}"
                    elif "name" in author:
                        author_name = author["name"]

                    if author_name:
                        author_info = {
                            "value": author_name,
                            "type": constants.AGENT
                        }

                        if "email" in author:
                            author_info["email"] = author["email"]

                        if "affiliation" in author and "name" in author["affiliation"]:
                            author_info["affiliation"] = author["affiliation"]["name"]

                        if "identifier" in author:
                            author_info["identifier"] = author["identifier"]

                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            author_info,
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )

            if "license" in data:
                license_raw = data["license"]
                license_info = parse_license(license_raw)
                if license_info:
                    if isinstance(license_raw, str):
                        val_lic = license_raw
                    else:
                        val_lic = license_info.get("name", "")

                    result_dict = {
                        "value": val_lic,
                        "type": constants.LICENSE
                    }

                    if license_info.get("url"):
                        result_dict["url"] = license_info["url"]
                    if license_info.get("identifier"):
                        result_dict["identifier"] = license_info["identifier"]
                    if license_info.get("spdx_id"):
                        result_dict["spdx_id"] = license_info["spdx_id"]

                    metadata_result.add_result(
                        constants.CAT_LICENSE,
                        result_dict,
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "softwareRequirements" in data:
                requirements = parse_software_requirements(data["softwareRequirements"])
                for requirement in requirements:
                    metadata_result.add_result(
                        constants.CAT_REQUIREMENTS,
                        {
                            "value": requirement.get("value"),
                            # "name": requirement.get("name"),
                            # "version": requirement.get("version"),
                            **({"name": requirement["name"]} if "name" in requirement else {}),
                            **({"version": requirement["version"]} if "version" in requirement else {}),
                            "type": constants.SOFTWARE_DEPENDENCY
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
            if "programmingLanguage" in data:
                programming_language = data["programmingLanguage"]
                if isinstance(programming_language, list):
                    for lang in programming_language:
                        lang_info = parse_programming_language(lang)
                        if lang_info:
                            metadata_result.add_result(
                                constants.CAT_PROGRAMMING_LANGUAGES,
                                lang_info,
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                else:
                    lang_info = parse_programming_language(programming_language)
                    if lang_info:
                        metadata_result.add_result(
                            constants.CAT_PROGRAMMING_LANGUAGES,
                            lang_info,
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )

    except Exception as e:
        logging.error(f"Error parsing codemeta JSON file {file_path}: {str(e)}")

    return metadata_result

def map_codemeta_author(author):
    given = author.get("givenName")
    family = author.get("familyName")
    name = author.get("name")

    if not name and (given or family):
        name = f"{given or ''} {family or ''}".strip()

    mapped = {
        constants.PROP_TYPE: constants.AGENT,
        constants.PROP_NAME: name,
        constants.PROP_GIVEN_NAME: given,
        constants.PROP_FAMILY_NAME: family
    }

    identifier = author.get("identifier") or author.get("@id")
    if isinstance(identifier, str) and "orcid.org" in identifier:
        mapped[constants.PROP_URL] = identifier

    return {k: v for k, v in mapped.items() if v is not None}

def map_reference_publication(pub_data):
    if not pub_data:
        return None

    result = {
        constants.PROP_VALUE: pub_data.get("title", ""),
        constants.PROP_TITLE: pub_data.get("title", ""),
        constants.PROP_TYPE: constants.SCHOLARLY_ARTICLE
    }

    if pub_data.get("url"):
        result[constants.PROP_URL] = pub_data.get("url")

    if pub_data.get("date_published"):
        result[constants.PROP_DATE_PUBLISHED] = pub_data.get("date_published")

    if pub_data.get("identifier"):
        result[constants.PROP_DOI] = pub_data.get("identifier")

    authors_raw = pub_data.get("author")

    if authors_raw:
        if isinstance(authors_raw, dict):
            authors_iter = [authors_raw]
        elif isinstance(authors_raw, list):
            authors_iter = authors_raw
        else:
            authors_iter = []

        mapped_authors = [
            map_codemeta_author(a)
            for a in authors_iter
            if isinstance(a, dict)
        ]

        result["authors"] = mapped_authors

    return result

