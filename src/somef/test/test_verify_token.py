import sys
import unittest
from unittest.mock import patch, MagicMock

from .. import somef_cli
from ..process_results import Result


class TestTokenVerification(unittest.TestCase):

    @patch("somef.somef_cli.process_repository.is_gitlab", return_value=True)
    def test_github_token_on_gitlab_repo(self, mock_is_gitlab):
        """--github-token on a GitLab repo returns None (mismatch warning)"""
        result = somef_cli.verify_and_resolve_token(
            "https://gitlab.com/group/project",
            github_token="some-token", gitlab_token=None,
            codeberg_token=None, bitbucket_token=None, bitbucket_email=None
        )
        self.assertIsNone(result)

    @patch("somef.somef_cli.requests.get")
    def test_github_token_invalid_401(self, mock_get):
        """Invalid token (API 401) returns None (falls back to config)"""
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_get.return_value = mock_resp

        result = somef_cli.verify_and_resolve_token(
            "https://github.com/owner/repo",
            github_token="bad-token", gitlab_token=None,
            codeberg_token=None, bitbucket_token=None, bitbucket_email=None
        )
        self.assertIsNone(result)

    @patch("somef.somef_cli.requests.get")
    def test_bitbucket_token_without_email(self, mock_get):
        """Bitbucket token without email exits with error"""
        with self.assertRaises(SystemExit):
            somef_cli.verify_and_resolve_token(
                "https://bitbucket.org/workspace/repo",
                github_token=None, gitlab_token=None,
                codeberg_token=None, bitbucket_token="some-token",
                bitbucket_email=None
            )

    @patch("somef.somef_cli.cli_get_data")
    @patch("somef.somef_cli.verify_and_resolve_token", return_value="token test-abc")
    @patch("somef.somef_cli.validators.url", return_value=True)
    def test_run_cli_forwards_authorization(self, mock_url, mock_verify, mock_get_data):
        """Token resolves into authorization and is forwarded to cli_get_data"""
        mock_get_data.return_value = Result()
        somef_cli.run_cli(
            repo_url="https://github.com/owner/repo",
            github_token="test-abc",
            threshold=0.8, output=None
        )
        kwargs = mock_get_data.call_args.kwargs
        self.assertEqual(kwargs["authorization"], "token test-abc")


if __name__ == "__main__":
    unittest.main()