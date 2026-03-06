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
            # cat_result = result.results[constants.CAT_APPLICATION_DOMAIN][0]
            # self.assertEqual(cat_result[constants.PROP_RESULT]['value'], "Semantic web")
            values = [
                r[constants.PROP_RESULT]['value']
                for r in result.results[constants.CAT_APPLICATION_DOMAIN]
            ]
            assert "Semantic web" in values


    def test_threshold_old_vs_new(self):
            """This test shows the difference between the old and new code using a fake model: the old code adds a result, the new code doesn’t."""

            # Fake model to simulate predict and predict_proba
            class FakeModel:
                def __init__(self):
                    self.classes_ = ["Semantic web", "Other"] 
                def predict(self, text):
                    return ["Semantic web"] 
                def predict_proba(self, text):
                    # Semantic web = 0.75 (< threshold 0.8)
                    # Other = 0.85 (> threshold 0.8)
                    return [[0.75, 0.85]]

            text = "Dummy README"
            threshold = 0.8

            # --- old code: use max(proba) ---
            def run_old(text, threshold, results):
                model = FakeModel()
                cat = model.predict(text)[0]
                prob = max(model.predict_proba(text)[0])
                if cat != "Other" and prob > threshold:
                    results.add_result(
                        constants.CAT_APPLICATION_DOMAIN,
                        {
                            constants.PROP_TYPE: constants.STRING,
                            constants.PROP_VALUE: cat
                        },
                        prob,
                        constants.TECHNIQUE_SUPERVISED_CLASSIFICATION
                    )
                return results

            # --- new code: use probability of predict class ---
            def run_new(text, threshold, results):
                model = FakeModel()
                cat = model.predict(text)[0]
                proba = model.predict_proba(text)[0]
                prob = proba[model.classes_.index(cat)]
                if cat != "Other" and prob > threshold:
                    results.add_result(
                        constants.CAT_APPLICATION_DOMAIN,
                        {
                            constants.PROP_TYPE: constants.STRING,
                            constants.PROP_VALUE: cat
                        },
                        prob,
                        constants.TECHNIQUE_SUPERVISED_CLASSIFICATION
                    )
                return results


            # Test old code: must add the result
            result_old = run_old(text, threshold, Result())
            print(result_old.results)
            self.assertEqual(
                result_old.results[constants.CAT_APPLICATION_DOMAIN][0]['result']['value'],
                "Semantic web"
            )
            self.assertEqual(
                result_old.results[constants.CAT_APPLICATION_DOMAIN][0]['confidence'],
                0.85
            )
            self.assertEqual(
                result_old.results[constants.CAT_APPLICATION_DOMAIN][0]['technique'],
                constants.TECHNIQUE_SUPERVISED_CLASSIFICATION
            )

            # Test new code: must avoid the result
            result_new = run_new(text, threshold, Result())
            print(result_new.results)
            self.assertEqual(
                len(result_new.results.get(constants.CAT_APPLICATION_DOMAIN, [])),
                0
            )