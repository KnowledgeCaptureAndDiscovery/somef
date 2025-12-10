import os
import unittest
import json
from pathlib import Path
from .. import somef_cli

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep
class TestWiki(unittest.TestCase):
    # def test_no_wiki(self):
    #     """Checks if codemeta file has been exported without wiki"""

    
    def test_wiki_with_content(self):
        """Checks if codemeta file has been exported without wiki content"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            repo_url='https://github.com/juanjemdIos/fair_ontologies',
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=test_data_path + 'test_wiki_with_content.json',
                            pretty=False,
                            missing=False)
        
        json_file_path = test_data_path + "test_wiki_with_content.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_wiki_with_content.json", "r")
        data = text_file.read()
        text_file.close()

        assert "https://github.com/juanjemdIos/fair_ontologies/wiki" in json.dumps(data), \
        "Wiki URL should be present in the JSON"

        os.remove(json_file_path)

    def test_wiki_without_content(self):
        """Checks if codemeta file has been exported with wiki content"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            # repo_url='https://github.com/dgarijo/Widoco',
                            repo_url=None,
                            local_repo= test_data_repositories + "Widoco",
                            doc_src=None,
                            in_file=None,
                            output=None,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=test_data_path + 'test_wiki_without_content.json',
                            pretty=False,
                            missing=False)
        
        json_file_path = test_data_path + "test_wiki_without_content.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_wiki_without_content.json", "r")
        data = text_file.read()
        text_file.close()

        assert "https://github.com/dgarijo/Widoco/wiki" not in json.dumps(data), \
        "Wiki URL should not be present in the JSON"

        os.remove(json_file_path)