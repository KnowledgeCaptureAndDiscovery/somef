import unittest

from somef import regular_expressions

test_data_path = "test_data/"
test_data_repositories = "test_data/repositories/"


class TestCli(unittest.TestCase):

    def test_extract_bibtex(self):
        with open(test_data_path + "test_extract_bibtex.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_bibtex(test_text)
            assert "@inproceedings" in c[0]

    def test_extract_dois(self):
        with open(test_data_path + "test_extract_dois.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_dois(test_text)
            assert len(c) == 2

    def test_extract_binder_links(self):
        with open(test_data_path + "test_extract_binder_links.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_binder_links(test_text)
            assert len(c) == 2

    def test_extract_title_underline(self):
        with open(test_data_path + "test_extract_title_underline.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text)
            assert "Taguette" == c

    def test_extract_title_hash(self):
        with open(test_data_path + "test_extract_title_hash.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text)
            assert "T2WML: A Cell-Based Language To Map Tables Into Wikidata Records" == c

    def test_extract_title_with_md(self):
        with open(test_data_path + "test_extract_title_with_md.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_title(test_text)
            # print(c)
            assert "SOMEF" == c

    def test_extract_readthedocs_1(self):
        with open(test_data_path + "test_extract_readthedocs_1.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_readthedocs(test_text)
            assert ["https://oba.readthedocs.io/"] == c

    def test_extract_readthedocs_2(self):
        with open(test_data_path + "test_extract_readthedocs_2.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_readthedocs(test_text)
            # print(c)
            assert ["https://kgtk.readthedocs.io/"] == c

    def test_extract_readthedocs_3(self):
        test_text = """
        See full documentation at [https://somef.readthedocs.io/en/latest/](https://somef.readthedocs.io/en/latest/)
        """
        c = regular_expressions.extract_readthedocs(test_text)
        print(c)
        assert ["https://somef.readthedocs.io/"] == c

    def test_extract_readthedocs_issue_407(self):
        with open(test_data_path + "test_extract_readthedocs_3.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_readthedocs(test_text)
            print(c)
            assert ["https://owl-to-oas.readthedocs.io/"] == c

    def test_extract_gitter_chat(self):
        with open(test_data_path + "test_extract_gitter_chat.txt", "r") as data_file:
            test_text = data_file.read()
            c = regular_expressions.extract_support_channels(test_text)
            # print(c)
            assert "https://gitter.im/OpenGeoscience/geonotebook" in c

    def test_repo_status(self):
        with open(test_data_path + "test_repo_status.txt", "r") as data_file:
            test_text = data_file.read()
            repo_status = regular_expressions.extract_repo_status(test_text)
            assert len(repo_status) > 0

    def test_issue_291(self):
        repo_url = "https://github.com/dgarijo/Widoco"
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url)
            assert (not logo == "")

    def test_issue_291_2(self):
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_logo_uscisii2.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url)
            assert (not logo == "")

    def test_issue_291_3(self):
        repo_url = "https://github.com/tensorflow/tensorflow/"
        with open(test_data_path + "test_logo_tensorflow.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url)
            assert (not logo == "")

    def test_issue_images(self):
        repo_url = "https://github.com/usc-isi-i2/kgtk/"
        with open(test_data_path + "test_issue_images.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, repo_url)
            assert len(images) > 0

    def test_issue_181(self):
        with open(test_data_path + "test_issue_181.txt", "r") as data_file:
            test_text = data_file.read()
            arxiv_links = regular_expressions.extract_arxiv_links(test_text)
            assert len(arxiv_links) > 0

    def test_issue_270(self):
        with open(test_data_path + "test_issue_270.txt", "r") as data_file:
            test_text = data_file.read()
            support_channels = regular_expressions.extract_support_channels(test_text)
            assert len(support_channels) == 2

    def test_logo(self):
        with open(test_data_path + "test_logo.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/oeg-upm/Chowlk")
            assert (not logo == "")

    def test_logo2(self):
        with open(test_data_path + "test_logo2.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/pytorch/pytorch")
            assert (not logo == "")

    def test_images(self):
        with open(test_data_path + "test_images.txt", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/pytorch/pytorch")
            assert (len(images) > 0 and not logo == "")

    def test_issue_320(self):
        with open(test_data_path + "README-urllib3.md", "r") as data_file:
            test_text = data_file.read()
            logo, images = regular_expressions.extract_images(test_text, "https://github.com/urllib3/urllib3")
            assert (not logo == "")

    def test_issue_337(self):
        text = """## Interactive web interface

Visit the public website at [www.mapshaper.org](http://www.mapshaper.org) or use the web UI locally via the `mapshaper-gui` script. 

All processing is done in the browser, so your data stays private, even when using the public website.

The web UI works in recent desktop versions of Chrome, Firefox, Safari and Internet Explorer. Safari before v10.1 and IE before v10 are not supported.

        """
        text = regular_expressions.remove_links_images(text)
        assert text.find("[www.mapshaper.org](http://www.mapshaper.org)") == -1
