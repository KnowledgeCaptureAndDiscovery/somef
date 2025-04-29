import unittest
import os
from pathlib import Path
from ..parser.python_parser import parse_pyproject_toml
from ..parser.python_parser import parse_requirements_txt
from..parser.python_parser import parse_setup_py
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
        self.assertEqual(len(dependencies), 25)

    def test_inspect4py_repository(self):
        """Test parsing of inspect4py repository files"""
  
        inspect4py_dir = test_data_repositories + os.path.sep + "inspect4py"
        requirements_path = os.path.join(inspect4py_dir, "requirements.txt")
        pyproject_path = os.path.join(inspect4py_dir, "pyproject.toml")
        setup_path = os.path.join(inspect4py_dir, "setup.py")
        
        ############### This is for testing requirements.txt parsing #######################
        result = Result()
        metadata_result = parse_requirements_txt(requirements_path, result, "https://example.org/requirements.txt")
        
        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        self.assertEqual(len(dependencies), 12, "Incorrect number of requirements found in requirements.txt")
        
        # Decided to randomly check if some specific dependencies are found in the requirements.txt file
        req_names = [req["result"]["name"] for req in dependencies]
        self.assertIn("docstring_parser", req_names)
        self.assertIn("astor", req_names)
        
        ####################### This is for testing pyroject.toml parsing #######################
        result = Result()
        metadata_result = parse_pyproject_toml(pyproject_path, result, "https://example.org/pyproject.toml")
        
        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        self.assertEqual(len(dependencies), 11, "Incorrect number of requirements found in pyproject.toml")
        
        req_names = [req["result"]["name"] for req in dependencies]
        self.assertIn("bs4", req_names)
        self.assertIn("docstring_parser", req_names)
        
        ####################### This is for testing setup.py parsing #######################
        result = Result()
        metadata_result = parse_setup_py(setup_path, result, "https://example.org/setup.py")

        self.assertIn(constants.CAT_DESCRIPTION, result.results)
        description = result.results[constants.CAT_DESCRIPTION][0]["result"]["value"]
        self.assertEqual(description, "Static code analysis package for Python repositories")
        
        self.assertIn(constants.CAT_LICENSE, result.results)
        license_info = result.results[constants.CAT_LICENSE][0]["result"]["value"]
        self.assertEqual(license_info, "BSD-3-Clause")

        self.assertIn(constants.CAT_PROGRAMMING_LANGUAGES, result.results)
        programming_languages = result.results[constants.CAT_PROGRAMMING_LANGUAGES]
        self.assertEqual(programming_languages[0]["result"]["value"], "Python")


    def test_parse_pyproject_toml_requirements_version(self):
        """Test parsing requirements with version and name. If version, must have name"""
        pyproject_path = test_data_repositories + os.path.sep+ "sunpy"+ os.path.sep+ "pyproject.toml"
        result = Result()

        metadata_result = parse_pyproject_toml(pyproject_path, result, "https://example.org/pyproject.toml")
        
        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]

        for item in dependencies:
            result = item.get("result", {})
            version = result.get("version", None)  
            name = result.get("name", None)  

            self.assertTrue(version is None or name is not None, f"Error in requirement: {item}")

    
    def test_issue_769(self):
        """Test parsing requirements with brakes"""
        pyproject_path = test_data_repositories + os.path.sep+ "sunpy"+ os.path.sep+ "pyproject.toml"
        result = Result()

        metadata_result = parse_pyproject_toml(pyproject_path, result, "https://example.org/pyproject.toml")
        
        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]

        self.assertTrue(
                any(item.get("result", {}).get("name") == "setuptools_scm[toml]" 
                    and item.get("result", {}).get("version") == ">=8.0.1" 
                    for item in dependencies),
                    "Expected dependency 'setuptools_scm[toml]' with version '>=8.0.1' not found."
)

if __name__ == "__main__":
    unittest.main()