import unittest
import os
from pathlib import Path

from somef.parser.gemspec_parser import parse_gemspec_file
from somef.process_results import Result
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestGemSpecParser(unittest.TestCase):

    def test_parse_gemspec(self):
        gemspec_file_path = test_data_repositories + os.path.sep + "bootstrap-datepicker-rails" + os.path.sep + "bootstrap-datepicker-rails.gemspec"
        result = Result()
    
        metadata_result = parse_gemspec_file(gemspec_file_path, result, "https://example.org/bootstrap-datepicker-rails.gemspec")

        authors_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(authors_results) == 2, "Expected two authors")

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], "bootstrap-datepicker-rails.gemspec")
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)
        
        id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(id_results) > 0, "No identifier found")
        self.assertEqual(id_results[0]["result"]["value"], "bootstrap-datepicker-rails")
        self.assertEqual(id_results[0]["result"]["type"], constants.STRING)
        
        description_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(description_results) > 0, "No description found")
        self.assertEqual(description_results[0]["result"]["value"], "A date picker for Twitter Bootstrap")
        self.assertEqual(description_results[0]["result"]["type"], constants.STRING)
        
        homepage_results = metadata_result.results.get(constants.CAT_HOMEPAGE, [])
        self.assertTrue(len(homepage_results) > 0, "No homepage found")
        self.assertEqual(homepage_results[0]["result"]["value"], "https://github.com/Nerian/bootstrap-datepicker-rails")
        self.assertEqual(homepage_results[0]["result"]["type"], constants.URL)
        
        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "MIT")
        self.assertEqual(license_results[0]["result"]["type"], constants.LICENSE)
        
        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")

        found_jquery = False
        found_bootstrap = False
        for req_result in requirements_results:
            dependency = req_result["result"]
            if dependency.get("name") == "railties" and dependency.get("dependency_type") == "runtime":
                found_jquery = True

        self.assertTrue(found_jquery, "Dependency not found")

    def test_parse_gemspec_another_authors(self):
        gemspec_file_path = test_data_repositories + os.path.sep + "bootstrap-datepicker-rails" + os.path.sep + "bootstrap-datepicker-rails-2.gemspec"
        result = Result()
    
        metadata_result = parse_gemspec_file(gemspec_file_path, result, "https://example.org/bootstrap-datepicker-rails.gemspec")
       
        authors_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(authors_results) == 1, "Expected one authors")
        self.assertEqual(authors_results[0]["result"]["value"], "Gonzalo Rodríguez-Baltanás Díaz")


        # To do Version
        # To do Email
        
if __name__ == "__main__":
    unittest.main()