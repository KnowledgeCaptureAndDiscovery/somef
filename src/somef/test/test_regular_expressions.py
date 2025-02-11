import unittest
import os
from pathlib import Path

from .. import regular_expressions
from ..process_results import Result
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestRegExp(unittest.TestCase):

    def test_extract_bibtex(self):
        """Test designed to check if bibtext citations are detected"""
        with open(test_data_path + "test_extract_bibtex.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_bibtex(test_text, Result(), test_data_path + "test_extract_bibtex.txt")
            result = c.results[constants.CAT_CITATION][0]
            assert "@inproceedings" in result["result"]["value"]

    def test_issue_553(self):
        """
        Test designed to check if a bibtex and the corresponding DOI with a repository that was problematic
        Source: https://github.com/KnowledgeCaptureAndDiscovery/somef/issues/553
        """
        with open(test_data_path + "README-devilog.md", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_bibtex(test_text, Result(), test_data_path + "test_extract_bibtex1.txt")
            result = c.results[constants.CAT_CITATION][0]
            doi = result["result"]["doi"]
            assert "@inproceedings" in result["result"]["value"] and doi == "10.1109/ICECCME55909.2022.9988605"

    def test_issue_553_2(self):
        """
        Test designed to check if a bibtex and the corresponding DOI with a repository that was problematic
        In this case, a quote block is not used. Instead, curly brackets are used with multiple levels of nesting
        """
        with open(test_data_path + "README-GENI.md", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_bibtex(test_text, Result(), test_data_path + "test_extract_bibtex2.txt")
            result = c.results[constants.CAT_CITATION][0]
            assert "@article" in result["result"]["value"]

    def test_extract_dois(self):
        """Test designed to check if doi links are detected"""
        with open(test_data_path + "test_extract_dois.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_doi_badges(test_text, Result(), test_data_path + "test_extract_dois.txt")
            assert len(c.results[constants.CAT_IDENTIFIER]) == 2

    def test_extract_binder_links(self):
        """Test designed to check if binder links are detected"""
        with open(test_data_path + "test_extract_binder_links.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_binder_links(test_text, Result(),
                                                         test_data_path + "test_extract_binder_links.txt")
            assert len(c.results[constants.CAT_EXECUTABLE_EXAMPLE]) == 2

    def test_extract_title_underline(self):
        """Test designed to check if titles with underline markdown notation are detected"""
        with open(test_data_path + "test_extract_title_underline.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text, Result(),
                                                  test_data_path + "test_extract_title_underline.txt")
            res = c.results[constants.CAT_FULL_TITLE][0]
            assert "Taguette" == res[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_title_hash(self):
        """Test designed to check if titles with hash notation are detected"""
        with open(test_data_path + "test_extract_title_hash.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text, Result(), test_data_path + "test_extract_title_hash.txt")
            res = c.results[constants.CAT_FULL_TITLE][0]
            assert "T2WML: A Cell-Based Language To Map Tables Into Wikidata Records" == res[constants.PROP_RESULT][
                constants.PROP_VALUE]

    def test_extract_title_with_md(self):
        """Test designed to check if titles are detected"""
        with open(test_data_path + "test_extract_title_with_md.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text, Result(),
                                                  test_data_path + "test_extract_title_with_md.txt")
            res = c.results[constants.CAT_FULL_TITLE][0]
            assert "SOMEF" == res[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_readthedocs_1(self):
        """Test designed to check if readthedocs links are detected"""
        with open(test_data_path + "test_extract_readthedocs_1.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_readthedocs(test_text, Result(),
                                                        test_data_path + "test_extract_readthedocs_1.txt")
            result = c.results[constants.CAT_DOCUMENTATION][0]
            assert "https://oba.readthedocs.io/" == result[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_readthedocs_1_1(self):
        """Test to check if a result is added with a different name, then it gets added as a related link"""
        with open(test_data_path + "test_extract_readthedocs_1.txt", "r") as data_file:
            test_text = data_file.read()
            r = Result()
            r.add_result(constants.CAT_NAME, {
                constants.PROP_TYPE: constants.STRING,
                constants.PROP_VALUE: "unrelated"
            }, 1, test_data_path + "test_extract_readthedocs_1.txt")
            c = regular_expressions.extract_readthedocs(test_text, r, test_data_path + "test_extract_readthedocs_1.txt")
            result = c.results[constants.CAT_RELATED_DOCUMENTATION][0]
            assert "https://oba.readthedocs.io/" == result[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_readthedocs_2(self):
        """Test designed to check if readthedocs links are detected"""
        with open(test_data_path + "test_extract_readthedocs_2.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_readthedocs(test_text, Result(),
                                                        test_data_path + "test_extract_readthedocs_2.txt")
            result = c.results[constants.CAT_DOCUMENTATION][0]
            assert "https://kgtk.readthedocs.io/" == result[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_readthedocs_3(self):
        """Test designed to check if readthedoc links are detected"""
        test_text = """
        See full documentation at [https://somef.readthedocs.io/en/latest/](https://somef.readthedocs.io/en/latest/)
        """
        c = regular_expressions.extract_readthedocs(test_text, Result(), test_data_path + "invented_path.txt")
        result = c.results[constants.CAT_DOCUMENTATION][0]
        assert "https://somef.readthedocs.io/" == result[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_readthedocs_issue_407(self):
        """Test designed to check if readthedocs links are detected"""
        with open(test_data_path + "test_extract_readthedocs_3.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_readthedocs(test_text, Result(),
                                                        test_data_path + "test_extract_readthedocs_3.txt")
            result = c.results[constants.CAT_DOCUMENTATION][0]
            assert "https://owl-to-oas.readthedocs.io/" == result[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_gitter_chat(self):
        """Test designed to check if gitter chats are detected"""
        with open(test_data_path + "test_extract_gitter_chat.txt", "r") as data_file:
            test_text = data_file.read()
            channels = regular_expressions.extract_support_channels(test_text, Result(),
                                                                    test_data_path + "test_extract_gitter_chat.txt")
            result = channels.results[constants.CAT_SUPPORT_CHANNELS]
            assert "https://gitter.im/OpenGeoscience/geonotebook" == result[0][constants.PROP_RESULT][
                constants.PROP_VALUE]

    def test_repo_status(self):
        """Test designed to check if repostatus badges are detected"""
        with open(test_data_path + "test_repo_status.txt", "r") as data_file:
            test_text = data_file.read()
            repo_status = regular_expressions.extract_repo_status(test_text, Result(),
                                                                  test_data_path + "test_repo_status.txt")
            result = repo_status.results[constants.CAT_STATUS]
            assert len(result) > 0 and result[0][constants.PROP_RESULT][
                constants.PROP_VALUE] == "https://www.repostatus.org/#active"

    def test_issue_291(self):
        """Test designed to check if logos are detected"""
        repo_url = "https://github.com/dgarijo/Widoco"
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, repo_url, None, Result(),
                                                         test_data_path + "README-widoco.md", "master")
            logo = results.results[constants.CAT_LOGO]
            assert (logo[0][constants.PROP_RESULT][
                        constants.PROP_VALUE] == "https://raw.githubusercontent.com/dgarijo/Widoco/master/src/main/resources/logo/logo2.png")

    def test_issue_291_2(self):
        """Test designed to check if logos are detected"""
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_logo_uscisii2.txt", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, repo_url, None, Result(),
                                                         test_data_path + "test_logo_uscisii2.txt", "master")
            logo = results.results[constants.CAT_LOGO]
            assert (logo[0][constants.PROP_RESULT][
                        constants.PROP_VALUE] == "https://github.com/usc-isi-i2/kgtk/raw/master/docs/images/kgtk_logo_200x200.png")

    def test_issue_291_3(self):
        """Test designed to check if logos are detected"""
        repo_url = "https://github.com/tensorflow/tensorflow/"
        with open(test_data_path + "test_logo_tensorflow.txt", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, repo_url, None, Result(),
                                                         test_data_path + "test_logo_tensorflow.txt", "main")
            logo = results.results[constants.CAT_LOGO]
            assert (logo[0][constants.PROP_RESULT][
                        constants.PROP_VALUE] == "https://www.tensorflow.org/images/tf_logo_horizontal.png")

    def test_issue_images(self):
        """Test designed to check if images are detected"""
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_issue_images.txt", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, repo_url, None, Result(),
                                                         test_data_path + "test_issue_images.txt", "main")
            img = results.results[constants.CAT_IMAGE]
            print(img)
            assert len(img) == 2

    #Test commented out because arxiv links with no context has demonstrated not to be useful
    def test_issue_181(self):
        """Test designed to check if arxiv papers are detected"""
        with open(test_data_path + "test_issue_181.txt", "r") as data_file:
            test_text = data_file.read()
            result = regular_expressions.extract_arxiv_links(test_text, Result(), test_data_path + "test_issue_181.txt")
            arxiv_urls = result.results[constants.CAT_RELATED_PAPERS]
            assert len(arxiv_urls) > 0
    def test_issue_181_2(self):
        """Test designed to check if arxiv papers are detected"""
        with open(test_data_path + "test_issue_181_2.txt", "r") as data_file:
            test_text = data_file.read()
            result = regular_expressions.extract_arxiv_links(test_text, Result(), test_data_path + "test_issue_181_2.txt")
            arxiv_url = result.results[constants.CAT_RELATED_PAPERS][0]['result']['value']
            expected_result = "https://arxiv.org/abs/2203.01044"
            self.assertEquals(expected_result,arxiv_url)
    def test_issue_181_3(self):
        """Test to test arxiv as embedded url, including same in bibtex"""
        with open(test_data_path + "test_issue_181_3.txt", "r") as data_file:
            test_text = data_file.read()
            result = regular_expressions.extract_arxiv_links(test_text, Result(),
                                                             test_data_path + "test_issue_181_3.txt")
            arxiv_url = result.results[constants.CAT_RELATED_PAPERS][0]['result']['value']
            expected_result = "https://arxiv.org/abs/1907.11111"
            self.assertEquals(expected_result, arxiv_url)

    def test_issue_270(self):
        """Test designed to check if support channels are detected"""
        with open(test_data_path + "test_issue_270.txt", "r") as data_file:
            test_text = data_file.read()
            support_channels = regular_expressions.extract_support_channels(test_text, Result(),
                                                                            test_data_path + "test_issue_270.txt")
            assert len(support_channels.results[constants.CAT_SUPPORT_CHANNELS]) == 2

    def test_logo(self):
        """Test designed to check if logos are detected"""
        with open(test_data_path + "test_logo.txt", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/Chowlk", None, Result(),
                                                         test_data_path + "test_logo.txt", "master")
            logo = results.results[constants.CAT_LOGO]
            assert (logo[0][constants.PROP_RESULT][
                        constants.PROP_VALUE] == "https://raw.githubusercontent.com/oeg-upm/Chowlk/webservice/resources/logo.png")

    def test_logo2(self):
        """Test designed to check if logos are detected"""
        with open(test_data_path + "test_logo2.txt", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/pytorch/pytorch", None, Result(),
                                                         test_data_path + "test_logo2.txt", "master")
            logo = results.results[constants.CAT_LOGO]
            assert (logo[0][constants.PROP_RESULT][
                        constants.PROP_VALUE] == "https://raw.githubusercontent.com/pytorch/pytorch/master/docs/source/_static/img/pytorch-logo-dark.png")

    def test_images(self):
        """Test designed to check if images are detected"""
        with open(test_data_path + "test_images.txt", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/pytorch/pytorch", None, Result(),
                                                         test_data_path + "test_images.txt", "master")
            images = results.results[constants.CAT_IMAGE]
            assert len(images) > 0

    def test_issue_320(self):
        """Test designed to check if logos are detected"""
        with open(test_data_path + "README-urllib3.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/urllib3/urllib3", None, Result(),
                                                         test_data_path + "README-urllib3.md", "master")
            logo = results.results[constants.CAT_LOGO]
            assert len(logo) > 0

    def test_issue_337(self):
        """Test designed to check if links are removed from the text sent to classifiers"""
        text = """## Interactive web interface

Visit the public website at [www.mapshaper.org](http://www.mapshaper.org) or use the web UI locally via the `mapshaper-gui` script. 

All processing is done in the browser, so your data stays private, even when using the public website.

The web UI works in recent desktop versions of Chrome, Firefox, Safari and Internet Explorer. Safari before v10.1 and IE before v10 are not supported.

        """
        text = regular_expressions.remove_links_images(text)
        assert text.find("[www.mapshaper.org](http://www.mapshaper.org)") == -1

    def test_issue_427(self):
        with open(test_data_repositories + "Widoco" + os.path.sep + "README.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, None, test_data_repositories + "Widoco", Result(),
                                                         test_data_repositories + "Widoco" + os.path.sep + "README.md",
                                                         "master")
            logo = results.results[constants.CAT_LOGO]
            assert (logo[0][constants.PROP_RESULT][constants.PROP_VALUE].find('test_data') > 0)

    def test_issue_446(self):
        """Test that jitpack URLs are not returned"""
        with open(test_data_path + "README-licensius.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/licensius/", None, Result(),
                                                         test_data_repositories + "Widoco" + os.path.sep + "README.md",
                                                         "master")
            logo_results = results.results
            assert (constants.CAT_LOGO not in logo_results.keys())

    def test_issue_446_1(self):
        """Test that jitpack URLs are not returned"""
        with open(test_data_path + "README-PPool.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/PPool/", None, Result(),
                                                         test_data_path + "README-PPool.md", "master")
            all_results = results.results
            assert (constants.CAT_LOGO not in all_results.keys() and constants.CAT_IMAGE not in all_results.keys())

    def test_issue_446_2(self):
        """Test that jitpack URLs are not returned"""
        with open(test_data_path + "README-loupe-api.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/PPool/", None, Result(),
                                                         test_data_path + "README-loupe-api.md", "master")
            all_results = results.results
            assert (constants.CAT_LOGO not in all_results.keys() and len(all_results[constants.CAT_IMAGE]) == 1)

    def test_issue_467(self):
        """Test designed to check if logo is correctly obtained"""
        with open(test_data_path + "README-wothive.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/wot-hive/", None, Result(),
                                                         test_data_path + "README-wothive.md", "master")
            logo_results = results.results[constants.CAT_LOGO]
            assert logo_results[0][constants.PROP_RESULT][constants.PROP_VALUE] == \
                   "https://raw.githubusercontent.com/oeg-upm/wot-hive/AndreaCimminoArriaga-wothive-logo/logo.png"

    def test_issue_463(self):
        """Test designed to check if a repo with a badge but not logo is correctly ignored"""
        with open(test_data_path + "README-OBA-SPARQL.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text,
                                                              "https://github.com/KnowledgeCaptureAndDiscovery/OBA_sparql/",
                                                              None, Result(), test_data_path + "README-OBA-SPARQL.md", "master")
            all_results = results.results
            assert constants.CAT_LOGO not in all_results.keys()

    def test_issue_463_2(self):
        """Test designed to check if a repo with a badge but not logo is correctly ignored"""
        with open(test_data_path + "README-base-images.md", "r") as data_file:
            test_text = data_file.read()
            results = regular_expressions.extract_images(test_text, "https://github.com/mintproject/base_images",
                                                              None, Result(), test_data_path + "README-base-images.md", "master")
            all_results = results.results
            assert constants.CAT_LOGO not in all_results.keys()

    def test_wiki(self):
        """Test designed to check if a repository with wiki links retrieves the wiki links as documentation"""
        with open(test_data_path + "test_wiki.md", "r") as data_file:
            test_text = data_file.read()
            repo_status = regular_expressions.extract_wiki_links(test_text, "https://github.com/oeg-upm/mapeathor",
                                                                 Result(), test_data_path + "test_wiki.md")
            result = repo_status.results[constants.CAT_DOCUMENTATION]
            assert len(result) > 0 and result[0][constants.PROP_RESULT][
                constants.PROP_VALUE] == "https://github.com/oeg-upm/Mapeathor/wiki"

    def test_package_distribution(self):
        """Test designed to check if a repository with pypi links is properly recovered"""
        with open(test_data_path + "README-mapeathor.md", "r") as data_file:
            test_text = data_file.read()
            repo_status = regular_expressions.extract_package_distributions(test_text, Result(),
                                                                            test_data_path + "README-mapeathor.md")
            result = repo_status.results[constants.CAT_PACKAGE_DISTRIBUTION]
            assert len(result) > 0 and result[0][constants.PROP_RESULT][
                constants.PROP_VALUE] == "https://pypi.org/project/mapeathor/"

    def test_package_distribution_2(self):
        """Test designed to check if a repository with pypi links is properly recovered"""
        with open(test_data_path + "test_pypi.md", "r") as data_file:
            test_text = data_file.read()
            repo_status = regular_expressions.extract_package_distributions(test_text, Result(),
                                                                            test_data_path + "test_pypi.md")
            result = repo_status.results[constants.CAT_PACKAGE_DISTRIBUTION]
            assert len(result) > 0 and "https://pypi.org/project/inspect4py" in result[0][constants.PROP_RESULT][
                constants.PROP_VALUE]
            
    def test_issue_700(self):
        """Test designed to check empty value should not lead to a category in title """
        with open(test_data_path + "README-ci-sample-project.md", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text, Result(),
                                                  test_data_path + "README-ci-sample-project.md")

            assert constants.CAT_FULL_TITLE not in c.results, "Category CAT_FULL_TITLE should be absent if there is no valid title."