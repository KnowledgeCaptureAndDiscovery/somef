import unittest
import os
from pathlib import Path
from .. import supervised_classification
from ..process_results import Result
from ..utils import constants

# Test data for tests
test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep


class TestSupervisedClassification(unittest.TestCase):

    def test_run_category_classification(self):
        """Test to check if category classification runs correctly."""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            result = supervised_classification.run_category_classification(text, 0.8, Result())
            # self.assertEqual(len(result.results[constants.CAT_APPLICATION_DOMAIN]), 1)
            cat_result = result.results[constants.CAT_APPLICATION_DOMAIN][0]
            self.assertEqual(cat_result[constants.PROP_RESULT]['value'], "Semantic web")
