import os
import unittest
import json
from pathlib import Path
from .. import somef_cli
from ..utils import constants
from .. import process_repository
from ..process_results import Result
from unittest.mock import patch, MagicMock

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep


def _make_mock_response(status_code, content=b""):
    """Helper: create a minimal mock requests.Response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.content = content
    resp.headers = {}
    try:
        resp.json.return_value = json.loads(content)
    except json.JSONDecodeError:
        pass
    return resp


class TestBitbucketRepository(unittest.TestCase):

    @patch("somef.process_repository.requests.get")
    def test_load_bitbucket_metadata(self, mock_get):
        repo_json = json.load(open(test_data_path + "api_responses/bitbucket/bitbucket_response.json"))
        tags_json = json.load(open(test_data_path + "api_responses/bitbucket/bitbucket_tags.json"))

        mock_get.side_effect = [
            _make_mock_response(200, json.dumps(repo_json).encode()),
            _make_mock_response(200, json.dumps(tags_json).encode())
        ]

        result, owner, repo_name, branch, path = \
            process_repository.load_bitbucket_repository_metadata(
                Result(), "https://bitbucket.org/bitbucketpipelines/pipelines-guide-python"
            )

        self.assertIn(constants.CAT_NAME, result.results)
        self.assertIn(constants.CAT_DESCRIPTION, result.results)
        self.assertIn(constants.CAT_CODE_REPOSITORY, result.results)
        self.assertIn(constants.CAT_FULL_NAME, result.results)
        self.assertIn(constants.CAT_FORKS_URLS, result.results)
        self.assertIn(constants.CAT_PROGRAMMING_LANGUAGES, result.results)
        # this repo has not issues 
        self.assertNotIn(constants.CAT_ISSUE_TRACKER, result.results)
        # this repo has not releases
        self.assertIn(constants.CAT_RELEASES, result.results)
        self.assertEqual(len(result.results[constants.CAT_RELEASES]), 1)
        self.assertEqual(result.results[constants.CAT_RELEASES][0]["result"]["value"], "v1.0")
        self.assertEqual(owner, "bitbucketpipelines")
        self.assertEqual(repo_name, "pipelines-guide-python")
        self.assertEqual(branch, "master")


    @patch("somef.process_repository.requests.get")
    def test_bitbucket_api_error_returns_empty(self, mock_get):
        mock_get.return_value = _make_mock_response(404)
        result, owner, repo_name, branch, path = \
            process_repository.load_bitbucket_repository_metadata(
                Result(), "https://bitbucket.org/nonexistent/repo"
            )
        self.assertEqual(owner, "")
        self.assertNotIn(constants.CAT_NAME, result.results)


    @unittest.skipIf(os.getenv("CI") == "true", "Skipped in CI because it is already verified locally")
    def test_bitbucket_integration_cli(self):
        output_file = test_data_path + "test-bitbucket-integration.json"
        somef_cli.run_cli(
            threshold=0.8,
            ignore_classifiers=False,
            repo_url="https://bitbucket.org/bitbucketpipelines/pipelines-guide-python",
            local_repo=None,
            doc_src=None,
            in_file=None,
            output=output_file,
            graph_out=None,
            graph_format="turtle",
            codemeta_out=None,
            pretty=True,
            missing=True,
            readme_only=False,
            reconcile_authors=False
        )

        with open(output_file, "r") as f:
            json_content = json.load(f)

        name_entries = json_content.get(constants.CAT_NAME, [])
        self.assertTrue(
            any(e["technique"] == constants.TECHNIQUE_BITBUCKET_API and e["result"]["value"] == "pipelines-guide-python"
                for e in name_entries),
            "Name from Bitbucket_API should be 'pipelines-guide-python'"
        )

        code_repo_entries = json_content.get(constants.CAT_CODE_REPOSITORY, [])
        self.assertTrue(
            any(e["technique"] == constants.TECHNIQUE_BITBUCKET_API and e["result"]["value"] == "https://bitbucket.org/bitbucketpipelines/pipelines-guide-python"
                for e in code_repo_entries)
        )

        full_name_entries = json_content.get(constants.CAT_FULL_NAME, [])
        self.assertTrue(
            any(e["technique"] == constants.TECHNIQUE_BITBUCKET_API and e["result"]["value"] == "bitbucketpipelines/pipelines-guide-python"
                for e in full_name_entries)
        )

        pl_entries = json_content.get(constants.CAT_PROGRAMMING_LANGUAGES, [])
        self.assertTrue(
            any(e["technique"] == constants.TECHNIQUE_BITBUCKET_API and e["result"]["value"] == "python"
                for e in pl_entries)
        )


        ft_entries = json_content.get(constants.CAT_FULL_TITLE, [])
        self.assertTrue(
            any(e.get("result", {}).get("value") == "Pipelines Python"
                for e in ft_entries)
        )

        # print(json_content[constants.CAT_FULL_TITLE])
        # print(json_content[constants.CAT_FORKS_URLS])
        self.assertTrue(any(e["technique"] == constants.TECHNIQUE_BITBUCKET_API 
                            for e in json_content.get(constants.CAT_FORKS_URLS, [])))

        self.assertTrue(any(e["technique"] == "file_exploration" 
                            for e in json_content.get(constants.CAT_HAS_BUILD_FILE, [])))

        os.remove(output_file)

