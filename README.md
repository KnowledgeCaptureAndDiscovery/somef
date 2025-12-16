# Software Metadata Extraction Framework (SOMEF)

[![Documentation Status](https://readthedocs.org/projects/somef/badge/?version=latest)](https://somef.readthedocs.io/en/latest/?badge=latest)
[![Python](https://img.shields.io/pypi/pyversions/somef.svg?style=plastic)](https://badge.fury.io/py/somef) [![PyPI](https://badge.fury.io/py/somef.svg)](https://badge.fury.io/py/somef) [![DOI](https://zenodo.org/badge/190487675.svg)](https://zenodo.org/badge/latestdoi/190487675) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

<img src="docs/logo.png" alt="logo" width="150"/>

A command line interface for automatically extracting relevant metadata from code repositories (readme, configuration files, documentation, etc.).

**Demo:** See a [demo running somef as a service](https://somef.linkeddata.es), through the [SOMEF-Vider tool](https://github.com/SoftwareUnderstanding/SOMEF-Vider/).

**Authors:** Daniel Garijo, Allen Mao, Miguel Ángel García Delgado, Haripriya Dharmala, Vedant Diwanji, Jiaying Wang, Aidan Kelley, Jenifer Tabita Ciuciu-Kiss, Luca Angheluta and Juanje Mendoza.

## Features

Given a readme file (or a GitHub/Gitlab repository) SOMEF will extract the following categories (if present), listed in alphabetical order:

- **Acknowledgement**: Text acknowledging funding sources or contributors
- **Application domain**: The application domain of the repository. Current supported domains include: Astrophysics, Audio, Computer vision, Graphs, Natural language processing, Reinforcement learning, Semantc web, Sequential. Domains are not mutually exclusive. These domains have been extracted from [awesome lists](https://github.com/topics/awesome-list) and [Papers with code](https://paperswithcode.com/). Find more information in our [documentation](https://somef.readthedocs.io/en/latest/)
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
  - Date published
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
- **Releases** (GitHub only): Pointer to the available versions of a software component. For each release, somef will track the following properties:
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
- **Runtime platform**: specifies runtime platform or script interpreter dependencies required to run the project..
- **Script files**: Bash script files contained in the repository
- **Stargazers count**: Total number of stargazers of the project
- **Support**: Guidelines and links of where to obtain support for a software component
- **Support channels**: Help channels one can use to get support about the target software component
- **Type**: type of software (command line application, notebook, ontology, scientific workflow, etc.)
- **Usage examples**: Assumptions and considerations recorded by the authors when executing a software component, or examples on how to use it
- **Workflows**: URL and path to the computational workflow files present in the repository

We use different supervised classifiers, header analysis, regular expressions, the GitHub/Gitlab API to retrieve all these fields (more than one technique may be used for each field) and language specific metadata parsers (e.g., for package files). Each extraction records its provenance, with the confidence and technique used on each step. For more information check the [output format description](https://somef.readthedocs.io/en/latest/output/)

## Documentation

See full documentation at [https://somef.readthedocs.io/en/latest/](https://somef.readthedocs.io/en/latest/)

## Cite SOMEF:

Journal publication (preferred):

```
@article{10.1162/qss_a_00167,
    author = {Kelley, Aidan and Garijo, Daniel},
    title = "{A Framework for Creating Knowledge Graphs of Scientific Software Metadata}",
    journal = {Quantitative Science Studies},
    pages = {1-37},
    year = {2021},
    month = {11},
    issn = {2641-3337},
    doi = {10.1162/qss_a_00167},
    url = {https://doi.org/10.1162/qss_a_00167},
    eprint = {https://direct.mit.edu/qss/article-pdf/doi/10.1162/qss\_a\_00167/1971225/qss\_a\_00167.pdf},
}
```

Conference publication (first):

```
@INPROCEEDINGS{9006447,
author={A. {Mao} and D. {Garijo} and S. {Fakhraei}},
booktitle={2019 IEEE International Conference on Big Data (Big Data)},
title={SoMEF: A Framework for Capturing Scientific Software Metadata from its Documentation},
year={2019},
doi={10.1109/BigData47090.2019.9006447},
url={http://dgarijo.com/papers/SoMEF.pdf},
pages={3032-3037}
}
```

## Requirements

- Python 3.9 or Python 3.10 (default version support)

SOMEF has been tested on Unix, MacOS and Windows Microsoft operating systems.

If you face any issues when installing SOMEF, please make sure you have installed the following packages: `build-essential`, `libssl-dev`, `libffi-dev` and `python3-dev`.

## Install from Pypi

SOMEF [is available in Pypi!](https://pypi.org/project/somef/) To install it just type:

```
pip install somef
```

## Install from GitHub

To run SOMEF, please follow the next steps:

Clone this GitHub repository

```
git clone https://github.com/KnowledgeCaptureAndDiscovery/somef.git
```

We use [Poetry](https://python-poetry.org/) to ensure library compatibility. It can be installed as follows:

```
curl -sSL https://install.python-poetry.org | python3 -
```

This option is recommended over installing Poetry with pip install.

Now Poetry will handle the installation of SOMEF and all its dependencies configured in the `toml` file.

To test the correct installation of poetry run (poetry version `> 2.0.0`):

```
poetry --version
```

Install somef and all their dependencies.

```
cd /somef
poetry install
```

Now we need to access our virtual environment, to do so you can run the following command:

```bash
poetry env activate
```
If the environment is not active, paste the command shown when `poetry env activate` is run, typically something like the command below: 

```bash
source /path_to_env/ENV_NAME/bin/activate
```

To learn more about poetry environment management, visit their official documentation [here](https://python-poetry.org/docs/managing-environments/).

Test the SOMEF installation run:

```bash
somef --help
```

If everything goes fine, you should see:

```bash
Usage: somef [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  configure  Configure credentials
  describe   Running the Command Line Interface
  version    Show somef version.
```

## Installing through Docker

We provide a Docker image with SOMEF already installed. To run through Docker, you may build the Dockerfile provided in the repository by running:

```bash
docker build -t somef .
```

Or just use the Docker image already built in [DockerHub](https://hub.docker.com/r/kcapd/somef):

```bash
docker pull kcapd/somef
```

Then, to run your image just type:

```bash
docker run --rm -it kcapd/somef 
```

And you will be ready to use SOMEF (see section below). If you want to have access to the results we recommend [mounting a volume](https://docs.docker.com/storage/volumes/). For example, the following command will mount the current directory as the `out` folder in the Docker image:

```bash
docker run -it --rm -v $PWD/:/out kcapd/somef 
```

If you move any files produced by somef into `/out`, then you will be able to see them in your current directory.

## Configure

Before running SOMEF for the first time, you must **configure** it appropriately (you only need to do this once). Run:

```bash
somef configure
```

And you will be asked to provide the following:

- A GitHub authentication token [**optional, leave blank if not used**], which SOMEF uses to retrieve metadata from GitHub. If you don't include an authentication token, you can still use SOMEF. However, you may be limited to a series of requests per hour. For more information, see [https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
- The path to the trained classifiers (pickle files). If you have your own classifiers, you can provide them here. Otherwise, you can leave it blank

If you want somef to be automatically configured (without GitHUb authentication key and using the default classifiers) just type:

```bash
somef configure -a
```

For showing help about the available options, run:

```bash
somef configure --help
```

Which displays:

```bash
Usage: somef configure [OPTIONS]

  Configure GitHub credentials and classifiers file path

Options:
  -a, --auto  Automatically configure SOMEF
  -h, --help  Show this message and exit.
```

### Updating SOMEF

If you update SOMEF to a newer version, we recommend you `configure` again the library (by running `somef configure`). The rationale is that different versions may rely on classifiers which may be stored in a different path.

## Usage

```bash
$ somef describe --help
  SOMEF Command Line Interface
Usage: somef describe [OPTIONS]

  Running the Command Line Interface

Options:
  -t, --threshold FLOAT           Threshold to classify the text  [required]
  Input: [mutually_exclusive, required]
    -r, --repo_url URL            Github/Gitlab Repository URL
    -d, --doc_src PATH            Path to the README file source
    -i, --in_file PATH            A file of newline separated links to GitHub/
                                  Gitlab repositories

  Output: [required_any]
    -o, --output PATH             Path to the output file. If supplied, the
                                  output will be in JSON

    -c, --codemeta_out PATH       Path to an output codemeta file
    -g, --graph_out PATH          Path to the output Knowledge Graph export
                                  file. If supplied, the output will be a
                                  Knowledge Graph, in the format given in the
                                  --format option chosen (turtle, json-ld)

  -f, --graph_format [turtle|json-ld]
                                  If the --graph_out option is given, this is
                                  the format that the graph will be stored in

  -p, --pretty                    Pretty print the JSON output file so that it
                                  is easy to compare to another JSON output
                                  file.

  -m, --missing                   The JSON will include a field
                                  somef_missing_categories to report with the
                                  missing metadata fields that SOMEF was not
                                  able to find.

  -kt, --keep_tmp PATH            SOMEF will NOT delete the temporary folder
                                  where files are stored for analysis. Files
                                  will be stored at the
                                  desired path

  -all, --requirements_all        Export all detected requirements, including
                                  text and libraries (default).

  -v, --requirements_v            Export only requirements from structured
                                  sources (pom.xml, requirements.txt, etc.)

  -h, --help                      Show this message and exit.
```

## Usage example:

The following command extracts all metadata available from [https://github.com/dgarijo/Widoco/](https://github.com/dgarijo/Widoco/).

```bash
somef describe -r https://github.com/dgarijo/Widoco/ -o test.json -t 0.8
```

Try SOMEF in Binder with our sample notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)

## Contribute:

If you want to contribute with a pull request, please do so by submitting it to the `dev` branch.

## Next features:

To see upcoming features, please have a look at our [open issues](https://github.com/KnowledgeCaptureAndDiscovery/somef/issues) and [milestones](https://github.com/KnowledgeCaptureAndDiscovery/somef/milestones)

## Extending SOMEF categories:

To run a classifier with an additional category or remove an existing one, a corresponding path entry in the config.json should be provided and the category type should be added/removed in the category variable in `cli.py`.

## Metadata Support

SOMEF supports the extraction and analysis of metadata in package files of several programming languages.  Current support includes: `setup.py` and `pyproject.toml` for Python, `pom.xml` for Java, `.gemspec` for Ruby, `DESCRIPTION` for R, `bower.json` for JavaScript, HTML or CSS, `.cabal` for Haskell, `cargo.toml` for RUST, `composer` for PHP, `.juliaProject.toml` for Julia , `AUTHORS`, `codemeta.json`, and `citation.cff`
This includes identifying dependencies, runtime requirements, and development tools specified in project configuration files.  

## Limitations

SOMEF is designed to work primarily with repositories written in English.  
Repositories in other languages may not be processed as effectively, and results could be incomplete or less accurate.
