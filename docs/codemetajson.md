The following metadata fields can be extracted from a codemeta.json file.   
These fields are defined in the [Codemeta specification](https://github.com/codemeta/codemeta/blob/master/crosswalk.csv), currently at version **3.0**, and are mapped according to the properties and classes defined in the CodeMeta vocabulary.

| SOMEF metadata category       | Expected value type            |       SOMEF metadata field  | CODEMETA.JSON metadata field          |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **application_domain**        |  String(application_domain[i].result is of type String)  | application_domain[i].result.value   |     applicationCategory      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.value |     author.name or author.givenName + author.familyName                   |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.email                 |     author.email    |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.affiliation    |     author.affiliation  |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.identifier     |     author.identifier or author.@id  |
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    citation[i].result.value     |     referencePublication.name or referencePublication.title           |    
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    citation[i].result.title     |      referencePublication.name or referencePublication.title            |    
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    citation[i].result.url  |         referencePublication.url   |    
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    citation[i].result.date_published  |     referencePublication.datePublished        
| **citation**                  |  Scholarly_article (citation[i].result is of type Scholarly_article) |    citation[i].result.doi       |     referencePublication.identifier   | 
| **code_repository**           |  Url (code_repository[i].result is of type Url)  |    code_repository[i].result.value   |     codeRepository           |
| **continuous_integration**    |  Url (continuous_integration[i].result is of type Url) |    continuous_integration[i].result.value |     contIntegration          |
| **date_created**              |   String (date_created[i].result is of type String) |    date_created[i].result.value  |     dateCreated              |
| **date_updated**              |  String (date_updated[i].result is of type String) |    date_updated[i].result.value   |     dateModified             |
| **date_published**            |  String(date_published[i].result is of type String) |    date_published[i].result .value   |     datePublished  |
| **description**               |   String (description[i].result is of type String) |    description[i].result.value   |     description                    |
| **development_status**        |  String(development_status[i].result is of type String)|    development_status[i].result.value  |     developmentStatus  |
| **download_url**              |  Url (download_url[i].result is of type Url)   |    download_url[i].result.value          |     downloadUrl              |
| **has_package_file**         |  Url(has_package_file[i].result is of type Url) |    has_package_file[i].result.value         |   URL of the codemeta.json file |
| **funding**                   |  String (funding[i].result is of type String)|    funding[i].result.funder       |     funding.funder or funding.funder.name  |    
| **funding**                   |  String (funding[i].result is of type String)|    funding[i].result.funding     |     String.fundingIdentifier | 
| **identifier**                |  String (identifier[i].result is of type String)|    identifier[i].result.value       |     identifier                     |
| **issue_tracker**             |  Url (issue_tracker[i].result is of type Url)  |   issue_tracker[i].result.value           |     issueTracker             |
| **keywords**                  |  String(keywords[i].result is of type String) |    keywords[i].result.value          |     keywords                 |
| **license**                   |  License(license[i].result is of type License) |    license[i].result .value        |     license.name                   |
| **license**                   |  License(license[i].result is of type License) |    license[i].result .url          |     license.url                |
| **license**                   |  License(license[i].result is of type License)|    license[i].result .spdx_id       |    license.identifier if "spdx.org/licenses/  |  
| **license**                   |  License(license[i].result is of type License) |    license[i].result .identifier   |  license.identifier or https://spdx.org/licenses/{license}  | 
| **name**                      |  String (name[i].result is of type String)|    name[i].result .value              |     name       |
| **programming_languages**     | Programming_languages (programming_languages[i].result is of type Programming_languages) |      programming_languages[i].result.value    |     programmingLanguage.name |
| **programming_languages**     | Programming_languages (programming_languages[i].result is of type Programming_languages) |      programming_languages[i].result.name |     programmingLanguage.name  |
| **programming_languages**     | Programming_languages (programming_languages[i].result is of type Programming_languages) |     programming_languages[i].result.version |     programmingLanguage.version           |
| **programming_languages**     | Programming_languages (programming_languages[i].result is of type Programming_languages) |     programming_languages[i].result.url |     programmingLanguage.url          |
| **readme_url**                |  String (readme_url[i].result is of type String)|    readme_url[i].result.value       |     readme                    |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application)  |    requirements[i].result.value  |      softwareRequirements or softwareRequirements.name == softwareRequirements.version         |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |    requirements[i].result.name   |    softwareRequirements or softwareRequirements.name or    softwareRequirements.identifier  |
| **requirements**              | Software_application (requirements[i].result is of type Software_application) |    requirements[i].result.version                       |     softwareRequirements or softwareRequirements.version |
| **version**                 |  String (version[i].result is of type String)|   version[i].result.value   |     softwareVersion  or version        |


 