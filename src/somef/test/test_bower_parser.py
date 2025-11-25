import unittest
import os
from pathlib import Path

from somef.parser.bower_parser import parse_bower_json_file
from somef.process_results import Result
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestBowerParser(unittest.TestCase):

    def test_parse_bower_json(self):
        bower_file_path = test_data_repositories + os.path.sep + "js-template" + os.path.sep + "bower.json"

        result = Result()
    
        metadata_result = parse_bower_json_file(bower_file_path, result, "https://example.org/bower.json")
        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], "bower.json")
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)
        
        name_results = metadata_result.results.get(constants.CAT_NAME, [])
        self.assertTrue(len(name_results) > 0, "No name found")
        self.assertEqual(name_results[0]["result"]["value"], "alarm")
        self.assertEqual(name_results[0]["result"]["type"], constants.STRING)
        
        description_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(description_results) > 0, "No description found")
        self.assertEqual(description_results[0]["result"]["value"], "Alarm clock project during week1 day2 JS at Epicodus.")
        self.assertEqual(description_results[0]["result"]["type"], constants.STRING)
        
        # there is a homepage with "" in the bower. None, null and "" must not show in metadatos

        # homepage_results = metadata_result.results.get(constants.CAT_HOMEPAGE, [])
        # self.assertTrue(len(homepage_results) > 0, "No homepage found")
        # self.assertEqual(homepage_results[0]["result"]["value"], "")
        # self.assertEqual(homepage_results[0]["result"]["type"], constants.URL)

        homepage_results = metadata_result.results.get(constants.CAT_HOMEPAGE, [])
        self.assertEqual(len(homepage_results), 0, "Expected no homepage for this bower.json")
        
        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "ISC")
        self.assertEqual(license_results[0]["result"]["type"], constants.LICENSE)
        
        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")
        
        authors_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(authors_results) > 0, "No authors found")
        self.assertEqual(len(authors_results), 2, "Expected two authors")

        self.assertEqual(authors_results[0]["result"]["value"], "Andrew Accuardi <andrewaccuardi@gmail.com>")
        self.assertEqual(authors_results[1]["result"]["value"], "Another Author <anotherauthor@gmail.com>")

        found_jquery = False
        found_bootstrap = False
        for req_result in requirements_results:
            dependency = req_result["result"]
            if dependency.get("name") == "jquery" and dependency.get("dependency_type") == "runtime":
                found_jquery = True
        self.assertTrue(found_jquery, "jQuery dependency not found")
        
    def test_parse_2_bower_json(self):
        bower_file_path = test_data_repositories + os.path.sep + "chosen" + os.path.sep + "bower.json"

        result = Result()
    
        metadata_result = parse_bower_json_file(bower_file_path, result, "https://example.org/bower.json")
        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], "bower.json")
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)
        
        name_results = metadata_result.results.get(constants.CAT_NAME, [])
        self.assertTrue(len(name_results) > 0, "No name found")
        self.assertEqual(name_results[0]["result"]["value"], "chosen")
        self.assertEqual(name_results[0]["result"]["type"], constants.STRING)
        
        description_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(description_results) > 0, "No description found")
        self.assertEqual(description_results[0]["result"]["value"], "Chosen is a JavaScript plugin that makes select boxes user-friendly. It is currently available in both jQuery and Prototype flavors.")
        self.assertEqual(description_results[0]["result"]["type"], constants.STRING)
        

        homepage_results = metadata_result.results.get(constants.CAT_HOMEPAGE, [])
        self.assertEqual(homepage_results[0]["result"]["value"], "https://harvesthq.github.io/chosen/")
        
        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "https://github.com/harvesthq/chosen/blob/master/LICENSE.md")
        self.assertEqual(license_results[0]["result"]["type"], constants.LICENSE)
        
        
        authors_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(authors_results) > 0, "No authors found")
        self.assertEqual(len(authors_results), 4, "Expected two authors")

        self.assertEqual(authors_results[0]["result"]["value"], "Patrick Filler")


if __name__ == "__main__":
    unittest.main()