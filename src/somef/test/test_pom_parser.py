import unittest
import os
from pathlib import Path

from somef.parser.pom_xml_parser import parse_pom_file
from somef.process_results import Result
from somef.utils import constants

# Test data for tests
test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestPomParser(unittest.TestCase):

    def test_parse_pom_file(self):
        pom_file_path = test_data_path + "pom_widoco.xml"
        result = Result()
    
        metadata_result = parse_pom_file(pom_file_path, result)

        identifier_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(identifier_results) > 0, "No identifier found")
        self.assertEqual(identifier_results[0]["result"]["value"], "es.oeg.widoco")

        name_results = metadata_result.results.get(constants.CAT_NAME, [])
        self.assertEqual(len(name_results), 0, "Name detection should be disabled")

        version_results = metadata_result.results.get(constants.CAT_VERSION, [])
        self.assertTrue(len(version_results) > 0, "No version found")
        self.assertEqual(version_results[0]["result"]["value"], "1.4.26")
        self.assertEqual(version_results[0]["result"]["type"], "release")

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], "pom.xml")
        self.assertEqual(package_results[0]["result"]["type"], "maven")

        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")
        dependencies = requirements_results[0]["result"]["value"]
        self.assertTrue(len(dependencies) > 0, "Empty dependencies list")
        
        found_junit = False
        for dep in dependencies:
            if dep.get("artifactId") == "junit":
                found_junit = True
                self.assertEqual(dep.get("version"), "4.13.1")
                self.assertEqual(dep.get("groupId"), "junit")
                break
        self.assertTrue(found_junit, "JUnit dependency not found")

        repo_results = metadata_result.results.get(constants.CAT_PACKAGE_DISTRIBUTION, [])
        self.assertTrue(len(repo_results) > 0, "No repository information found")
        
        repos = repo_results[0]["result"]["value"]
        found_jitpack = False
        for repo in repos:
            if repo.get("id") == "jitpack.io":
                found_jitpack = True
                self.assertEqual(repo.get("url"), "https://jitpack.io")
                break
        self.assertTrue(found_jitpack, "jitpack.io repository not found")

        scm_results = [r for r in metadata_result.results.get(constants.CAT_PACKAGE_DISTRIBUTION, []) 
                      if r["result"].get("type") == "url" and isinstance(r["result"]["value"], str)]
        self.assertEqual(len(scm_results), 0, "SCM URL should not exist in this POM")

        issue_results = metadata_result.results.get(constants.CAT_SCM, [])
        self.assertEqual(len(issue_results), 0, "Issue tracker should not exist in this POM")

        author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertEqual(len(author_results), 0, "No authors should be found in this POM")

        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertEqual(len(license_results), 0, "No licenses should be found in this POM")

if __name__ == "__main__":
    unittest.main()