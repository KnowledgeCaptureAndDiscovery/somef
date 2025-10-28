The following metadata fields can be extracted from a composer.json file.   
These fields are defined in the [Composer.json specification](https://getcomposer.org/doc/04-schema.md), currently at version **2.8.12**, and are mapped to CodeMeta properties following the internal mapping implemented in the parser, since no dedicated CodeMeta crosswalk for composer.json exists.

| SOMEF metadata category       | Category describes                          | SOMEF metadata field    | COMPOSER.JSON value    |
|-------------------------------|---------------------------------------------|-------------------------|------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value      |     authors.name |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.name       |     authors.name |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email      |     authors.email |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.url   |     authors.homepage |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.role        |    authors.role     |
| **code_repository**           |  Url (code_repository[i].result is of type Url)  | Url.value   |     repository or repository.url           |
| **description**               |  String (description[i].result is of type String) |   String.value  |   description                       |
| **has_package_field**         |  Url(has_package_file[i].result is of type Url) |  Url.value    |   "composer.json"        |
| **homepage**                  |  Url(homepage[i].result is of type Url)  |   Url.value          |   homepage                    |
| **keywords**                  |  String(keywords[i].result is of type String) |   String.value  |     keywords         |
| **license**                   |  License(license[i].result is of type License) |   License.value  |    license                 |
| **license**                   |  License(license[i].result is of type License) |   License.spdx_id |   license(name:value)   -> license.value if spdx_id        |
| **license**                   |  License(license[i].result is of type License) |   License.name    |   license(name:value)   -> license.name           |
| **package_id**                |  String (package_id[i].result is of type String)|   String.value   |   name                        |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.value                  |   require.name require.version or require-dev.name require-dev.version       |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.name                   |   require.name or require-dev.name           |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.version                |     require.version or require-dev.version            |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.dependency_type        |     require = runtime or require-dev = dev            |
| **version**                   |  Release(version[i].result is of type Release)  |   Release.value                      |   version                    |
| **version**                   |  Release(version[i].result is of type Release)  |   Release.tag                        |   version                   |
