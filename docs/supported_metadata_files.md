# Supported Metadata Files

This project supports extracting metadata from specific types of files commonly used to declare authorship and contribution in open source repositories.


## Supported Metadata Files in SOMEF

SOMEF can extract metadata from a wide range of files commonly found in software repositories. Below is a list of supported file types, along with clickable examples from real projects:

| File Name          | Language       | Description | Detail | Source Spec. | Version Spec.| Example |
|--------------------|----------------|-------------|--------|--------------|--------------|---------|
| `AUTHORS.md`       | General                    | Lists contributors, authors, and affiliations relevant to the project |  <div align="center">[🔍](./author.md)</div>| [📄](https://opensource.google/documentation/reference/releasing/authors/)| |[Example](https://gist.github.com/juliengdt/91d80c812e41be891dcf) |
| `pom.xml`          | Java / Maven   | Project configuration file containing metadata and dependencies | <div align="center">[🔍](./pom.md) | [📄](https://maven.apache.org/pom.html) | [4.0.0](https://maven.apache.org/xsd/maven-4.0.0.xsd) | [Example](https://github.com/apache/maven/blob/master/pom.xml) | 
| `bower.json`       | JavaScript (Bower)         | Package descriptor used for configuring packages that can be used as a dependency for Bower-managed front-end projects. |  <div align="center">[🔍](./bower.md)</div>| [📄](https://github.com/bower/spec/blob/master/json.md)| |[Example](https://github.com/juanjemdIos/somef/blob/master/src/somef/test/test_data/repositories/js-template/bower.json) |
| `package.json`     | JavaScript / Node.js       | Defines metadata, scripts, and dependencies for Node.js projects |  <div align="center">[🔍](./packagejson.md)| [📄](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)| 10.9.4|[Example](https://github.com/npm/cli/blob/latest/package.json) | 
| `codemeta.json`       |        JSON-LD              | Metadata file for research software using JSON-LD vocabulary | <div align="center">[🔍](./codemetajson.md)</div> | [📄](https://github.com/codemeta/codemeta/blob/master/crosswalk.csv)| [v3.0](https://w3id.org/codemeta/3.0)|[Example](https://github.com/codemeta/codemeta/blob/master/codemeta.json) |
| `readme.me` | Markdown                     | Main documentation file of repository |  <div align="center">[🔍](./readmefile.md)</div>| | |[Example](https://github.com/KnowledgeCaptureAndDiscovery/somef/blob/master/README.md) |
| `composer.json`    | PHP                        | Manifest file serves as the package descriptor used in PHP projects. | <div align="center">[🔍](./composer.md)</div>| [📄](https://getcomposer.org/doc/04-schema.md)| [2.8.12](https://getcomposer.org/changelog/2.8.12)|[Example](https://github.com/composer/composer/blob/main/composer.json) |
| `juliaProject.toml`   | Python                     | Defines the package metadata and dependencies for Julia projects, used by the Pkg package manager.|  <div align="center">[🔍](./julia.md)</div>| [📄](https://docs.julialang.org/en/v1/)| |[Example](https://github.com/JuliaLang/TOML.jl/blob/master/Project.toml) | 
| `pyproject.toml`   | Python                     | Modern Python project configuration file used by tools like Poetry and Flit |  <div align="center">[🔍](./pyprojecttoml.md)</div>| [📄](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)| |[Example](https://github.com/KnowledgeCaptureAndDiscovery/somef/blob/master/pyproject.toml) | 
| `requirements.txt` | Python                     | Lists Python package dependencies |  <div align="center">[🔍](./requirementstxt.md)</div>| [📄](https://pip.pypa.io/en/stable/reference/requirements-file-format/)| 25.2|[Example](https://github.com/oeg-upm/FAIR-Research-Object/blob/main/requirements.txt) |
| `setup.py`         | Python                     | Package file format used in python projects |  <div align="center">[🔍](./setuppy.md)</div>| [📄](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#setup-args)| |[Example](https://github.com/oeg-upm/soca/blob/main/setup.py) | 
| `DESCRIPTION`      | R                          | Metadata file for R packages including title, author, and version |  <div align="center">[🔍](./description.md)</div> | [📄](https://r-pkgs.org/description.html)| | [Example](https://github.com/cran/ggplot2/blob/master/DESCRIPTION) |
| `*.gemspec`        | Ruby                       | Manifest file serves as the package descriptor used in Ruby gem projects. | <div align="center">[🔍](./gemspec.md)</div>| [📄](https://guides.rubygems.org/specification-reference/)| |[Example](https://github.com/rubygems/rubygems/blob/master/bundler/bundler.gemspec) |
| `cargo.toml`       | Rust                       | Manifest file serves as the package descriptor used in Rust projects | <div align="center">[🔍](./cargo.md)</div> | [📄](https://doc.rust-lang.org/cargo/reference/manifest.html)| |[Example](https://github.com/rust-lang/cargo/blob/master/Cargo.toml) |
| `*.cabal`       | Haskell                       | Manifest file serving as the package descriptor for Haskell projects.| <div align="center">[🔍](./cabal.md)</div> | [📄](https://cabal.readthedocs.io/en/3.10/cabal-package.html)| |[Example](https://github.com/haskell/cabal/blob/master/Cabal/Cabal.cabal) |
| `dockerfile`       | Dockerfile                       | Build specification file for container images that can include software metadata via LABEL instructions (OCI specification).| <div align="center">[🔍](./dockerfiledoc.md)</div> | [📄](https://docs.docker.com/reference/dockerfile/)| |[Example](https://github.com/FairwindsOps/nova/blob/master/Dockerfile) |


> **Note:** The general principles behind metadata mapping in SOMEF are based on the [CodeMeta crosswalk](https://github.com/codemeta/codemeta/blob/master/crosswalk.csv) and the [CodeMeta JSON-LD context](https://github.com/codemeta/codemeta/blob/master/codemeta.jsonld).  
> However, each supported file type may have specific characteristics and field interpretations.




## Types of metadata in SOMEF

| Type                 | Metadata Category         |
|----------------------|---------------------------|
| Agent                | authors                   |
| Keywords             | keywords                  |
| License              | license                   |
| Release              | version                   |
| Software_application | requirements              |
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

```
        if project_data["dependencies"]:
            for dependency in project_data["dependencies"]:
                metadata_result.add_result(
                    constants.CAT_REQUIREMENTS, 
                    {
                        "value": f'{dependency.get("groupId", "")}.{dependency.get("artifactId", "")}'.strip("."),
                        "name": dependency.get("artifactId", ""),
                        "version": dependency.get("version", ""),
                        "type": constants.SOFTWARE_APPLICATION
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )
```


After applying the mapping logic, the metadata for the dependency is stored under the requirements category (CAT_REQUIREMENTS in this case) with the following JSON structure:

``` somef json 

    "requirements": [
        {
            "result": {
                "value": "org.apache.maven.maven-model",
                "name": "maven-model",
                "version": "3.9.0",
                "type": "Software_application"
            },
            "confidence": 1,
            "technique": "code_parser",
            "source": "https://raw.githubusercontent.com/dgarijo/Widoco/master/pom.xml"
        },
```
