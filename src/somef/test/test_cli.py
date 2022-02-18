import unittest

from somef.cli import *

class TestCli(unittest.TestCase):

    def test_extract_bibtex(self):
        test_txt = """
    **Citing WIDOCO**: If you used WIDOCO in your work, please cite the ISWC 2017 paper: https://iswc2017.semanticweb.org/paper-138

```bib
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
```
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
        test_text = """# T2WML: A Cell-Based Language To Map Tables Into Wikidata Records
    
[![Coverage Status](https://coveralls.io/repos/github/usc-isi-i2/t2wml/badge.svg?branch=master&service=github)](https://coveralls.io/github/usc-isi-i2/t2wml)
    
* [Running T2WML for Development](#development)
## Wrong header
        """
        c = extract_title(test_text)
        print(c)
        assert "T2WML: A Cell-Based Language To Map Tables Into Wikidata Records" == c


    def test_extract_title_with_md(self):
        test_text = """# SOMEF 
        [![DOI](https://zenodo.org/badge/190487675.svg)](https://zenodo.org/badge/latestdoi/190487675) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)
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
        c = extract_support_channels(text)
        print(c)
        assert "https://gitter.im/OpenGeoscience/geonotebook" in c

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
        assert len(repo_status) > 0


    def test_issue_171(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/RDFLib/rdflib/tree/6.0.2", header)
        assert len(github_data['contributors']) > 0


    def test_issue_209(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/RDFLib/rdflib/tree/6.0.2", header)
        assert len(github_data['hasScriptFile']) > 0


    def test_issue_181(self):
        text = """
        This repository is for RDN introduced in the following paper

[Yulun Zhang](http://yulunzhang.com/), [Yapeng Tian](http://yapengtian.org/), [Yu Kong](http://www1.ece.neu.edu/~yukong/), [Bineng Zhong](https://scholar.google.de/citations?user=hvRBydsAAAAJ&hl=en), and [Yun Fu](http://www1.ece.neu.edu/~yunfu/), "Residual Dense Network for Image Super-Resolution", CVPR 2018 (spotlight), [[arXiv]](https://arxiv.org/abs/1802.08797) 

[Yulun Zhang](http://yulunzhang.com/), [Yapeng Tian](http://yapengtian.org/), [Yu Kong](http://www1.ece.neu.edu/~yukong/), [Bineng Zhong](https://scholar.google.de/citations?user=hvRBydsAAAAJ&hl=en), and [Yun Fu](http://www1.ece.neu.edu/~yunfu/), "Residual Dense Network for Image Restoration", arXiv 2018, [[arXiv]](https://arxiv.org/abs/1812.10477)
        
        ## Citation
```
@article{pyrobot2019,
  title={PyRobot: An Open-source Robotics Framework for Research and Benchmarking},
  author={Adithyavairavan Murali and Tao Chen and Kalyan Vasudev Alwala and Dhiraj Gandhi and Lerrel Pinto and Saurabh Gupta and Abhinav Gupta},
  journal={arXiv preprint arXiv:1906.08236},
  year={2019}
}
```
        """
        arxiv_links = extract_arxiv_links(text)
        assert len(arxiv_links) > 0

    def test_issue_211(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/probot/probot/tree/v12.1.1", header)
        assert len(github_data['contributingGuidelines']) > 0 and len(github_data['license']) > 0

    def test_issue_218(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/pytorch/captum/tree", header)
        assert len(github_data['citation']) > 0

    def test_issue_224(self):
        repo_data = cli_get_data(0.8, False, repo_url="https://github.com/tensorflow/tensorflow/tree/v2.6.0")
        data_graph = DataGraph()
        data_graph.add_somef_data(repo_data)
        with open("test-tensorflow-2.6.0.ttl", "wb") as out_file:
            out_file.write(data_graph.g.serialize(format="turtle", encoding="UTF-8"))
        text_file = open("test-tensorflow-2.6.0.ttl", "r", encoding="UTF-8")
        data = text_file.read()
        text_file.close()
        assert data.find("sd:dateCreated") >= 0

    def test_issue_280(self):
        with open("input-test.txt", "r") as in_handle:
            # get the line (with the final newline omitted) if the line is not empty
            repo_list = [line[:-1] for line in in_handle if len(line) > 1]

        # convert to a set to ensure uniqueness (we don't want to get the same data multiple times)
        repo_set = set(repo_list)
        # check if the urls in repo_set if are valids
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

    def test_issue_268(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/probot/probot/tree/v12.1.1", header)
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
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://gitlab.com/gitlab-org/ci-sample-projects/platform-team", header)
        assert len(github_data['downloadUrl']) > 0

    def test_issue_291(self):
        repo_url = "https://github.com/dgarijo/Widoco"
        text = """
# WIzard for DOCumenting Ontologies (WIDOCO)
[![DOI](https://zenodo.org/badge/11427075.svg)](https://zenodo.org/badge/latestdoi/11427075) [![](https://jitpack.io/v/dgarijo/Widoco.svg)](https://jitpack.io/#dgarijo/Widoco)

![Logo](src/main/resources/logo/logo2.png)

WIDOCO helps you to publish and create an enriched and customized documentation of your ontology automatically, by following a series of steps in a GUI.

**Author**: Daniel Garijo Verdejo (@dgarijo)

**Contributors**: María Poveda, Idafen Santana, Almudena Ruiz, Miguel Angel García, Oscar Corcho, Daniel Vila, Sergio Barrio, Martin Scharm, Maxime Lefrancois, Alfredo Serafini, @kartgk, Pat Mc Bennett, Christophe Camel.

**Citing WIDOCO**: If you used WIDOCO in your work, please cite the ISWC 2017 paper: https://iswc2017.semanticweb.org/paper-138
                """
        logo = extract_logo(text, repo_url)
        assert len(logo) > 0

    def test_issue_images(self):
        repo_url = "https://github.com/dgarijo/Widoco"
        text = """
<img src="https://github.com/usc-isi-i2/kgtk/raw/master/docs/images/kgtk_logo_200x200.png" width="150"/>
<img src="https://github.com/usc-isi-i2/kgtk/blob/master/docs/images/kgtk-data-model.png" width="150"/>
<img src="https://github.com/usc-isi-i2/kgtk/blob/master/docs/images/kgtk-pipeline.png" width="150"/>

# KGTK: Knowledge Graph Toolkit

[![doi](https://zenodo.org/badge/DOI/10.5281/zenodo.3828068.svg)](https://doi.org/10.5281/zenodo.3828068)  ![travis ci](https://travis-ci.org/usc-isi-i2/kgtk.svg?branch=master)  [![Coverage Status](https://coveralls.io/repos/github/usc-isi-i2/kgtk/badge.svg?branch=master)](https://coveralls.io/github/usc-isi-i2/kgtk?branch=master)
"""
        images = extract_images(text, repo_url)
        assert len(images) > 0


    def test_issue_285(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/vroddon/rdfchess", header)
        assert not 'license' in github_data == True


    def test_issue_270(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/oeg-upm/OpenRefineExtension_Transformation", header)
        assert ('codeRepository' in github_data) == True

        def test_issue_270(self):
            text = """
<p align="center">
    <a href="https://github.com/3b1b/manim">
        <img src="https://raw.githubusercontent.com/3b1b/manim/master/logo/cropped.png">
    </a>
</p>

[![pypi version](https://img.shields.io/pypi/v/manimgl?logo=pypi)](https://pypi.org/project/manimgl/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)
[![Manim Subreddit](https://img.shields.io/reddit/subreddit-subscribers/manim.svg?color=ff4301&label=reddit&logo=reddit)](https://www.reddit.com/r/manim/)
[![Manim Discord](https://img.shields.io/discord/581738731934056449.svg?label=discord&logo=discord)](https://discord.com/invite/bYCyhM9Kz2)
[![docs](https://github.com/3b1b/manim/workflows/docs/badge.svg)](https://3b1b.github.io/manim/)

Manim is an engine for precise programmatic animations, designed for creating explanatory math videos.
            """
            support_channels = extract_support_channels(text)
            assert len(support_channels) == 2


    def test_issue_311(self):
        from somef import cli
        cli.run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url=None,
                    doc_src="repostatus-README.md",
                    in_file=None,
                    output=None,
                    graph_out=None,
                    graph_format="turtle",
                    codemeta_out="test-repostatus-311.json-ld",
                    pretty=True,
                    missing=False)
        text_file = open("test-tensorflow-2.6.0.json-ld", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("\"repoStatus\":") < 0


    def test_issue_284(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/3b1b/manim", header)
        assert ('stargazersCount' in github_data) == True

    def test_issue_272(self):
        header = {}
        header['accept'] = 'application/vnd.github.v3+json'
        text, github_data = load_repository_metadata("https://github.com/3b1b/manim", header)
        assert ('longTitle' in github_data) == False

    def test_issue_281(self):
        run_cli(threshold=0.8,
                    ignore_classifiers=False,
                    repo_url=None,
                    doc_src="repostatus-README.md",
                    in_file=None,
                    output="test-281.json",
                    graph_out=None,
                    graph_format="turtle",
                    codemeta_out=None,
                    pretty=True,
                    missing=True)
        text_file = open("test-281.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("missingCategories") > 0

    def test_logo(self):
        text = """![Logo](https://github.com/oeg-upm/Chowlk/blob/webservice/static/resources/logo.png)

# Chowlk Converter
Tool to transform ontology conceptualizations made with diagrams.net into OWL code.
        """
        logos = extract_logo(text,"https://github.com/oeg-upm/Chowlk")
        # print(logos)
        assert(len(logos)>0)

    def test_logo2(self):
        text = """![PyTorch Logo](https://github.com/pytorch/pytorch/blob/master/docs/source/_static/img/pytorch-logo-dark.png)
--------------------------------------------------------------------------------

PyTorch is a Python package that provides two high-level features:
        """
        logos = extract_logo(text, "https://github.com/pytorch/pytorch")
        # print(logos)
        assert (len(logos) > 0)

    def test_images(self):
        text = """![PyTorch Logo](https://github.com/pytorch/pytorch/blob/master/docs/source/_static/img/pytorch-logo-dark.png)

--------------------------------------------------------------------------------

PyTorch is a Python package that provides two high-level features:
- Tensor computation (like NumPy) with strong GPU acceleration
- Deep neural networks built on a tape-based autograd system

You can reuse your favorite Python packages such as NumPy, SciPy, and Cython to extend PyTorch when needed.

<!-- toc -->

- [More About PyTorch](#more-about-pytorch)
  - [A GPU-Ready Tensor Library](#a-gpu-ready-tensor-library)
  - [Dynamic Neural Networks: Tape-Based Autograd](#dynamic-neural-networks-tape-based-autograd)
  - [Python First](#python-first)
  - [Imperative Experiences](#imperative-experiences)
  - [Fast and Lean](#fast-and-lean)
  - [Extensions Without Pain](#extensions-without-pain)
- [Installation](#installation)
  - [Binaries](#binaries)
    - [NVIDIA Jetson Platforms](#nvidia-jetson-platforms)
  - [From Source](#from-source)
    - [Install Dependencies](#install-dependencies)
    - [Get the PyTorch Source](#get-the-pytorch-source)
    - [Install PyTorch](#install-pytorch)
      - [Adjust Build Options (Optional)](#adjust-build-options-optional)
  - [Docker Image](#docker-image)
    - [Using pre-built images](#using-pre-built-images)
    - [Building the image yourself](#building-the-image-yourself)
  - [Building the Documentation](#building-the-documentation)
  - [Previous Versions](#previous-versions)
- [Getting Started](#getting-started)
- [Resources](#resources)
- [Communication](#communication)
- [Releases and Contributing](#releases-and-contributing)
- [The Team](#the-team)
- [License](#license)

<!-- tocstop -->

| System | 3.7 | 3.8 |
| :---: | :---: | :--: |
| Linux CPU | [![Build Status](https://ci.pytorch.org/jenkins/job/pytorch-master/badge/icon)](https://ci.pytorch.org/jenkins/job/pytorch-master/) | <center>—</center> |
| Linux GPU | [![Build Status](https://ci.pytorch.org/jenkins/job/pytorch-master/badge/icon)](https://ci.pytorch.org/jenkins/job/pytorch-master/) | <center>—</center> |
| Windows CPU / GPU | [![Build Status](https://ci.pytorch.org/jenkins/job/pytorch-builds/job/pytorch-win-ws2016-cuda9-cudnn7-py3-trigger/badge/icon)](https://ci.pytorch.org/jenkins/job/pytorch-builds/job/pytorch-win-ws2016-cuda9-cudnn7-py3-trigger/) |  <center>—</center> |
| Linux (ppc64le) CPU | [![Build Status](https://powerci.osuosl.org/job/pytorch-master-nightly-py3-linux-ppc64le/badge/icon)](https://powerci.osuosl.org/job/pytorch-master-nightly-py3-linux-ppc64le/) | <center>—</center> |
| Linux (ppc64le) GPU | [![Build Status](https://powerci.osuosl.org/job/pytorch-master-nightly-py3-linux-ppc64le-gpu/badge/icon)](https://powerci.osuosl.org/job/pytorch-master-nightly-py3-linux-ppc64le-gpu/) | <center>—</center> |
| Linux (aarch64) CPU | [![Build Status](http://openlabtesting.org:15000/badge?project=pytorch%2Fpytorch&job_name=pytorch-arm64-build-daily-master-py37)](https://status.openlabtesting.org/builds/builds?project=pytorch%2Fpytorch&job_name=pytorch-arm64-build-daily-master-py37) | [![Build Status](http://openlabtesting.org:15000/badge?project=pytorch%2Fpytorch&job_name=pytorch-arm64-build-daily-master-py38)](https://status.openlabtesting.org/builds/builds?project=pytorch%2Fpytorch&job_name=pytorch-arm64-build-daily-master-py38) |

See also the [CI HUD at hud.pytorch.org](https://hud.pytorch.org/ci/pytorch/pytorch/master).

Usually, PyTorch is used either as:

- A replacement for NumPy to use the power of GPUs.
- A deep learning research platform that provides maximum flexibility and speed.

Elaborating Further:

### A GPU-Ready Tensor Library

If you use NumPy, then you have used Tensors (a.k.a. ndarray).

![Tensor illustration](./docs/source/_static/img/tensor_illustration.png)

PyTorch provides Tensors that can live either on the CPU or the GPU and accelerates the
computation by a huge amount.
            """
        images = extract_images(text, "https://github.com/pytorch/pytorch")
        print(images)
        assert (len(images) > 0)
    
    def test_issue_200(self):
        run_cli(threshold=0.8,
                ignore_classifiers=False,
                repo_url=None,
                doc_src="README-widoco.md",
                in_file=None,
                output="test-200.json",
                graph_out=None,
                graph_format="turtle",
                codemeta_out=None,
                pretty=True,
                missing=True)
        text_file = open("test-200.json", "r")
        data = text_file.read()
        text_file.close()
        assert data.find("parentHeader") > 0