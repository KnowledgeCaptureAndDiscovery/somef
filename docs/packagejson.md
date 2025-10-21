The following metadata fields can be extracted from a package.json file.   
These fields are defined in the [Package.json specification](https://docs.npmjs.com/cli/v10/configuring-npm/package-json), currently at version **10.9.4**, and are mapped according to the [CodeMeta crosswalk for package.json](https://github.com/codemeta/codemeta/blob/master/crosswalks/NodeJS.csv).

| SOMEF metadata category       | SOMEF metadata field                 | PACKAGE.JSON value    |
|-------------------------------|--------------------------------------|---------------------  |
| **package_id**                |      package_id.value                |         name          |
| **description**               |      description.value               | description            |
| **homepage**                  | homepage.value                       | homepage               |
| **version**                   |          version.value               | version               |
| **code_repository**           |        code_repository.value         |    repository.url or repository.directory  |
| **issue_tracker**             |        issue_tracker.value           | bugs or bugs.url                   |
| **authors**                   |         authors.value                |      author.name    |
| **authors**                   |         authors.email                |       author.email  |
| **authors**                   |         authors.url                  |       author.url  |
| **authors**                   |         authors.name                 |       author.name  |
| **license**                   |   license.value                      |     license or license.type                  |
| **keywords**                  |   keywords.value                     |        keywords               |
| **runtime_platform**          |   runtime_platform.value             | engines(package:version) -> version |
| **runtime_platform**          |   runtime_platform.name              | engines(package:version) -> package |
| **requirements**              |      requirements.value              | dependencies.name@dependencies.version or devDependencies.name@devDependencies.version                        |
| **requirements**              |      requirements.name              | dependencies.name or devDependencies.name                       |
| **requirements**              |      requirements.version              | dependencies.name or devDependencies.name                       |
| **has_package_field**         |   package.json                    ∫     |

