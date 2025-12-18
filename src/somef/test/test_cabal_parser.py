import unittest
import os
from pathlib import Path

from somef.parser.cabal_parser import parse_cabal_file
from somef.process_results import Result
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestCabalParser(unittest.TestCase):

    def test_parse_cabal(self):
        cabal_file_path = test_data_repositories + os.path.sep + "unused" + os.path.sep + "unused.cabal"
        result = Result()

        metadata_result = parse_cabal_file(cabal_file_path, result, "https://example.org/unused.cabal")
        
        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        # self.assertEqual(package_results[0]["result"]["value"], "unused.cabal")
        self.assertEqual(package_results[0]["result"]["value"], "https://example.org/unused.cabal")      
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)
        
        id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(id_results) > 0, "No identifier found")
        self.assertEqual(id_results[0]["result"]["value"], "unused")
        self.assertEqual(id_results[0]["result"]["type"], constants.STRING)

        description_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(description_results) > 0, "No description found")
        self.assertEqual(description_results[0]["result"]["value"], "Please see README.md")
        self.assertEqual(description_results[0]["result"]["type"], constants.STRING)

        homepage_results = metadata_result.results.get(constants.CAT_HOMEPAGE, [])
        self.assertTrue(len(homepage_results) > 0, "No homepage found")
        self.assertEqual(homepage_results[0]["result"]["value"], "https://github.com/joshuaclayton/unused#readme")
        self.assertEqual(homepage_results[0]["result"]["type"], constants.URL)

        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "MIT")
        self.assertEqual(license_results[0]["result"]["type"], constants.LICENSE)

        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")
    
        found_dep = False
        for req_result in requirements_results:
            dependency = req_result["result"]
            if dependency.get("name") == "terminal-progress-bar" and dependency.get("dependency_type") == "runtime":
                found_dep = True
        self.assertTrue(found_dep, "Dependency not found")

    def test_parse_2_cabal(self):
        cabal_file_path = test_data_repositories + os.path.sep + "haskell" + os.path.sep + "cabal.cabal"
        result = Result()

        metadata_result = parse_cabal_file(cabal_file_path, result, "https://example.org/cabal.cabal")
        
        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        # self.assertEqual(package_results[0]["result"]["value"], "cabal.cabal")
        self.assertEqual(package_results[0]["result"]["value"], "https://example.org/cabal.cabal")
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)
        description_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(description_results) > 0, "No description found")
        expected_start = "The Haskell Common Architecture"

        self.assertTrue(
            description_results[0]["result"]["value"].strip().startswith(expected_start)
        )

        homepage_results = metadata_result.results.get(constants.CAT_HOMEPAGE, [])
        self.assertTrue(len(homepage_results) > 0, "No homepage found")
        self.assertEqual(homepage_results[0]["result"]["value"], "http://www.haskell.org/cabal/")
        self.assertEqual(homepage_results[0]["result"]["type"], constants.URL)

        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "BSD-3-Clause")
        self.assertEqual(license_results[0]["result"]["type"], constants.LICENSE)

        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertEqual(requirements_results[0]["result"]["name"], "Cabal-syntax")
        self.assertEqual(requirements_results[1]["result"]["version"], ">= 0.4.0.1  && < 0.6")

        issue_tracker_results = metadata_result.results.get(constants.CAT_ISSUE_TRACKER, [])
        self.assertEqual(issue_tracker_results[0]["result"]["value"], "https://github.com/haskell/cabal/issues")

    
if __name__ == "__main__":
    unittest.main()