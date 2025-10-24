The following metadata fields can be extracted from a codemeta.json file.   
These fields are defined in the [Codemeta specification](https://w3id.org/codemeta/3.0), currently at version **3.0**, and are mapped according to the properties and classes defined in the CodeMeta vocabulary.

| SOMEF metadata category       | Category describes            |       SOMEF metadata field  | CODEMETA.JSON value          |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **application_domain**        |  String(application_domain[i].result is of type String)  | String.value   |     applicationCategory      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value                 |     author.name or author.givenName + author.familyName                   |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email                 |     author.email    |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.affiliation    |     author.affiliation  |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.identifier                             |     author.identifier or author.@id  |
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    Scholarly_article.value     |     referencePublication.name or referencePublication.title           |    
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    Scholarly_article.title     |      referencePublication.name or referencePublication.title            |    
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    Scholarly_article.url       |         referencePublication.url         |    
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    Scholarly_article.date_published  |     referencePublication.datePublished               |    
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    Scholarly_article.doi       |     referencePublication.identifier                  | 
| **code_repository**           |  Url (code_repository[i].result is of type Url)  |    Url.value   |     codeRepository           |
| **continuous_integration**    |  Url (continuous_integration[i].result is of type Url) |    Url.value |     contIntegration          |
| **date_created**              |   String (date_created[i].result is of type String) |    String.value  |     dateCreated              |
| **date_updated**              |  String (date_updated[i].result is of type String) |    String.value   |     dateModified             |
| **date_published**            |  String(date_published[i].result is of type String) |    String.value        datePublished  |
| **description**               |   String (description[i].result is of type String) |    String.value   |     description                    |
| **development_status**        |  String(development_status[i].result is of type String)|    String.value  |     developmentStatus  |
| **download_url**              |  Url (download_url[i].result is of type Url)   |    Url.value          |     downloadUrl              |
| **has_package_field**         |  Url(has_package_file[i].result is of type Url) |    Url.value         |   "codemeta.json" |
| **funding**                   |  String (funding[i].result is of type String)|    String.funder       |     funding.funder or funding.funder.name  |    
| **funding**                   |  String (funding[i].result is of type String)|    funding.funding     |     String.fundingIdentifier | 
| **identifier**                |  String (identifier[i].result is of type String)|    String.value       |     identifier                     |
| **issue_tracker**             |  Url (issue_tracker[i].result is of type Url)  |    Url.value           |     issueTracker             |
| **keywords**                  |  String(keywords[i].result is of type String) |    String.value          |     keywords                 |
| **license**                   |  License(license[i].result is of type License) |    License.value        |     license.name                   |
| **license**                   |  License(license[i].result is of type License) |    License.url          |     license.url                |
| **license**                   |  License(license[i].result is of type License)|    License.spdx_id       |    license.identifier if "spdx.org/licenses/  |  
| **license**                   |  License(license[i].result is of type License) |    License.identifier   |  license.identifier or https://spdx.org/licenses/{license}  | 
| **name**                      |  String (name[i].result is of type String)|    String.value              |     name                     |
| **programming_languages**       | Programming_languages (programming_languages[i].result is of type Programming_languages) |      Programming_languages.value                    |     programmingLanguage.name |
| **programming_languages**              | Programming_languages (programming_languages[i].result is of type Programming_languages) |      Programming_languages.name                     |     programmingLanguage.name        |
| **programming_languages**              | Programming_languages (programming_languages[i].result is of type Programming_languages) |     Programming_languages.version                   |     programmingLanguage.version           |
| **programming_languages**              | Programming_languages (programming_languages[i].result is of type Programming_languages) |     Programming_languages.url                       |     programmingLanguage.url          |
| **readme_url**                |  String (readme_url[i].result is of type String)|    String.value       |     readme                    |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application)  |    Software_application.value  |      softwareRequirements or softwareRequirements.name == softwareRequirements.version         |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |    Software_application.name   |    softwareRequirements or softwareRequirements.name or    softwareRequirements.identifier  |
| **requirements**              | Software_application (requirements[i].result is of type Software_application) |    Software_application.version                       |     softwareRequirements or softwareRequirements.version |
| **version**                 |  String (version[i].result is of type String)|    String.value   |     softwareVersion  or version        |
 