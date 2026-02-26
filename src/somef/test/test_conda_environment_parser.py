import json
import os
import unittest
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep
test_data_api_json = str(Path(__file__).parent / "test_data" / "api_responses") + os.path.sep

class TestCondaEnvironmentParser(unittest.TestCase): 

    def test_issue_489(self):

        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url=None,
                            local_repo=test_data_repositories + "stable-diffusion",
                            doc_src=None,
                            in_file=None,
                            output=test_data_path + "test_issue_489.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=False,
                            readme_only=False)
        
        text_file = open(test_data_path + "test_issue_489.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)

        requeriments= json_content.get("requirements", [])

        assert len(requeriments) == 26, f"Expected 26 requeriments, found {len(requeriments)}"
        python_reqs = [
            r for r in requeriments
            if r["result"].get("name") == "python"
        ]

        assert python_reqs, "Expected python dependency not found"
        assert python_reqs[0]["result"]["dependency_type"] == "conda"
        assert python_reqs[0]["result"]["version"] == "3.8.5"

        albumentations_reqs = [
            r for r in requeriments
            if r["result"].get("name") == "albumentations"
        ]
        assert albumentations_reqs, "Expected albumentations dependency not found"
        assert albumentations_reqs[0]["result"]["dependency_type"] == "pip"
        assert albumentations_reqs[0]["result"]["version"] == "0.4.3"

        os.remove(test_data_path + "test_issue_489.json")

   