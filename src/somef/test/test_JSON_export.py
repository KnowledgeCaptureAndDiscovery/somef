import json
import os
import unittest
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestJSONExport(unittest.TestCase):
    def test_issue_417(self):
        """Checks whether a repository correctly extracts to Codemeta"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/dgarijo/Widoco",
                          local_repo=None,
                          doc_src=None,
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + "test-417.json-ld",
                          pretty=True,
                          missing=False,
                          readme_only=False)
        text_file = open(test_data_path + "test-417.json-ld", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        issue_tracker = json_content["issueTracker"]  # JSON is in Codemeta format
        assert issue_tracker == 'https://github.com/dgarijo/Widoco/issues' and len(json_content["citation"]) > 0 and \
               len(json_content["name"]) > 0 and len(json_content["identifier"]) > 0 and \
               len(json_content["description"]) > 0 and len(json_content["readme"]) > 0 and \
               len(json_content["author"]) > 0 and len(json_content["buildInstructions"]) > 0 and \
               len(json_content["softwareRequirements"]) > 0 and len(json_content["programmingLanguage"]) > 0 and \
               len(json_content["keywords"]) > 0 and len(json_content["logo"]) > 0 and \
               len(json_content["license"]) > 0 and len(json_content["dateCreated"]) > 0
        os.remove(test_data_path + "test-417.json-ld")

    def test_issue_311(self):
        """Checks if Codemeta export has labels defined outside Codemeta"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "repostatus-README.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + "test-repostatus-311.json-ld",
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "test-repostatus-311.json-ld", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("\"repoStatus\":") < 0
        os.remove(test_data_path + "test-repostatus-311.json-ld")

    def test_issue_150(self):
        """Codemeta export checks"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-mapshaper.md",
                          local_repo=None,
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + "test-150.json-ld",
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "test-150.json-ld", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_ACKNOWLEDGEMENT) == -1
        os.remove(test_data_path + "test-150.json-ld")

    def test_issue_281(self):
        """Checks if missing categories are properly added to the output JSON, when required"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "repostatus-README.md",
                          in_file=None,
                          output=test_data_path + "test-281.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-281.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_MISSING) > 0
        os.remove(test_data_path + "test-281.json")


if __name__ == '__main__':
    unittest.main()
