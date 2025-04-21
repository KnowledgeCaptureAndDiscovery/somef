import unittest
import os
from pathlib import Path
from ..parser.python_parser import parse_pyproject_toml
from ..process_results import Result
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestPythonParser(unittest.TestCase):
    
    def test_parse_pyproject_toml(self):
        pyproject_path = test_data_repositories + os.path.sep+ "gammalearn"+ os.path.sep+ "pyproject.toml"
        result = Result()

        metadata_result = parse_pyproject_toml(pyproject_path, result, "https://example.org/pyproject.toml")
        
        package_id = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        # print(package_id)
        self.assertTrue(len(package_id) > 0, "No identifier found")
        self.assertEqual(package_id[0]["result"]["value"], "gammalearn")
        
        self.assertIn(constants.CAT_DESCRIPTION, result.results)
        description = result.results[constants.CAT_DESCRIPTION][0]["result"]["value"]
        self.assertEqual(description, "A framework to easily train deep learning model on Imaging Atmospheric Cherenkov Telescopes data")
        
        self.assertIn(constants.CAT_AUTHORS, result.results)
        authors = result.results[constants.CAT_AUTHORS]
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0]["result"]["name"], "M. Jacquemont")
        self.assertEqual(authors[0]["result"]["email"], "jacquemont@lapp.in2p3.fr")
        self.assertEqual(authors[1]["result"]["name"], "T. Vuillaume")
        self.assertEqual(authors[1]["result"]["email"], "thomas.vuillaume@lapp.in2p3.fr")
        
        self.assertIn(constants.CAT_LICENSE, result.results)
        license_info = result.results[constants.CAT_LICENSE][0]["result"]["value"]
        self.assertEqual(license_info, "License file: LICENSE")
        
        self.assertIn(constants.CAT_CODE_REPOSITORY, result.results)
        repo_url = result.results[constants.CAT_CODE_REPOSITORY][0]["result"]["value"]
        self.assertEqual(repo_url, "https://gitlab.in2p3.fr/gammalearn/gammalearn")
        
        self.assertIn(constants.CAT_DOCUMENTATION, result.results)
        doc_url = result.results[constants.CAT_DOCUMENTATION][0]["result"]["value"]
        self.assertEqual(doc_url, "https://gammalearn.pages.in2p3.fr/gammalearn/")
        
        self.assertIn(constants.CAT_ISSUE_TRACKER, result.results)
        issue_url = result.results[constants.CAT_ISSUE_TRACKER][0]["result"]["value"]
        self.assertEqual(issue_url, "https://gitlab.in2p3.fr/gammalearn/gammalearn/-/issues")
        
        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        self.assertEqual(len(dependencies), 23)

if __name__ == "__main__":
    unittest.main()