The following metadata fields can be extracted from a composer.json file.   
These fields are defined in the [Composer.json specification](https://getcomposer.org/doc/04-schema.md), currently at version **2.8.12**, and are mapped to CodeMeta properties following the internal mapping implemented in the parser, since no dedicated CodeMeta crosswalk for composer.json exists.

| SOMEF metadata category       | Expected value type                          | SOMEF metadata field    | COMPOSER.JSON metadata field     |
|-------------------------------|---------------------------------------------|-------------------------|------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result .value      |     authors.name |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result .name       |     authors.name |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result .email      |     authors.email |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result url   |     authors.homepage |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result .role        |    authors.role     |
| **code_repository**           |  Url (code_repository[i].result is of type Url)  | code_repository[i].result.value   |     repository or repository.url           |
| **description**               |  String (description[i].result is of type String) |   description[i].result.value  |   description                       |
| **has_package_file**         |  Url(has_package_file[i].result is of type Url) |  has_package_file[i].result.value    |   URL of the composer.json file        |
| **homepage**                  |  Url(homepage[i].result is of type Url)  |   homepage[i].result.value          |   homepage                    |
| **keywords**                  |  String(keywords[i].result is of type String) |   keywords[i].result.value  |     keywords         |
| **license**                   |  License(license[i].result is of type License) |   license[i].result.value  |    license                 |
| **license**                   |  License(license[i].result is of type License) |   license[i].result.spdx_id |   license(name:value)   -> license.value if spdx_id        |
| **license**                   |  License(license[i].result is of type License) |   license[i].result.name    |   license(name:value)   -> license.name           |
| **package_id**                |  String (package_id[i].result is of type String)|   package_id[i].result.value   |   name                        |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.value                  |   require.name require.version or require-dev.name require-dev.version       |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.name                   |   require.name or require-dev.name           |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.version                |     require.version or require-dev.version            |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.dependency_type        |     require = runtime or require-dev = dev            |
| **version**                   |  Release(version[i].result is of type Release)  |   version[i].result.value                      |   version                    |
| **version**                   |  Release(version[i].result is of type Release)  |   version[i].result.tag                        |   version                   |
