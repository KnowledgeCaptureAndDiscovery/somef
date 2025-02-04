import os
import unittest
import json
from pathlib import Path
from .. import somef_cli

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestWiki(unittest.TestCase):
    
    def test_codemeta_version(self):
        """Checks if codemeta version is v3"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url='https://github.com/dgarijo/Widoco',
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=test_data_path + 'test_codemeta_v3.json',
                            pretty=False,
                            missing=False)
        
        json_file_path = test_data_path + "test_codemeta_v3.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_codemeta_v3.json", "r")
        data = text_file.read()
        text_file.close()

        assert "https://doi.org/10.5063/schema/codemeta-3.0" in json.dumps(data), \
        "Json must be contained codemeta version 3"

        os.remove(json_file_path)