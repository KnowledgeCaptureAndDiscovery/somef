The following metadata fields can be extracted from a package.json file.   
These fields are defined in the [Package.json specification](https://docs.npmjs.com/cli/v10/configuring-npm/package-json), currently at version **10.9.4**, and are mapped according to the [CodeMeta crosswalk for package.json](https://github.com/codemeta/codemeta/blob/master/crosswalks/NodeJS.csv).

| SOMEF metadata category       | Category describes  | SOMEF metadata field                 | PACKAGE.JSON value    |
|-------------------------------|---------------------|--------------------------------------|---------------------  |
| **authors**                   |  Agent (authors[i].result is of type Agent)  |     Agent.value                |       author.name    |
| **authors**                   |  Agent (authors[i].result is of type Agent)  |     Agent.email                |       author.email  |
| **authors**                   |  Agent (authors[i].result is of type Agent)  |     Agent.url                  |       author.url  |
| **authors**                   |  Agent (authors[i].result is of type Agent)  |     Agent.name                 |       author.name  |
| **code_repository**           |   Url (code_repository[i].result is of type Url)  |     Url.value         |    repository.url or repository.directory  |
| **description**               |  String(description[i].result is of type String) |   String.value               | description            |
| **has_package_field**         |   Url (has_package_file[i].result is of type Url) |   Url.value   |                   "package.json"                       |
| **homepage**                  |  Url (homepage[i].result is of type Url)    |         Url.value                       | homepage               |
| **issue_tracker**             |   Url (issue_tracker[i].result is of type Url)|     Url.value           | bugs or bugs.url                   |
| **keywords**                  |   String(keywords[i].result is of type String) |   String.value                     |        keywords               |
| **license**                   |   License(license[i].result is of type License) |   License.value       |     license or license.type                  |
| **package_id**                |  String(package_id[i].result is of type String) |    String.value                |         name          |
| **requirements**              |    Software_application (requirements[i].result is of type Software_application)|  Software_application.value              | dependencies.name@dependencies.version or devDependencies.name@devDependencies.version                        |
| **requirements**              |    Software_application (requirements[i].result is of type Software_application)|  Software_application.name              | dependencies.name or devDependencies.name                       |
| **requirements**              |   Software_application (requirements[i].result is of type Software_application) |  Software_application.version              | dependencies.name or devDependencies.name                       |
| **runtime_platform**          |   String (runtime_platform[i].result is of type String) |   String.value             | engines(package:version) -> version |
| **runtime_platform**          |   String (runtime_platform[i].result is of type String) |   String.name              | engines(package:version) -> package |
| **version**                   |   Release (version[i].result is of type Release)   |       Release.value               | version               |
