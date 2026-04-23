The following metadata fields can be extracted from a codemeta.json file.   
These fields are defined in the [Codemeta specification](https://github.com/codemeta/codemeta/blob/master/crosswalk.csv), currently at version **3.0**, and are mapped according to the properties and classes defined in the CodeMeta vocabulary.

| Software metadata category    |    SOMEF metadata JSON path  | CODEMETA.JSON metadata file field          |
|-------------------------------|------------------------------|--------------------------------------------|
| application_domain        |   application_domain[i].result.value   |     applicationCategory      |
| author - value                   |   author[i].result.value |     author.name or author.givenName + author.familyName                   |
| author - email                   |   author[i].result.email                 |     author.email    |
| author - affiliation                  |   author[i].result.affiliation    |     author.affiliation  |
| author - identifier                   |   author[i].result.identifier     |     author.identifier or author.@id  |
| citation - value                 |   citation[i].result.value     |     referencePublication.name or referencePublication.title           |    
| citation - title                  |   citation[i].result.title     |      referencePublication.name or referencePublication.title            |    
| citation - url                  |   citation[i].result.url  |         referencePublication.url   |    
| citation - date published                  |   citation[i].result.date_published  |     referencePublication.datePublished        
| citation - doi                   |   citation[i].result.doi       |     referencePublication.identifier   | 
| code_repository           |   code_repository[i].result.value   |     codeRepository           |
| continuous_integration    |   continuous_integration[i].result.value |     contIntegration          |
| contributor - value   |   contributor[i].result.value |     contributor.givenName + contributor.familyName or just name if organization       |
| contributor - name  |   contributor[i].result.value |     contributor.givenName + contributor.familyName or just name if organization       |
| contributor - last_name  |   contributor[i].result.value |     contributor.familyName         |
| contributor - given_name  |   contributor[i].result.value |     contributor.givenName         |
| contributor - identifier  |   contributor[i].result.value |     contributor.@id          |
| contributor - email   |   contributor[i].result.value |     contributor.email         |
| date_created              |   date_created[i].result.value  |     dateCreated              |
| date_updated              |   date_updated[i].result.value   |     dateModified             |
| date_published            |   date_published[i].result .value   |     datePublished  |
| description               |   description[i].result.value   |     description                    |
| development_status       |   development_status[i].result.value  |     developmentStatus  |
| download_url              |   download_url[i].result.value          |     downloadUrl              |
| has_package_file         |   has_package_file[i].result.value         |   URL of the codemeta.json file |
| funding - funder          |   funding[i].result.funder       |     funder.@id or funder.name  *(1)*|    
| funding - funding         |   funding[i].result.funding     |     funding *(1)*| 
| funding - value	        |   funding[i].result.value	|   funding string or funder.name *(1)*|
| identifier               |   identifier[i].result.value       |     identifier                     |
| issue_tracker             |   issue_tracker[i].result.value           |     issueTracker             |
| keywords                  |   keywords[i].result.value          |     keywords                 |
| license - value                   |   license[i].result .value        |     license.name                   |
| license - url                  |   license[i].result.url          |     license.url                |
| license - spdx id                  |   license[i].result.spdx_id       |    license.identifier if "spdx.org/licenses/  |  
| license - identifier                  |   license[i].result.identifier   |  license.identifier or https://spdx.org/licenses/{license}  | 
| name                      |   name[i].result.value              |     name       |
| programming_languages - value     |   programming_languages[i].result.value    |     programmingLanguage.name |
| programming_languages - name     |   programming_languages[i].result.name |     programmingLanguage.name  |
| programming_languages - version     |   programming_languages[i].result.version |     programmingLanguage.version           |
| programming_languages - url     |   programming_languages[i].result.url |     programmingLanguage.url          |
| readme_url                |   readme_url[i].result.value       |     readme                    |
| requirements - value              |   requirements[i].result.value  |      softwareRequirements or softwareRequirements.name == softwareRequirements.version         |
| requirements - name              |   requirements[i].result.name   |    softwareRequirements or softwareRequirements.name or    softwareRequirements.identifier  |
| requirements - version              |   requirements[i].result.version                       |     softwareRequirements or softwareRequirements.version |
| version                   |   version[i].result.value   |     softwareVersion  or version        |


---

*(1)* 

- SOMEF json result: 

```
"funding": [
  {
    "result": {
      "value": "1549758; Codemeta: A Rosetta Stone for Metadata in Scientific Software",
      "type": "String",
      "funder": {
        "@id": "https://doi.org/10.13039/100000001",
        "@type": "Organization",
        "name": "National Science Foundation"
      },
      "funding": "1549758; Codemeta: A Rosetta Stone for Metadata in Scientific Software"
    },
    "confidence": 1,
    "technique": "code_parser",
    "source": "https://raw.githubusercontent.com/.../codemeta.json"
  }
]
```

- CODEMETA output: 
```
"funder": {
    "@id": "https://doi.org/10.13039/100000001",
    "@type": "Organization",
    "name": "National Science Foundation"
  },
"funding": "1549758; Codemeta: A Rosetta Stone for Metadata in Scientific Software",
```



