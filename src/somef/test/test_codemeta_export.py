import os
import unittest
import json
from pathlib import Path
from .. import somef_cli

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestCodemetaExport(unittest.TestCase):
    
    def test_codemeta_version(self):
        """Checks if codemeta version is v3"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + 'test_codemeta_v3.json',
                          pretty=True,
                          missing=True)
        
        json_file_path = test_data_path + "test_codemeta_v3.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_codemeta_v3.json", "r")
        data = text_file.read()
        text_file.close()

        assert "https://w3id.org/codemeta/v3.0" in json.dumps(data), \
        "Json must be contained codemeta version 3"

        os.remove(json_file_path)


    def test_codemeta_reference_publication(self):
        """Checks if codemeta file has referencePublication category"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + 'test_codemeta_reference_publication.json',
                          pretty=True,
                          missing=True)
        
        json_file_path = test_data_path + "test_codemeta_reference_publication.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_codemeta_reference_publication.json", "r")
        data = text_file.read()
        text_file.close()

        assert "referencePublication" in data, "Key 'referencePublication' is missing in JSON"

        os.remove(json_file_path)


    def test_scholarly_article(self):
        """Checks if codemeta file has referencePublication category with schholarly article type"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + 'test_scholarly_article.json',
                          pretty=True,
                          missing=True)
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


    def test_citation_cff(self):
        """Checks if codemeta file has some citation.cff in reference publication"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + 'test_citation_cff.json',
                          pretty=True,
                          missing=True)
        
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


    