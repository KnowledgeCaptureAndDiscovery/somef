import os
import unittest
import json
from pathlib import Path
from .. import somef_cli
from ..parser import pom_xml_parser
from ..export import json_export

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep
test_data_api_json = str(Path(__file__).parent / "test_data" / "api_responses") + os.path.sep

class TestGoogleCompliantExport(unittest.TestCase):


    def test_google_compliant_version(self):
        """Checks if codemeta version is v3"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format=None,
                          google_codemeta_out=test_data_path + "test_google_compliant.json",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        
                
        json_file_path = test_data_path + "test_google_compliant.json"
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        text_file = open(test_data_path + "test_google_compliant.json", "r")
        data = data = json.load(text_file)
        text_file.close()
        
        assert "@context" in data, "JSON-LD must contain @context" 
        assert data["@context"].get("@vocab") == "https://schema.org/", "Context @vocab must be https://schema.org/" 
        assert data["@context"].get("codemeta") == "https://w3id.org/codemeta/3.0/", "Context must define codemeta prefix" 
        
        
        assert "codemeta:referencePublication" in data, "JSON must contain codemeta:referencePublication" 
        refpub = data["codemeta:referencePublication"] 
        assert isinstance(refpub, list), "referencePublication must be a list" 
        assert refpub[0].get("@type") == "ScholarlyArticle", "referencePublication entries must be ScholarlyArticle" 


        os.remove(json_file_path)