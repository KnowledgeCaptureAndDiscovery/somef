The following metadata fields can be extracted from a pom.xml file.   
These fields are defined in the [Maven POM specification](https://maven.apache.org/pom.html), currently at version **4.0.0**, and are mapped according to the [CodeMeta crosswalk for Java (Maven)](https://github.com/codemeta/codemeta/blob/master/crosswalks/Java%20(Maven).csv).

| SOMEF metadata category       | Category describes  |   SOMEF metadata field                 | POM.XML value    |
|-------------------------------|---------------------|----------------------------------------|------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value       |     developer.name |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.name       |     developer.name |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email      |     developer.email |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.url         |     developer.url |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.affiliation |     developer.organization |
| **has_package_field**         |  Url (has_package_file[i].result is of type Url) | Url.value      |   "pom.xml" |
| **homepage**                  |  Url (homepage[i].result is of type Url)                |   Url.value | homepage |
| **issue_tracker**             |  Url (issue_tracker[i].result is of type Url)    | Url.value    | issueManagement.url                  |
| **package_distribution**      |  Url (package_distribution[i].result is of type Url)    |   Url.value  | scm.url |
| **package_distribution**      |  Url (package_distribution[i].result is of type Url)    |   Url.value  | repositories.repository(id, name, url)|
| **requirements**              |  Software_application (requirements[i].result is of type Software_application)  | Software_application.value   | groupId.arfifactId                          |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application)  | Software_application.name   |  arfifactId                        |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) | Software_application.version   | version                       |
| **package_id**                |  String (package_id[i].result is of type String)   | String.value   | group_id.artifact_id                         |
| **runtime_platform**          | String (runtime_platform[i].result is of type String)  |   String.value |  properties -> regex version  |
| **runtime_platform**          | String (runtime_platform[i].result is of type String) |   String.name |   properties -> regex name   |
| **version**                   | Release (version[i].result is of type Release)   | Release.value  | version                    |

<!-- Not in documentation ->  -->