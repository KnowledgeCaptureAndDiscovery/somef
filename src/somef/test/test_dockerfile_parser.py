import json
import os
import unittest
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep

class TestDockerfileParser(unittest.TestCase): 

    def test_issue_725(self):
        """Checks if this repository has properties extracted from Dockerfile Fairwinds"""

        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url=None,
                            local_repo=test_data_repositories + "Fairwinds",
                            doc_src=None,
                            in_file=None,
                            output=test_data_path + "test_issue_725.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=False,
                            readme_only=False)
        
        text_file = open(test_data_path + "test_issue_725.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)

        owners = json_content.get("owner", [])

        code_parser_owners = [
            entry["result"]["value"]
            for entry in owners
            if entry.get("technique") == "code_parser"
        ]

        assert "FairwindsOps, Inc." in code_parser_owners, (
            "Expected owner 'FairwindsOps, Inc.' extracted from Dockerfile "
            f"with technique 'code_parser'. Found: {code_parser_owners}"
        )

        descriptions = json_content.get("description", [])
        docker_descriptions = [
            entry["result"]["value"]
            for entry in descriptions
            if entry.get("technique") == "code_parser"
        ]

        expected_description = (
            "Nova is a cli tool to find outdated or deprecated Helm charts "
            "running in your Kubernetes cluster."
        )

        assert expected_description in docker_descriptions, (
            "Expected description extracted from Dockerfile not found.\n"
            f"Expected: {expected_description}\n"
            f"Found: {docker_descriptions}"
        )

        documentation = json_content.get("documentation", [])

        doc_urls = [
            entry["result"]["value"]
            for entry in documentation
            if entry.get("technique") == "code_parser"
        ]

        expected_doc = "https://nova.docs.fairwinds.com/"

        assert expected_doc in doc_urls, (
            f"Expected documentation URL '{expected_doc}' not found. "
            f"Found: {doc_urls}"
        )

        authors = json_content.get("authors", [])

        author_values = [
            entry["result"]["value"]
            for entry in authors
            if entry.get("technique") == "code_parser"
        ]

        expected_author = "FairwindsOps, Inc."

        assert expected_author in author_values, (
            f"Expected author '{expected_author}' not found. "
            f"Authors found: {author_values}"
        )
        os.remove(test_data_path + "test_issue_725.json")

    def test_issue_725_2(self):
        """Checks if this repository has properties extracted from Dockerfile Prometeus"""

        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url=None,
                            local_repo=test_data_repositories + "Prometeus",
                            doc_src=None,
                            in_file=None,
                            output=test_data_path + "test_issue_725_2.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=False,
                            readme_only=False)
        
        text_file = open(test_data_path + "test_issue_725_2.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)

        code_repos = json_content.get("code_repository", [])
        code_parser_repos = [
            entry["result"]["value"]
            for entry in code_repos
            if entry.get("technique") == "code_parser"
        ]

        expected_repo = "https://github.com/prometheus/prometheus"

        assert expected_repo in code_parser_repos, (
            f"Expected code_repository '{expected_repo}' extracted with technique "
            f"'code_parser'. Found: {code_parser_repos}"
        )

        licenses = json_content.get("license", [])
        code_parser_licenses = [
            entry["result"]
            for entry in licenses
            if entry.get("technique") == "code_parser"
        ]

        assert any(
            lic.get("spdx_id") == "Apache-2.0"
            for lic in code_parser_licenses
        ), (
            "Expected license with SPDX ID 'Apache-2.0' extracted from Dockerfile "
            f"using 'code_parser'. Found: {code_parser_licenses}"
        )

        descriptions = json_content.get("description", [])
        code_parser_descriptions = [
            entry["result"]["value"]
            for entry in descriptions
            if entry.get("technique") == "code_parser"
        ]

        expected_description = "The Prometheus monitoring system and time series database"
        assert expected_description in code_parser_descriptions, (
            "Expected description extracted from Dockerfile not found.\n"
            f"Expected: {expected_description}\n"
            f"Found: {code_parser_descriptions}"
        )

        names = json_content.get("name", [])
        code_parser_names = [
            entry["result"]["value"]
            for entry in names
            if entry.get("technique") == "code_parser"
        ]

        expected_name = "Prometheus"
        assert expected_name in code_parser_names, (
            f"Expected name '{expected_name}' extracted from Dockerfile "
            f"using 'code_parser'. Found: {code_parser_names}"
        )

        documentation = json_content.get("documentation", [])
        code_parser_docs = [
            entry["result"]["value"]
            for entry in documentation
            if entry.get("technique") == "code_parser"
        ]

        expected_doc = "https://prometheus.io/docs"
        assert expected_doc in code_parser_docs, (
            f"Expected documentation URL '{expected_doc}' extracted from Dockerfile "
            f"using 'code_parser'. Found: {code_parser_docs}"
        )
        os.remove(test_data_path + "test_issue_725_2.json")

if __name__ == '__main__':
    unittest.main()
