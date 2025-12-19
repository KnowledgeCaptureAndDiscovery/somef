import json
import os
import unittest
import validators
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestCli(unittest.TestCase):

    # Commenting this test because it downloads a big repository, and just checks that a ttl has a field.
    # The original issue was about having some fields missing in ttl. This does not seem to do that.
    # TO REVIEW.
    # def test_issue_224(self):
    #     repo_data = cli_get_data(0.8, False, repo_url="https://github.com/tensorflow/tensorflow/tree/v2.6.0")
    #     data_graph = DataGraph()
    #     data_graph.add_somef_data(repo_data)
    #     with open("test-tensorflow-2.6.0.ttl", "wb") as out_file:
    #         out_file.write(data_graph.g.serialize(format="turtle", encoding="UTF-8"))
    #     text_file = open("test-tensorflow-2.6.0.ttl", "r", encoding="UTF-8")
    #     data = text_file.read()
    #     text_file.close()
    #     assert data.find("sd:dateCreated") >= 0

    def test_issue_280(self):
        """Checks if SOMEF fails with a non-valid URL"""
        with open(test_data_path + "input-test.txt", "r") as in_handle:
            # get the line (with the final newline omitted) if the line is not empty
            repo_list = [line[:-1] for line in in_handle if len(line) > 1]
        # convert to a set to ensure uniqueness (we don't want to get the same data multiple times)
        repo_set = set(repo_list)
        # check if the urls in repo_set if are valid
        remove_urls = []
        for repo_elem in repo_set:
            if not validators.url(repo_elem):
                print("Not a valid repository url. Please check the url provided: " + repo_elem)
                # repo_set.remove(repo_url)
                remove_urls.append(repo_elem)
        # remove non valid urls in repo_set
        for remove_url in remove_urls:
            repo_set.remove(remove_url)
        assert len(repo_set) > 0

    def test_issue_200(self):
        """Tests if the hierarchical representation of headers is properly stored in the output"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=test_data_path + "test-200.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-200.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.PROP_PARENT_HEADER) > 0
        os.remove(test_data_path + "test-200.json")

    def test_issue_343(self):
        """Assesses problems with the parser"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-ya2o.md",
                          in_file=None,
                          output=test_data_path + "test-343.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-343.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.PROP_PARENT_HEADER) > 0
        os.remove(test_data_path + "test-343.json")

    def test_issue_355(self):
        """Checks somef failures against specific repositories"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=None,
                          local_repo=test_data_repositories + "bimerr-epw",
                          in_file=None,
                          output=test_data_path + "repositories/repos_oeg/test-355.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "repositories/repos_oeg/test-355.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_FULL_TITLE) > 0
        os.remove(test_data_path + "repositories/repos_oeg/test-355.json")

    def test_issue_346(self):
        """Checks if acks are properly detected"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-wothive.md",
                          in_file=None,
                          output=test_data_path + "test-346.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-346.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("acknowledgement") > 0
        os.remove(test_data_path + "test-346.json")

    def test_issue_241(self):
        """Checks the detection of package distributions"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-tensorflow-2.6.0.md",
                          in_file=None,
                          output=test_data_path + "test-241.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-241.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_PACKAGE_DISTRIBUTION) > 0
        os.remove(test_data_path + "test-241.json")

    def test_issue_380(self):
        """Checks if parser works well against level 3 and 4 headers"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-raidologist.md",
                          in_file=None,
                          output=test_data_path + "test-380.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-380.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_INSTALLATION) > 0
        os.remove(test_data_path + "test-380.json")

    def test_issue_379(self):
        """ Checks if a target readme works (it caused duplicate excerpts)"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-raidologist.md",
                          in_file=None,
                          output=test_data_path + "test-379.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-379.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        description = json_content[constants.CAT_DESCRIPTION]
        assert len(description) > 0
        os.remove(test_data_path + "test-379.json")

    def test_issue_383(self):
        """Checks if the section `Contact` can be properly parsed"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-mapeathor.md",
                          in_file=None,
                          output=test_data_path + "test-383.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-383.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("- [Ana Iglesias-Molina](https://github.com/anaigmo) (ana.iglesiasm@upm.es)") > 0
        os.remove(test_data_path + "test-383.json")

    def test_issue_384(self):
        """Assesses header extraction errors"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-fair-ontologies.md",
                          in_file=None,
                          output=test_data_path + "test-384.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-384.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("A public demo of FOOPS! is available here:") > 0
        os.remove(test_data_path + "test-384.json")

    def test_issue_378(self):
        """Checks classification of a header based on what was written in upper level headers"""
        somef_cli.run_cli(threshold=0.9,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-easytv-annotator.md",
                          in_file=None,
                          output=test_data_path + "test-378.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-378.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        installation = json_content[constants.CAT_INSTALLATION]
        assert_true = False
        print(installation)
        for install in installation:
            result_install = install[constants.PROP_RESULT]
            if constants.PROP_PARENT_HEADER in result_install.keys():
                if result_install[constants.PROP_ORIGINAL_HEADER] == "Hard way" and \
                        "Installation" in result_install[constants.PROP_PARENT_HEADER]:
                    assert_true = True
        assert assert_true
        os.remove(test_data_path + "test-378.json")

    def test_issue_378_2(self):
        """Checks classification of a header based on what was written in upper level headers"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-easytv-annotator.md",
                          in_file=None,
                          output=test_data_path + "test-378-2.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-378-2.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        installation = json_content[constants.CAT_INSTALLATION]
        final_result = False
        for install in installation:
            install_result = install[constants.PROP_RESULT]
            if constants.PROP_PARENT_HEADER in install_result.keys():
                if install_result[constants.PROP_ORIGINAL_HEADER] == "Easy way" and \
                        "Installation" in install_result[constants.PROP_PARENT_HEADER] \
                        and "easytv-annotator" in install_result[constants.PROP_PARENT_HEADER]:
                    final_result = True
        os.remove(test_data_path + "test-378-2.json")
        assert final_result

    def test_issue_260(self):
        """Checks if colab notebooks are detected"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-kgtk-notebooks.md",
                          in_file=None,
                          output=test_data_path + "test-260.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-260.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_EXECUTABLE_EXAMPLE) > 0
        os.remove(test_data_path + "test-260.json")

    def test_issue_319_1(self):
        """Check if citation file format is recognized and returned"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=None,
                          local_repo=test_data_repositories + "Widoco",
                          in_file=None,
                          output=test_data_path + "test-319-1.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-319-1.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.FORMAT_CFF) > 0
        os.remove(test_data_path + "test-319-1.json")

    def test_issue_388(self):
        """Test checks that ontologies are recognized appropriately"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=None,
                          local_repo=test_data_repositories + "Widoco",
                          in_file=None,
                          output=test_data_path + "test-388.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "test-388.json", "r")
        data = text_file.read()
        json_content = json.loads(data)
        text_file.close()
        assert len(json_content[constants.CAT_ONTOLOGIES]) == 2
        os.remove(test_data_path + "test-388.json")

    def test_issue_319_2(self):
        """Test checks that the output format of citation files is specified in the output"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=None,
                          local_repo=test_data_repositories + "kgtk-notebooks",
                          in_file=None,
                          output=test_data_path + "test-319-2.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-319-2.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.FORMAT_JUPYTER_NB) > 0
        os.remove(test_data_path + "test-319-2.json")

    def test_issue_385(self):
        """More checks based on parent headers"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=test_data_path + "README-tada-gam.md",
                          in_file=None,
                          output=test_data_path + "test-385.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-385.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        usage = json_content[constants.CAT_USAGE]
        assert len(usage) == 3
        os.remove(test_data_path + "test-385.json")

    def test_issue_398(self):
        """Checks that repostatus has confidence (always 1.0)"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=test_data_repositories + "Widoco",
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-398.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True)
        text_file = open(test_data_path + "test-398.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        repo_status = json_content[constants.CAT_STATUS][0]
        confidence = repo_status[constants.PROP_CONFIDENCE]
        assert confidence == 1
        os.remove(test_data_path + "test-398.json")

    # def test_issue_393(self):
    #     """Checks that if a folder within a repository is passed to the tool, it does not break"""
    #     cli.run_cli(threshold=0.8,
    #                 ignore_classifiers=False,
    #                 repo_url="https://github.com/oeg-upm/wot-hive/tree/main/docker/auroral-hive",
    #                 doc_src=None,
    #                 in_file=None,
    #                 output=test_data_path + "test-393.json",
    #                 graph_out=None,
    #                 graph_format="turtle",
    #                 codemeta_out=None,
    #                 pretty=True,
    #                 missing=True)
    #     text_file = open(test_data_path + "test-393.json", "r")
    #     data = text_file.read()
    #     text_file.close()
    #     json_content = json.loads(data)
    #     acknowledgement = json_content['acknowledgement']
    #     assert acknowledgement is not None
    #     os.remove(test_data_path + "test-393.json")

    def test_issue_314(self):
        """Checks that the program can be run using only a single readme"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/oeg-upm/wot-hive/tree/main/docker/auroral-hive",
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-314.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=True)
        text_file = open(test_data_path + "test-314.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        acknowledgement = json_content[constants.CAT_ACKNOWLEDGEMENT]
        assert acknowledgement is not None
        os.remove(test_data_path + "test-314.json")

    def test_issue_314_1(self):
        """Checks that the program can be run using only a single readme. GitHub"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            # repo_url="https://github.com/tensorflow/tensorflow/tree/v2.6.0",
                            repo_url=None,
                            # doc_src=None,
                            doc_src= test_data_path + "README-tensorflow-2.6.0.md",
                            in_file=None,
                            output=test_data_path + "test-314-1.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=True,
                            readme_only=True)
        text_file = open(test_data_path + "test-314-1.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        image = json_content[constants.CAT_IMAGE]
        assert image is not None
        os.remove(test_data_path + "test-314-1.json")

    def test_issue_314_2(self):
        """Checks that the program can be run using only a single readme. Gitlab"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            #   repo_url="https://gitlab.com/jleblay/tokei",
                            repo_url=None,  
                            #   doc_src=None,
                            doc_src= test_data_path + "README-tokei.md",
                            in_file=None,
                            output=test_data_path + "test-314-2.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=False,
                            readme_only=True)
        text_file = open(test_data_path + "test-314-2.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        description = json_content[constants.CAT_DESCRIPTION]
        assert description is not None
        os.remove(test_data_path + "test-314-2.json")

    def test_issue_314_3(self):
        """Checks that the program can be run using only a single readme. Gitlab"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            # repo_url="https://gitlab.com/unboundedsystems/adapt/-/tree/release-0.1",
                            repo_url=None,
                            # doc_src=None,
                            doc_src= test_data_path + "README-unboundedsystems.md",
                            in_file=None,
                            output=test_data_path + "test-314-3.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=True,
                            readme_only=True)
        text_file = open(test_data_path + "test-314-3.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        description = json_content[constants.CAT_DESCRIPTION]
        assert description is not None
        os.remove(test_data_path + "test-314-3.json")

    def test_gitlab(self):
        """Checks if SOMEF works against Gitlab. Full analysis"""
        somef_cli.run_cli(threshold=0.8,
                          repo_url="https://gitlab.com/jleblay/tokei",
                          output=test_data_path + "test-314-2.json",
                          pretty=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-314-2.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        description = json_content[constants.CAT_DESCRIPTION]
        assert description is not None
        os.remove(test_data_path + "test-314-2.json")

    def test_issue_403(self):
        """Checks that the readme link returned by somef is correct"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/oeg-upm/wot-hive",
                        #   repo_url=None,
                        #   local_repo=test_data_repositories + "wot-hive",
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-403.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-403.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        readme_url = json_content[constants.CAT_README_URL][0]
        excerpt = readme_url[constants.PROP_RESULT][constants.PROP_VALUE]
        assert excerpt == 'https://raw.githubusercontent.com/oeg-upm/wot-hive/main/README.md'
        os.remove(test_data_path + "test-403.json")

    def test_issue_408(self):
        """Checks that the documentation links (docs) are found only if the docs folder has documents that seem like
        documentation"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=test_data_repositories + "bimerr-epw",
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-408.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-408.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(
            "https://github.com/oeg-upm/bimerr-epw/tree/master/Code/TDATA2RDFANDV/static/rest_framework/docs") == -1
        os.remove(test_data_path + "test-408.json")

    def test_issue_225_406(self):
        """Checks if wiki links are detected"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-mapshaper.md",
                          in_file=None,
                          output=test_data_path + "test-225.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-225.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("\"" + constants.PROP_FORMAT + "\": \"" + constants.FORMAT_WIKI + "\"")
        os.remove(test_data_path + "test-225.json")

    def test_issue_406(self):
        """Test that checks whether the extracted elements in the documentation have a type"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-OWL-To-OAS.md",
                          in_file=None,
                          output=test_data_path + "test-406.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-406.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("\"" + constants.PROP_FORMAT + "\": \"" + constants.FORMAT_READTHEDOCS + "\"") >= 0
        os.remove(test_data_path + "test-406.json")

    def test_issue_255(self):
        """Tests if somef can detect wiki articles"""
        somef_cli.run_cli(threshold=0.8,
                            ignore_classifiers=False,
                            # repo_url="https://github.com/mbloch/mapshaper/",
                            repo_url=None,
                            local_repo=None,
                            # doc_src=None,
                            doc_src=test_data_path + "README-mapshaper.md",
                            in_file=None,
                            output=test_data_path + "test-255.json",
                            graph_out=None,
                            graph_format="turtle",
                            codemeta_out=None,
                            pretty=True,
                            missing=True,
                            readme_only=False)
        text_file = open(test_data_path + "test-255.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("https://github.com/mbloch/mapshaper/wiki") != -1
        os.remove(test_data_path + "test-255.json")

    def test_issue_255_1(self):
        """Tests if somef can detect the abscence of wikis if a repo does not have it."""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/SoftwareUnderstanding/software_types/",
                          local_repo=None,
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-255-1.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-255-1.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("https://github.com/SoftwareUnderstanding/software_types/wiki") == -1
        os.remove(test_data_path + "test-255-1.json")

    def test_issue_375(self):
        """Checks that svg badges are not captured as images"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-pylops.md",
                          in_file=None,
                          output=test_data_path + "test-375.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-375.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("https://img.shields.io/badge/chat-slack-green.svg") == -1
        os.remove(test_data_path + "test-375.json")

    def test_issue_136(self):
        """Tests that checks if the DOI is extracted from a reference publication in somef"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-widoco.md",
                          in_file=None,
                          output=test_data_path + "test-136.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-136.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("doi") >= 0
        os.remove(test_data_path + "test-136.json")

    def test_issue_136_1(self):
        """Tests that checks if the DOI is extracted from a reference publication in somef"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-tokei.md",
                          in_file=None,
                          output=test_data_path + "test-136-1.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-136-1.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("doi") >= 0
        os.remove(test_data_path + "test-136-1.json")

    def test_issue_353(self):
        """Tests that somef can successfully download a given github repo (reportedly failing)"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/proycon/analiticcl",
                          local_repo=None,
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-353.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-353.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.CAT_DESCRIPTION) >= 0
        os.remove(test_data_path + "test-353.json")

    def test_issue_366(self):
        """Checks if somef can detect Docker compose files"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=test_data_repositories + "wot-hive",
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-366.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-366.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(constants.FORMAT_DOCKERFILE) >= 0
        os.remove(test_data_path + "test-366.json")

    def test_issue_428(self):
        """Checks if the text before the main header is passed on to the classifiers"""
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-manim.md",
                          in_file=None,
                          output=test_data_path + "test-428.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-428.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(
            "Manim is an engine for precise programmatic animations, designed for creating explanatory math videos.") > 0
        os.remove(test_data_path + "test-428.json")

    def test_issue_443(self):
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-epw2rdf-contents.md",
                          in_file=None,
                          output=test_data_path + "test-443.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-443.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        installation = json_content[constants.CAT_INSTALLATION]
        assert installation is not None
        os.remove(test_data_path + "test-443.json")

    def test_issue_443_3(self):
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/oeg-upm/pcake",
                          local_repo=None,
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-443.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-443.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        description = json_content[constants.CAT_DESCRIPTION]
        assert description is not None
        os.remove(test_data_path + "test-443.json")

    def test_issue_457(self):
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-pytorch.md",
                          in_file=None,
                          output=test_data_path + "test-457.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-457.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        description = json_content[constants.CAT_DESCRIPTION]
        assert description is not None
        os.remove(test_data_path + "test-457.json")

    def test_issue_556(self):
        """
        This test assesses whether documentation links that have been commented in the readme out are ignored.
        In a nutshell, this test verifies that all comments are gone.
        Source: https://github.com/KnowledgeCaptureAndDiscovery/somef/issues/556
        """
        out_file = "test-556.json"
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url=None,
                          local_repo=None,
                          doc_src=test_data_path + "README-TINTO.md",
                          in_file=None,
                          output=test_data_path + out_file,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + out_file, "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        doc = json_content[constants.CAT_DOCUMENTATION][0]
        doc = doc['result']['value']  # the actual value found in the document
        assert ("<!--- **[Read the documentation]" not in doc)
        os.remove(test_data_path + out_file)

    def test_issue_445(self):
        """Checks that ACKs are recognized both in files and in headers, and combined appropriately"""
        somef_cli.run_cli(threshold=0.9,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=None,
                          local_repo=test_data_repositories + "ack",
                          in_file=None,
                          output=test_data_path + "repositories/repos_oeg/test-445.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "repositories/repos_oeg/test-445.json", "r")
        data = text_file.read()
        json_content = json.loads(data)
        text_file.close()
        assert len(json_content[constants.CAT_ACKNOWLEDGEMENT]) == 2
        os.remove(test_data_path + "repositories/repos_oeg/test-445.json")

    def test_issue_567(self):
        """Checks that an image file called ACKNOWLEDGEMENTS is not recognized as ACK.
        Motivated by https://github.com/KnowledgeCaptureAndDiscovery/somef/issues/567
        """
        out_file = "repositories/software_catalog/test-567.json"
        somef_cli.run_cli(threshold=0.9,
                          ignore_classifiers=False,
                          repo_url=None,
                          doc_src=None,
                          local_repo=test_data_repositories + "software_catalog",
                          in_file=None,
                          output=test_data_path + out_file,
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + out_file, "r")
        data = text_file.read()
        json_content = json.loads(data)
        text_file.close()
        assert constants.CAT_ACKNOWLEDGEMENT not in json_content
        os.remove(test_data_path + "repositories/software_catalog/test-567.json")

    def test_categorization(self):
        """Checks that the categorization is done properly"""
        somef_cli.run_cli(threshold=0.6,
                          ignore_classifiers=False,
                          repo_url="https://github.com/oeg-upm/devops-infra",
                          doc_src=None,
                          local_repo=None,
                          in_file=None,
                          output=test_data_path + "repositories/repos_oeg/test-category.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=False)
        text_file = open(test_data_path + "repositories/repos_oeg/test-category.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        repo_status = json_content[constants.CAT_TYPE][0]
        print(repo_status)
        repo_type = repo_status[constants.PROP_RESULT][constants.PROP_VALUE]
        print(repo_type)
        assert repo_type == "ontology"
        os.remove(test_data_path + "repositories/repos_oeg/test-category.json")

    def test_redundant_files(self):
        """
        This test checks if the redundant files for the repository TEC-Toolkit/CFO work correctly.
        An error was detected in this repo
        """
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/Tec-Toolkit/ECFO",
                          local_repo=None,
                          doc_src=None,
                          in_file=None,
                          output=test_data_path + "test-ecfo.json",
                          graph_out=None,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=True,
                          readme_only=False)
        text_file = open(test_data_path + "test-ecfo.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        t = json_content[constants.CAT_TYPE][0]
        assert t[constants.PROP_RESULT][constants.PROP_VALUE] == "ontology"
        os.remove(test_data_path + "test-ecfo.json")
