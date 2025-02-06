import os
import unittest
import json
from pathlib import Path
from .. import somef_cli

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestCitationCFF(unittest.TestCase):

    def test_citation_cff(self):
        """Checks if codemeta file has some citation.cff in reference publication"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url='https://github.com/dgarijo/Widoco',
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=test_data_path + 'test_citation_cff.json',
                            pretty=False,
                            missing=False)
        
        json_file_path = test_data_path + "test_citation_cff.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_citation_cff.json", "r")
        data = json.load(text_file) 
        text_file.close()

        reference_publications = data["referencePublication"]
        assert all("CITATION.cff" not in ref for ref in reference_publications), \
        f"'CITATION.cff' found in referencePublication: {reference_publications}"

        os.remove(json_file_path)