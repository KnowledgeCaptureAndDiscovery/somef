import os
import unittest
import json
from pathlib import Path
from .. import somef_cli

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestCodemetaExport(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Runs somef_cli once and saves the JSON"""
        cls.json_file = test_data_path + "test_json_codemeta_export.json"
        
        somef_cli.run_cli(
            threshold=0.8,
            ignore_classifiers=False,
            repo_url="https://github.com/tpronk/somef-demo-repo/",
            doc_src=None,
            in_file=None,
            output=None,
            graph_out=None,
            graph_format="turtle",
            codemeta_out=cls.json_file,
            pretty=True,
            missing=True,
            readme_only=False
        )

        with open(cls.json_file, "r") as f:
            cls.json_content = json.load(f)


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

        assert "https://w3id.org/codemeta/3.0" in json.dumps(data), \
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
    
    def test_last_release(self):
        """Checks that if exist the last release and notes"""
        assert "releaseNotes" in self.json_content and "softwareVersion" in self.json_content, "Missing releaseNotes or softwareVersion in JSON"
    
    def test_spdx_id(self):
        """Checks that if exist the spdfx in license"""
        assert "license" in self.json_content, "Missing 'license' field in JSON"
        assert "identifier" in self.json_content["license"], "Missing 'identifier' in license"
    
    def test_development_status(self):
        """Checks that if exist the repository status"""
        assert "developmentStatus" in self.json_content, "Missing developmentStatus in JSON"

    def test_reference_publication_url_natural_language(self):

        """Checks that referencePublication contains a ScholarlyArticle with a URL in citation natural language"""
        assert "referencePublication" in self.json_content, "Missing referencePublication in JSON"
        assert isinstance(self.json_content["referencePublication"], list), "referencePublication should be a list"
        assert any("url" in pub for pub in self.json_content["referencePublication"]), "No URL found in referencePublication"

    def test_date_published(self):
        """Checks that if exist the first date published"""
        assert "datePublished" in self.json_content, "Missing first date published in JSON"

    def test_author_in_reference_publication(self):
        """Checks that if exist expected author in referencePublication"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + 'test_authors_reference.json',
                          pretty=True,
                          missing=True)
        json_file_path = test_data_path + "test_authors_reference.json"
        # check if the file has been created in the correct path
        assert os.path.exists(json_file_path), f"File {json_file_path} doesn't exist."

        with open(test_data_path + "test_authors_reference.json", "r") as text_file:
            data = json.load(text_file) 

        expected_family_name = "Garijo"
        expected_given_name = "Daniel"

        found = any(
            any(
                author.get("familyName") == expected_family_name and author.get("givenName") == expected_given_name
                for author in ref.get("author", [])
            )
            for ref in data["referencePublication"]
        )
        
        assert "referencePublication" in data, "Key 'referencePublication' is missing in JSON"
        assert isinstance(data["referencePublication"], list), "'referencePublication' is not a list"
        assert found, f"Author {expected_given_name} {expected_family_name} not found in referencePublication"
        os.remove(json_file_path)

    def test_codemeta_relevants_programming_languages(self):
        """Checks if codemeta file has filter just relevants programming language"""

        assert "programmingLanguage" in self.json_content, "Key 'programmingLanguage' is missing in JSON"
        expected_languages = ["Jupyter Notebook"]
        assert set(self.json_content["programmingLanguage"]) == set(expected_languages), f"Mismatch: {self.json_content['programmingLanguage']}"


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
 
    