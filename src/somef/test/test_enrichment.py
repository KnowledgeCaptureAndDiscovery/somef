import json
import os
import unittest
from unittest.mock import patch
from pathlib import Path
from .. import somef_cli
from ..utils import constants
from ..utils.enrichment import run_enrichment

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep


class TestEnrichment(unittest.TestCase):

    @unittest.skipIf(os.getenv("CI") == "true", "Skipped in CI because it requires external APIs")
    def test_enrichment_integration(self):
        """Tests that --enrich adds openalex_id, openaire_id, swhid,
        orcid identifier and funding project properties to the output."""

        somef_cli.run_cli(threshold=0.8,
                          repo_url="https://github.com/oeg-upm/rsfc",
                          output=test_data_path + "test-enrich.json",
                          enrich=True,
                          pretty=True)

        with open(test_data_path + "test-enrich.json") as f:
            data = json.load(f)

        citations = data.get("citation", [])
        # self.assertTrue(any("openalex_id" in c["result"] for c in citations))
        # self.assertTrue(any("openaire_id" in c["result"] for c in citations))

        identifiers = data.get(constants.CAT_IDENTIFIER, [])
        constants.PROP_OPENAIRE_ID
        self.assertTrue(any(
            constants.PROP_OPENAIRE_ID in c["result"] or constants.PROP_OPENALEX_ID in c["result"]
            for c in citations
        ))
        self.assertTrue(any(
            constants.PROP_OPENAIRE_ID in i["result"] or constants.PROP_OPENALEX_ID in i["result"]
            for i in identifiers
        ))
        self.assertTrue(any(constants.PROP_SWHID in i["result"] for i in identifiers))

        authors = data.get("author", [])
        self.assertTrue(any(
            constants.PROP_IDENTIFIER in a["result"] and "orcid" in a["result"].get(constants.PROP_IDENTIFIER, "").lower()
            for a in authors
        ))

        fundings = data.get("funding", [])
        if fundings:
            self.assertTrue(any(constants.PROP_PROJECT_CODE in f["result"] for f in fundings))
            self.assertTrue(any(constants.PROP_GRANT_ID in f["result"] for f in fundings))

        os.remove(test_data_path + "test-enrich.json")


    @unittest.skipIf(os.getenv("CI") == "true", "Skipped in CI")
    def test_enrichment_funding(self):
        """Tests funding enrichment with a repo that has codemeta.json with funding."""
        
        somef_cli.run_cli(threshold=0.8,
                        repo_url="https://github.com/codemeta/codemeta",
                        output=test_data_path + "test-enrich-funding.json",
                        enrich=True,
                        pretty=True)

        with open(test_data_path + "test-enrich-funding.json") as f:
            data = json.load(f)

        fundings = data.get("funding", [])
        self.assertTrue(any("project_code" in f["result"] for f in fundings))
        self.assertTrue(any("project_title" in f["result"] for f in fundings))

        os.remove(test_data_path + "test-enrich-funding.json")


    @patch("somef.utils.enrichment.search_openalex_author")
    def test_enrichment_author_orcid(self, mock_search):
        """Tests that an author without ORCID gets one via search_openalex_author"""

        mock_search.return_value = "https://orcid.org/0000-0003-0454-7145"

        results = {
            constants.CAT_AUTHORS: [
                {
                    "result": {
                        constants.PROP_NAME: "Daniel Garijo",
                    }
                }
            ],
            constants.CAT_CONTRIBUTORS: [],
            constants.CAT_CITATION: [],
            constants.PROP_FUNDING: [],
            constants.PROP_IDENTIFIER: [],
        }

        enriched = run_enrichment(results)

        author_result = enriched[constants.CAT_AUTHORS][0]["result"]
        self.assertIn(constants.PROP_IDENTIFIER, author_result)
        self.assertIn("orcid", author_result[constants.PROP_IDENTIFIER].lower())


    @patch("somef.utils.enrichment.get_openaire_project")
    def test_enrichment_funding_project(self, mock_project):
        """Tests that a funding entry gets enriched with project metadata from OpenAIRE"""

        mock_project.return_value = {
            constants.PROP_PROJECT_CODE: "12345",
            constants.PROP_PROJECT_TITLE: "Test Project",
            constants.PROP_PROJECT_ACRONYM: "TP",
            constants.PROP_GRANT_ID: "EU.H2020.123",
            constants.PROP_FUNDER: "European Commission",
            constants.PROP_START_DATE: "2020-01-01",
            constants.PROP_END_DATE: "2023-12-31",
        }

        results = {
            constants.PROP_FUNDING: [
                {
                    "result": {
                        constants.PROP_FUNDING: "EU.H2020.123",
                    }
                }
            ],
            constants.CAT_CITATION: [],
            constants.PROP_IDENTIFIER: [],
            constants.CAT_AUTHORS: [],
            constants.CAT_CONTRIBUTORS: [],
        }

        enriched = run_enrichment(results)

        fund_result = enriched[constants.PROP_FUNDING][0]["result"]
        self.assertEqual(fund_result[constants.PROP_PROJECT_CODE], "12345")
        self.assertEqual(fund_result[constants.PROP_PROJECT_TITLE], "Test Project")
        self.assertEqual(fund_result[constants.PROP_GRANT_ID], "EU.H2020.123")


    @patch("somef.utils.enrichment.get_openalex_id")
    @patch("somef.utils.enrichment.get_openaire_id")
    def test_enrichment_openaire_fallback(self, mock_openaire, mock_openalex):
        """Tests that OpenAlex is used as fallback when OpenAIRE returns nothing for a DOI"""

        mock_openaire.return_value = None 
        mock_openalex.return_value = "https://openalex.org/W123456"

        results = {
            constants.CAT_CITATION: [
                {
                    "result": {
                        "doi": "10.1007/978-3-319-68204-4_9",
                    }
                }
            ],
            constants.PROP_IDENTIFIER: [],
            constants.CAT_AUTHORS: [],
            constants.CAT_CONTRIBUTORS: [],
            constants.PROP_FUNDING: [],
        }

        enriched = run_enrichment(results)

        cit_result = enriched[constants.CAT_CITATION][0]["result"]
        self.assertNotIn(constants.PROP_OPENAIRE_ID, cit_result)
        self.assertIn(constants.PROP_OPENALEX_ID, cit_result)
        self.assertEqual(cit_result[constants.PROP_OPENALEX_ID], "https://openalex.org/W123456")