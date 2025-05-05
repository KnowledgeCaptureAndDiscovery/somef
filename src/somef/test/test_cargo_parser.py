import unittest
import os
import sys
from pathlib import Path
from somef.process_results import Result
from somef.parser.cargo_parser import parse_cargo_toml
from somef.utils import constants

class TestCargoParser(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.cargo_toml_path = os.path.join(self.test_dir, "test_data", "repositories", "rustdesk", "Cargo.toml")
        
        self.assertTrue(os.path.exists(self.cargo_toml_path), f"Test file not found: {self.cargo_toml_path}")

    def test_parse_cargo_toml(self):
        result = Result()
        parse_cargo_toml(self.cargo_toml_path, result, "test")
        
        self.assertIn(constants.CAT_PACKAGE_ID, result.results)
        package_id = result.results[constants.CAT_PACKAGE_ID][0]["result"]["value"]
        self.assertEqual(package_id, "rustdesk")
        
        self.assertIn(constants.CAT_VERSION, result.results)
        version = result.results[constants.CAT_VERSION][0]["result"]["value"]
        self.assertEqual(version, "1.4.0")
        
        self.assertIn(constants.CAT_DESCRIPTION, result.results)
        description = result.results[constants.CAT_DESCRIPTION][0]["result"]["value"]
        self.assertEqual(description, "RustDesk Remote Desktop")
        
        self.assertIn(constants.CAT_AUTHORS, result.results)
        authors = result.results[constants.CAT_AUTHORS]
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0]["result"]["name"], "rustdesk")
        self.assertEqual(authors[0]["result"]["email"], "info@rustdesk.com")
        
        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        
        dep_names = [d["result"]["name"] for d in dependencies]
        self.assertIn("async-trait", dep_names)
        self.assertIn("serde", dep_names)
        self.assertIn("lazy_static", dep_names)


if __name__ == "__main__":
    unittest.main()