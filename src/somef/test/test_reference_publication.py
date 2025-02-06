import os
import unittest
import json
from pathlib import Path
from .. import somef_cli

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestWiki(unittest.TestCase):

    def test_codemeta_reference_publication(self):
        """Checks if codemeta file has referencePublication category"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url='https://github.com/dgarijo/Widoco',
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=test_data_path + 'test_codemeta_reference_publication.json',
                            pretty=False,
                            missing=False)
        
        json_file_path = test_data_path + "test_codemeta_reference_publication.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_codemeta_reference_publication.json", "r")
        data = text_file.read()
        text_file.close()

        assert "referencePublication" in data, "Key 'referencePublication' is missing in JSON"

        os.remove(json_file_path)