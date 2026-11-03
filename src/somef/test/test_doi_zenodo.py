import copy
import json
import os
import unittest

from somef.zenodo_deposit import ZenodoDeposit
from somef.process_results import Result
from somef.somef_cli import run_cli
from somef.utils import constants

TEST_DATA = os.path.join(os.path.dirname(__file__), "test_data", "api_responses", "zenodo")
RECORD_FILE = "zenodo_somef_22943101.json"
DOI = "10.5281/zenodo.22943101"
REPO = "https://github.com/KnowledgeCaptureAndDiscovery/somef"


class TestDOIZenodo(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(TEST_DATA, RECORD_FILE), encoding="utf-8") as f:
            self.record = json.load(f)

    def test_repository_and_files(self):
        """Checks that the repository, tag and files are found for all accepted DOI formats."""

        for value in [DOI, f"https://doi.org/{DOI}",
                      "https://zenodo.org/records/22943101",
                      "https://zenodo.org/record/22943101"]:
            deposit = ZenodoDeposit(value, record=self.record)
            self.assertEqual(deposit.repository_url, REPO)
        self.assertEqual(deposit.tag, "0.11.4")
        self.assertEqual(deposit.source, "https://zenodo.org/records/22943101")
        self.assertEqual(deposit.files(), [(
            "KnowledgeCaptureAndDiscovery/somef-0.11.4.zip",
            "https://zenodo.org/api/records/22943101/files/KnowledgeCaptureAndDiscovery/somef-0.11.4.zip/content")])

    def test_repository_edge_cases(self):
        """Checks records without a repository and repositories without a tag."""

        record = copy.deepcopy(self.record)
        record["metadata"]["related_identifiers"] = []
        deposit = ZenodoDeposit(DOI, record=record)
        self.assertIsNone(deposit.repository_url)
        self.assertIsNone(deposit.tag)

        record["metadata"]["related_identifiers"] = [
            {"identifier": "https://github.com/owner/repo.git", "relation": "isSupplementTo"}]
        deposit = ZenodoDeposit(DOI, record=record)
        self.assertEqual(deposit.repository_url, "https://github.com/owner/repo")
        self.assertIsNone(deposit.tag)

    def test_load_metadata(self):
        """Checks that the Zenodo record metadata is mapped to SOMEF categories."""

        results = ZenodoDeposit(DOI, record=self.record).load_metadata(Result()).results

        def values(category):
            return [r[constants.PROP_RESULT][constants.PROP_VALUE] for r in results[category]]

        self.assertEqual(values(constants.CAT_DATE_PUBLISHED), ["2026-09-24"])
        self.assertEqual(values(constants.CAT_CODE_REPOSITORY), [REPO])
        self.assertEqual(values(constants.CAT_VERSION), ["0.11.4"])
        self.assertEqual(values(constants.CAT_IDENTIFIER), ["https://doi.org/10.5281/zenodo.22943101"])

        license_result = results[constants.CAT_LICENSE][0][constants.PROP_RESULT]
        self.assertEqual(license_result[constants.PROP_SPDX_ID], "MIT")
        self.assertEqual(license_result[constants.PROP_NAME], "MIT License")

        description = values(constants.CAT_DESCRIPTION)[0]
        self.assertTrue(description.startswith("This release includes minor bug fixes"))
        self.assertIn("Full Changelog", description)
        self.assertNotIn("<", description)

        entry = results[constants.CAT_DATE_PUBLISHED][0]
        self.assertEqual(entry["technique"], "Zenodo_API")
        self.assertEqual(entry["source"], "https://zenodo.org/records/22943101")

        self.assertNotIn(constants.CAT_CONTRIBUTORS, results)
        self.assertNotIn(constants.CAT_KEYWORDS, results)

    def test_authors(self):
        """Checks the extraction of authors: names, ORCID and accents."""

        results = ZenodoDeposit(DOI, record=self.record).load_metadata(Result()).results
        authors = [a[constants.PROP_RESULT] for a in results[constants.CAT_AUTHORS]]
        self.assertEqual(len(authors), 11)

        self.assertEqual(authors[0][constants.PROP_NAME], "Daniel Garijo")
        self.assertEqual(authors[0][constants.PROP_LAST_NAME], "Garijo")
        self.assertEqual(authors[0][constants.PROP_GIVEN_NAME], "Daniel")
        self.assertEqual(authors[0][constants.PROP_URL], "https://orcid.org/0000-0003-0454-7145")

        self.assertEqual(authors[1][constants.PROP_NAME], "Allen Mao")
        self.assertNotIn(constants.PROP_URL, authors[1])

        self.assertIn("Miguel Angel García", [a[constants.PROP_NAME] for a in authors])

    def test_invalid_input(self):
        """Checks that invalid DOIs and incompatible options are rejected."""
        for bad in ["10.1000/other.123", "https://github.com/owner/repo", "", None]:
            with self.assertRaises(ValueError):
                ZenodoDeposit(bad, record=self.record)
        self.assertIsNone(run_cli(doi="not-a-doi"))
        self.assertIsNone(run_cli(doi=DOI, repo_url="https://github.com/owner/repo"))


if __name__ == "__main__":
    unittest.main()
