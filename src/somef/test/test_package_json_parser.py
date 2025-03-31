import unittest
import os
from pathlib import Path

from somef.parser.package_json_parser import parse_package_json_file
from somef.process_results import Result
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestPackageJsonParser(unittest.TestCase):

    def test_parse_package_json_file(self):
        package_file_path = test_data_path + "package_neors.json"
        result = Result()
        
        metadata_result = parse_package_json_file(package_file_path, result)
        
        package_id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(package_id_results) > 0, "No package ID found")
        self.assertEqual(package_id_results[0]["result"]["value"], "jsonlab")
        self.assertEqual(package_id_results[0]["result"]["type"], constants.STRING)
        self.assertEqual(package_id_results[0]["technique"], constants.TECHNIQUE_CODE_CONFIG_PARSER)
        
        description_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(description_results) > 0, "No description found")
        self.assertEqual(description_results[0]["result"]["value"], 
                         "An open-source MATLAB/Octave JSON encoder and decoder")
        self.assertEqual(description_results[0]["result"]["type"], constants.STRING)
        
        version_results = metadata_result.results.get(constants.CAT_VERSION, [])
        self.assertTrue(len(version_results) > 0, "No version found")
        self.assertEqual(version_results[0]["result"]["value"], "1.9")
        self.assertEqual(version_results[0]["result"]["type"], constants.RELEASE)
        
        repo_results = metadata_result.results.get(constants.CAT_CODE_REPOSITORY, [])
        self.assertTrue(len(repo_results) > 0, "No repository found")
        self.assertEqual(repo_results[0]["result"]["value"], "git+https://github.com/fangq/jsonlab.git")
        self.assertEqual(repo_results[0]["result"]["type"], constants.URL)
        
        issue_results = metadata_result.results.get(constants.CAT_ISSUE_TRACKER, [])
        self.assertTrue(len(issue_results) > 0, "No issue tracker found")
        self.assertEqual(issue_results[0]["result"]["value"], "https://github.com/fangq/jsonlab/issues")
        self.assertEqual(issue_results[0]["result"]["type"], constants.URL)

        author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(author_results) > 0, "No author found")
        self.assertEqual(author_results[0]["result"]["name"], "Qianqian Fang <q.fang at neu.edu>")
        self.assertEqual(author_results[0]["result"]["type"], "author")
        self.assertEqual(author_results[0]["result"]["value"], "Qianqian Fang <q.fang at neu.edu>")
        
        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "GPL-3.0")
        self.assertEqual(license_results[0]["result"]["type"], constants.LICENSE)
        
        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], "package.json")
        self.assertEqual(package_results[0]["result"]["type"], "npm")

        keywords_results = metadata_result.results.get(constants.CAT_KEYWORDS, [])
        self.assertEqual(len(keywords_results), 0, "Keywords should not be found in this package.json")
        
        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertEqual(len(requirements_results), 0, "No dependencies should be found in this package.json")
        
if __name__ == "__main__":
    unittest.main()