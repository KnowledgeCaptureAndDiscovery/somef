import unittest
import os
import sys
import json
from pathlib import Path
from somef.process_results import Result
from somef.parser.composer_parser import parse_composer_json
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestComposerParser(unittest.TestCase):
    def test_parse_composer_json(self):
        composer_path = test_data_repositories + os.path.sep+ "composer"+ os.path.sep+ "composer.json"
        result = Result()

        metadata_result = parse_composer_json(composer_path, result, "https://example.org/composer.json")
        
        self.assertIn(constants.CAT_PACKAGE_ID, metadata_result.results)
        package_id = result.results[constants.CAT_PACKAGE_ID][0]["result"]["value"]
        self.assertEqual(package_id, "composer/composer")
        
        self.assertIn(constants.CAT_DESCRIPTION, metadata_result.results)
        description = result.results[constants.CAT_DESCRIPTION][0]["result"]["value"]
        self.assertEqual(description, "Composer helps you declare, manage and install dependencies of PHP projects. It ensures you have the right stack everywhere.")
        
        self.assertIn(constants.CAT_LICENSE, metadata_result.results)
        license_value = result.results[constants.CAT_LICENSE][0]["result"]["value"]
        self.assertEqual(license_value, "MIT")
        
        self.assertIn(constants.CAT_REQUIREMENTS, metadata_result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        dep_names = [d["result"]["name"] for d in dependencies]
        self.assertIn("php", dep_names)


    def test_parse_composer_json_2(self):
        composer_path = test_data_repositories + os.path.sep+ "codecov"+ os.path.sep+ "composer.json"
        result = Result()

        metadata_result = parse_composer_json(composer_path, result, "https://example.org/composer_2.json")

        self.assertIn(constants.CAT_DESCRIPTION, metadata_result.results)
        description = result.results[constants.CAT_DESCRIPTION][0]["result"]["value"]
        self.assertEqual(description, "Codecov Example PHP")

        self.assertIn(constants.CAT_PACKAGE_ID, metadata_result.results)
        package_id = result.results[constants.CAT_PACKAGE_ID][0]["result"]["value"]
        self.assertEqual(package_id, "codecov/codecov-php")
        
        self.assertIn(constants.CAT_REQUIREMENTS, metadata_result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        self.assertEqual(dependencies[0]["result"]["name"], "php")
        self.assertEqual(dependencies[0]["result"]["dependency_type"], "runtime")
        self.assertEqual(dependencies[1]["result"]["dependency_type"], "dev")

if __name__ == "__main__":
    unittest.main()