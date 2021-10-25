import unittest

from somef.cli import *

class TestCli(unittest.TestCase):

    def test_extract_bibtex(self):
        test_txt = """
    Author: Daniel Garijo Verdejo (@dgarijo)
    Contributors: María Poveda, Idafen Santana, Almudena Ruiz, Miguel Angel García, Oscar Corcho, Daniel Vila, Sergio Barrio, Martin Scharm, Maxime Lefrancois, Alfredo Serafini, @kartgk.
    Citing WIDOCO: If you used WIDOCO in your work, please cite the ISWC 2017 paper: https://iswc2017.semanticweb.org/paper-138
    bib
    @inproceedings{garijo2017widoco,
      title={WIDOCO: a wizard for documenting ontologies},
      author={Garijo, Daniel},
      booktitle={International Semantic Web Conference},
      pages={94--102},
      year={2017},
      organization={Springer, Cham},
      doi = {10.1007/978-3-319-68204-4_9},
      funding = {USNSF ICER-1541029, NIH 1R01GM117097-01},
      url={http://dgarijo.com/papers/widoco-iswc2017.pdf}
    }
    If you want to cite the latest version of the software, you can do so by using: https://zenodo.org/badge/latestdoi/11427075.
        """
        c = extract_bibtex(test_txt)
        # Only one element is returned.
        assert "@inproceedings" in c[0]


    def test_extract_dois(self):
        test_text = """
        Title goes here (with another undesired link)
        [![DOI](https://zenodo.org/badge/11427075.svg)](https://zenodo.org/badge/latestdoi/11427075)[![](https://jitpack.io/v/dgarijo/Widoco.svg)](https://jitpack.io/#dgarijo/Widoco)
        Some text. Another DOI below:
        [![DOI](https://zenodo.org/badge/11427077.svg)](https://zenodo.org/badge/latestdoi/11427077)
        """
        c = extract_dois(test_text)
        print(c)
        assert len(c) == 2


    def test_extract_binder_links(self):
        test_text = """
        * **Basic KGTK functionality**: This notebook may take **5-10 minutes** to launch, please be patient. Note that in this notebook some KGTK commands (graph analytics and embeddings) **will not run**. To launch the notebook in your browser, click on the "Binder" icon: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/usc-isi-i2/kgtk/master?filepath=examples%2FExample5%20-%20AIDA%20AIF.ipynb)
    
        * **Advanced KGTK functionality**: This notebook may take **10-20 minutes to launch**. It includes basic KGTK functionality and **graph analytics and embedding capabilities** of KGTK:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dgarijo/kgtk/dev?filepath=%2Fkgtk%2Fexamples%2FCSKG%20Use%20Case.ipynb)
        """
        c = extract_binder_links(test_text)
        print(c)
        assert len(c) == 2


    def test_extract_title_underline(self):
        test_text = """
    Taguette
    ========
    Some text goes here
    
    Other header
    ------------
        """
        c = extract_title(test_text)
        assert "Taguette" == c


    def test_extract_title_hash(self):
        test_text = """
    # T2WML: A Cell-Based Language To Map Tables Into Wikidata Records
    
    [![Coverage Status](https://coveralls.io/repos/github/usc-isi-i2/t2wml/badge.svg?branch=master&service=github)](https://coveralls.io/github/usc-isi-i2/t2wml)
    
    * [Running T2WML for Development](#development)
    ## Wrong header
        """
        c = extract_title(test_text)
        print(c)
        assert "T2WML: A Cell-Based Language To Map Tables Into Wikidata Records" == c


    def test_extract_title_with_md(self):
        test_text = """
    # SOMEF [![DOI](https://zenodo.org/badge/190487675.svg)](https://zenodo.org/badge/latestdoi/190487675) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)
        """
        c = extract_title(test_text)
        print(c)
        assert "SOMEF" == c


    def test_extract_readthedocs_1(self):
        test_text = """
        For instructions on using OBA to create your API server, go to the 
        [documentation](https://oba.readthedocs.io/en/latest/)
        """
        c = extract_readthedocs(test_text)
        print(c)
        assert ["https://oba.readthedocs.io/"] == c


    def test_extract_readthedocs_2(self):
        test_text = """
        # Ontology-Based APIs (OBA) [![Build Status]
        (https://travis-ci.org/KnowledgeCaptureAndDiscovery/OBA.svg?branch=master)]
        (https://travis-ci.org/KnowledgeCaptureAndDiscovery/OBA)
        [![DOI](https://zenodo.org/badge/184804693.svg)](https://zenodo.org/badge/latestdoi/184804693)
        ### Documentation
        https://kgtk.readthedocs.io/en/latest/ as you may have guessed
        """
        c = extract_readthedocs(test_text)
        print(c)
        assert ["https://kgtk.readthedocs.io/"] == c


    def test_extract_readthedocs_3(self):
        test_text = """
        See full documentation at [https://somef.readthedocs.io/en/latest/](https://somef.readthedocs.io/en/latest/)
        """
        c = extract_readthedocs(test_text)
        print(c)
        assert ["https://somef.readthedocs.io/"] == c

    def test_extract_gitter_chat(self):
        text = """## GeoNotebook [![CircleCI](https://circleci.com/gh/OpenGeoscience/geonotebook.svg?style=shield)](https://circleci.com/gh/OpenGeoscience/geonotebook) [![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/OpenGeoscience/geonotebook)
        GeoNotebook is an application that provides client/server
                  """
        c = extract_gitter_chat(text)
        print(c)
        assert "https://gitter.im/OpenGeoscience/geonotebook" == c

    def test_issue_166(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/tensorflow/tensorflow/tree/v2.6.0", header)
        assert len(github_data['acknowledgments']) > 0


    def test_repo_status(self):
        text = """repostatus.org
        ==============

        [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

        A standard to easily communicate to humans and machines the development/support and usability status of software repositories/projects.

        For the majority of documentation and human-readable text, see https://www.repostatus.org/ or the [gh-pages branch](https://github.com/jantman/repostatus.org/tree/gh-pages) from which it is built.

        Please feel free to leave comments as Issues, or open pull requests.
        """
        repo_status = extract_repo_status(text)
        assert  len(repo_status) > 0


    def test_issue_171(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/RDFLib/rdflib/tree/6.0.2", header)
        assert len(github_data['contributors']) > 0