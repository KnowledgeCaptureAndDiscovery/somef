SOMEF supports three main output formats. Each of them contains different information with different levels of granularity. Below we enumerate them from more granular to less granular:

## JSON format
**Version:** 1.0.0

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
- `application_domain`: The application domain of the repository. This may be related to the research area of a software component (e.g., Astrophysics) or the general domain/functionality of the tool (i.e., machine learning projects)
- `acknowledgement`: Any text that the authors have prepared to acknnowledge the contribution from others, or project funding.
- `contributors`: Contributors to a software component
- `contributing guidelines`: Guidelines indicating how to contribute to a software component.
- `citation`: Software citation (usually in `.bib` form) as the authors have stated in their readme file, or through a `CFF` file.
- `code_of_conduct`: Link to the code of conduct file of the project
- `code_repository`: Link to the source code (typically the repository where the readme can be found)
- `contact`: Contact person responsible for maintaining a software component.
- `description`: A description of what the software does
- `documentation`: Where to find additional documentation about a software component.
- `download_url`: URL where to download the target software (typically the installer, package or a tarball to a stable version)
- `executable_example`: Jupyter notebooks ready for execution (e.g., through myBinder)
- `faq`: Frequently asked questions about a software component
- `forks_count`: Number of forks of the project at the time of the extraction.
- `forks_url`: Links to forks made of the project (GitHub only)
- `full_name`: Name + owner (owner/name) (if available)
- `full_title`: If the repository has a short name, we will attempt to extract the longer version of the repository name. For example, a repository may be called "Widoco", but the longer title is "Wizard for documenting ontologies".
- `has_build_file`: Build file to create a Docker image for the target software
- `has_executable_notebook`: Jupyter notebooks included in a repository. 
- `has_script_file`: Snippets of code contained in the repository.
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
- `programming_languages`: Languages used in the repository.
- `readme_url`: URL to the main README file in the repository.
- `releases`: Pointer to the available versions of a software component.
- `repository_status`: Repository status as it is described in [repostatus.org](https://www.repostatus.org/).
- `requirements`: Pre-requisites and dependencies needed to execute a software component.
- `stargazers_count`: Total number of stargazers of the project.
- `support`: Guidelines and links of where to obtain support for a software component.
- `support_channels`: Help channels one can use to get support about the target software component.
- `usage`: Usage examples and considerations of a code repository.

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
      "url": "https://arxiv.org/pdf/2006.00088.pdf"
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
- `License`: object representing all the metadata SOMEF extracts from a license.
- `Agent`: user (typically, a person) or organization responsible for authoring a software release or a paper.
- `Publication`: Scientific paper associated with the code repository.

The following literal types are currently supported:
- `Number`: A numerical value. We do not distinguish between integer or float.
- `Date`: Dates in xsd:date format.
- `String`: Any representation in text that is not considered a number, date or url.
- `Url`: uniform resource locator of a file.
- `Text_excerpt`: The value is a string that has been extracted from a file.

The table below summarizes all types and their corresponding properties:

| Property | Describes | Expected value | Definition |
|---|---|---|---|
| **author** | Release, Publication | Agent,  Organization | Person or organization responsible for creating an article or a software release. |
| **doi** | Publication | Url | When a publication is detected, but the format is in bibtek or CFF, SOMEF will add a `doi`  field with the detected DOI value. The result includes a full URL. |
| **description** | Release | String | Descriptive text with the purpose of the release |
| **date_created** | Release | Date | Date of creation of a release |
| **date_published** | Release | Date | Date of publication of a release |
| **html_url** | Release | Url | link to the HTML representation of a release |
| **name** | License, Release,  User, Publication | String | Title or name used to designate the release, license user or publication. |
| **original_header** | Text_excerpt | String | If the result value is extracted from a markdown file like a README, the original header of that section is also returned. |
| **parent_header** | Text_excerpt | String | If the result value is extracted from a markdown file like a README, the parent header of the current section is also returned (in case it exists). |
| **tag** | Release | String | named version of a release |
| **url** | Release, Publication | Url | Uniform resource locator of the resource |
| **zipball_url** | Release | Url | URL to the zip file where to download a software release |
| **tarball_url** | Release | Url | URL to the tar ball file where to download a software release |


### Format
The following formats for a result value are currently recognized:
- `bibtex`: format typically used to [document bibliography](https://www.bibtex.com/g/bibtex-format/) in LateX projects.
- `cff`: [Citation file format](https://citation-file-format.github.io/), an increasingly popular format for citing software projects.
- `jupyter_notebook`: [computational notebooks](https://ipython.org/ipython-doc/3/notebook/nbformat.html) typically used in data science.
- `dockerfile`: [Docker files](https://docs.docker.com/engine/reference/builder/) used to build Docker images.
- `docker_compose`: [orchestration file](https://docs.docker.com/compose/compose-file/) used to communicate multiple containers.
- `readthedocs`: documentation format used by many repositories in order to describe their projects.
- `wiki`: documentation format used in GitHub repositories.

### Technique
The techniques can be of several types: 
- `header_analysis`: the result was extracted by analyzing the headers used in the README file and assessing their proximity to commonly used headers (and other synonims).
- `supervised_classification`: the results were obtained after running text classifiers trained for detecting that type of header.
- `file_exploration`: the result comes from an exploration of the files in the repository
- `GitHub_API`: the result was obtained from the GitHub API.
- `GitLab_API`: the result was obtained from the GitLab API.
- `regular_expression`: the result was obtained after performing regular expressions on the files in the repository.
- `code_parser`: the result was obtained from code configuration files with metadata markup. 

### Missing categories
If SOMEF is run with the `-m` flag, a report of the categories that the program was not able to find is returned. The format for this field is slightly different than the rest, providing a list of the missing categories. An example can be seen below:

```json
"missing_categories": [
  "description", 
  "citation"
]
```
Meaning that SOMEF was not able to find a description or a citation in the target repository. Missing categories will not be added in Codemeta and Turtle exports.


## Turtle format 
RDF represents information in triples (subject, predicate and object), where the subject is the entity to be described (in this case a code repository), the predicate is the property describing the subject (e.g., `description`) and the object is the value obtained (which can be an object or a literal). Representing the provenance information returned by SOMEF is therefore challenging, and would require adopting reification mechanisms that make the output more complex. Therefore we simplify the output by providing our best guess for each of the extracted fields.

Our RDF representation uses the [Software Description Ontology](https://w3id.org/okn/o/sd/). The `excerpt` and `confidence` fields are ommitted in this representation (every category with confidence above the threshold specified when running SOMEF will be included in the results). 

## Codemeta format 
JSON-LD representation following the [Codemeta specification](https://codemeta.github.io/) (which itself extends [Schema.org](https://schema.org/)). The `excerpt` and `confidence` fields are ommitted in this representation (every category with confidence above the threshold specified when running SOMEF will be included in the results). In addition, any metadata category outside from what is defined in Codemeta will be avoided.
