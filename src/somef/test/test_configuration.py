import unittest
from ..configuration import get_configuration_file
from somef.utils import constants


class TestConfiguration(unittest.TestCase):
    def test_default_uri(self):
        try:
            key = get_configuration_file()[constants.CONF_DEFAULT_BASE_URI]
        except KeyError:
            # SOMEF is not configured, the default is OK.
            key = "https://w3id.org/okn/i/"
        self.assertEqual(key, "https://w3id.org/okn/i/")


if __name__ == '__main__':
    unittest.main()
