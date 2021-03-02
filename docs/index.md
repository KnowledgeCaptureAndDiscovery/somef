# Software Metadata Extraction Framework (SOMEF) [![DOI](https://zenodo.org/badge/190487675.svg)](https://zenodo.org/badge/latestdoi/190487675)

**Authors**: Daniel Garijo, Allen Mao, Haripriya Dharmala, Vedant Diwanji, Jiaying Wang and Aidan Kelley.

The aim of SOMEF is to help automatically extract metadata from scientific software from their readme files and GitHub repositories and make it available in a machine-readable manner. Thanks to SOMEF, we can populate knowedge graphs of scientific software metadata and relate different software together.

SOMEF has currently been tested with GitHub repositories, but it can extract metadata from any readme file written in mardown syntax.

!!! info
    If you experience any issues when using SOMEF, please open an issue on our [GitHub repository](https://github.com/KnowledgeCaptureAndDiscovery/somef/issues).

## Features
Given a readme file (or a GitHub repository) SOMEF will extract the following categories (if present):

- **Name**: Name identifying a software component
- **Full name**: Full name of the software (not abbreviated)
- **Description**: A description of what the software does.
- **Citation**: Preferred citation (usually in `.bib` form) as the authors have stated in their readme file.
- **Installation instructions**: A set of instructions that indicate how to install a target repository
- **Invocation**: Execution command(s) needed to run a scientific software component
- **Usage examples**: Assumptions and considerations recorded by the authors when executing a software component, or examples on how to use it.
- **Documentation**:
- **Requirements**: Pre-requisites and dependencies needed to execute a software component.
- **Contributors**: Contirbutors to a software component
- **FAQ**: Frequently asked questions about a software component
- **Support**: Guidelines and links of where to obtain support for a software component
- **License**: License and usage terms of a software component
- **Contact**: Contact person responsible for maintaining a software component
- **Download URL**: URL where to download the target software (typically the installer, package or a tarball to a stable version)
- **DOI**: Digital Object Identifier associated with the software (if any)
- **DockerFile**: Build file to create a Docker image for the target software
- **Notebooks**: Jupyter notebooks included in a repository
- **Owner**: Name of the user or organization in charge of the repository
- **Keywords**: set of terms used to commonly identify a software component
- **Source code**: Link to the source code (typically the repository where the readme can be found)
- **Releases**: Pointer to the available versions of a software component
- **Changelog**: Description of the changes between versions
- **Issue tracker**: Link where to open issues for the target repository
- **Programming languages**: Languages used in the repository

SOMEF uses the [Software  Description Ontology](https://w3id.org/okn/o/sd), which extends [Schema.org](https://schema.org) and [Codemeta](https://codemeta.github.io/terms/) to represent all the categories listed above. To see different export options please see [the getting started page](https://somef.readthedocs.io/en/latest/usage/).

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

