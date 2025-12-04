import unittest
import os
from pathlib import Path
# from ..parser.python_parser import parse_pyproject_toml
from ..parser.python_parser import parse_requirements_txt
from..parser.python_parser import parse_setup_py
from ..process_results import Result
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestPythonParser(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()