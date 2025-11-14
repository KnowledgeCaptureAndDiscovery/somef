SOMEF supports three main output formats. Each of them contains different information with different levels of granularity. Below we enumerate them from more granular to less granular:

## JSON format
**Version:** 1.0.1

Default SOMEF response (and more complete in terms of metadata). The JSON format returns a set of categories, as shown in the snippet below:

```json
{
  "<categoryName>": [
    {
      ...
    }
  ],
  "<categoryName2>": [
    {
      ...
    }
  ],
  "somef_provenance":{    
    "date": "2022-05-20 12:00:00",
    "somef_version": "0.9.1", 
    "somef_schema_version":"1.0.0"
  }
}
```
In the snippet, each `<categoryName>` corresponds to the different categories SOMEF was able to find. An additional JSON field called `somef_provenance` returns provenance information of the SOMEF execution. The `somef_provenance` field always has the same two properties, as shown in the table below:

| Property | Mandatory? | Expected value | Definition |
|---|---|---|---|
| **date** | Yes | Date | Date when the extraction was performed. Knowing the date is critical, as a repository may change its README file. |
| **somef_version** | Yes | String | Version of SOMEF used to extract metadata from a code repository. |
| **somef_schema_version** | Yes | String | Version of SOMEF schema used to represent the JSON output format. |

!!! info
    If a property is `mandatory` then it will always be returned in the  output JSON.

### Category
Each extracted metadata category is returned as a list, which contains the number of results SOMEF found about that category when exploring a code repository. For example, the snippet below shows a repository with two descriptions (a short one extracted from the GitHub API and a longer one extracted from the README file). SOMEF aims to return both of them:

```json
"description": [
  {
    "result": {
        "value": "KGTK is a Python library ...",
        "type": "text"
    },
    "confidence": 0.8294290479925978,
    "technique": "Supervised classification",
    "source": "<url to readme file>"
  },
  {
    "result": {
        "value": "Python library for large KG manipulation",
        "type": "text"
    },
    "confidence": 1,
    "technique": "GitHub API"
  }
]
```
For each element of the list, SOMEF returns a `result` object, together with its `confidence` value, the `technique` used in the extraction and the `source` file where it's coming from (in case there is one). For example, in the snippet above, SOMEF extracted a description from the README file of the repository using supervised classification, and a short description using the GitHub API.

The `confidence` depends on the `technique` used. In this case, the confidence is driven by the classifier which makes the prediction. For the GitHub API the confidence is higher, as it was a description added manually by the authors.

SOMEF aims to recognize the following categories (in alphabetical order):

