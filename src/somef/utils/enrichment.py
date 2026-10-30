
import requests
import re
import logging
import json
from urllib.parse import quote
from ..utils import constants
import xml.etree.ElementTree as ET

def _safe_json_response(resp):
    try:
        data = resp.json()
    except ValueError:
        return None
    return data if isinstance(data, dict) else None

def _extract_doi_from_value(value):
    if isinstance(value, str):
        match = re.search(constants.REGEXP_DOI_IN_URL, value)
        return match.group(0) if match else None

    if isinstance(value, dict):
        for key in ("doi", "value", "identifier", "url"):
            doi = _extract_doi_from_value(value.get(key))
            if doi:
                return doi
        return None

    if isinstance(value, list):
        for item in value:
            doi = _extract_doi_from_value(item)
            if doi:
                return doi

    return None

def get_openalex_id(doi):
    url = f"{constants.OPENALEX_BASE}/works/doi:{doi}"
    try:
        resp = requests.get(url)
    except requests.RequestException:
        return None                             
    if resp.status_code != 200:
        return None
    data = _safe_json_response(resp)
    if data:
        return data.get("id")
    return None

def get_openaire_id(doi) -> dict | None:
    # url = f"{constants.OPENAIRE_BASE}/search/researchProducts?doi={doi}&format=json"
    url = f"{constants.OPENAIRE_BASE}/research-products?filter=ids.doi:{doi}&pageSize=1"
    try:
        resp = requests.get(url, timeout=15)
    except requests.RequestException:
        return None
    if resp.status_code != 200:
        return None
    
    data = _safe_json_response(resp)
    
    if not data:
        return None

    results = data.get("results")
    if not isinstance(results, list) or not results:
        return None
    first_result = results[0]
    if doi.lower() not in json.dumps(first_result).lower():
            return None

    raw_id = first_result.get("id")
    if raw_id:
        return f"{constants.OPENAIRE_EXPLORE}/search/result?id={raw_id}"
    return None

def get_zenodo_swhid(doi):
    """Get SWHID from a Zenodo DOI"""

    match = re.search(constants.REGEXP_FIND_ZENODO, doi)
    if not match:
        return None
    record_id = match.group(1)
    
    url = f"{constants.ZENODO_API_BASE}/records/{record_id}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    
    data = resp.json()
    
    swh = data.get("swh", {})
    if swh:
        return swh.get("id") or swh.get(constants.PROP_SWHID)

    for rel_id in data.get("metadata", {}).get("related_identifiers", []):
        if rel_id.get("identifier", "").startswith("swh:"):
            return rel_id["identifier"]
    
    return None


def extract_doi(result):
    """Extract a DOI from a result dict which may contain a DOI in different fields and formats."""

    doi = result.get("doi")
    if doi:
        return doi

    for entry in result.get("identifier", []):
        if entry.get("type") == "doi":
            return entry.get("value")

    for key in ("url", "value"):
        doi_url = re.search(constants.REGEXP_DOI_IN_URL, result.get(key, ""))
        if doi_url:
            return doi_url.group(1)
        
    return None


def search_openalex_author(name):
    url = f"{constants.OPENALEX_BASE}/authors?search={requests.utils.quote(name)}"
    try:
        resp = requests.get(url)
    except requests.RequestException:
        return None
    if resp.status_code != 200:
        return None
    data = _safe_json_response(resp)
    if not data:
        return None

    results = data.get("results", [])
    if isinstance(results, list) and results and isinstance(results[0], dict):
        return results[0].get("orcid")
    return None


def collect_existing_orcids(results):
    """
    Collect ORCIDs already present in the data.
    Looks for ORCIDs in citation authors (url field) and in author/contributor entries (identifier and url fields).
    """
    orcid_map = {}
    
    for citation in results.get(constants.CAT_CITATION, []):
        for author in citation["result"].get(constants.PROP_AUTHOR, []):
            add_orcid_to_map(orcid_map, author.get(constants.PROP_NAME, ""), author.get(constants.PROP_URL, ""))
            add_orcid_to_map(orcid_map, author.get(constants.PROP_NAME, ""), author.get(constants.PROP_IDENTIFIER, ""))
 
    for category in (constants.CAT_AUTHORS, constants.CAT_CONTRIBUTORS):
        for entry in results.get(category, []):
            result = entry["result"]
            add_orcid_to_map(orcid_map, result.get(constants.PROP_NAME, ""), result.get(constants.PROP_IDENTIFIER, ""))
            add_orcid_to_map(orcid_map, result.get(constants.PROP_NAME, ""), result.get(constants.PROP_URL, ""))
    return orcid_map


