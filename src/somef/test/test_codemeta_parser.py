import unittest
import os
from pathlib import Path

from somef.parser.codemeta_parser import parse_codemeta_json_file
from somef.process_results import Result
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestCodemetaParser(unittest.TestCase):

    def test_parse_codemeta_file(self):
        codemeta_file_path = test_data_repositories + os.path.sep + "Widoco" + os.path.sep + "codemeta.json"
        result = Result()
        
        metadata_result = parse_codemeta_json_file(codemeta_file_path, result, "https://example.org/codemeta.json")
       
        name_results = metadata_result.results.get(constants.CAT_NAME, [])
        self.assertTrue(len(name_results) > 0, "No name found")
        self.assertEqual(name_results[0]["result"]["value"], "Widoco")
        self.assertEqual(name_results[0]["result"]["type"], constants.STRING)
        
        repo_results = metadata_result.results.get(constants.CAT_CODE_REPOSITORY, [])
        self.assertTrue(len(repo_results) > 0, "No repository found")
        self.assertEqual(repo_results[0]["result"]["value"], "https://github.com/dgarijo/Widoco")
        self.assertEqual(repo_results[0]["result"]["type"], constants.URL)
        
        issue_results = metadata_result.results.get(constants.CAT_ISSUE_TRACKER, [])
        self.assertTrue(len(issue_results) > 0, "No issue tracker found")
        self.assertEqual(issue_results[0]["result"]["value"], "https://github.com/dgarijo/Widoco/issues")
        self.assertEqual(issue_results[0]["result"]["type"], constants.URL)
        
        date_created_results = metadata_result.results.get(constants.CAT_DATE_CREATED, [])
        self.assertTrue(len(date_created_results) > 0, "No date created found")
        self.assertEqual(date_created_results[0]["result"]["value"], "2013-07-15")
        self.assertEqual(date_created_results[0]["result"]["type"], constants.STRING)
        
        date_updated_results = metadata_result.results.get(constants.CAT_DATE_UPDATED, [])
        self.assertTrue(len(date_updated_results) > 0, "No date updated found")
        self.assertEqual(date_updated_results[0]["result"]["value"], "2025-01-31")
        self.assertEqual(date_updated_results[0]["result"]["type"], constants.STRING)
        
        download_url_results = metadata_result.results.get(constants.CAT_DOWNLOAD_URL, [])
        self.assertTrue(len(download_url_results) > 0, "No download URL found")
        self.assertEqual(download_url_results[0]["result"]["value"], "https://github.com/dgarijo/Widoco/releases")
        self.assertEqual(download_url_results[0]["result"]["type"], constants.URL)
        
        keywords_results = metadata_result.results.get(constants.CAT_KEYWORDS, [])
        self.assertTrue(len(keywords_results) > 0, "No keywords found")
        expected_keywords = ["documentation", "metadata", "ontology", "ontology-diagram", 
                            "ontology-evaluation", "wizard"]
        self.assertEqual(keywords_results[0]["result"]["value"], expected_keywords)
        self.assertEqual(keywords_results[0]["result"]["type"], constants.STRING)
        
        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertTrue(len(license_results) > 0, "No license found")
        self.assertEqual(license_results[0]["result"]["value"], "Apache License 2.0")
        self.assertEqual(license_results[0]["result"]["url"], "https://raw.githubusercontent.com/dgarijo/Widoco/master/LICENSE")
        self.assertEqual(license_results[0]["result"]["identifier"], "https://spdx.org/licenses/Apache-2.0")
        
        version_results = metadata_result.results.get(constants.CAT_VERSION, [])
        self.assertTrue(len(version_results) > 0, "No version found")
        self.assertEqual(version_results[0]["result"]["value"], "v1.4.25")
        
        desc_results = metadata_result.results.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(len(desc_results) > 0, "No description found")
        
        id_results = metadata_result.results.get(constants.CAT_IDENTIFIER, [])
        self.assertTrue(len(id_results) > 0, "No identifier found")
        self.assertEqual(id_results[0]["result"]["value"], "https://doi.org/10.5281/zenodo.11093793")
        
        ref_pub_results = metadata_result.results.get(constants.CAT_REF_PUBLICATION, [])
        self.assertTrue(len(ref_pub_results) > 0, "No referenced publications found")
        self.assertEqual(ref_pub_results[0]["result"]["title"], "WIDOCO: a wizard for documenting ontologies")
        self.assertEqual(ref_pub_results[0]["result"]["url"], "http://dgarijo.com/papers/widoco-iswc2017.pdf")
        self.assertEqual(ref_pub_results[0]["result"]["date_published"], "2017")
        self.assertEqual(ref_pub_results[0]["result"]["doi"], "10.1007/978-3-319-68204-4_9")
        
if __name__ == "__main__":
    unittest.main()