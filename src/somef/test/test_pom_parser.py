import unittest
import os
from pathlib import Path

from somef.parser.pom_xml_parser import parse_pom_file
from somef.parser import pom_xml_parser
from somef.process_results import Result
from somef.utils import constants

# Test data for tests
test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestPomParser(unittest.TestCase):

    def test_parse_pom_file(self):
        pom_xml_parser.processed_pom = False
        pom_file_path = test_data_repositories + os.path.sep + "Widoco" + os.path.sep + "pom.xml"
        result = Result()
    
        metadata_result = parse_pom_file(pom_file_path, result, "https://example.org/pom.xml")

        identifier_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(identifier_results) > 0, "No identifier found")
        self.assertEqual(identifier_results[0]["result"]["value"], "es.oeg.widoco")

        name_results = metadata_result.results.get(constants.CAT_NAME, [])
        self.assertEqual(len(name_results), 0, "Name detection should be disabled")

        version_results = metadata_result.results.get(constants.CAT_VERSION, [])
        self.assertTrue(len(version_results) > 0, "No version found")
        self.assertEqual(version_results[0]["result"]["value"], "1.4.26")
        self.assertEqual(version_results[0]["result"]["type"], constants.RELEASE)

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        # self.assertEqual(package_results[0]["result"]["value"], "pom.xml")
        self.assertEqual(package_results[0]["result"]["value"], "https://example.org/pom.xml")
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)

        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")
        
        found_junit = False
        for req_result in requirements_results:
            dependency = req_result["result"]
            if dependency.get("name") == "junit":
                found_junit = True
                self.assertEqual(dependency.get("version"), "4.13.1")
                self.assertEqual(dependency.get("value"), "junit.junit")
                break
        self.assertTrue(found_junit, "JUnit dependency not found")
        
        repo_results = metadata_result.results.get(constants.CAT_PACKAGE_DISTRIBUTION, [])
        self.assertTrue(len(repo_results) > 0, "No repository information found")

        repos = repo_results[1]["result"]
        # found_jitpack = False
        value = repos.get("value", None)
        url   = repos.get("url", None)

        self.assertEqual(value, "jitpack.io", "jitpack.io repository not found")
        self.assertEqual(url,   "https://jitpack.io", "url jitpack.io repository not found")
    
        scm_results = [r for r in metadata_result.results.get(constants.CAT_PACKAGE_DISTRIBUTION, []) 
                      if r["result"].get("type") == "url" and isinstance(r["result"]["value"], str)]
       
        # self.assertEqual(len(scm_results), 0, "SCM URL should not exist in this POM")
        self.assertEqual(len(scm_results), 0, "Expected one package distribution from SCM URL")

        issue_results = metadata_result.results.get(constants.CAT_ISSUE_TRACKER, [])
        self.assertEqual(len(issue_results), 0, "Issue tracker should not exist in this POM")

        author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertEqual(len(author_results), 0, "No authors should be found in this POM")

        license_results = metadata_result.results.get(constants.CAT_LICENSE, [])
        self.assertEqual(len(license_results), 0, "No licenses should be found in this POM")

        runtime_results = metadata_result.results.get(constants.CAT_RUNTIME_PLATFORM, [])
        self.assertEqual(runtime_results[0]["result"]["name"], "Java")


    def test_parse_pom_file_2(self):
        pom_xml_parser.processed_pom = False
        pom_file_path = test_data_repositories + os.path.sep + "maven" + os.path.sep + "pom.xml"
        result = Result()

        metadata_result = parse_pom_file(pom_file_path, result, "https://example2.org/pom.xml")
        identifier_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(identifier_results) > 0, "No identifier found")
        self.assertEqual(identifier_results[0]["result"]["value"], ".maven")

        version_results = metadata_result.results.get(constants.CAT_VERSION, [])
        self.assertTrue(len(version_results) > 0, "No version found")
        self.assertEqual(version_results[0]["result"]["value"], "4.1.0-SNAPSHOT")
        self.assertEqual(version_results[0]["result"]["type"], constants.RELEASE)

        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")
        self.assertEqual(requirements_results[2]["result"]["value"], "org.apache.maven.maven-jline")

        author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
  
        self.assertEqual(len(author_results), 0, "No authors should be found in this POM")

        scm_results = [r for r in metadata_result.results.get(constants.CAT_PACKAGE_DISTRIBUTION, []) 
                      if r["result"].get("type") == "url" and isinstance(r["result"]["value"], str)]
        # because url is https://github.com/apache/maven/tree/${project.scm.tag} and is not permited '${project.scm.tag}'
        self.assertEqual(len(scm_results), 0, "Expected one package distribution from SCM URL")

        runtime_results = metadata_result.results.get(constants.CAT_RUNTIME_PLATFORM, [])
        self.assertTrue(len(runtime_results) > 0, "No runtime found")
        self.assertEqual(runtime_results[0]["result"]["name"], "Java")
        self.assertEqual(runtime_results[0]["result"]["version"], "17")

if __name__ == "__main__":
    unittest.main()