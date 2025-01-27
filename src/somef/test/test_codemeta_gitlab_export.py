import os
import unittest
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestCodemetaGitlabExport(unittest.TestCase):
    def test_codemeta_gitlab_export(self):
        """Checks if codemeta file has been exported from a gitlab repo"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url='https://gitlab.com/escape-ossr/eossr',
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=test_data_path + 'test_gitlab.json',
                            pretty=False,
                            missing=False)
        
        json_file_path = test_data_path + "test_gitlab.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_gitlab.json", "r")
        data = text_file.read()
        text_file.close()
        # check if has been correctly created with the normal structure
        assert data.find(constants.CAT_IDENTIFIER) > 0
        os.remove(test_data_path + "test_gitlab.json")
