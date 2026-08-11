import unittest
from unittest.mock import MagicMock, patch
from .. import configuration
from ..utils import constants


class TestConfiguration(unittest.TestCase):
    def test_default_uri(self):
        try:
            key = configuration.get_configuration_file()[constants.CONF_DEFAULT_BASE_URI]
        except KeyError:
            # SOMEF is not configured, the default is OK.
            key = "https://w3id.org/okn/i/"
        self.assertEqual(key, "https://w3id.org/okn/i/")

    @patch("somef.configuration.requests.get")
    @patch("somef.configuration.get_configuration_file")
    def test_configuration_tokens_valid(self, mock_get_config, mock_requests_get):
        """Checks that a valid GitHub token is verified against the GitHub API with the stored header."""

        mock_get_config.return_value = {
            constants.CONF_GITHUB_AUTHORIZATION: "token fake-token",
        }
        response = MagicMock()
        response.status_code = 200
        mock_requests_get.return_value = response

        results = configuration.test_configuration_tokens()

        mock_requests_get.assert_called_once_with(
            "https://api.github.com/user",
            headers={constants.PROP_AUTHORIZATION: "token fake-token"},
            timeout=10,
        )
        
        self.assertEqual(results["GitHub"]["ok"], True)
        self.assertEqual(results["GitHub"]["message"], "token valid")

if __name__ == '__main__':
    unittest.main()
