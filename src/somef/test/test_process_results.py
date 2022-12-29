import unittest
from ..utils import constants
from ..process_results import Result


class TestCli(unittest.TestCase):

    def test_add_result(self):
        # This test checks if results are correctly aggregated in their corresponding category
        a = Result()
        a.add_result("description", {"value":"This is a short desc", "type":"string"}, 0.9, constants.TECHNIQUE_SUPERVISED_CLASSIFICATION, "README.md")
        a.add_result("description", {"value":"This is a long description", "type":"string"}, 0.8, constants.TECHNIQUE_REGULAR_EXPRESSION)
        assert len(a.results["description"]) == 2

    def test_add_result_2(self):
        # This test checks if results that are incorrect (i.e., don't have type and value) get added
        a = Result()
        a.add_result("description", {"value":"This is a short desc", "type":"string"}, 0.9, constants.TECHNIQUE_SUPERVISED_CLASSIFICATION, "README.md")
        # incorrect result (no type) below
        a.add_result("description", {"value":"This is a short desc"}, 0.8, constants.TECHNIQUE_REGULAR_EXPRESSION)
        assert len(a.results["description"]) == 1

    # Test 3: category should be among the accepted categories. TO DO if time