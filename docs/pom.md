The following metadata fields can be extracted from a pom.xml file.   
These fields are defined in the [Maven POM specification](https://maven.apache.org/pom.html), currently at version **4.0.0**, and are mapped according to the [CodeMeta crosswalk for Java (Maven)](https://github.com/codemeta/codemeta/blob/master/crosswalks/Java%20(Maven).csv).

| SOMEF metadata category       | SOMEF metadata field                 | POM.XML value    |
|-------------------------|--------------------------------------------|------------------|
| **authors**       |  authors.name  |     developer.name                            |
| **authors**       |  authors.email  |    developer.email                            |
| **authors**       |  author.url  |     developer.url                            |
| **authors**       |  author.organization |     developer.organization                          |
| **requirements**  |   requirements.value   | groupId.arfifactId                          |
| **requirements**  |   requirements.name   |  arfifactId                        |
| **requirements**  |   requirements.version   | version                       |
| **package_id**    |   package_id.value   | group_id.artifact_id                         |
| **version**      |    version.value  | version                    |
| **has_package_field**   | has_package_field.value      |   pom.xml |
| **issue_tracker**  |     issue_tracker.value    | issue_tracker                      |
| **package_distribution**        |   package_distribution.value  | scm_url, repositories(id, name, url)|
| **homepage**         | homepage.value | homepage |
| **runtime_platform**     |   runtime_platform.value |  version  |
| **runtime_platform**     |   runtime_platform.name |   name   |


