# Supported Metadata Files

This project supports extracting metadata from specific types of files commonly used to declare authorship and contribution in open source repositories.


## Supported Metadata Files in SOMEF

SOMEF can extract metadata from a wide range of files commonly found in software repositories. Below is a list of supported file types, along with clickable examples from real projects:

| File Name          | Language       | Description | Detail | Source Spec. | Version Spec.| Example |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: |
| `AUTHORS.md`     | General        | Lists contributors, authors, and affiliations relevant to the project | [🔍](./author.md)| [📄](https://opensource.google/documentation/reference/releasing/authors/)| N/A| [Example](https://gist.github.com/juliengdt/91d80c812e41be891dcf) |
| `*.bib` | BibTeX | Bibliographic database file for references and citations | [🔍](./bibtext.md) | [📄](https://www.bibtex.org/Format/) | [Latest](https://www.bibtex.org/) | [Example](https://raw.githubusercontent.com/relion-wi/relion/master/citating.bib) |
| `pom.xml`          | Java / Maven   | Project configuration file containing metadata and dependencies | [🔍](./pom.md) | [📄](https://maven.apache.org/pom.html) | [4.0.0](https://maven.apache.org/xsd/maven-4.0.0.xsd) |  [Example](https://github.com/apache/maven/blob/master/pom.xml) | 
| `bower.json`       | JavaScript (Bower)         | Package descriptor used for configuring packages that can be used as a dependency for Bower-managed front-end projects. | [🔍](./bower.md)| [📄](https://github.com/bower/spec/blob/master/json.md)| [0.3.4](https://github.com/bower/spec/blob/master/json.md)| [Example](https://github.com/juanjemdIos/somef/blob/master/src/somef/test/test_data/repositories/js-template/bower.json) |
| `package.json`     | JavaScript / Node.js       | Defines metadata, scripts, and dependencies for Node.js projects | [🔍](./packagejson.md)| [📄](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)| [Latest](https://docs.npmjs.com/cli/v11/configuring-npm/package-json)| [Example](https://github.com/npm/cli/blob/latest/package.json) | 
| `codemeta.json`       |        JSON-LD              | Metadata file for research software using JSON-LD vocabulary |  [🔍](./codemetajson.md) | [📄](https://github.com/codemeta/codemeta/blob/master/crosswalk.csv)| [v3.0](https://w3id.org/codemeta/3.0)| [Example](https://github.com/codemeta/codemeta/blob/master/codemeta.json) |
| `readme.md` | Markdown                     | Main documentation file of repository | [🔍](./readmefile.md)| [📄](https://spec.commonmark.org/)| [v0.31.2](https://github.com/commonmark/commonmark-spec)| [Example](https://github.com/KnowledgeCaptureAndDiscovery/somef/blob/master/README.md) |
| `composer.json`    | PHP                        | Manifest file serves as the package descriptor used in PHP projects. |  [🔍](./composer.md)| [📄](https://getcomposer.org/doc/04-schema.md)| [2.8.12](https://getcomposer.org/changelog/2.8.12)| [Example](https://github.com/composer/composer/blob/main/composer.json) |
| `juliaProject.toml`   | Julia                     | Defines the package metadata and dependencies for Julia projects, used by the Pkg package manager.| [🔍](./julia.md)| [📄](https://docs.julialang.org/en/v1/)| [v1.0](https://pkgdocs.julialang.org/v1/project-toml/)| [Example](https://github.com/JuliaLang/TOML.jl/blob/master/Project.toml) | 
| `pyproject.toml`   | Python                     | Modern Python project configuration file used by tools like Poetry and Flit |   [🔍](./pyprojecttoml.md)| [📄](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)| [PEP 621](https://peps.python.org/pep-0621/)| [Example](https://github.com/KnowledgeCaptureAndDiscovery/somef/blob/master/pyproject.toml) | 
| `requirements.txt` | Python                     | Lists Python package dependencies | [🔍](./requirementstxt.md)| [📄](https://pip.pypa.io/en/stable/reference/requirements-file-format/)| [Latest](https://pip.pypa.io/en/stable/reference/requirements-file-format/)| [Example](https://github.com/oeg-upm/FAIR-Research-Object/blob/main/requirements.txt) |
| `setup.py`         | Python                     | Package file format used in python projects | [🔍](./setuppy.md)| [📄](https://setuptools.pypa.io/en/latest/references/keywords.html)| [v75.0.0](https://github.com/pypa/setuptools)| [Example](https://github.com/oeg-upm/soca/blob/main/setup.py) | 
| `DESCRIPTION`      | R                          | Metadata file for R packages including title, author, and version |   [🔍](./description.md) | [📄](https://cran.r-project.org/doc/manuals/R-exts.html#The-DESCRIPTION-file)| [v4.4.1](https://cran.r-project.org/doc/manuals/r-release/R-exts.html) |  [Example](https://github.com/cran/ggplot2/blob/master/DESCRIPTION) |
| `*.gemspec`        | Ruby                       | Manifest file serves as the package descriptor used in Ruby gem projects. |  [🔍](./gemspec.md)| [📄](https://guides.rubygems.org/specification-reference/)| [v3.5.22](https://github.com/rubygems/rubygems)|[Example](https://github.com/rubygems/rubygems/blob/master/bundler/bundler.gemspec) |
| `cargo.toml`       | Rust                       | Manifest file serves as the package descriptor used in Rust projects |  [🔍](./cargo.md) | [📄](https://doc.rust-lang.org/cargo/reference/manifest.html)| [v0.85.0](https://github.com/rust-lang/cargo) | [Example](https://github.com/rust-lang/cargo/blob/master/Cargo.toml) |
| `*.cabal`       | Haskell                       | Manifest file serving as the package descriptor for Haskell projects.|  [🔍](./cabal.md) | [📄](https://cabal.readthedocs.io/en/3.10/cabal-package.html)| [v3.12](https://github.com/haskell/cabal)| [Example](https://github.com/haskell/cabal/blob/master/Cabal/Cabal.cabal) |
| `dockerfile`       | Dockerfile                       | Build specification file for container images that can include software metadata via LABEL instructions (OCI specification).|  [🔍](./dockerfiledoc.md) | [📄](https://docs.docker.com/reference/dockerfile/)| [v1.11](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md)| [Example](https://github.com/FairwindsOps/nova/blob/master/Dockerfile) |
| `CITATION.cff` | YAML | Citation File Format for software citation metadata | [🔍](./citationcff.md) | [📄](https://citation-file-format.github.io/) | [v1.2.0](https://github.com/citation-file-format/citation-file-format) | [Example](https://github.com/citation-file-format/citation-file-format/blob/main/CITATION.cff) |
| `publiccode.yml`       | YAML                      | YAML metadata file for public sector software projects| [🔍](./publiccode.md)| [📄](https://yml.publiccode.tools/)| [v0.3.0](https://yml.publiccode.tools/schema.html)| [Example](https://github.com/maykinmedia/objects-api/blob/master/publiccode.yaml) |
| `environment.yml`       | YAML                      | Conda environment specification file declaring software dependencies for reproducible environments|  [🔍](./condaenvironment.md) | [📄](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually)| [Latest](https://github.com/conda/conda)| [Example](https://github.com/CompVis/stable-diffusion/blob/main/environment.yaml) |


> **Note:** The general principles behind metadata mapping in SOMEF are based on the [CodeMeta crosswalk](https://github.com/codemeta/codemeta/blob/master/crosswalk.csv) and the [CodeMeta JSON-LD context](https://github.com/codemeta/codemeta/blob/master/codemeta.jsonld).  
> However, each supported file type may have specific characteristics and field interpretations.




## Types of metadata in SOMEF

| Type                 | Metadata Category         |
|----------------------|---------------------------|
| Agent                | authors                   |
| Keywords             | keywords                  |
| License              | license                   |
| Release              | version                   |
| SoftwareDependency | requirements              |
| String               | description               |
| String               | name                      |
| String               | package_id                |
| String               | runtime_platform          |
| Url                  | has_package_file         |
| Url                  | homepage                  |
| Url                  | issue_tracker             |
| Url                  | package_distribution      |


## Example: Dependency Metadata Extraction from Configuration Files

SOMEF parses configuration files like `pom.xml` to extract **structured metadata** about software dependencies and other requirements.

---

### Source File: Snippet from `Widoco/pom.xml`

Below is the XML fragment for the Maven dependency that is being parsed:

```xml
<dependencies>
  <dependency>
    <groupId>org.apache.maven</groupId>
    <artifactId>maven-model</artifactId>
    <version>3.9.0</version>
  </dependency>
  </dependencies>
```


The following Python code snippet show the logic used by the SOMEF parser to transform the XML elements to the JSON metadata structure:

```python
        if project_data["dependencies"]:
            for dependency in project_data["dependencies"]:
                metadata_result.add_result(
                    constants.CAT_REQUIREMENTS, 
                    {
                        "value": f'{dependency.get("groupId", "")}.{dependency.get("artifactId", "")}'.strip("."),
                        "name": dependency.get("artifactId", ""),
                        "version": dependency.get("version", ""),
                        "type": constants.SOFTWARE_DEPENDENCY
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )
```


After applying the mapping logic, the metadata for the dependency is stored under the requirements category (CAT_REQUIREMENTS in this case) with the following JSON structure:

```json
    "requirements": [
        {
            "result": {
                "value": "org.apache.maven.maven-model",
                "name": "maven-model",
                "version": "3.9.0",
                "type": "SoftwareDependency"
            },
            "confidence": 1,
            "technique": "code_parser",
            "source": "https://raw.githubusercontent.com/dgarijo/Widoco/master/pom.xml"
        }
    ]
```
