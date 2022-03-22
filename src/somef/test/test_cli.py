import unittest

import os
from somef.cli import *

test_data_path = "test_data/"
test_data_repositories = "test_data/repositories/"


class TestCli(unittest.TestCase):

    def test_extract_bibtex(self):
        with open(test_data_path + "test_extract_bibtex.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_bibtex(test_text)
            assert "@inproceedings" in c[0]

    def test_extract_dois(self):
        with open(test_data_path + "test_extract_dois.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_dois(test_text)
            assert len(c) == 2

    def test_extract_binder_links(self):
        with open(test_data_path + "test_extract_binder_links.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_binder_links(test_text)
            assert len(c) == 2

    def test_extract_title_underline(self):
        with open(test_data_path + "test_extract_title_underline.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_title(test_text)
            assert "Taguette" == c

    def test_extract_title_hash(self):
        with open(test_data_path + "test_extract_title_hash.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_title(test_text)
            assert "T2WML: A Cell-Based Language To Map Tables Into Wikidata Records" == c

    def test_extract_title_with_md(self):
        with open(test_data_path + "test_extract_title_with_md.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_title(test_text)
            # print(c)
            assert "SOMEF" == c

    def test_extract_readthedocs_1(self):
        with open(test_data_path + "test_extract_readthedocs_1.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_readthedocs(test_text)
            assert ["https://oba.readthedocs.io/"] == c

    def test_extract_readthedocs_2(self):
        with open(test_data_path + "test_extract_readthedocs_2.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_readthedocs(test_text)
            # print(c)
            assert ["https://kgtk.readthedocs.io/"] == c

    def test_extract_readthedocs_3(self):
        test_text = """
        See full documentation at [https://somef.readthedocs.io/en/latest/](https://somef.readthedocs.io/en/latest/)
        """
        c = extract_readthedocs(test_text)
        print(c)
        assert ["https://somef.readthedocs.io/"] == c

    def test_extract_gitter_chat(self):
        with open(test_data_path + "test_extract_gitter_chat.txt", "r") as data_file:
            test_text = data_file.read()
            c = extract_support_channels(test_text)
            # print(c)
            assert "https://gitter.im/OpenGeoscience/geonotebook" in c

    # This repo does no longer have a file with ACK.
    # def test_issue_166(self):
    #     header = {}
    #     header['accept'] = 'application/vnd.github.v3+json'
    #     text, github_data = load_repository_metadata("https://github.com/tensorflow/tensorflow/tree/v2.6.0", header)
    #     assert len(github_data['acknowledgments']) > 0

    def test_repo_status(self):
        with open(test_data_path + "test_repo_status.txt", "r") as data_file:
            test_text = data_file.read()
            repo_status = extract_repo_status(test_text)
            assert len(repo_status) > 0

    # This issue should be changed to making a snapshot of the zip file
    def test_issue_171(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "rdflib-6.0.2")
        assert len(github_data['contributors']) > 0

    # This issue should be changed to making a snapshot of the zip file
    def test_issue_209(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "rdflib-6.0.2")
        assert len(github_data['hasScriptFile']) > 0

    def test_issue_181(self):
        with open(test_data_path + "test_issue_181.txt", "r") as data_file:
            test_text = data_file.read()
            arxiv_links = extract_arxiv_links(test_text)
            assert len(arxiv_links) > 0

    # This issue should be changed to making a snapshot of the zip file
    def test_issue_211(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "probot-12.1.1")
        assert len(github_data['contributingGuidelines']) > 0 and ('license' in github_data.keys() or 'licenseText' in github_data.keys())

    # This issue should be changed to making a snapshot of the zip file
    def test_issue_218(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "captum")
        assert len(github_data['citation']) > 0

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

    # This issue should be changed to making a snapshot of the zip file
    def test_issue_268(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "probot-12.1.1")
        assert len(github_data['licenseText']) > 0

    # Commenting this issue: this repo does no longer have an ACK file
    # def test_issue_210(self):
    #     from somef import cli
    #     cli.run_cli(threshold=0.8,
    #                 ignore_classifiers=False,
    #                 repo_url="https://github.com/tensorflow/tensorflow/tree/v2.6.0",
    #                 doc_src=None,
    #                 in_file=None,
    #                 output=None,
    #                 graph_out=None,
    #                 graph_format="turtle",
    #                 codemeta_out="test-tensorflow-2.6.0.json-ld",
    #                 pretty=True,
    #                 missing=False)
    #     text_file = open("test-tensorflow-2.6.0.json-ld", "r")
    #     data = text_file.read()
    #     text_file.close()
    #     assert data.find("\"acknowledgments\":") >= 0

    def test_issue_286(self):
        header = {'accept': 'application/vnd.github.v3+json'}
        text, github_data = load_repository_metadata("https://gitlab.com/gitlab-org/ci-sample-projects/platform-team",
                                                     header)
        assert len(github_data['downloadUrl']) > 0

    def test_issue_291(self):
        repo_url = "https://github.com/dgarijo/Widoco"
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, repo_url)
            assert (not logo == "")

    def test_issue_291_2(self):
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_logo_uscisii2.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, repo_url)
            assert (not logo == "")

    def test_issue_291_3(self):
        repo_url = "https://github.com/tensorflow/tensorflow/"
        with open(test_data_path + "test_logo_tensorflow.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, repo_url)
            assert (not logo == "")

    def test_issue_images(self):
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_issue_images.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, repo_url)
            assert len(images) > 0

    def test_issue_285(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "RDFChess")
        assert ('license' not in github_data) == True

    def test_issue_no_readme(self):
        header = {'accept': 'application/vnd.github.v3+json'}
        text, github_data = load_repository_metadata("https://github.com/oeg-upm/OpenRefineExtension_Transformation",                                                     header)
        assert ('codeRepository' in github_data) == True

    def test_issue_270(self):
        with open(test_data_path + "test_issue_270.txt", "r") as data_file:
            test_text = data_file.read()
            support_channels = extract_support_channels(test_text)
            assert len(support_channels) == 2

    def test_issue_311(self):
        run_cli(threshold=0.8,
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

    def test_issue_284_issue_272(self):
        header = {'accept': 'application/vnd.github.v3+json'}
        text, github_data = load_repository_metadata("https://github.com/3b1b/manim", header)
        assert (('stargazersCount' in github_data) == True) and (('longTitle' in github_data) == False)

    # Merging with previous issue to avoid multiple requests.
    # def test_issue_272(self):
    #     header = {'accept': 'application/vnd.github.v3+json'}
    #     text, github_data = load_repository_metadata("https://github.com/3b1b/manim", header)
    #     assert ('longTitle' in github_data) == False

    def test_issue_281(self):
        run_cli(threshold=0.8,
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

    def test_logo(self):
        with open(test_data_path + "test_logo.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, "https://github.com/oeg-upm/Chowlk")
            assert (not logo == "")

    def test_logo2(self):
        with open(test_data_path + "test_logo2.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, "https://github.com/pytorch/pytorch")
            assert (not logo == "")

    def test_images(self):
        with open(test_data_path + "test_images.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, "https://github.com/pytorch/pytorch")
            assert (len(images) > 0 and not logo == "")

    def test_issue_200(self):
        run_cli(threshold=0.8,
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
        run_cli(threshold=0.8,
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

    def test_issue_285(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "repos-oeg/cogito-kgg-module")
        assert ('license' not in github_data) == True

    def test_issue_355(self):
        run_cli(threshold=0.8,
                ignore_classifiers=False,
                repo_url=None,
                doc_src=None,
                local_repo=test_data_path + "repositories/repos_oeg/bimerr-core",
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
        #os.remove(test_data_path + "repositories/repos_oeg/test-355.json")

    def test_no_repository_metadata(self):
        credentials_file = Path(
            os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
        ).expanduser()
        if credentials_file.exists():
            with credentials_file.open("r") as fh:
                file_paths = json.load(fh)
        else:
            sys.exit("Error: Please provide a config.json file.")
        header = {}
        if 'Authorization' in file_paths.keys():
            header['Authorization'] = file_paths['Authorization']
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/RDFLib/rdflib/tree/6.0.2", header, True)
        assert ('releases' not in github_data) == True

    def test_issue_150(self):
        run_cli(threshold=0.8,
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
        run_cli(threshold=0.8,
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
        run_cli(threshold=0.8,
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

    def test_issue_320(self):
        with open(test_data_path + "README-urllib3.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = extract_images(test_text, "https://github.com/urllib3/urllib3")
            assert (not logo == "")

    def test_issue_361(self):
        text, github_data = load_local_repository_metadata(test_data_repositories + "rdflib-6.0.2")
        assert len(text) > 0

    def test_issue_380(self):
        run_cli(threshold=0.8,
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
        run_cli(threshold=0.8,
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
        run_cli(threshold=0.8,
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
        run_cli(threshold=0.8,
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
        run_cli(threshold=0.8,
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
                if install['originalHeader'] == "Hard way" and install['parentHeader'] == "Installation":
                    assert_true = True
        assert assert_true
        os.remove(test_data_path + "test-378.json")