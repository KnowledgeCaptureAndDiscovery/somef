import re
import requests
import logging
import os
import zipfile

from .utils import constants
from .process_results import Result
from .regular_expressions import detect_license_spdx
# from .process_repository import rate_limit_get


class ZenodoDeposit:
    """
    A Zenodo deposit loaded from a DOI or record URL (issue 889).
    Accepted inputs: https://doi.org/10.5281/zenodo.X, 10.5281/zenodo.X,
    https://zenodo.org/records/X (or /record/X)
    """

    def __init__(self, doi, record=None):
        """
        Validates the DOI or record URL and downloads the Zenodo record.
        Raises ValueError if the input is not a Zenodo DOI or the record
        cannot be retrieved.
        """
        if not doi:
            raise ValueError("Missing Zenodo DOI")
        match = re.search(constants.REGEXP_ZENODO_RECORD_ID, doi, re.IGNORECASE)
        if not match:
            raise ValueError(
                f"Not a Zenodo DOI: {doi}. Expected https://doi.org/10.5281/zenodo.X, "
                f"10.5281/zenodo.X or https://zenodo.org/records/X")
        
        if record is None:
            try:
                response = requests.get(f"{constants.ZENODO_API_BASE}/records/{match.group(1)}",
                                        timeout=30)
                response.raise_for_status()
            except requests.RequestException as e:
                raise ValueError(f"Cannot retrieve Zenodo record for '{doi}': {e}") from e
            self.record = response.json()
        else:
            self.record = record

        self.doi = doi
        links = self.record.get("links") or {}
        self.source = links.get("self_html") or f"https://zenodo.org/records/{self.record.get('id')}"
        self.repository_url, self.tag = self._find_repository()

    def files(self):
        """Returns a list of (file name, download link) for the files in the deposit."""
        files = []
        for zenodo_file in self.record.get("files") or []:
            links = zenodo_file.get("links") or {}
            link = links.get("self") or links.get("download")
            if link:
                files.append((zenodo_file.get("key"), link))
        return files

    def _find_repository(self):
        """
        Looks for the origin repository in related_identifiers.
        Returns (url, tag) or (None, None). The tag is only captured from
        /tree/X (GitHub) and /-/tree/X (GitLab) links.
        """
        for rel in (self.record.get("metadata") or {}).get("related_identifiers") or []:
            match = re.match(constants.REGEXP_ZENODO_REPOSITORY_PATTERN, rel.get("identifier") or "")
            if match:
                url = re.sub(r'\.git$', '', match.group(1))
                return url, match.group(2)
        return None, None

    @staticmethod
    def _agent(person):
        """Zenodo person (creators/contributors) -> agent dict, same shape as authors.md."""
        name = (person.get("name") or "").strip()
        if not name:
            return None
        agent = {
            constants.PROP_TYPE: constants.AGENT,
            constants.PROP_VALUE: name,
            constants.PROP_NAME: name,
        }
        if "," in name:
            family, _, given = name.partition(",")
            family, given = family.strip(), given.strip()
            if family and given:
                agent[constants.PROP_VALUE] = agent[constants.PROP_NAME] = f"{given} {family}"
                agent[constants.PROP_LAST_NAME] = family
                agent[constants.PROP_GIVEN_NAME] = given
        orcid = person.get("orcid")
        if orcid:
            agent[constants.PROP_URL] = orcid if orcid.startswith("http") else f"https://orcid.org/{orcid}"
        return agent

    def load_metadata(self, repo_metadata: Result) -> Result:
        """
        Maps the metadata of the deposit into SOMEF categories (issue 889).
        """
        metadata = self.record.get("metadata") or {}
        source = self.source
        technique = constants.TECHNIQUE_ZENODO_API
        confidence = 1

        def add(category, result):
            repo_metadata.add_result(category, result, confidence, technique, source)

        if metadata.get("title"):
            add(constants.CAT_FULL_TITLE,
                {constants.PROP_TYPE: constants.STRING, constants.PROP_VALUE: metadata["title"]})

        if metadata.get("description"):
            description = re.sub(constants.REGEXP_CLEAN_HTML_TAGS, " ", metadata["description"])
            description = re.sub(r'\s+', " ", description).strip()
            add(constants.CAT_DESCRIPTION,
                {constants.PROP_TYPE: constants.STRING, constants.PROP_VALUE: description})

        for person in metadata.get("creators") or []:
            agent = self._agent(person)
            if agent:
                add(constants.CAT_AUTHORS, agent)
        for person in metadata.get("contributors") or []:
            agent = self._agent(person)
            if agent:
                add(constants.CAT_CONTRIBUTORS, agent)

        if metadata.get("version"):
            add(constants.CAT_VERSION,
                {constants.PROP_TYPE: constants.STRING, constants.PROP_VALUE: str(metadata["version"])})

        license_data = metadata.get("license") or {}
        if license_data.get("id"):
            spdx = detect_license_spdx(license_data["id"], 'JSON')
            if spdx:
                add(constants.CAT_LICENSE, {
                    constants.PROP_VALUE: spdx["url"], constants.PROP_TYPE: constants.LICENSE,
                    constants.PROP_NAME: spdx["name"], constants.PROP_URL: spdx["url"],
                    constants.PROP_SPDX_ID: spdx["spdx_id"], constants.PROP_IDENTIFIER: spdx["url"]})
            else:
                add(constants.CAT_LICENSE, {
                    constants.PROP_VALUE: license_data["id"], constants.PROP_TYPE: constants.LICENSE,
                    constants.PROP_NAME: license_data.get("title") or license_data["id"]})

        if metadata.get("keywords"):
            add(constants.CAT_KEYWORDS,
                {constants.PROP_TYPE: constants.STRING,
                 constants.PROP_VALUE: ", ".join(metadata["keywords"])})

        doi_url = self.record.get("doi_url") or (
            f"https://doi.org/{self.record['doi']}" if self.record.get("doi") else None)
        if doi_url:
            add(constants.CAT_IDENTIFIER,
                {constants.PROP_TYPE: constants.URL, constants.PROP_VALUE: doi_url})

        if metadata.get("publication_date"):
            add(constants.CAT_DATE_PUBLISHED,
                {constants.PROP_TYPE: constants.DATE, constants.PROP_VALUE: metadata["publication_date"]})

        for _, file_link in self.files():
            add(constants.CAT_DOWNLOAD_URL,
                {constants.PROP_TYPE: constants.URL, constants.PROP_VALUE: file_link})

        if self.repository_url:
            add(constants.CAT_CODE_REPOSITORY,
                {constants.PROP_TYPE: constants.URL, constants.PROP_VALUE: self.repository_url})

        return repo_metadata

    # def download_files(self, target_dir, download_limit=None):
    #     """
    #     Downloads the deposit files into target_dir.
    #     Returns the path to the folder containing the files, or None.
    #     """
    #     files = self.files()
    #     if not files:
    #         logging.warning(f"Zenodo record {self.record.get('id')} has no downloadable files")
    #         return None
    #     record_id = str(self.record.get("id"))
    #     dest = os.path.join(target_dir, record_id)
    #     os.makedirs(dest, exist_ok=True)
    #     for name, link in files:
    #         safe_name = os.path.basename(os.path.normpath(name or ""))
    #         if not safe_name:
    #             continue
    #         logging.info(f"Downloading {link}")
    #         response, _ = rate_limit_get(link, size_limit_mb=download_limit)
    #         if response is None or response.status_code != 200:
    #             logging.warning(f"Could not download Zenodo file {name}")
    #             continue
    #         file_path = os.path.join(dest, safe_name)
    #         with open(file_path, "wb") as f:
    #             f.write(response.content)
    #         if safe_name.lower().endswith(".zip"):
    #             try:
    #                 with zipfile.ZipFile(file_path, "r") as zip_ref:
    #                     zip_ref.extractall(dest)
    #                 os.remove(file_path)
    #             except zipfile.BadZipFile:
    #                 logging.warning(f"Zenodo file {name} is not a valid zip")
    #     return dest