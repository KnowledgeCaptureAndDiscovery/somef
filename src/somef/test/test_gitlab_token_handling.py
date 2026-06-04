import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from .. import somef_cli
from ..parser import codeowners_parser
from ..process_results import Result
from ..utils import constants


class TestGitlabTokenHandling(unittest.TestCase):
    @patch("somef.parser.codeowners_parser.requests.get")
    def test_enrich_user_gitlab_adds_bearer_prefix(self, mock_get):
        # Simulate a successful GitLab user lookup response.
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = [
            {
                "name": "Alice",
                "organization": "Example Org",
                "public_email": "alice@example.org",
            }
        ]
        mock_get.return_value = response

        # Pass a raw token and verify the request header is normalized to Bearer.
        result = codeowners_parser.enrich_user(
            "alice",
            constants.RepositoryType.GITLAB,
            server_url="gitlab.example.org",
            gitlab_authorization="my-token",
        )

        # Ensure request URL, auth header, and timeout are built correctly.
        mock_get.assert_called_once_with(
            "https://gitlab.example.org/api/v4/users?username=alice",
            headers={"Authorization": "Bearer my-token"},
            timeout=5,
        )
        # Ensure selected fields from the GitLab payload are mapped into SOMEF output.
        self.assertEqual(result[constants.PROP_CODEOWNERS_NAME], "Alice")
        self.assertEqual(result[constants.PROP_CODEOWNERS_COMPANY], "Example Org")
        self.assertEqual(result[constants.PROP_CODEOWNERS_EMAIL], "alice@example.org")

    @patch("somef.parser.codeowners_parser.requests.get")
    def test_enrich_user_gitlab_preserves_existing_bearer_prefix(self, mock_get):
        # Simulate a valid response; this test focuses on header formatting only.
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = [{"name": "Bob"}]
        mock_get.return_value = response

        # Pass an already-prefixed token and verify no duplicate prefix is introduced.
        codeowners_parser.enrich_user(
            "bob",
            constants.RepositoryType.GITLAB,
            server_url="https://gitlab.example.org",
            gitlab_authorization="Bearer already-prefixed",
        )

        mock_get.assert_called_once_with(
            "https://gitlab.example.org/api/v4/users?username=bob",
            headers={"Authorization": "Bearer already-prefixed"},
            timeout=5,
        )

    @patch("somef.somef_cli.json_export.unify_results", return_value={})
    @patch("somef.somef_cli.cli_get_data")
    @patch("somef.somef_cli.validators.url", return_value=True)
    def test_run_cli_forwards_gitlab_token_single_repo(self, _mock_valid_url, mock_cli_get_data, _mock_unify):
        # Avoid network/repository processing and only assert argument forwarding.
        mock_cli_get_data.return_value = Result()

        # Run single-repository mode with a GitLab token.
        somef_cli.run_cli(
            repo_url="https://gitlab.com/group/project",
            output=None,
            codemeta_out=None,
            google_codemeta_out=None,
            gitlab_token="token-123",
        )

        # Ensure CLI propagates the token into the lower-level authorization argument.
        self.assertEqual(mock_cli_get_data.call_count, 1)
        kwargs = mock_cli_get_data.call_args.kwargs
        self.assertEqual(kwargs["gitlab_authorization"], "token-123")

    @patch("somef.somef_cli.json_export.unify_results", return_value={})
    @patch("somef.somef_cli.cli_get_data")
    @patch("somef.somef_cli.validators.url", return_value=True)
    def test_run_cli_forwards_gitlab_token_in_file_mode(self, _mock_valid_url, mock_cli_get_data, _mock_unify):
        # Avoid network/repository processing and only assert argument forwarding.
        mock_cli_get_data.return_value = Result()

        # Build a temporary input file to trigger batch mode.
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "repos.txt"
            input_file.write_text("https://gitlab.com/group/project\n", encoding="utf-8")

            # Run file mode with a GitLab token.
            somef_cli.run_cli(
                in_file=str(input_file),
                output=None,
                codemeta_out=None,
                google_codemeta_out=None,
                gitlab_token="token-456",
            )

        # Ensure CLI propagates the token in batch mode as well.
        self.assertEqual(mock_cli_get_data.call_count, 1)
        kwargs = mock_cli_get_data.call_args.kwargs
        self.assertEqual(kwargs["gitlab_authorization"], "token-456")


if __name__ == "__main__":
    unittest.main()