def add_orcid_to_map(orcid_map, name, value):
    """Add an ORCID to the map if value contains an ORCID and name is not empty."""
    if value and "orcid" in value.lower() and name:
        orcid_map[name.lower().strip()] = value


def clean_name(name):
    """Remove newlines and surrounding whitespace from a name string."""
    return name.replace("\n", "").strip()


def has_orcid(result):
    """Check if a result already has an ORCID."""
    for key in ("identifier", "url"):
        val = result.get(key, "")
        if "orcid" in val.lower():
            return True
    return False


def get_openaire_project(identifier):
    """Search for a project in OpenAIRE by grant ID or call identifierr"""
    # url = f"{constants.OPENAIRE_BASE}/search/projects?keywords={requests.utils.quote(identifier)}"
    url = f"{constants.OPENAIRE_BASE}/projects?code={requests.utils.quote(identifier)}&pageSize=1"
  
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    
    data = _safe_json_response(resp)
    if not data:
        return None

    results = data.get("results")
    if not isinstance(results, list) or not results or not isinstance(results[0], dict):
        return None
  
    project = results[0]
    funding = project.get("funding") or {}
    funder = funding.get("funder") or {}

    return {
        constants.PROP_PROJECT_CODE: project.get("code"),
        constants.PROP_PROJECT_TITLE: project.get("title"),
        constants.PROP_PROJECT_ACRONYM: project.get("acronym"),
        constants.PROP_GRANT_ID: project.get("callidentifier"),
        # constants.PROP_FUNDER: project.findtext(".//funder/shortname"),
        constants.PROP_FUNDER: funder.get("shortname"),
        constants.PROP_START_DATE: project.get("startdate"),
        constants.PROP_END_DATE: project.get("enddate"),
    }

def run_enrichment(results) -> dict:

    logging.info("Enrichment process started.")

    for citation in results.get(constants.CAT_CITATION, []):
        doi = extract_doi(citation["result"])
        if doi:
            openaire_id = get_openaire_id(doi)
            if openaire_id:
                citation["result"][constants.PROP_OPENAIRE_ID] = openaire_id
            else:
                citation["result"][constants.PROP_OPENALEX_ID] = get_openalex_id(doi)

    for identifier in results.get(constants.PROP_IDENTIFIER, []):
        value = identifier["result"].get("value", "")
        doi = _extract_doi_from_value(value)
        if doi:
            openaire_id = get_openaire_id(doi)
            if openaire_id:
                identifier["result"][constants.PROP_OPENAIRE_ID] = openaire_id
            else:
                openalex_id = get_openalex_id(doi)
                if openalex_id:
                    identifier["result"][constants.PROP_OPENALEX_ID] = openalex_id

            if "zenodo" in doi.lower() and constants.PROP_SWHID not in identifier["result"]:
                swhid = get_zenodo_swhid(doi)
                if swhid:
                    identifier["result"][constants.PROP_SWHID] = swhid

    orcid_map = collect_existing_orcids(results)

    for category in (constants.CAT_AUTHORS, constants.CAT_CONTRIBUTORS):
        for entry in results.get(category, []):
            result = entry["result"]
            if has_orcid(result): 
                continue
            name = clean_name(result.get(constants.PROP_NAME) or result.get("value", ""))
            if not name:
                continue
            
            orcid = orcid_map.get(name.lower())

            if not orcid:
                orcid = search_openalex_author(name)
            
            if orcid:
                result[constants.PROP_IDENTIFIER] = orcid

    for funding in results.get(constants.PROP_FUNDING, []):
        result = funding["result"]
        identifier = result.get(constants.PROP_FUNDING)
        if identifier:
            identifier = identifier.split(";")[0].strip()
        elif result.get(constants.PROP_IDENTIFIER):
            identifier = result.get(constants.PROP_IDENTIFIER)
        else:
            funder = result.get(constants.PROP_FUNDER)
            if isinstance(funder, dict):
                identifier = funder.get(constants.PROP_NAME)
            else:
                identifier = funder

        if identifier:
            project = get_openaire_project(identifier)
            # logging.info(f"Enrichment found project for funding identifier '{identifier}': {project}")
            if project:
                if project[constants.PROP_PROJECT_CODE]:
                    result[constants.PROP_PROJECT_CODE] = project[constants.PROP_PROJECT_CODE]
                if project[constants.PROP_PROJECT_TITLE]:
                    result[constants.PROP_PROJECT_TITLE] = project[constants.PROP_PROJECT_TITLE]
                if project[constants.PROP_PROJECT_ACRONYM]:
                    result[constants.PROP_PROJECT_ACRONYM] = project[constants.PROP_PROJECT_ACRONYM]
                if project[constants.PROP_GRANT_ID]:
                    result[constants.PROP_GRANT_ID] = project[constants.PROP_GRANT_ID]

    return results