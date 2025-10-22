The following metadata fields can be extracted from a codemeta.json file.   
These fields are defined in the [Codemeta specification](https://w3id.org/codemeta/3.0), currently at version **3.0**, and are mapped according to the properties and classes defined in the CodeMeta vocabulary.

| SOMEF metadata category       | SOMEF metadata field                       | CODEMETA.JSON value          |
|-------------------------------|--------------------------------------------|------------------------------|
| **application_domain**        |  application_domain.value                  |     applicationCategory      |
| **authors**                   |  authors.value                             |     author.name or author.givenName + author.familyName                   |
| **authors**                   |  authors.email                             |     author.email                  |
| **authors**                   |  authors.affiliation                             |     author.affiliation                   |
| **authors**                   |  authors.identifier                             |     author.identifier or author.@id                   |
| **citation**                  |  citation.value                            |     referencePublication.name or referencePublication.title           |    
| **citation**                  |  citation.title                            |      referencePublication.name or referencePublication.title            |    
| **citation**                  |  citation.url                              |         referencePublication.url         |    
| **citation**                  |  citation.date_published                   |     referencePublication.datePublished               |    
| **citation**                  |  citation.doi                              |     referencePublication.identifier                  | 
| **code_repository**           |  code_repository.value                     |     codeRepository           |
| **continuous_integration**    |  continuous_integration.value              |     contIntegration          |
| **date_created**              |  date_created.value                        |     dateCreated              |
| **date_updated**              |  date_updated.value                        |     dateModified             |
| **date_published**            |  date_published.value                      |     datePublished            |
| **description**               |  description.value                         |     description                    |
| **development_status**        |  development_status.value                  |     developmentStatus                       |
| **download_url**              |  download_url.value                        |     downloadUrl              |
| **funding**                   |  funding.funder                            |     funding.funder or funding.funder.name             |    
| **funding**                   |  funding.funding                           |     funding.fundingIdentifier                        |
| **identifier**                |  identifier.value                          |     identifier                     |
| **issue_tracker**             |  issue_tracker.value                       |     issueTracker             |
| **keywords**                  |  keywords.value                            |     keywords                 |
| **license**                   |  license.value                           |     license.name                   |
| **license**                   |  license.url                           |     license.url                |
| **license**                   |  license.identifier                        |  license.identifier or https://spdx.org/licenses/{license}               |
| **license**                   |  license.spdx_id                        |    license.identifier if "spdx.org/licenses/                 |  
| **name**                      |  name.value                                |     name                     |
| **programming_languages**              |  programming_languages.value                     |     programmingLanguage.name          |
| **programming_languages**              |  programming_languages.name                     |     programmingLanguage.name        |
| **programming_languages**              |  programming_languages.version                   |     programmingLanguage.version           |
| **programming_languages**              |  programming_languages.url                       |     programmingLanguage.url          |
| **readme_url**                |  readme_url.value                          |     readme                    |
| **requirements**              |  requirements.value                       |      softwareRequirements or softwareRequirements.name ==     softwareRequirements.version         |
| **requirements**              |  requirements.name                      |    oftwareRequirements or softwareRequirements.name or    softwareRequirements.identifier              |
| **requirements**              |  requirements.version                       |     softwareRequirements or softwareRequirements.version            |
| **version**                   |  version.value                             |     softwareVersion          |
| **version**                   |  version.value                             |     version                    |