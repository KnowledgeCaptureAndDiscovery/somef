# Software Metadata Extraction Framework (SOMEF) [![Python](https://img.shields.io/pypi/pyversions/somef.svg?style=plastic)](https://badge.fury.io/py/somef) [![PyPI](https://badge.fury.io/py/somef.svg)](https://badge.fury.io/py/somef) [![DOI](https://zenodo.org/badge/190487675.svg)](https://zenodo.org/badge/latestdoi/190487675) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)


**Authors:** Daniel Garijo, Allen Mao, Miguel Ángel García Delgado, Haripriya Dharmala, Vedant Diwanji, Jiaying Wang, Aidan Kelley and Jenifer Tabita Ciuciu-Kiss.

The aim of SOMEF is to help automatically extract metadata from scientific software from their readme files and GitHub repositories and make it available in a machine-readable manner. Thanks to SOMEF, we can populate knowedge graphs of scientific software metadata and relate different software together.

SOMEF has currently been tested with GitHub repositories, but it can extract metadata from any readme file written in mardown syntax.

!!! info
    If you experience any issues when using SOMEF, please open an issue on our [GitHub repository](https://github.com/KnowledgeCaptureAndDiscovery/somef/issues).

## Features
Given a readme file (or a GitHub repository) SOMEF will extract the following categories (if present):

- **Acknowledgement**: Text acknowledging funding sources or contributors
- **Application domain**: The application domain of the repository. This may be related to the research area of a software component (e.g., Astrophysics) or the general domain/functionality of the tool (i.e., machine learning projects)<sup>[1](#myfootnote1)</sup> 
- **Assets**: files attached to the release
  - url: URL of the publication of the file
  - name: name of the file
  - content_size: file size
  - content_url: direct download link for the release file
  - encoding_format: format of the file
  - upload_date: date of publishing
  - download_count: numbers of downloads
- **Authors**: Person(s) or organization(s) responsible for the project. We recognize the following properties:
  - Name: name of the author (including last name)
  - Given name: First name of an author
  - Family name: Last name of an author
  - Email: email of author
  - URL: website or ORCID associated with the author
- **Build file**: Build file(s) of the project. For example, files used to create a Docker image for the target software, package files, etc.
- **Citation**: Preferred citation as the authors have stated in their readme file. SOMEF recognizes Bibtex, Citation File Format files and other means by which authors cite their papers (e.g., by in-text citation). We aim to recognize the following properties:
  - Title: Title of the publication
  - Author: list of author names in the publication
  - URL: URL of the publication 
  - DOI: Digital object identifier of the publication
  - Date published:
- **Code of conduct**: Link to the code of conduct of the project
- **Code repository**: Link to the GitHub/GitLab repository used for the extraction
- **Contact**: Contact person responsible for maintaining a software component
- **Continuous integration**: Link to continuous integration service(s)
- **Contribution guidelines**: Text indicating how to contribute to this code repository
- **Contributors**: Contributors to a software component
- **Creation date**: Date when the repository was created
- **Date updated**: Date of last release.
- **Description**: A description of what the software does
- **Documentation**: Where to find additional documentation about a software component
- **Download URL**: URL where to download the target software (typically the installer, package or a tarball to a stable version)
- **Executable examples**: Jupyter notebooks ready for execution (e.g., files, or through myBinder/colab links)
- **FAQ**: Frequently asked questions about a software component
- **Forks count**: Number of forks of the project
- **Forks url**: Links to forks made of the project
- **Full name**: Name + owner (owner/name)
- **Full title**: If the repository is a short name, we will attempt to extract the longer version of the repository name
- **Homepage**: URL of the item.
- **Identifier**: Identifier associated with the software (if any), such as Digital Object Identifiers and Software Heritage identifiers (SWH). DOIs associated with publications will also be detected. 
- **Images**: Images used to illustrate the software component
- **Installation instructions**: A set of instructions that indicate how to install a target repository
- **Invocation**: Execution command(s) needed to run a scientific software component
- **Issue tracker**: Link where to open issues for the target repository
- **Keywords**: set of terms used to commonly identify a software component
- **License**: License and usage terms of a software component
- **Logo**: Main logo used to represent the target software component
- **Name**: Name identifying a software component
- **Ontologies**: URL and path to the ontology files present in the repository
- **Owner**: Name and type of the user or organization in charge of the repository
- **Package distribution**: Links to package sites like pypi in case the repository has a package available.
- **Package files**: Links to package files used to wrap the project in a package.
- **Programming languages**: Languages used in the repository
- **Related papers**: URL to possible related papers within the repository stated within the readme file (from Arxiv)
- **Releases** (GitHub and Gitlab): Pointer to the available versions of a software component. For each release, somef will track the following properties:
  - Assets: files attached to the release
  - Description: Release notes
  - Author: Agent responsible of creating the release
  - Name: Name of the release
  - Tag: version number of the release
  - Date of publication
  - Date of creation
  - Link to the html page of the release
  - Id of the release
  - Link to the tarball zip and code of the release 
- **Repository status**: Repository status as it is described in [repostatus.org](https://www.repostatus.org/).
- **Requirements**: Pre-requisites and dependencies needed to execute a software component
- **Run**: Running instructions of a software component. It may be wider than the `invocation` category, as it may include several steps and explanations.
- **Runtime platform**: specifies the programming language and version required to run the project.
- **Script files**: Bash script files contained in the repository
- **Stargazers count**: Total number of stargazers of the project
- **Support**: Guidelines and links of where to obtain support for a software component
- **Support channels**: Help channels one can use to get support about the target software component
- **Type**: type of software (command line application, notebook, ontology, scientific workflow, etc.)
- **Usage examples**: Assumptions and considerations recorded by the authors when executing a software component, or examples on how to use it
- **Workflows**: URL and path to the computational workflow files present in the repository

We use different supervised classifiers, header analysis, regular expressions, the GitHub/Gitlab API to retrieve all these fields (more than one technique may be used for each field) and language specific metadata parsers (e.g., for package files). Each extraction records its provenance, with the confidence and technique used on each step. For more information check the [output format description](https://somef.readthedocs.io/en/latest/output/)

<a name="myfootnote1">1</a> The available application domains currently are: 

- **Astrophysics**: a branch of space science that applies the laws of physics and chemistry to seek to understand the universe and our place in it. The field explores topics such as the birth, life and death of stars, planets, galaxies, nebulae and other objects in the universe.
- **Audio**: a process of transforming, exploring, and interpreting audio signals recorded by digital devices.
- **Computer vision**: a field of artificial intelligence (AI) that enables computers and systems to derive meaningful information from digital images, videos and other visual inputs — and take actions or make recommendations based on that information.
- **Graphs**: data structures that can be ingested by various algorithms, notably neural nets, learning to perform tasks such as classification, clustering and regression.
- **Natural language processing**: a branch of computer science—and more specifically, the branch of artificial intelligence or AI—concerned with giving computers the ability to understand text and spoken words in much the same way human beings can.
- **Reinforcement learning**: a machine learning training method based on rewarding desired behaviors and/or punishing undesired ones.
- **Semantc web**: a vision about an extension of the existing World Wide Web, which provides software programs with machine-interpretable metadata of the published information and data.
- **Sequential**: the process of producing a sequence of values from a set of input values.

## Used Technologies and Standards

### GitHub API
We use the [Github's API](https://developer.github.com/v3/) to retrieve some of metadata fields indicated above, like name, license changelog and releases of a software component. 

### Scikit Learn
[Scikit Learn](https://scikit-learn.org/stable/about.html) is a powerful machine learning framework that provides a variety of methods for supervised and unsupervised learning. We use some of these classifiers to train sentence-based models to detect software description, citation, installation instructions and invocation commands.

### Wordnet
[Wordnet](https://wordnet.princeton.edu/) is a public lexical database which we use to find synonyms of common headers used when describe software. 

### JSON
The JavaScript Object Notation (JSON) is a syntax for storing and exchanging data commonly used by Web developers. We use JSON to serialize  our results.

### RDF
We use the Resource Description Framework (RDF) to serialize our results. We currently provide two different serializations: [JSON-LD](https://www.w3.org/TR/json-ld11/) and [Turtle](https://www.w3.org/TR/turtle/). The main difference between the JSON and RDF serializations is that they are simpler and do not incorporate the confidence of the results.

SOMEF uses the [Software  Description Ontology](https://w3id.org/okn/o/sd), which extends [Schema.org](https://schema.org) and [Codemeta](https://codemeta.github.io/terms/). We also support a Codemeta-specific export.

