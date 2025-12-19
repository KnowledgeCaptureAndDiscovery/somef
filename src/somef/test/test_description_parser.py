import unittest
import os
from pathlib import Path

from somef.parser.description_parser import parse_description_file
from somef.process_results import Result
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestDescriptionParser(unittest.TestCase):

    def test_description(self):
        description_file_path = test_data_repositories + os.path.sep + "tidyverse" + os.path.sep + "DESCRIPTION"
        result = Result()
    
        # metadata_result = parse_description_file(description_file_path, result, "https://example.org/DESCRIPTION")
            
        metadata_result = parse_description_file(description_file_path, result, description_file_path)
    
        # print(metadata_result.results)
 
        # print(metadata_result.results.get(constants.CAT_PACKAGE_ID, []))

        authors_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(authors_results) == 3, "Expected three authors")
        self.assertEqual(authors_results[0]["result"]["value"],"Hadley Wickham", "First author name mismatch")
        self.assertEqual(authors_results[1]["result"]["value"],"Winston Chang","Second author name mismatch")

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        # self.assertEqual(package_results[0]["result"]["value"], "DESCRIPTION")
        # self.assertEqual(package_results[0]["result"]["value"], "https://example.org/DESCRIPTION")
        self.assertEqual(package_results[0]["result"]["value"], description_file_path)
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)
        
        id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(id_results) > 0, "No identifier found")
        self.assertEqual(id_results[0]["result"]["value"], "tidyverse")
        self.assertEqual(id_results[0]["result"]["type"], constants.STRING)
        
        description_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(description_results) > 0, "No description found")
        self.assertEqual(description_results[0]["result"]["value"], "The 'tidyverse' is a set of packages that work in harmony\n    because they share common data representations and 'API' design. This\n    package is designed to make it easy to install and load multiple\n    'tidyverse' packages in a single step. Learn more about the\n    'tidyverse' at <https://www.tidyverse.org>.")
        self.assertEqual(description_results[0]["result"]["type"], constants.STRING)
        
        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "MIT + file LICENSE")
        self.assertEqual(license_results[0]["result"]["type"], constants.STRING)


    def test_description_2(self):
        description_file_path = test_data_repositories + os.path.sep + "ggplot2" + os.path.sep + "DESCRIPTION"
        
        result = Result()
    
        # metadata_result = parse_description_file(description_file_path, result, "https://example.org/DESCRIPTION")
        metadata_result = parse_description_file(description_file_path, result, description_file_path)
        authors_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(authors_results) == 11, "Expected 11 authors")
        self.assertEqual(authors_results[1]["result"]["value"],"Winston Chang","Second author name mismatch")

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], description_file_path)
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)

        id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(id_results) > 0, "No identifier found")
        self.assertEqual(id_results[0]["result"]["value"], "ggplot2")
        self.assertEqual(id_results[0]["result"]["type"], constants.STRING)

        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "MIT + file LICENSE")
        self.assertEqual(license_results[0]["result"]["type"], constants.STRING)

        code_repository_results = metadata_result.results.get(constants.CAT_CODE_REPOSITORY, [])
        self.assertTrue(len(code_repository_results) > 0, "No code repository found")
        self.assertEqual(code_repository_results[0]["result"]["value"], "https://github.com/tidyverse/ggplot2")

        issue_tracker_results = metadata_result.results.get(constants.CAT_ISSUE_TRACKER, [])
        self.assertTrue(len(issue_tracker_results) > 0, "No issue tracker found")
        self.assertEqual(issue_tracker_results[0]["result"]["value"], "https://github.com/tidyverse/ggplot2/issues")

        
if __name__ == "__main__":
    unittest.main()