import os
import unittest
import json
from pathlib import Path
from .. import somef_cli

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestScholarlyArticle(unittest.TestCase):

    def test_scholarly_article(self):
        """Checks if codemeta file has referencePublication category with schholarly article type"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url='https://github.com/dgarijo/Widoco',
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=test_data_path + 'test_scholarly_article.json',
                            pretty=False,
                            missing=False)
        
        json_file_path = test_data_path + "test_scholarly_article.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        with open(test_data_path + "test_scholarly_article.json", "r") as text_file:
            data = json.load(text_file) 

        assert "referencePublication" in data, "Key 'referencePublication' is missing in JSON"
        assert isinstance(data["referencePublication"], list), "'referencePublication' is not a list"

        assert any(entry.get("@type") == "ScholarlyArticle" for entry in data["referencePublication"]), \
            "No entry in 'referencePublication' is of type 'ScholarlyArticle'"
        os.remove(json_file_path)