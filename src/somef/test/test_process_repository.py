import os
import tempfile
import unittest
from pathlib import Path

from .. import process_repository, process_files, somef_cli
from ..utils import constants

test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestProcessRepository(unittest.TestCase):

    def test_issue_171(self):
        """Test designed to check if contributors are detected"""
        text, github_data = process_files.process_repository_files(test_data_repositories + "rdflib-6.0.2", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(github_data['contributors']) > 0

    def test_issue_209(self):
        """Test designed to check if sh scripts are detected"""
        text, github_data = process_files.process_repository_files(test_data_repositories + "rdflib-6.0.2", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(github_data['hasScriptFile']) > 0

    def test_issue_211(self):
        """Test designed to check if contributor guidelines are detected"""
        text, github_data = process_files.process_repository_files(test_data_repositories + "probot-12.1.1", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(github_data['contributingGuidelines']) > 0 and (
                'license' in github_data.keys() or 'licenseText' in github_data.keys())

    def test_issue_218(self):
        """Test designed to check if citation files (.cff) are detected"""
        text, github_data = process_files.process_repository_files(test_data_repositories + "captum", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(github_data['citation']) > 0

    def test_issue_285(self):
        """Test designed to test repositories with no license (somef should not break)"""

        text, github_data = process_files.process_repository_files(test_data_repositories +
                                                                   "repos-oeg/cogito-kgg-module", {},
                                                                   constants.RepositoryType.LOCAL)
        assert 'license' not in github_data

    def test_issue_361(self):
        """Test designed to check if multiple readme combinations are detected"""
        text, github_data = process_files.process_repository_files(test_data_repositories +
                                                                   "rdflib-6.0.2", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(text) > 0

    def test_issue_389(self):
        """Test designed to check if Dockerfiles are detected"""
        text, github_data = process_files.process_repository_files(test_data_repositories +
                                                                   "wot-hive", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(github_data['hasBuildFile']) > 0

    def test_issue_no_readme(self):
        """Test designed to check if repositories with no readme are detected"""
        github_data, owner, repo, def_br = process_repository.load_online_repository_metadata(
            "https://github.com/oeg-upm/OpenRefineExtension_Transformation")
        assert 'codeRepository' in github_data

    def test_issue_268(self):
        """Test designed to check if license is properly captured"""
        text, github_data = process_files.process_repository_files(test_data_repositories +
                                                                   "probot-12.1.1", {},
                                                                   constants.RepositoryType.LOCAL)
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
        gitlab_data, owner, name, def_br = process_repository.load_gitlab_repository_metadata(
            "https://gitlab.com/gitlab-org/ci-sample-projects/platform-team")
        assert len(gitlab_data['downloadUrl']) > 0

    def test_issue_285(self):
        """Test designed to check if the tool is robust against repositories with empty license """
        readme_text, github_data = process_files.process_repository_files(test_data_repositories + "RDFChess",
                                                                                  {},
                                                                                  constants.RepositoryType.LOCAL)
        assert 'license' not in github_data

    def test_no_repository_metadata(self):
        """Test designed to assess repositories with no releases"""
        github_data = process_repository.load_online_repository_metadata(
            "https://github.com/RDFLib/rdflib/tree/6.0.2")
        assert 'releases' not in github_data

    def test_issue_284_issue_272(self):
        """Test designed to check if there are errors detecting title or stargazers"""
        github_data, owner, repo_name, default_br = process_repository.\
            load_online_repository_metadata("https://github.com/3b1b/manim")
        assert (('stargazersCount' in github_data) and ('longTitle' not in github_data))

    def test_feature_462(self):
        """Test designed to process a repo and keep the results in disk"""
        with tempfile.TemporaryDirectory() as tmp_folder:
            somef_cli.cli_get_data(0.8, ignore_classifiers=False,
                                   repo_url="https://github.com/KnowledgeCaptureAndDiscovery/OBA_sparql/",
                                   keep_tmp=tmp_folder)
            assert os.path.isfile(tmp_folder+"/KnowledgeCaptureAndDiscovery_OBA_sparql.zip")

    def test_feature_477(self):
        """
        Test designed to assess if readme.rst files are processed properly
        """
        text, github_data = process_files.process_repository_files(test_data_repositories + "mir_eval", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(text) > 0

    def test_feature_477_2(self):
        """
        Test designed to assess if readme.txt files are processed properly
        """
        text, github_data = process_files.process_repository_files(test_data_repositories + "resolver_deco", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(text) > 0

    def test_feature_466(self):
        """
        Test designed to assess if a readme with non utf-8 encoding can be processed successfully
        """
        text, github_data = process_files.process_repository_files(test_data_repositories + "corpuser", {},
                                                                   constants.RepositoryType.LOCAL)
        assert len(text) > 0