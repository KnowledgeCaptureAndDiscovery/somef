import unittest
import os
from pathlib import Path
from somef.process_results import Result
from somef.parser.publiccode_parser import parse_publiccode_file

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestPubliccodeParser(unittest.TestCase): 

    def test_issue_733(self):

        """Checks if this repository has properties extracted from publiccode.yaml. MaykinMedia repository"""
        publiccode_file_path = test_data_repositories + os.path.sep + "maykinMedia" + os.path.sep + "publiccode.yaml"
        result = Result()

        metadata_result = parse_publiccode_file(
            publiccode_file_path,
            result,
            publiccode_file_path
        )
        # print("Metadata results:", metadata_result.results)
        platform = metadata_result.results.get("runtime_platform", [])
        code_parser_platforms = [
            entry["result"]["value"]
            for entry in platform
            if entry.get("technique") == "code_parser"
        ]

        assert "web" in code_parser_platforms, (
            "Expected platform 'web' extracted from publiccode.yaml "
            f"with technique 'code_parser'. Found: {code_parser_platforms}"
        )

        code_repos = [entry["result"]["value"] for entry in metadata_result.results.get("code_repository", [])]
        assert "http://github.com/maykinmedia/objects-api.git" in code_repos

        app_domains = [entry["result"]["value"] for entry in metadata_result.results.get("application_domain", [])]
        expected_domains = ["data-collection", "it-development"]
        for domain in expected_domains:
            assert domain in app_domains

        requirements = metadata_result.results.get("requirements", [])
     
        req_map = {entry["result"]["name"]: entry["result"]["version"] for entry in requirements}
        assert req_map["Objecttypes API"] == ">=1.0"
        assert req_map["PostgreSQL"] == ">=14.0"

        version = metadata_result.results.get("version", [])
        self.assertEqual(version[0]["result"]["value"], "3.5.0")

        descriptions = metadata_result.results.get("description", [])
        self.assertTrue(len(descriptions) > 3, "Must be at least four descriptions found")
        self.assertEqual(descriptions[0]["result"]["value"], 'API voor het beheren van objecten')

        name = metadata_result.results.get("name", [])
        self.assertEqual(name[0]["result"]["value"], "Objects API")

        keywords_values = metadata_result.results.get("keywords", [])
        self.assertTrue(keywords_values)
        keywords = keywords_values[0]["result"]["value"]
        self.assertEqual(keywords[1],"Minimalistische objecten beheerinterface")
        self.assertEqual(keywords[3],"Minimalistic object management interface")

        development_status = metadata_result.results.get("development_status", [])
        self.assertEqual(development_status[0]["result"]["value"], 'beta')

        licenses = metadata_result.results.get("license", [])
        self.assertEqual(licenses[0]["result"]["value"], 'EUPL-1.2')
        date_updated = metadata_result.results.get("date_updated", [])
        self.assertEqual(date_updated[0]["result"]["value"], '2025-12-01')

        owners = metadata_result.results.get("owner", [])
        self.assertEqual(owners[0]["result"]["email"], 'info@maykinmedia.nl')
        self.assertEqual(owners[1]["result"]["value"], 'Joeri Bekker')

    def test_issue_733_2(self):

        """Checks if this repository has properties extracted from publiccode.yaml Example publiccode repository"""
        publiccode_file_path = test_data_repositories + os.path.sep + "publicCode-Example" + os.path.sep + "publiccode.yml"
        result = Result()

        metadata_result = parse_publiccode_file(
            publiccode_file_path,
            result,
            publiccode_file_path
        )
        # print("Metadata results:", metadata_result.results)
        platform = metadata_result.results.get("runtime_platform", [])
        code_parser_platforms = [
            entry["result"]["value"]
            for entry in platform
            if entry.get("technique") == "code_parser"
        ]

        assert "android" in code_parser_platforms, (
            "Expected platform 'android' extracted from publiccode.yaml "
            f"with technique 'code_parser'. Found: {code_parser_platforms}"
        )

        code_repos = [entry["result"]["value"] for entry in metadata_result.results.get("code_repository", [])]
        assert "https://example.com/italia/medusa.git" in code_repos

        app_domains = [entry["result"]["value"] for entry in metadata_result.results.get("application_domain", [])]
        expected_domains = ["content-management", "office"]
        for domain in expected_domains:
            assert domain in app_domains

        requirements = metadata_result.results.get("requirements", [])
     
        req_map = {entry["result"]["name"]: entry["result"]["version"] for entry in requirements}
        assert req_map["MySQL"] == ">=1.1,<1.3"
        assert req_map["PostgreSQL"] == "3.2"
        assert req_map["Oracle"] == ">=11.4"
        assert req_map["IBM SoftLayer"] is None
        assert req_map["NFC Reader"] is None

        version = metadata_result.results.get("version", [])
        self.assertEqual(version[0]["result"]["value"], "1.0")

        descriptions = metadata_result.results.get("description", [])
        self.assertTrue(len(descriptions) > 1, "Must be at least two descriptions found")
        self.assertEqual(descriptions[0]["result"]["value"], 'This description can have a maximum 150 characters long. We should not fill the remaining space with "Lorem Ipsum". End')

        name = metadata_result.results.get("name", [])
        self.assertEqual(name[0]["result"]["value"], "Medusa")

        keywords_values = metadata_result.results.get("keywords", [])
        self.assertTrue(keywords_values)
        keywords = keywords_values[0]["result"]["value"]
        self.assertEqual(keywords[1],"Will run without a problem")
        self.assertEqual(keywords[2],"Has zero bugs")

        development_status = metadata_result.results.get("development_status", [])
        self.assertEqual(development_status[0]["result"]["value"], 'development')

        licenses = metadata_result.results.get("license", [])
        print(licenses)
        self.assertEqual(licenses[0]["result"]["spdx_id"], 'AGPL-3.0')
        date_updated = metadata_result.results.get("date_updated", [])
        self.assertEqual(date_updated[0]["result"]["value"], '2017-04-15')


