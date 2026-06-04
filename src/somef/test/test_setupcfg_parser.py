import unittest
import os
from pathlib import Path
from somef.process_results import Result
from somef.parser.setupcfg_parser import parse_setup_cfg
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestSetupCfgParser(unittest.TestCase): 

    def test_issue_988(self):
        """
        Checks that setup.cfg files are parsed correctly.
        """
        setupcfg_file_path = test_data_repositories + os.path.sep + "soca" + os.path.sep + "setup.cfg"
        result = Result()

        metadata_result = parse_setup_cfg(setupcfg_file_path, result, setupcfg_file_path)
        # print(metadata_result.results)
        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], setupcfg_file_path)
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)

        id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(id_results) > 0, "No package id found")
        self.assertEqual(id_results[0]["result"]["value"], "soca")
        self.assertEqual(id_results[0]["result"]["type"], constants.STRING)

        author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(author_results) > 0, "No author found")
        self.assertEqual(author_results[0]["result"]["email"], "daniel.garijo@upm.es")
        self.assertEqual(author_results[0]["result"]["type"], constants.AGENT)

        homepage_results = metadata_result.results.get(constants.CAT_HOMEPAGE, [])
        self.assertTrue(len(homepage_results) > 0, "No homepage found")
        self.assertEqual(homepage_results[0]["result"]["value"], "https://github.com/oeg-upm/soca")
        self.assertEqual(homepage_results[0]["result"]["type"], constants.URL)
        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")
        found_dep = False
        for req_result in requirements_results:
            dependency = req_result["result"]
            if dependency.get("name") == "somef" and dependency.get("dependency_type") == constants.DEPENDENCY_TYPE_RUNTIME:
                found_dep = True
        self.assertTrue(found_dep, "Dependency 'somef' not found")

        runtime_results = metadata_result.results.get(constants.CAT_RUNTIME_PLATFORM, [])
        self.assertTrue(len(runtime_results) > 0, "No runtime platform found")
        self.assertEqual(runtime_results[0]["result"]["name"], "Python")
        self.assertEqual(runtime_results[0]["result"]["version"], ">= 3.10.0")