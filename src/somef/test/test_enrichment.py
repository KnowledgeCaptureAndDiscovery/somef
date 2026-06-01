import json
import os
import unittest
from pathlib import Path
from .. import somef_cli
from ..utils import constants

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
        self.assertTrue(any("openalex_id" in c["result"] for c in citations))
        self.assertTrue(any("openaire_id" in c["result"] for c in citations))

        identifiers = data.get("identifier", [])
        self.assertTrue(any("openalex_id" in i["result"] for i in identifiers))
        self.assertTrue(any("openaire_id" in i["result"] for i in identifiers))
        self.assertTrue(any("swhid" in i["result"] for i in identifiers))

        authors = data.get("author", [])
        self.assertTrue(any(
            "identifier" in a["result"] and "orcid" in a["result"].get("identifier", "").lower()
            for a in authors
        ))

        fundings = data.get("funding", [])
        if fundings:
            self.assertTrue(any("project_code" in f["result"] for f in fundings))
            self.assertTrue(any("grant_id" in f["result"] for f in fundings))

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