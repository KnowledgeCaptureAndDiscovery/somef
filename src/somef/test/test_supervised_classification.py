import unittest
import os
from pathlib import Path
from .. import supervised_classification

# Test data for tests
test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep


class TestRegExp(unittest.TestCase):

    def test_run_category_classification(self):
        """Test to check if category classification runs correctly."""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            categories = supervised_classification.run_category_classification(text, 0.8)
            self.assertEqual(len(categories), 1)
            self.assertEqual(categories[0]['value'], ["Semantic web"])
