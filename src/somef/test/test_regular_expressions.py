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
            c = regular_expressions.extract_binder_links(test_text, Result(), test_data_path + "test_extract_binder_links.txt")
            assert len(c.results[constants.CAT_EXECUTABLE_EXAMPLE]) == 2

    def test_extract_title_underline(self):
        """Test designed to check if titles with underline markdown notation are detected"""
        with open(test_data_path + "test_extract_title_underline.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text, Result(), test_data_path + "test_extract_title_underline.txt")
            res = c.results[constants.CAT_FULL_TITLE][0]
            assert "Taguette" == res[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_title_hash(self):
        """Test designed to check if titles with hash notation are detected"""
        with open(test_data_path + "test_extract_title_hash.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text, Result(), test_data_path +"test_extract_title_hash.txt")
            res = c.results[constants.CAT_FULL_TITLE][0]
            assert "T2WML: A Cell-Based Language To Map Tables Into Wikidata Records" == res[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_title_with_md(self):
        """Test designed to check if titles are detected"""
        with open(test_data_path + "test_extract_title_with_md.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text, Result(), test_data_path + "test_extract_title_with_md.txt")
            res = c.results[constants.CAT_FULL_TITLE][0]
            assert "SOMEF" == res[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_readthedocs_1(self):
        """Test designed to check if readthedocs links are detected"""
        with open(test_data_path + "test_extract_readthedocs_1.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_readthedocs(test_text, Result(), test_data_path + "test_extract_readthedocs_1.txt")
            result = c.results[constants.CAT_DOCUMENTATION][0]
            assert "https://oba.readthedocs.io/" == result[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_readthedocs_1_1(self):
        """Test to check if a result is added with a different name, then it gets added as a related link"""
        with open(test_data_path + "test_extract_readthedocs_1.txt", "r") as data_file:
            test_text = data_file.read()
            r = Result()
            r.add_result(constants.CAT_NAME,{
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
            c = regular_expressions.extract_readthedocs(test_text, Result(), test_data_path + "test_extract_readthedocs_2.txt")
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
            c = regular_expressions.extract_readthedocs(test_text, Result(), test_data_path + "test_extract_readthedocs_3.txt")
            result = c.results[constants.CAT_DOCUMENTATION][0]
            assert "https://owl-to-oas.readthedocs.io/" == result[constants.PROP_RESULT][constants.PROP_VALUE]

    def test_extract_gitter_chat(self):
        """Test designed to check if gitter chats are detected"""
        with open(test_data_path + "test_extract_gitter_chat.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_support_channels(test_text)
            # print(c)
            assert "https://gitter.im/OpenGeoscience/geonotebook" in c

    def test_repo_status(self):
        """Test designed to check if repostatus badges are detected"""
        with open(test_data_path + "test_repo_status.txt", "r") as data_file:
            test_text = data_file.read()
            repo_status = regular_expressions.extract_repo_status(test_text, Result(), test_data_path + "test_repo_status.txt")
            result = repo_status.results[constants.CAT_STATUS]
            assert len(result) > 0 and result[0][constants.PROP_RESULT][constants.PROP_VALUE] == "https://www.repostatus.org/#active"

    def test_issue_291(self):
        """Test designed to check if logos are detected"""
        repo_url = "https://github.com/dgarijo/Widoco"
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url, None)
            assert (not logo == "")

    def test_issue_291_2(self):
        """Test designed to check if logos are detected"""
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_logo_uscisii2.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url, None)
            assert (not logo == "")

    def test_issue_291_3(self):
        """Test designed to check if logos are detected"""
        repo_url = "https://github.com/tensorflow/tensorflow/"
        with open(test_data_path + "test_logo_tensorflow.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url, None)
            assert (not logo == "")

    def test_issue_images(self):
        """Test designed to check if images are detected"""
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_issue_images.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url, None)
            assert len(images) > 0

    def test_issue_181(self):
        """Test designed to check if arxiv papers are detected"""
        with open(test_data_path + "test_issue_181.txt", "r") as data_file:
            test_text = data_file.read()
            arxiv_links = regular_expressions.extract_arxiv_links(test_text)
            assert len(arxiv_links) > 0

    def test_issue_270(self):
        """Test designed to check if support channels are detected"""
        with open(test_data_path + "test_issue_270.txt", "r") as data_file:
            test_text = data_file.read()
            support_channels = regular_expressions.extract_support_channels(test_text)
            assert len(support_channels) == 2

    def test_logo(self):
        """Test designed to check if logos are detected"""
        with open(test_data_path + "test_logo.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/Chowlk", None)
            assert (not logo == "")

    def test_logo2(self):
        """Test designed to check if logos are detected"""
        with open(test_data_path + "test_logo2.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/pytorch/pytorch", None)
            assert (not logo == "")

    def test_images(self):
        """Test designed to check if images are detected"""
        with open(test_data_path + "test_images.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/pytorch/pytorch", None)
            assert (len(images) > 0 and not logo == "")

    def test_issue_320(self):
        """Test designed to check if logos are detected"""
        with open(test_data_path + "README-urllib3.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/urllib3/urllib3", None)
            assert (not logo == "")

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
            logo, images = regular_expressions.extract_images(test_text, None, test_data_repositories + "Widoco")
            assert (logo.find('test_data') > 0)

    def test_issue_446(self):
        """Test that jitpack URLs are not returned"""
        with open(test_data_path + "README-licensius.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/licensius/", None)
            assert (logo == "")

    def test_issue_446_1(self):
        """Test that jitpack URLs are not returned"""
        with open(test_data_path + "README-PPool.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/PPool/", None)
            assert (logo == "" and len(images) == 0)

    def test_issue_446_2(self):
        """Test that jitpack URLs are not returned"""
        with open(test_data_path + "README-loupe-api.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/PPool/", None)
            assert (logo == "" and len(images) == 1)

    def test_issue_467(self):
        """Test designed to check if logo is correctly obtained"""
        with open(test_data_path + "README-wothive.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text,"https://github.com/oeg-upm/wot-hive/", None)
            assert logo == "https://raw.githubusercontent.com/oeg-upm/wot-hive/AndreaCimminoArriaga-wothive-logo/logo.png"

    def test_issue_463(self):
        """Test designed to check if a repo with a badge but not logo is correctly ignored"""
        with open(test_data_path + "README-OBA-SPARQL.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text,"https://github.com/KnowledgeCaptureAndDiscovery/OBA_sparql/", None)
            assert logo == ""

    def test_issue_463_2(self):
        """Test designed to check if a repo with a badge but not logo is correctly ignored"""
        with open(test_data_path + "README-base-images.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text,"https://github.com/mintproject/base_images", None)
            assert logo == ""
