import os
import unittest
import json
import base64
from pathlib import Path
from .. import somef_cli
from ..utils import constants
from .. import process_repository
from ..parser import codeowners_parser
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

class TestCodebergRepository(unittest.TestCase):

    @patch("somef.process_repository.detect_license_spdx")
    @patch("somef.process_repository.requests.get")
    def test_load_codeberg_metadata(self, mock_get, mock_detect_license):
        """Load Codeberg repository metadata via mocked API. From the API response previously saved in local"""

        mock_detect_license.return_value = {
            "name": "MIT License",
            "spdx_id": "MIT",
            "@id": "https://spdx.org/licenses/MIT",
            "url": "https://spdx.org/licenses/MIT",
            "identifier": "https://spdx.org/licenses/MIT"
        }
        # load api response
        repo_json = json.load(open(test_data_path + "api_responses/codeberg/codeberg_forgejo.json"))
        lang_json = json.load(open(test_data_path + "api_responses/codeberg/codeberg_forgejo_languages.json"))
        releases_json = json.load(open(test_data_path + "api_responses/codeberg/codeberg_forgejo_releases.json"))

        license_response = {
            "name": "LICENSE",
            "path": "LICENSE",
            "content": base64.b64encode(b"MIT License").decode(),
            "encoding": "base64"
        }
        
        mock_get.side_effect = [
            _make_mock_response(200, json.dumps(repo_json).encode()),
            _make_mock_response(200, json.dumps(license_response).encode()),
            _make_mock_response(200, json.dumps(lang_json).encode()),
            _make_mock_response(200, json.dumps(releases_json).encode())
        ]

        result, owner, repo_name, branch, path = process_repository.load_codeberg_repository_metadata(
                Result(), "https://codeberg.org/forgejo/forgejo"
            )

        self.assertIn(constants.CAT_NAME, result.results)
        self.assertEqual(result.results[constants.CAT_NAME][0]["result"]["value"], "forgejo")
        self.assertIn(constants.CAT_STARS, result.results)
        self.assertIn(constants.CAT_DESCRIPTION, result.results)
        self.assertIn(constants.CAT_ISSUE_TRACKER, result.results)
        self.assertEqual(owner, "forgejo")
        self.assertEqual(repo_name, "forgejo")
        # language
        self.assertIn(constants.CAT_PROGRAMMING_LANGUAGES, result.results)
        # releases
        self.assertIn(constants.CAT_RELEASES, result.results)

        self.assertIn(constants.CAT_LICENSE, result.results)
        license_entry = result.results[constants.CAT_LICENSE][0]
        self.assertEqual(license_entry["technique"], constants.TECHNIQUE_CODEBERG_API)
        self.assertEqual(license_entry["result"]["spdx_id"], "MIT")
        self.assertEqual(license_entry["result"]["value"], "MIT")
        self.assertEqual(license_entry["result"]["name"], "MIT License")

    @patch("somef.process_repository.requests.get")
    def test_codeberg_api_error_returns_empty(self, mock_get):
        """HTTP error must return empty tuples, not crash."""
        mock_get.return_value = _make_mock_response(404)
        result, owner, repo_name, branch, path = \
            process_repository.load_codeberg_repository_metadata(
                Result(), "https://codeberg.org/nonexistent/repo"
            )
        self.assertEqual(owner, "")
        self.assertNotIn(constants.CAT_NAME, result.results)

    @unittest.skipIf(os.getenv("CI") == "true", "Skipped in CI because it is already verified locally")
    def test_codeberg_integration_cli(self):
        """End-to-end CLI test against a real Codeberg repository."""
        output_file = test_data_path + "test-codeberg-integration.json"

        somef_cli.run_cli(
            threshold=0.8,
            ignore_classifiers=False,
            repo_url="https://codeberg.org/forgejo/forgejo",
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
            any(e["technique"] == constants.TECHNIQUE_CODEBERG_API and e["result"]["value"] == "forgejo"
                for e in name_entries),
            "Name from Codeberg_API should be 'forgejo'"
        )

        desc_entries = json_content.get(constants.CAT_DESCRIPTION, [])
        self.assertTrue(
            any(e["technique"] == constants.TECHNIQUE_CODEBERG_API and e["result"]["value"] == "Beyond coding. We forge."
                for e in desc_entries),
            "Description from Codeberg_API should match"
        )

        code_repo_entries = json_content.get(constants.CAT_CODE_REPOSITORY, [])
        self.assertTrue(
            any(e["technique"] == constants.TECHNIQUE_CODEBERG_API and
                e["result"]["value"] == "https://codeberg.org/forgejo/forgejo"
                for e in code_repo_entries)
        )

        homepage_entries = json_content.get(constants.CAT_HOMEPAGE, [])
        self.assertTrue(
            any(e["technique"] == constants.TECHNIQUE_CODEBERG_API and
                e["result"]["value"] == "https://forgejo.org"
                for e in homepage_entries)
        )
        self.assertIn(constants.CAT_STARS, json_content)
        self.assertIn(constants.CAT_FORK_COUNTS, json_content)

        license_entries = json_content.get(constants.CAT_LICENSE, [])
        # print("License entries:", license_entries)
        self.assertTrue(
            any("Codeberg_API" in e["technique"] and
                e["result"].get("spdx_id") == "GPL-3.0"
                for e in license_entries),
            "License from Codeberg_API should have spdx_id GPL-3.0"
        )
        ci_entries = json_content.get(constants.CAT_CONTINUOUS_INTEGRATION, [])
        self.assertTrue(len(ci_entries) >= 10, f"Expected at least 10 CI workflows, got {len(ci_entries)}")
        
        os.remove(output_file)

    @patch("somef.parser.codeowners_parser.requests.get")
    def test_enrich_user_codeberg(self, mock_get):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "full_name": "Forgejo",
            "email": "forgejo@noreply.codeberg.org",
        }
        mock_get.return_value = response

        result = codeowners_parser.enrich_user(
            "forgejo",
            constants.RepositoryType.CODEBERG,
        )

        mock_get.assert_called_once_with(
            "https://codeberg.org/api/v1/users/forgejo",
            timeout=5,
        )
        self.assertEqual(result[constants.PROP_CODEOWNERS_NAME], "Forgejo")
        self.assertEqual(result[constants.PROP_CODEOWNERS_EMAIL], "forgejo@noreply.codeberg.org")