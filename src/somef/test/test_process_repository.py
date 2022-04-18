import unittest

import os
import sys
import json

from .. import process_repository
from pathlib import Path

test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestProcessRepository(unittest.TestCase):

    def test_issue_171(self):
        """Test designed to check if contributors are detected"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "rdflib-6.0.2")
        assert len(github_data['contributors']) > 0

    def test_issue_209(self):
        """Test designed to check if sh scripts are detected"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "rdflib-6.0.2")
        assert len(github_data['hasScriptFile']) > 0

    def test_issue_211(self):
        """Test designed to check if contributor guidelines are detected"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "probot-12.1.1")
        assert len(github_data['contributingGuidelines']) > 0 and (
                'license' in github_data.keys() or 'licenseText' in github_data.keys())

    def test_issue_218(self):
        """Test designed to check if citation files (.cff) are detected"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "captum")
        assert len(github_data['citation']) > 0

    def test_issue_285(self):
        """Test designed to test repositories with no license (somef should not break)"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories +
                                                                              "repos-oeg/cogito-kgg-module")
        assert 'license' not in github_data

    def test_issue_361(self):
        """Test designed to check if multiple readme combinations are detected"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "rdflib-6.0.2")
        assert len(text) > 0

    def test_issue_389(self):
        """Test designed to check if Dockerfiles are detected"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "wot-hive")
        print(github_data)
        assert len(github_data['hasBuildFile']) > 0

    def test_issue_no_readme(self):
        """Test designed to check if repositories with no readme are detected"""
        credentials_file = Path(
            os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
        ).expanduser()
        if credentials_file.exists():
            with credentials_file.open("r") as fh:
                file_paths = json.load(fh)
        else:
            sys.exit("Error: Please provide a config.json file.")
        header = {}
        if 'Authorization' in file_paths.keys():
            header['Authorization'] = file_paths['Authorization']
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = process_repository.load_github_repository_metadata(
            "https://github.com/oeg-upm/OpenRefineExtension_Transformation", header)
        assert 'codeRepository' in github_data

    def test_issue_268(self):
        """Test designed to check if license is properly captured"""
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "probot-12.1.1")
        assert len(github_data['licenseText']) > 0

    # Commenting this issue: this repo does no longer have an ACK file
    # def test_issue_210(self):
    #     from somef import cli
    #     cli.run_cli(threshold=0.8,
    #                 ignore_classifiers=False,
    #                 repo_url="https://github.com/tensorflow/tensorflow/tree/v2.6.0",
    #                 doc_src=None,
    #                 in_file=None,
    #                 output=None,
    #                 graph_out=None,
    #                 graph_format="turtle",
    #                 codemeta_out="test-tensorflow-2.6.0.json-ld",
    #                 pretty=True,
    #                 missing=False)
    #     text_file = open("test-tensorflow-2.6.0.json-ld", "r")
    #     data = text_file.read()
    #     text_file.close()
    #     assert data.find("\"acknowledgments\":") >= 0

    def test_issue_286(self):
        """Test designed to check if gitlab repositories are properly parsed"""
        credentials_file = Path(
            os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
        ).expanduser()
        if credentials_file.exists():
            with credentials_file.open("r") as fh:
                file_paths = json.load(fh)
        else:
            sys.exit("Error: Please provide a config.json file.")
        header = {}
        if 'Authorization' in file_paths.keys():
            header['Authorization'] = file_paths['Authorization']
        header['accept'] = 'application/vnd.github.v3+json'
        text, gitlab_data = process_repository.load_gitlab_repository_metadata(
            "https://gitlab.com/gitlab-org/ci-sample-projects/platform-team",
            header)
        assert len(gitlab_data['downloadUrl']) > 0

    def test_issue_285(self):
        """Test designed to check if the tool is robust against repositories with empty license """
        text, github_data = process_repository.load_local_repository_metadata(test_data_repositories + "RDFChess")
        assert 'license' not in github_data

    def test_no_repository_metadata(self):
        """Test designed to assess repositories with no releases"""
        credentials_file = Path(
            os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
        ).expanduser()
        if credentials_file.exists():
            with credentials_file.open("r") as fh:
                file_paths = json.load(fh)
        else:
            sys.exit("Error: Please provide a config.json file.")
        header = {}
        if 'Authorization' in file_paths.keys():
            header['Authorization'] = file_paths['Authorization']
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = process_repository.load_github_repository_metadata(
            "https://github.com/RDFLib/rdflib/tree/6.0.2",
            header, True)
        assert 'releases' not in github_data

    def test_issue_284_issue_272(self):
        """Test designed to check if there are errors detecting title or stargazers"""
        credentials_file = Path(
            os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
        ).expanduser()
        if credentials_file.exists():
            with credentials_file.open("r") as fh:
                file_paths = json.load(fh)
        else:
            sys.exit("Error: Please provide a config.json file.")
        header = {}
        if 'Authorization' in file_paths.keys():
            header['Authorization'] = file_paths['Authorization']
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = process_repository.load_github_repository_metadata("https://github.com/3b1b/manim", header)
        assert (('stargazersCount' in github_data) and ('longTitle' not in github_data))
