import json
import logging
from ..process_results import Result
from ..utils import constants

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

def parse_authors(author_data):
    """
    Parse author information from codemeta.json
    
    Parameters
    ----------
    author_data: list or dict
    The author data from codemeta.json
        
    Returns
    -------
    list
    """
    authors = []
    
    if isinstance(author_data, list):
        for author in author_data:
            if isinstance(author, dict):
                author_info = {}
                
                if "name" in author:
                    author_info["name"] = author["name"]
                elif "givenName" in author and "familyName" in author:
                    author_info["name"] = f"{author.get('givenName', '')} {author.get('familyName', '')}".strip()
                
                if "email" in author:
                    author_info["email"] = author["email"]
                
                if "affiliation" in author:
                    if isinstance(author["affiliation"], dict):
                        author_info["affiliation"] = author["affiliation"].get("name", "")
                    elif isinstance(author["affiliation"], str):
                        author_info["affiliation"] = author["affiliation"]
                
                if "identifier" in author:
                    author_info["identifier"] = author["identifier"]
                elif "@id" in author:
                    author_info["identifier"] = author["@id"]
                
                if author_info:  
                    authors.append(author_info)
            elif isinstance(author, str):
                authors.append({"name": author})

    elif isinstance(author_data, dict):
        author_info = {}
        
        if "name" in author_data:
            author_info["name"] = author_data["name"]
        elif "givenName" in author_data and "familyName" in author_data:
            author_info["name"] = f"{author_data.get('givenName', '')} {author_data.get('familyName', '')}".strip()
        
        if "email" in author_data:
            author_info["email"] = author_data["email"]
        
        if "affiliation" in author_data:
            if isinstance(author_data["affiliation"], dict):
                author_info["affiliation"] = author_data["affiliation"].get("name", "")
            elif isinstance(author_data["affiliation"], str):
                author_info["affiliation"] = author_data["affiliation"]
        
        if "identifier" in author_data:
            author_info["identifier"] = author_data["identifier"]
        elif "@id" in author_data:
            author_info["identifier"] = author_data["@id"]
        
        if author_info: 
            authors.append(author_info)
    
    return authors

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
        # Extract SPDX ID from identifier if it's an SPDX URL
        identifier = license_info.get("identifier", "")
        if "spdx.org/licenses/" in identifier:
            spdx_id = identifier.split("spdx.org/licenses/")[-1].split("/")[0]
            license_info["spdx_id"] = spdx_id
    elif isinstance(license_data, str):
        # Assume the string is the SPDX ID (e.g., "Apache-2.0")
        license_info["name"] = license_data
        license_info["identifier"] = f"https://spdx.org/licenses/{license_data}"
        license_info["spdx_id"] = license_data
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
    
    if isinstance(requirements_data, list):
        for req in requirements_data:
            if isinstance(req, str):
                requirements.append(req)
    elif isinstance(requirements_data, str):
        requirements.append(requirements_data)
    
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

def parse_description(description_data):
    """
    Parse description information from codemeta.json
    This can be either a string or a list of strings
    
    Parameters
    ----------
    description_data: str or list
    The description data from codemeta.json
        
    Returns
    -------
    list
    """
    descriptions = []
    
    if isinstance(description_data, str):
        descriptions.append(description_data)
    elif isinstance(description_data, list):
        for desc in description_data:
            if isinstance(desc, str):
                descriptions.append(desc)
    
    return descriptions

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
                    constants.CAT_APPLICATION_CATEGORY,
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
                metadata_result.add_result(
                    constants.CAT_DATE_CREATED,
                    {
                        "value": data["dateCreated"],
                        "type": constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )
            
            if "dateModified" in data:
                metadata_result.add_result(
                    constants.CAT_DATE_UPDATED,
                    {
                        "value": data["dateModified"],
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
                        if pub_data:
                            result_dict = {
                                "value": pub_data.get("title", ""),
                                "title": pub_data.get("title", ""),
                                "type": constants.SCHOLARLY_ARTICLE
                            }
                            
                            if pub_data.get("url"):
                                result_dict["url"] = pub_data.get("url")
                            
                            if pub_data.get("date_published"):
                                result_dict["date_published"] = pub_data.get("date_published")
                                
                            if pub_data.get("identifier"):
                                result_dict["doi"] = pub_data.get("identifier")
                                
                            metadata_result.add_result(
                                constants.CAT_REF_PUBLICATION,
                                result_dict,
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                elif isinstance(ref_publications, dict):
                    pub_data = parse_referenced_publication(ref_publications)
                    if pub_data:
                        result_dict = {
                            "value": pub_data.get("title", ""),
                            "title": pub_data.get("title", ""),
                            "type": constants.SCHOLARLY_ARTICLE
                        }
                        
                        if pub_data.get("url"):
                            result_dict["url"] = pub_data.get("url")
                        
                        if pub_data.get("date_published"):
                            result_dict["date_published"] = pub_data.get("date_published")
                            
                        if pub_data.get("identifier"):
                            result_dict["doi"] = pub_data.get("identifier")
                            
                        metadata_result.add_result(
                            constants.CAT_REF_PUBLICATION,
                            result_dict,
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
                license_info = parse_license(data["license"])
                if license_info:
                    result_dict = {
                        "type": constants.LICENSE
                    }
                    
                    if license_info.get("name"):
                        result_dict["name"] = license_info.get("name")
                    
                    if license_info.get("url"):
                        result_dict["url"] = license_info.get("url")
                    
                    if license_info.get("identifier"):
                        result_dict["identifier"] = license_info.get("identifier")
                    
                    if license_info.get("spdx_id"):
                        result_dict["spdx_id"] = license_info.get("spdx_id")
                    
                    metadata_result.add_result(
                        constants.CAT_LICENSE,
                        result_dict,
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

            if "author" in data:
                authors = parse_authors(data["author"])
                if authors:
                    for author in authors:
                        author_dict = {
                            "type": "string"
                        }
                        
                        if "name" in author:
                            author_dict["name"] = author["name"]
                        
                        if "email" in author:
                            author_dict["email"] = author["email"]
                        
                        if "affiliation" in author:
                            author_dict["affiliation"] = author["affiliation"]
                        
                        if "identifier" in author:
                            author_dict["identifier"] = author["identifier"]
                        
                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            author_dict,
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )

            if "license" in data:
                license_info = parse_license(data["license"])
                if license_info:
                    result_dict = {
                        "value": license_info.get("name", ""), 
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
                if requirements:
                    metadata_result.add_result(
                        constants.CAT_REQUIREMENTS,
                        {
                            "value": requirements,
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
    
    except Exception as e:
            logging.error(f"Error parsing codemeta JSON file {file_path}: {str(e)}")
    
    return metadata_result

