The following metadata fields can be extracted from a pyproject.toml file.   
These fields are defined in the [pyproject.toml specification](https://packaging.python.org/en/latest/guides/writing-pyproject-toml), and are mapped according to the [CodeMeta crosswalk for python](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| SOMEF metadata category  |   Category describes                | SOMEF metadata field    | PYPROJECT.TOML value    |
|--------------------------|-------------------------------------|-------------------------|-------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value       |     author.name                  |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email       |     author.email                  |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.name        |     author.name                |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.url         |     author.url               |
| **code_repository** |    Url (code_repository[i].result is of type Url)  |  Url.value                    |  projects.urls.repository or tool.poetry.repository |
| **description**          |  String (description[i].result is of type String) |   String.value |  project.description or tool.poetry.description                |
| **documentation** |     Url (documentation[i].result is of type Url)  |  Url.value              |  projects.urls.documentation or tool.poetry.documentation |
| **download_url** |     Url (download_url[i].result is of type Url)  |  Url.value                |  projects.urls.download or tool.poetry.download|        
| **license**                   |  License(license[i].result is of type License) |    License.value  |   license.file or license.type or license                   |
| **license**                   |  License(license[i].result is of type License) |    License.name    |  license.name              |
| **license**                   |  License(license[i].result is of type License)|    License.spdx_id |    license.identifier if "spdx.org/licenses/  |  
| **has_package_field**    |  Url(has_package_file[i].result is of type Url)    | Url.value    |   "pyproject.toml"      |
| **homepage**             |  Url(homepage[i].result is of type Url)    |   Url.value          |   project.homepage or tool.poetry.homepage     |
| **issue_tracker** |     Url (issue_tracker[i].result is of type Url)  |  Url.value              |  pprojects.urls.issue or tool.poetry.issue |
| **keywords** |    String(keywords[i].result is of type String) |    String.value          |     keywords                 |
| **package_id**           |  String (package_id[i].result is of type String)  |   String.value |   project.name or tool.poetry.name  |
| **readme_url** |      Url (readme_url[i].result is of type Url)  |  Url.value                   |  projects.urls.readme or tool.poetry.readme|
| **related_documentation** |  Url (download_url[i].result is of type Url)  |  Url.value          |  projects.urls or tool.poetry |  
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  Software_application.value  |   dependencies(name=version) or build-system.requires[i] parsing |
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  Software_application.name   |   dependencies(name=version) -> dependencies.name or build-system.requires[i] parsing -> name     |
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  Software_application.version   | dependencies[i](name=version) -> dependencies.version or build-system.requires[i] parsing -> version  |
| **runtime_platform**          | String (runtime_platform[i].result is of type String)  |   String.value |  depeendencies or requires-python -> regex version  |
| **runtime_platform**          | String (runtime_platform[i].result is of type String) |   String.name |   depeendencies or requires-python -> regex name   |
| **version**              |  Release(version[i].result is of type Release)    |  Release.value |  project.version or tool.poetry.version |
| **version**              |  Release(version[i].result is of type Release)    |  version.tag                            |     project.version or tool.poetry.version                            |