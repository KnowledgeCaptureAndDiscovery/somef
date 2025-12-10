import json
import os
import unittest
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep
test_data_api_json = str(Path(__file__).parent / "test_data" / "api_responses") + os.path.sep

class TestJSONExport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs somef_cli once and saves the JSON"""
        # cls.json_file = test_data_path + "test_json_widoco_export.json"
        cls.api_results_file = test_data_api_json + "widoco_api_response.json"
        with open(cls.api_results_file, "r", encoding="utf-8") as f:
            cls.json_content= json.load(f)

        # somef_cli.run_cli(threshold=0.8,
        #                   ignore_classifiers=False,
        #                   repo_url="https://github.com/dgarijo/Widoco",
        #                   local_repo=None,
        #                   doc_src=None,
        #                   in_file=None,
        #                   output=cls.json_file,
        #                   graph_out=None,
        #                   graph_format="turtle",
        #                   codemeta_out=None,
        #                   pretty=True,
        #                   missing=False,
        #                   readme_only=False)

        # with open(cls.json_file, "r") as f:
        #     cls.json_content = json.load(f)

    # def test_issue_417(self):
    #     """Checks whether a repository correctly extracts to Codemeta"""


    #     somef_cli.run_cli(threshold=0.8,
    #                       ignore_classifiers=False,
    #                       repo_url="https://github.com/dgarijo/Widoco",
    #                       local_repo=None,              
    #                       doc_src=None,
    #                       in_file=None,
    #                       output=None,
    #                       graph_out=None,
    #                       graph_format="turtle",
    #                       codemeta_out=test_data_path + "test-417.json-ld",
    #                       pretty=True,
    #                       missing=False,
    #                       readme_only=False)
        
    #     text_file = open(test_data_path + "test-417.json-ld", "r")
    #     data = text_file.read()
    #     text_file.close()
    #     json_content = json.loads(data)
    #     issue_tracker = json_content["issueTracker"]  # JSON is in Codemeta format
     
    #     #len(json_content["citation"]) 
    #     #codemeta category citation is now referencePublication
    #     assert issue_tracker == 'https://github.com/dgarijo/Widoco/issues' and len(json_content["referencePublication"]) > 0 and \
    #            len(json_content["name"]) > 0 and len(json_content["identifier"]) > 0 and \
    #            len(json_content["description"]) > 0 and len(json_content["readme"]) > 0 and \
    #            len(json_content["author"]) > 0 and len(json_content["buildInstructions"]) > 0 and \
    #            len(json_content["softwareRequirements"]) > 0 and len(json_content["programmingLanguage"]) > 0 and \
    #            len(json_content["keywords"]) > 0 and len(json_content["logo"]) > 0 and \
    #            len(json_content["license"]) > 0 and len(json_content["dateCreated"]) > 0
        
    #     os.remove(test_data_path + "test-417.json-ld")

    def test_issue_311(self):
        """Checks if Codemeta export has labels defined outside Codemeta"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "repostatus-README.md",
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + "test-repostatus-311.json-ld",
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "test-repostatus-311.json-ld", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("\"repoStatus\":") < 0
        os.remove(test_data_path + "test-repostatus-311.json-ld")

    def test_issue_150(self):
        """Codemeta export checks"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-mapshaper.md",
                          local_repo=None,
                          in_file=None,
                          output=None,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=test_data_path + "test-150.json-ld",
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "test-150.json-ld", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_ACKNOWLEDGEMENT) == -1
        os.remove(test_data_path + "test-150.json-ld")

    def test_issue_281(self):
        """Checks if missing categories are properly added to the output JSON, when required"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "repostatus-README.md",
                          in_file=None,
                          output=test_data_path + "test-281.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-281.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_MISSING) > 0
        os.remove(test_data_path + "test-281.json")

    def test_issue_629(self):
        """Checks if citattion have news properties """
        # somef_cli.run_cli(threshold=0.8,
        #                   ignore_classifiers=False,
        #                   repo_url=None,
        #                   doc_src=None,
        #                   local_repo=test_data_repositories + "Widoco",
        #                   in_file=None,
        #                   output=test_data_path + "test_issue_629.json",
        #                   graph_out=None,
        #                   graph_format="turtle",
        #                   codemeta_out=None,
        #                   pretty=True,
        #                   missing=True)
        
        # with open(test_data_path + "test_issue_629.json", "r") as text_file:
        #     data = json.load(text_file) 

        # citation = data.get("citation", [])
        citation = self.json_content.get("citation", [])
        assert citation, "No 'citation' found in JSON"
        assert any(
            entry.get("result", {}).get("format") == "cff" and
            "doi" in entry.get("result", {}) and
            "title" in entry.get("result", {})
            for entry in citation
        ), "Citation.cff must have doi and title"

        # os.remove(test_data_path + "test_issue_629.json")



    def test_issue_651(self):
        """Checks if keywords is in the missing categories because is empty"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-panda.md",
                          in_file=None,
                          output=test_data_path + "test-651.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)

        with open(test_data_path + "test-651.json", "r") as text_file:
            data = json.load(text_file)

        assert 'keywords' in data.get(constants.CAT_MISSING, []), "Keywords is not in CAT_MISSING" 
        os.remove(test_data_path + "test-651.json")

    def test_issue_745(self):
        """Checks whether all the items in license has a spdx_id"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            # repo_url="https://github.com/sunpy/sunpy",
                            repo_url=None,
                            local_repo=test_data_repositories + "sunpy",
                            doc_src=None,
                            in_file=None,
                            output=test_data_path + "test_issue_745.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=False,
                            readme_only=False)
        
        text_file = open(test_data_path + "test_issue_745.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        licenses = json_content["license"]

        # print('---------------------------')
        # print(licenses)

        for i, license_entry in enumerate(licenses):
            assert "spdx_id" in license_entry["result"], f"Missing 'spdx_id' in license{i}"
            assert license_entry["result"]["spdx_id"], f"'spdx_id' empty in license {i}"
        
        os.remove(test_data_path + "test_issue_745.json")

    def test_issue_499(self):
        """Checks whether a repository correctly extracts assets from release"""
        
        # somef_cli.run_cli(threshold=0.8,
        #                 ignore_classifiers=False,
        #                 repo_url="https://github.com/dgarijo/Widoco",
        #                 local_repo=None,
        #                 doc_src=None,
        #                 in_file=None,
        #                 output=test_data_path + "test-499.json-ld",
        #                 graph_out=None,
        #                 graph_format="turtle",
        #                 codemeta_out= None,
        #                 pretty=True,
        #                 missing=False,
        #                 readme_only=False)
        
        # text_file = open(test_data_path + "test-499.json-ld", "r")
        # data = text_file.read()
        # text_file.close()
        # json_content = json.loads(data)

        assert "releases" in self.json_content, "Missing 'releases' key in JSON content"
        assert isinstance(self.json_content["releases"], list), "'releases' should be a list"

        release_1425 = None
        for release in self.json_content["releases"]:
            if release.get("result", {}).get("tag") == "v1.4.25":
                release_1425 = release
                break

        assert release_1425 is not None, "No release with tag 'v1.4.25' found"

        assets = release_1425.get("result", {}).get("assets", [])
        assert any(asset.get("name") == "widoco-1.4.25-jar-with-dependencies_JDK-11.jar" for asset in assets), \
            "Asset 'widoco-1.4.25-jar-with-dependencies_JDK-11.jar' not found in release v1.4.25"

        # os.remove(test_data_path + "test-499.json-ld")

    def test_issue_577(self):
        """Checks if there are idenfiers from Software Heritage in the README file"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco-swh.md",
                          in_file=None,
                          output=test_data_path + "test-577.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)

        with open(test_data_path + "test-577.json", "r") as text_file:
            data = json.load(text_file)
      
        expected_values = {
            "https://doi.org/10.5281/zenodo.11093793",
            "https://archive.softwareheritage.org/swh:1:rev:fec66b89a4f4acb015a44c7f8cb671d49bec626a"
        }
        identifiers = data.get("identifier", [])
        found_values = set()
    
        for item in identifiers:
            value = item["result"]["value"]        
            found_values.add(value)

        for expected in expected_values:
            assert expected in found_values, f"Expected identifier not found: {expected}"

        os.remove(test_data_path + "test-577.json")


    def test_issue_580(self):
        """Checks if there are Project homepage in the readme file"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-citation-file-format.md",
                          in_file=None,
                          output=test_data_path + "test-580.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)

        with open(test_data_path + "test-580.json", "r") as text_file:
            data = json.load(text_file)
      
        found = False  
        homepage_entries = data.get("homepage", [])
        print('---------------------------')
        print(homepage_entries)
        for item in homepage_entries:
            technique = item.get("technique")
            result = item.get("result", {})
            value = result.get("value")

            if technique == "regular_expression" and value == "https://citation-file-format.github.io":
                found = True
                break  

        assert found, "Expected homepage not found"

        os.remove(test_data_path + "test-580.json")

    def test_issue_653(self):
        """Checks if json from widoco repo has more than 30 releases"""
        assert len(self.json_content["releases"]) > 30, f"Expected more than 30 releases, found {len(self.json_content['release'])}"

    def test_not_recursive_folders(self):
        """
        Checks that build files in subfolders are ignored if they already exist in the root,
        and that duplicates do not appear in the results.
        pom.xml has been duplicated in docs/pom.xml
        """

        output_path = test_data_path + 'test_widoco_not_recursive_folders.json'

        somef_cli.run_cli(  threshold=0.8,
                            local_repo=test_data_repositories + "Widoco",
                            doc_src=None,
                            in_file=None,
                            output=output_path,
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=False,
                            readme_only=False)


        with open(output_path, "r") as f:
            json_content = json.load(f)

        build_files = [
            entry[constants.PROP_RESULT][constants.PROP_VALUE]
            for key in json_content
            for entry in json_content[key]
            if key == constants.CAT_HAS_BUILD_FILE
        ]

        # root
        assert any("pom.xml" in bf for bf in build_files), "The root pom.xml should be present"
        # No docs/pom.xml
        assert not any("docs/pom.xml" in bf for bf in build_files), "The pom.xml in docs/ should not be processed"
        assert len(build_files) == len(set(build_files)), "There should be no duplicate build files"


    def test_runtime_platform(self):
        """
        Checks that the runtime_platform information is correctly extracted from the project.
        """
        
        runtime_entries = [
            entry[constants.PROP_RESULT]
            for key in self.json_content
            for entry in self.json_content[key]
            if key == constants.CAT_RUNTIME_PLATFORM
        ]

        assert len(runtime_entries) > 0, "There should be at least one runtime_platform entry"

        found_java = any(
            entry.get("name") == "Java" and entry.get("value") == "Java: 1.8"
            for entry in runtime_entries
        )
        assert found_java, "Java runtime with value Java: 1.8 should be present"


    def test_issue_830(self):
        """Checks if citattion have identifiers """
        citation = self.json_content.get("citation", [])
        assert citation, "No 'citation' found in JSON"
        assert any(
            entry.get("result", {}).get("format") == "cff"
            and any(id.get("value") == "10.5281/zenodo.591294"
            for id in entry.get("result", {}).get("identifier", [])
        )
            for entry in citation
        ), "Citation.cff must have identifier id 10.5281/zenodo.591294"

    # @classmethod
    # def tearDownClass(cls):
    #     """delete temp file JSON just if all the test pass"""
    #     if os.path.exists(cls.json_file): 
    #         try:
    #             os.remove(cls.json_file)
    #             print(f"Deleted {cls.json_file}") 
    #         except Exception as e:
    #             print(f"Failed to delete {cls.json_file}: {e}")  

if __name__ == '__main__':
    unittest.main()