- `acknowledgement`: Any text that the authors have prepared to acknnowledge the contribution from others, or project funding.
- `application_domain`: The application domain of the repository. This may be related to the research area of a software component (e.g., Astrophysics) or the general domain/functionality of the tool (i.e., machine learning projects). See all current recognized application domains [here](https://somef.readthedocs.io/en/latest/#myfootnote1).
- `authors`: Person or organization responsible of the project. This property is also used to indicate the responsible entities of a publication associated with the code repository.
- `citation`: Software citation (usually in `.bib` form) as the authors have stated in their readme file, or through a `CFF` file.
- `code_of_conduct`: Link to the code of conduct file of the project
- `code_repository`: Link to the source code (typically the repository where the readme can be found)
- `contact`: Contact person responsible for maintaining a software component.
- `continuous_integration`: Link to continuous integration service, supported on GitHub as well as in GitLab.
- `contributing guidelines`: Guidelines indicating how to contribute to a software component.
- `contributors`: Contributors to a software component
- `date_created`: Date when the software component was created.
- `date_updated`: Date when the software component was last updated (note that this will always be older than the date of the extraction).
- `description`: A description of what the software component does.
- `development_status`: The project’s development stage: beta, deprecated...
- `documentation`: Where to find additional documentation about a software component.
- `download_url`: URL where to download the target software (typically the installer, package or a tarball to a stable version)
- `executable_example`: Jupyter notebooks ready for execution (e.g., through myBinder, colab or files)
- `faq`: Frequently asked questions about a software component
- `forks_count`: Number of forks of the project at the time of the extraction.
- `forks_url`: Links to forks made of the project (GitHub only)
- `full_name`: Name + owner (owner/name) (if available)
- `full_title`: If the repository has a short name, we will attempt to extract the longer version of the repository name. For example, a repository may be called "Widoco", but the longer title is "Wizard for documenting ontologies".
- `has_build_file`: Build file to create a Docker image for the target software 
- `has_script_file`: Snippets of code contained in the repository.
- `homepage`: URL of the item.
- `identifier`: Identifiers detected within a repository (e.g., Digital Object Identifier).
- `images`: Images used to illustrate the software component.
- `installation`: A set of instructions that indicate how to install a target repository
- `invocation`: Execution command(s) needed to run a scientific software component
- `issue_tracker`: Link where to open issues for the target repository
- `keywords`: set of terms used to commonly identify a software component
- `license`: License and usage terms of a software component
- `logo`: Main logo used to represent the target software component.
- `name`: Name identifying a software component
- `ontologies`: URL and path to the ontology files present in the repository.
- `owner`: Name of the user or organization in charge of the repository
- `package_distribution`: Link to official package repositories where the software can be downloaded from (e.g., `pypi`).
- `package_file`: Link to a package file used in the repository (e.g., `pyproject.toml`, `setup.py`).
- `programming_languages`: Languages used in the repository.
- `readme_url`: URL to the main README file in the repository.
- `related_papers`: URL to possible related papers within the repository stated within the readme file.
- `releases`: Pointer to the available versions of a software component.
- `repository_status`: Repository status as it is described in [repostatus.org](https://www.repostatus.org/).
- `requirements`: Pre-requisites and dependencies needed to execute a software component.
- `run`: Running instructions of a software component. It may be wider than the `invocation` category, as it may include several steps and explanations.
- `stargazers_count`: Total number of stargazers of the project.
- `support`: Guidelines and links of where to obtain support for a software component.
- `support_channels`: Help channels one can use to get support about the target software component.
- `type`: Software type: Commandline Application, Notebook Application, Ontology, Scientific Workflow. Non-Software types: Static Website, Uncategorized
- `usage`: Usage examples and considerations of a code repository.
- `workflows`: URL and path to the computational workflow files present in the repository.
- `homepage`: URL to the homepage of the software or organization.
- `reference_publication`: URL to the paper associated with the code repository.
- `package_id`: Identifier extracted from packages. (e.g., `packages.json`)
-  `funding`: Funding code for the related project.
- `has_package_file`: Specifies what package file is present in the code repository.

The following table summarized the properties used to describe a `category`:

| Property | Mandatory? | Expected value | Definition |
|---|---|---|---|
| **confidence** | Yes | Number | Value ranging from 0 (very low)  to 1 (very high) indicating the confidence of the program in the quality of the extraction. |
| **result** | Yes | Result | Result obtained from the extraction in a code repository |
| **source** | No | Url | URL of the source file used for the extraction. |
| **technique** | Yes | String | Technique used for the extraction. One of the following list: Supervised classification, header analysis, regular expression, GitHub API, File exploration, Code parsing |

### Result
Field returning the extracted output from the code repository. An example can be seen below for a citation found in BibteX format in a README file of a code repository:

```json
"citation": [
  {
    "result": {
      "value": "@inproceedings{ilievski2020kgtk,\n  title={{KGTK}: A Toolkit for Large Knowledge Graph Manipulation and Analysis}},\n  author={Ilievski, Filip and Garijo, Daniel and Chalupsky, Hans and Divvala, Naren Teja and Yao, Yixiang and Rogers, Craig and Li, Ronpeng and Liu, Jun and Singh, Amandeep and Schwabe, Daniel and Szekely, Pedro},\n  booktitle={International Semantic Web Conference},\n  pages={278--293},\n  year={2020},\n  organization={Springer}\n  url={https://arxiv.org/pdf/2006.00088.pdf}\n}",
      "format": "bibtex",
      "type": "string",
      "title": "{KGTK}: A Toolkit for Large Knowledge Graph Manipulation and Analysis",
      "url": "https://arxiv.org/pdf/2006.00088.pdf",
      "original_header": "citation"
    },
    "confidence": 1.0,
    "technique": "Regular expression",
    "source": "<url to README file>"
  }
]
```

A result may have the following fields:

| Property | Mandatory? | Expected value | Definition |
|---|---|---|---|
| **format** | No | String | Format in which the value is returned. For example, it may be a Dockerfile, a jupyter notebook, or a citation in BibteX.
| **type** | Yes | String | Text indicating the value type of the result. In some cases it refers to the type of literal being returned, while in others it refers to the type of the object. For example, a  `license` may be detected as a URL, as a text excerpt detected from a file, or as an object with both name and url. |
| **value** | Yes | String, Number, Date or Url | Text with the result of the extraction performed by SOMEF. The value is always a single object, not a list. |


Depending on the `type` of the result, additional properties may be found. 

The following object `types` are currently supported:

- `Release`: software releases of the current code repository, as available from GitHub.
- `Programming_language`: Programming language used in the repository. 
- `License`: object representing all the metadata SOMEF extracts from a license.
- `Agent`: user (typically, a person) or organization responsible for authoring a software release or a paper.
- `Publication`: Scientific paper associated with the code repository.
- `SoftwareApplication`: Class to represent software dependencies between projects.
- `Runtime_platform`: specifies runtime platform or script interpreter dependencies required to run the project..
The following literal types are currently supported:

- `Number`: A numerical value. We do not distinguish between integer, long or float.
- `Date`: Dates in xsd:date format.
- `String`: Any representation in text that is not considered a number, date or url. There are two special types of strings.
  - `Text_excerpt`: The value is a string that has been extracted from a file.
  - `File_dump`: The  value is a string with the contents of a file (e.g., a `citation.cff` file, or a `license.md` file).
- `Url`: uniform resource locator of a file.


<!-- |
The table below summarizes all types and their corresponding properties:

| Property | Describes | Expected value | Definition |
|---|---|---|---|
| **author** | Release, Publication | Agent,  Organization | Person or organization responsible for creating an article or a software release. |
| **doi** | Publication | Url | When a publication is detected, but the format is in bibtek or CFF, SOMEF will add a `doi`  field with the detected DOI value. The result includes a full URL. |
| **description** | Release | String | Descriptive text with the purpose of the release |
| **date_created** | Release | Date | Date of creation of a release |
| **date_published** | Release | Date | Date of publication of a release |
| **email** | Agent | String | Email of an author |
| **family_name** | Agent | String | Last name of an author |
| **given_name** | Agent | String | First name of an author |
| **html_url** | Release | Url | link to the HTML representation of a release |
| **name** | License, Release,  User, Programming_language | String | Title or name used to designate the release, license user or programming language. |
| **original_header** | Text_excerpt | String | If the result value is extracted from a markdown file like a README, the original header of that section is also returned. |
| **parent_header** | Text_excerpt | [String] | If the result value is extracted from a markdown file like a README, the parent header(s) of the current section are also returned (in case they exist). |
| **release_id** | Release | String | Id of a software release. |
| **size** | Programming_language | Number | File size content (bytes) of a code repository using a given programming language |
| **spdx_id** | License | String | Spdx id corresponding to this license |
| **tag** | Release | String | named version of a release |
| **tarball_url** | Release | Url | URL to the tar ball file where to download a software release |
| **title** | Publication | String | Title of the publication |
 **url** | Release, Publication, License, Agent | Url | Uniform resource locator of the resource |
| **zipball_url** | Release | Url | URL to the zip file where to download a software release | -->


The tables below summarizes all types and their corresponding properties-

An AGENT has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **email** | String | Email of an author |
| **family_name** | String | Last name of an author |
| **given_name** | String | First name of an author |
| **name** | String | Name used to designate the person or organization|
| **url** | Url | Uniform resource locator of the resource |
| **affiliation** | String | name of organization or affiliation  |
| **identifier** | String | id of an agent  |
| **role** | String | role of agent  |

An ASSET has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **content_size** | Integer | size of file |
| **content_url** | String | direct download link for the release file |
| **download_count** | Integer | numbers of downloads |
| **encoding_format** | String | format of the file |
| **name** | String | Title or name of the file |
| **upload_date** | Date | Date of creation of a release |
| **url** |  Url | Uniform resource locator of the resource |



A LICENSE has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **name** | String | Title or name of the license |
| **spdx_id** | String | Spdx id corresponding to this license |
| **url** |  Url | Uniform resource locator of the license |
| **identifier** |  String | id of licence |

A PROGRAMMING_LANGUAGE has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **name** | String | Name of the language |
| **size** | Integer | File size content (bytes) of a code repository using a given programming language |


A PUBLICATION has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **author** | Agent,  Organization | Person or organization responsible for creating an article or a software release. |
| **doi** | Url | When a publication is detected, but the format is in bibtek or CFF, SOMEF will add a `doi`  field with the detected DOI value. The result includes a full URL. |
| **title** | String | Title of the publication |
| **url** | Url | Uniform resource locator of the resource |


A RELEASE has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **assets** |  Asset  | Files attached to the release
| **author** | Agent,  Organization | Person or organization responsible for creating an article or a software release. |
| **description** | String | Descriptive text with the purpose of the release |
| **date_created** | Date | Date of creation of a release |
| **date_published** | Date | Date of publication of a release |
| **html_url** | Url | link to the HTML representation of a release |
| **name** | String | Title or name used to designate the release, license user or programming language. |
| **release_id** | String | Id of a software release. |
| **tag** | String | named version of a release |
| **tarball_url** | Url | URL to the tar ball file where to download a software release |
| **url** | Url | Uniform resource locator of the resource |
| **zipball_url** | Url | URL to the zip file where to download a software release |


<!-- A REQUIREMENTS has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **name** | String | Name of the requeriment |
| **version** | String | named version of a requeriment |
| **dependency_type** | String | type: dev, runtime... | -->


A RUNTIME_PLATFORM has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **name** | String | Name of the runtime platform (e.g., Java) |
  **version** | String | version of the runtime platform |
| **value** | String | name and version of the runtime platform |


A SCHOLARLY_ARTICLE has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **title** | String | Title of reference or citation |
| **value** | String | Title of reference or citation |
| **url** | String | Link to reference or citation |
| **date_published** | String | date of publication reference or citation |
| **doi** | String | Identifier of reference|


A SOFTWARE_APPLICATION has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **name** | String | Name of the software |
| **value** | String | Name and version of the software |
| **version** | String | version of software |
| **development_type** | String | runtime or dev |

A TEXT_EXCERPT has the following properties:

| Property | Expected value | Definition |
|---|---|---|
| **original_header** | String | If the result value is extracted from a markdown file like a README, the original header of that section is also returned. |
| **parent_header** | [String] | If the result value is extracted from a markdown file like a README, the parent header(s) of the current section are also returned (in case they exist). |



### Format
The following formats for a result value are currently recognized:

- `bibtex`: format typically used to [document bibliography](https://www.bibtex.com/g/bibtex-format/) in LateX projects.
- `cff`: [Citation file format](https://citation-file-format.github.io/), an increasingly popular format for citing software projects.
- `jupyter_notebook`: [computational notebooks](https://ipython.org/ipython-doc/3/notebook/nbformat.html) typically used in data science.
- `dockerfile`: [Docker files](https://docs.docker.com/engine/reference/builder/) used to build Docker images.
- `docker_compose`: [orchestration file](https://docs.docker.com/compose/compose-file/) used to communicate multiple containers.
- `readthedocs`: documentation format used by many repositories in order to describe their projects.
- `wiki`: documentation format used in GitHub repositories.
- `setup.py`: package file format used in python projects.
- `pyproject.toml`: package file format used in python projects.
- `pom.xml`: package file used in Java projects.
- `package.json`: package file used in Javascript projects.
- `bower.json`: package descriptor used for configuring packages that can be used as a dependency for Bower-managed front-end projects.
- `composer.json`: manifest file serves as the package descriptor used in PHP projects.
- `cargo.toml.json`: manifest file serves as the package descriptor used in Rust projects.
- `[name].gemspec`:manifest file serves as the package descriptor used in Ruby gem projects.


### Technique
The techniques can be of several types: 

- `code_parser`: the result was obtained from parsing package files with metadata. 
- `header_analysis`: the result was extracted by analyzing the headers used in the README file and assessing their proximity to commonly used headers (and other synonims).
- `file_exploration`: the result comes from an exploration of the files in the repository
- `GitHub_API`: the result was obtained from the GitHub API.
- `GitLab_API`: the result was obtained from the GitLab API.
- `regular_expression`: the result was obtained after performing regular expressions on the files in the repository.
- `software_type_heuristics`: the result was obtained from analysis of the repository based on various heuristics from the README, code and extension analysis. 
- `supervised_classification`: the results were obtained after running text classifiers trained for detecting that type of header.


### Missing categories
If SOMEF is run with the `-m` flag, a report of the categories that the program was not able to find is returned. The format for this field is slightly different than the rest, providing a list of the missing categories. An example can be seen below:

```json
"somef_missing_categories": [
  "description", 
  "citation"
]
```
In this case, SOMEF was not able to find a description or a citation in the target repository. Missing categories will not be added in Codemeta and Turtle exports. Note that the prefix `somef` is added in the field, to indicate that this is a special type of category.


## Turtle format 
RDF represents information in triples (subject, predicate and object), where the subject is the entity to be described (in this case a code repository), the predicate is the property describing the subject (e.g., `description`) and the object is the value obtained (which can be an object or a literal). Representing the provenance information returned by SOMEF is therefore challenging, and would require adopting reification mechanisms that make the output more complex. Therefore we simplify the output by providing our _best guess_ for each of the extracted fields. This is done by analyzing the results, comparing those that may be redundant or come from the same files, and removing those with low confidence or included in other fields.

Our RDF representation uses the [Software Description Ontology](https://w3id.org/okn/o/sd/). The `result`, `provenance` and `confidence` fields are ommitted in this representation (every category with confidence above the threshold specified when running SOMEF will be included in the results). 

Below you can see an example of a software represented in sd:
```
@prefix ns1: <https://w3id.org/okn/o/sd#> .
@prefix ns2: <https://schema.org/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

## SOFTWARE METADATA

<https://w3id.org/okn/i/Software/mapeathor> a ns1:Software ;
    ns2:license <https://w3id.org/okn/i/License/mapeathor> ;
    ns1:contactDetails """- [Ana Iglesias-Molina](https://github.com/anaigmo) - [ana.iglesiasm@upm.es](mailto:ana.iglesiasm@upm.es)...
""" ;
    ns1:dateCreated "2019-06-09T19:45:24+00:00"^^xsd:dateTime ;
    ns1:dateModified "2022-11-03T15:19:23+00:00"^^xsd:dateTime ;
    ns1:description "Translator of spreadsheet mappings into R2RML, RML or YARRRML";
    ns1:hasBuildFile "https://raw.githubusercontent.com/oeg-upm/mapeathor/master/Dockerfile"^^xsd:anyURI,
    ns1:hasDocumentation "https://github.com/oeg-upm/Mapeathor/wiki"^^xsd:anyURI ;
    ns1:hasDownloadUrl "https://github.com/oeg-upm/mapeathor/releases"^^xsd:anyURI ;
    ns1:hasExecutableInstructions """The easiest way of running Mapeathor is using the [web service](https://morph.oeg.fi.upm.es/demo/mapeathor) and the [Swagger](https://morph.oeg.fi.upm.es/tool/mapeathor/swagger/) instance. For CLI lovers, the service is available as a [PyPi package](https://pypi.org/project/mapeathor/) and Docker image. The instructions of the latest can be found in the [wiki](https://github.com/oeg-upm/Mapeathor/wiki).
""" ;
    ns1:hasLongName "Mapeathor" ;
    ns1:hasSourceCode <https://w3id.org/okn/i/SoftwareSource/mapeathor> ;
    ns1:hasUsageNotes """##Example
A more detailed explanation is provided in the [wiki](https://github.com/oeg-upm/Mapeathor/wiki);
    ns1:hasVersion <https://w3id.org/okn/i/Release/21580066>;
    ns1:identifier "https://doi.org/10.5281/zenodo.5973906"^^xsd:anyURI ;
    ns1:issueTracker "https://api.github.com/repos/oeg-upm/mapeathor/issues"^^xsd:anyURI ;
    ns1:keywords "data-integration, knowledge-graph, r2rml, rml" ;
    ns1:name "oeg-upm/mapeathor" ;
    ns1:readme "https://raw.githubusercontent.com/oeg-upm/mapeathor/master/README.md"^^xsd:anyURI .

## LICENSE INFORMATION

<https://w3id.org/okn/i/License/mapeathor> a ns2:CreativeWork ;
    owl:sameAs <https://spdx.org/licenses/Apache-2.0> ;
    ns1:name "Apache License 2.0" ;
    ns1:url "https://raw.githubusercontent.com/oeg-upm/mapeathor/master/LICENSE"^^xsd:anyURI .

## INFORMATION ON RELEASES

<https://w3id.org/okn/i/Release/21580066> a ns1:SoftwareVersion ;
    ns1:author <https://w3id.org/okn/i/Agent/anaigmo> ;
    ns1:dateCreated "2019-11-08T15:24:55+00:00"^^xsd:dateTime ;
    ns1:datePublished "2019-11-19T10:26:47+00:00"^^xsd:dateTime ;
    ns1:downloadUrl "https://api.github.com/repos/oeg-upm/mapeathor/tarball/v1.0"^^xsd:anyURI,
        "https://api.github.com/repos/oeg-upm/mapeathor/zipball/v1.0"^^xsd:anyURI,
        "https://github.com/oeg-upm/mapeathor/releases/tag/v1.0"^^xsd:anyURI ;
    ns1:hasVersionId "v1.0" ;
    ns1:name "First template" ;
    ns1:url "https://api.github.com/repos/oeg-upm/mapeathor/releases/21580066"^^xsd:anyURI .

## INFORMATION ON SOURCE CODE
<https://w3id.org/okn/i/SoftwareSource/mapeathor> a ns2:SoftwareSourceCode ;
    ns1:codeRepository "https://github.com/oeg-upm/mapeathor"^^xsd:anyURI ;
    ns1:name "oeg-upm/mapeathor" ;
    ns1:programmingLanguage "Dockerfile",
        "Python" .

## INFORMATION ON AUTHORS
<https://w3id.org/okn/i/Agent/anaigmo> a ns2:Person ;
    ns2:name "anaigmo" .

```
As shown in the Turtle snippet above, SOMEF represents the software as an entity, its relationship with each release (software version), the license found in the repository and the Person who owns it.

## Codemeta format 
JSON-LD representation following the [Codemeta specification](https://codemeta.github.io/) (which itself extends [Schema.org](https://schema.org/)). The `result`, `provenance` and `confidence` fields are ommitted in this representation (every category with confidence above the threshold specified when running SOMEF will be included in the results). In addition, any metadata category outside from what is defined in Codemeta will be avoided.
