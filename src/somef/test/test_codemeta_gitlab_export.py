import os
import unittest
import json
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestCodemetaGitlabExport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ejecuta somef_cli una sola vez y guarda el JSON"""
        cls.json_file = test_data_path + "test_json_codemeta_gitlab_export.json"
        
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url='https://gitlab.com/escape-ossr/eossr',
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=cls.json_file,
                            pretty=False,
                            missing=False)

        with open(cls.json_file, "r") as f:
            cls.json_content = json.load(f)

    def test_codemeta_gitlab_export(self):
        """Checks if codemeta file has been exported from a gitlab repo"""
        # somef_cli.run_cli(threshold=0.8,
        #                     ignore_classifiers=False,
        #                     repo_url='https://gitlab.com/escape-ossr/eossr',
        #                     doc_src=None,
        #                     in_file=None,
        #                     output=None,
        #                     graph_out=None,
        #                     graph_format="turtle",
        #                     codemeta_out=test_data_path + 'test_gitlab.json',
        #                     pretty=False,
        #                     missing=False)
        
        # json_file_path = test_data_path + "test_gitlab.json"
        # # check if the file has been created in the correct path
        # assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        # text_file = open(test_data_path + "test_gitlab.json", "r")
        # data = text_file.read()
        # text_file.close()
        # check if has been correctly created with the normal structure
        # assert data.find(constants.CAT_IDENTIFIER) > 0
        # os.remove(test_data_path + "test_gitlab.json")
        # assert self.json_content.find(constants.CAT_IDENTIFIER) > 0
        assert constants.CAT_IDENTIFIER in self.json_content, f"Missing key {constants.CAT_IDENTIFIER} in JSON"
        
    def test_gitlab_license(self):
        """Checks that if exist the spdfx in license"""
        assert "license" in self.json_content, "Missing 'license' field in JSON"
        assert "url" in self.json_content["license"], "Missing 'url' in license"

    @classmethod
    def tearDownClass(cls):
        """delete temp file JSON just if all the test pass"""
        if os.path.exists(cls.json_file):  # Verifica que el archivo exista
            try:
                os.remove(cls.json_file)
                print(f"Deleted {cls.json_file}")  # Mensaje para confirmar la eliminación
            except Exception as e:
                print(f"Failed to delete {cls.json_file}: {e}")  # Captura errores de eliminación   

if __name__ == "__main__":
    unittest.main()