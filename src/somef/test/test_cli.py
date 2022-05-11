import json
import os
import unittest
import validators
from pathlib import Path
from somef import cli
from somef import parser_somef

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

    def test_issue_311(self):
        """Checks if codemeta export has labels defined outside codemeta"""
        cli.run_cli(threshold=0.8,
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

    def test_issue_281(self):
        """Checks if missing categories are properly added to the output JSON, when required"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("missingCategories") > 0
        os.remove(test_data_path + "test-281.json")

    def test_issue_200(self):
        """Tests if the hierarchical representation of headers is properly stored in the output"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("parentHeader") > 0
        os.remove(test_data_path + "test-200.json")

    def test_issue_343(self):
        """Assesses problems with the parser"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("parentHeader") > 0
        os.remove(test_data_path + "test-343.json")

    def test_issue_355(self):
        """Checks somef failures against specific repositories"""
        cli.run_cli(threshold=0.8,
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
        print(data)
        text_file.close()
        assert data.find("longTitle") > 0
        os.remove(test_data_path + "repositories/repos_oeg/test-355.json")

    def test_issue_150(self):
        """Codemeta export checks"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("acknowledgement") == -1
        os.remove(test_data_path + "test-150.json-ld")

    def test_issue_346(self):
        """Checks if acks are properly detected"""
        cli.run_cli(threshold=0.8,
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
        cli.run_cli(threshold=0.8,
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
        assert data.find("packageDistribution") > 0
        os.remove(test_data_path + "test-241.json")

    def test_issue_380(self):
        """Checks if parser works well against level 3 and 4 headers"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("installation") > 0
        os.remove(test_data_path + "test-380.json")

    def test_issue_379(self):
        """ Checks if a target readme works (it caused duplicate excerpts)"""
        cli.run_cli(threshold=0.8,
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
        description = json_content['description']
        assert len(description) > 0
        os.remove(test_data_path + "test-379.json")

    def test_issue_383(self):
        """Checks if the section `Contact` can be properly parsed"""
        cli.run_cli(threshold=0.8,
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
        cli.run_cli(threshold=0.8,
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
        cli.run_cli(threshold=0.8,
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
        installation = json_content['installation']
        assert_true = False
        for install in installation:
            if 'parentHeader' in install.keys():
                if install['originalHeader'] == "Hard way" and "Installation" in install['parentHeader']:
                    assert_true = True
        assert assert_true
        os.remove(test_data_path + "test-378.json")

    def test_issue_378_2(self):
        """Checks classification of a header based on what was written in upper level headers"""
        cli.run_cli(threshold=0.8,
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
        installation = json_content['installation']
        assert_true = False
        for install in installation:
            if 'parentHeader' in install.keys():
                if install['originalHeader'] == "Easy way" and "Installation" in install['parentHeader'] \
                        and "easytv-annotator" in install["parentHeader"]:
                    assert_true = True
        assert assert_true
        os.remove(test_data_path + "test-378-2.json")

    def test_issue_260(self):
        """Checks if colab notebooks are detected"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("executableExample") > 0
        os.remove(test_data_path + "test-260.json")

    def test_issue_319_1(self):
        """Check if citation file format is recognized and returned"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("citation file format") > 0
        os.remove(test_data_path + "test-319-1.json")

    def test_issue_388(self):
        """Test checks that ontologies are recognized appropriately"""
        cli.run_cli(threshold=0.8,
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
        assert len(json_content["ontologies"]["excerpt"]) == 1
        os.remove(test_data_path + "test-388.json")

    def test_issue_319_2(self):
        """Test checks that the output format of citation files is specified in the output"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("jupyter notebook") > 0
        os.remove(test_data_path + "test-319-2.json")

    def test_issue_385(self):
        """More checks based on parent headers"""
        cli.run_cli(threshold=0.8,
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
        usage = json_content['usage']
        assert len(usage) == 3
        os.remove(test_data_path + "test-385.json")

    def test_issue_398(self):
        """Checks that repostatus has confidence (always 1.0)"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/dgarijo/Widoco",
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
        repo_status = json_content['repoStatus']
        confidence = repo_status['confidence']
        assert len(confidence) == 1
        os.remove(test_data_path + "test-398.json")

    def test_issue_393(self):
        """Checks that if a folder within a repository is passed to the tool, it does not break"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/oeg-upm/wot-hive/tree/main/docker/auroral-hive",
                    doc_src=None,
                    in_file=None,
                    output=test_data_path + "test-393.json",
                    graph_out=None,
                    graph_format="turtle",
                    codemeta_out=None,
                    pretty=True,
                    missing=True)
        text_file = open(test_data_path + "test-393.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        acknowledgement = json_content['acknowledgement']
        assert acknowledgement is not None
        os.remove(test_data_path + "test-393.json")

    def test_issue_314(self):
        """Checks that the program can be run using only a single readme"""
        cli.run_cli(threshold=0.8,
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
        acknowledgement = json_content['acknowledgement']
        assert acknowledgement is not None
        os.remove(test_data_path + "test-314.json")

    def test_issue_314_1(self):
        """Checks that the program can be run using only a single readme. GitHub"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/tensorflow/tensorflow/tree/v2.6.0",
                    doc_src=None,
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
        image = json_content['image']
        assert image is not None
        os.remove(test_data_path + "test-314-1.json")

    def test_issue_314_2(self):
        """Checks that the program can be run using only a single readme. Gitlab"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://gitlab.com/jleblay/tokei",
                    doc_src=None,
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
        description = json_content['description']
        assert description is not None
        os.remove(test_data_path + "test-314-2.json")

    def test_issue_314_3(self):
        """Checks that the program can be run using only a single readme. Gitlab"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://gitlab.com/unboundedsystems/adapt/-/tree/release-0.1",
                    doc_src=None,
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
        description = json_content['description']
        assert description is not None
        os.remove(test_data_path + "test-314-3.json")

    def test_issue_403(self):
        """Checks that the readme returned by somef is correct"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/oeg-upm/wot-hive",
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
        readme_url = json_content['readmeUrl']
        excerpt = readme_url['excerpt']
        assert excerpt == 'https://raw.githubusercontent.com/oeg-upm/wot-hive/main/README.md'
        os.remove(test_data_path + "test-403.json")

    def test_issue_408(self):
        """Checks that the documentation links (docs) are properly found"""
        cli.run_cli(threshold=0.8,
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

    def test_issue_408_1(self):
        """Checks that the documentation links (docs) are properly found"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/oeg-upm/bimerr-epw/",
                    local_repo=None,
                    doc_src=None,
                    in_file=None,
                    output=test_data_path + "test-408-1.json",
                    graph_out=None,
                    graph_format="turtle",
                    codemeta_out=None,
                    pretty=True,
                    missing=True,
                    readme_only=False)
        text_file = open(test_data_path + "test-408-1.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find(
            "https://github.com/oeg-upm/bimerr-epw/tree/master/Code/TDATA2RDFANDV/static/rest_framework/docs") == -1
        os.remove(test_data_path + "test-408-1.json")

    def test_issue_225_406(self):
        """Checks if wiki links are detected"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("\"type\": \"wiki\"")
        os.remove(test_data_path + "test-225.json")

    def test_issue_406(self):
        """Test that checks whether the extracted elements in the documentation have a type"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("\"type\": \"readthedocs\"")
        os.remove(test_data_path + "test-406.json")

    def test_issue_255(self):
        """Tests if somef can detect wiki articles"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/mbloch/mapshaper/",
                    local_repo=None,
                    doc_src=None,
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
        """Tests if somef can detect wiki articles"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/PyLops/pylops/",
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
        assert data.find("https://github.com/PyLops/pylops/wiki") == -1
        os.remove(test_data_path + "test-255-1.json")

    def test_issue_375(self):
        """Checks that svg badges are not captured as images"""
        cli.run_cli(threshold=0.8,
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
        cli.run_cli(threshold=0.8,
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
        cli.run_cli(threshold=0.8,
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
        cli.run_cli(threshold=0.8,
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
        assert data.find("description") >= 0
        os.remove(test_data_path + "test-353.json")

    def test_issue_366(self):
        """Checks if somef can detect Docker compose files"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("Docker file") >= 0
        os.remove(test_data_path + "test-366.json")

    def test_issue_417(self):
        """Checks for different codemeta errors"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/dgarijo/Widoco",
                    local_repo=None,
                    doc_src=None,
                    in_file=None,
                    output=None,
                    graph_out=None,
                    graph_format="turtle",
                    codemeta_out=test_data_path + "test-417.json-ld",
                    pretty=True,
                    missing=True,
                    readme_only=False)
        text_file = open(test_data_path + "test-417.json-ld", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        issue_tracker = json_content['issueTracker']
        assert issue_tracker == 'https://api.github.com/repos/dgarijo/Widoco/issues'
        os.remove(test_data_path + "test-417.json-ld")

    def test_issue_382(self):
        """Checks a given github repo works fine (contact section)"""
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/oeg-upm/mapeathor",
                    local_repo=None,
                    doc_src=None,
                    in_file=None,
                    output=test_data_path + "test-382.json",
                    graph_out=None,
                    graph_format="turtle",
                    codemeta_out=None,
                    pretty=True,
                    missing=True,
                    readme_only=False)
        text_file = open(test_data_path + "test-382.json", "r")
        data = text_file.read()
        text_file.close()
        json_content = json.loads(data)
        contact = json_content['contact']
        assert contact is not None
        os.remove(test_data_path + "test-382.json")

    def test_issue_428(self):
        """Checks a given github repo works fine (contact section)"""
        cli.run_cli(threshold=0.8,
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
        assert data.find("Manim is an engine for precise programmatic animations, designed for creating explanatory math videos.") > 0
        os.remove(test_data_path + "test-428.json")

    def test_issue_443(self):
        cli.run_cli(threshold=0.8,
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
        installation = json_content['installation']
        assert installation is not None
        os.remove(test_data_path + "test-443.json")

    def test_issue_443_2(self):
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url="https://github.com/oeg-upm/awesome-semantic-web",
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
        installation = json_content['installation']
        assert installation is not None
        os.remove(test_data_path + "test-443.json")

    def test_issue_443_3(self):
        cli.run_cli(threshold=0.8,
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
        description = json_content['description']
        assert description is not None
        os.remove(test_data_path + "test-443.json")

    def test_issue_457(self):
        cli.run_cli(threshold=0.8,
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
        description = json_content['description']
        assert description is not None
        os.remove(test_data_path + "test-457.json")