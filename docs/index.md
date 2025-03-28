# Software Metadata Extraction Framework (SOMEF) [![Python](https://img.shields.io/pypi/pyversions/somef.svg?style=plastic)](https://badge.fury.io/py/somef) [![PyPI](https://badge.fury.io/py/somef.svg)](https://badge.fury.io/py/somef) [![DOI](https://zenodo.org/badge/190487675.svg)](https://zenodo.org/badge/latestdoi/190487675) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)


**Authors:** Daniel Garijo, Allen Mao, Miguel Ángel García Delgado, Haripriya Dharmala, Vedant Diwanji, Jiaying Wang, Aidan Kelley and Jenifer Tabita Ciuciu-Kiss.

The aim of SOMEF is to help automatically extract metadata from scientific software from their readme files and GitHub repositories and make it available in a machine-readable manner. Thanks to SOMEF, we can populate knowedge graphs of scientific software metadata and relate different software together.

SOMEF has currently been tested with GitHub repositories, but it can extract metadata from any readme file written in mardown syntax.

!!! info
    If you experience any issues when using SOMEF, please open an issue on our [GitHub repository](https://github.com/KnowledgeCaptureAndDiscovery/somef/issues).

## Features
Given a readme file (or a GitHub repository) SOMEF will extract the following categories (if present):

- **Name**: Name identifying a software component
- **Full name**: Name + owner (owner/name)
- **Full title**: If the repository is a short name, we will attempt to extract the longer version of the repository  name
- **Description**: A description of what the software does.
- **Citation**: Preferred citation (usually in `.bib` form) as the authors have stated in their readme file.
- **ContinuousIntegration**: Link to a continuous integration service (e.g., GitHub or GitLab actions)
- **Installation instructions**: A set of instructions that indicate how to install a target repository
- **Invocation**: Execution command(s) needed to run a scientific software component
- **Usage examples**: Assumptions and considerations recorded by the authors when executing a software component, or examples on how to use it.
- **Documentation**: Where to find additional documentation about a software component.
- **Requirements**: Pre-requisites and dependencies needed to execute a software component.
- **Contributors**: Contributors to a software component
- **FAQ**: Frequently asked questions about a software component
- **Support**: Guidelines and links of where to obtain support for a software component
- **License**: License and usage terms of a software component
- **Contact**: Contact person responsible for maintaining a software component
- **Download URL**: URL where to download the target software (typically the installer, package or a tarball to a stable version)
- **DOI**: Digital Object Identifier associated with the software (if any)
- **DockerFile**: Build file to create a Docker image for the target software
- **Notebooks**: Jupyter notebooks included in a repository
- **Executable notebooks**: Jupyter notebooks ready for execution (e.g., through myBinder)
- **Owner**: Name of the user or organization in charge of the repository
- **Keywords**: set of terms used to commonly identify a software component
- **Source code**: Link to the source code (typically the repository where the readme can be found)
- **Releases**: Pointer to the available versions of a software component
- **Changelog**: Description of the changes between versions
- **Issue tracker**: Link where to open issues for the target repository
- **Programming languages**: Languages used in the repository
- **Repository Status**: Repository status as it is described in [repostatus.org](https://www.repostatus.org/)
- **Arxiv Links**: Links to Arxiv articles
- **Stargazers count**: Total number of stargazers of the project
- **Forks count**: Number of forks of the project
- **Forks url**: Links to forks made of the project
- **Code of Conduct**: Link to the code of conduct of the project
- **Scripts**: Snippets of code contained in the repository.
- **Support channels**: Help channels one can use to get support about the target software component.
- **Images**: Images used to illustrate the software component.
- **Logo**: Main logo used to represent the target software component.
- **Ontologies**: URL and path to the ontology files present in the repository.
- **Application domain**: The application domain of the repository. This may be related to the research area of a software component (e.g., Astrophysics) or the general domain/functionality of the tool (i.e., machine learning projects)<sup>[1](#myfootnote1)</sup> 

SOMEF uses the [Software  Description Ontology](https://w3id.org/okn/o/sd), which extends [Schema.org](https://schema.org) and [Codemeta](https://codemeta.github.io/terms/) to represent all the categories listed above. To see different export options please see [the getting started page](https://somef.readthedocs.io/en/latest/usage/).

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

