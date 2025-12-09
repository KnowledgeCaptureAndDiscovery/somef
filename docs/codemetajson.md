The following metadata fields can be extracted from a codemeta.json file.   
These fields are defined in the [Codemeta specification](https://github.com/codemeta/codemeta/blob/master/crosswalk.csv), currently at version **3.0**, and are mapped according to the properties and classes defined in the CodeMeta vocabulary.

| Software metadata category    |    SOMEF metadata JSON path  | CODEMETA.JSON metadata file field          |
|-------------------------------|------------------------------|--------------------------------------------|
| **application_domain**        |   application_domain[i].result.value   |     applicationCategory      |
| **authors**                   |   authors[i].result.value |     author.name or author.givenName + author.familyName                   |
| **authors**                   |   authors[i].result.email                 |     author.email    |
| **authors**                   |   authors[i].result.affiliation    |     author.affiliation  |
| **authors**                   |   authors[i].result.identifier     |     author.identifier or author.@id  |
| **citation**                  |   citation[i].result.value     |     referencePublication.name or referencePublication.title           |    
| **citation**                  |   citation[i].result.title     |      referencePublication.name or referencePublication.title            |    
| **citation**                  |   citation[i].result.url  |         referencePublication.url   |    
| **citation**                  |   citation[i].result.date_published  |     referencePublication.datePublished        
| **citation**                  |   citation[i].result.doi       |     referencePublication.identifier   | 
| **code_repository**           |   code_repository[i].result.value   |     codeRepository           |
| **continuous_integration**    |   continuous_integration[i].result.value |     contIntegration          |
| **date_created**              |   date_created[i].result.value  |     dateCreated              |
| **date_updated**              |   date_updated[i].result.value   |     dateModified             |
| **date_published**            |   date_published[i].result .value   |     datePublished  |
| **description**               |   description[i].result.value   |     description                    |
| **development_status**        |   development_status[i].result.value  |     developmentStatus  |
| **download_url**              |   download_url[i].result.value          |     downloadUrl              |
| **has_package_file**          |   has_package_file[i].result.value         |   URL of the codemeta.json file |
| **funding**                   |   funding[i].result.funder       |     funding.funder or funding.funder.name  |    
| **funding**                   |   funding[i].result.funding     |     String.fundingIdentifier | 
| **identifier**                |   identifier[i].result.value       |     identifier                     |
| **issue_tracker**             |   issue_tracker[i].result.value           |     issueTracker             |
| **keywords**                  |   keywords[i].result.value          |     keywords                 |
| **license**                   |   license[i].result .value        |     license.name                   |
| **license**                   |   license[i].result .url          |     license.url                |
| **license**                   |   license[i].result .spdx_id       |    license.identifier if "spdx.org/licenses/  |  
| **license**                   |   license[i].result .identifier   |  license.identifier or https://spdx.org/licenses/{license}  | 
| **name**                      |   name[i].result .value              |     name       |
| **programming_languages**     |   programming_languages[i].result.value    |     programmingLanguage.name |
| **programming_languages**     |   programming_languages[i].result.name |     programmingLanguage.name  |
| **programming_languages**     |   programming_languages[i].result.version |     programmingLanguage.version           |
| **programming_languages**     |   programming_languages[i].result.url |     programmingLanguage.url          |
| **readme_url**                |   readme_url[i].result.value       |     readme                    |
| **requirements**              |   requirements[i].result.value  |      softwareRequirements or softwareRequirements.name == softwareRequirements.version         |
| **requirements**              |   requirements[i].result.name   |    softwareRequirements or softwareRequirements.name or    softwareRequirements.identifier  |
| **requirements**              |   requirements[i].result.version                       |     softwareRequirements or softwareRequirements.version |
| **version**                   |   version[i].result.value   |     softwareVersion  or version        |


 