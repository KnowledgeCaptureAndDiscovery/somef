The following metadata fields can be extracted from a composer.json file.   
These fields are defined in the [Composer.json specification](https://getcomposer.org/doc/04-schema.md), currently at version **2.8.12**, and are mapped to CodeMeta properties following the internal mapping implemented in the parser, since no dedicated CodeMeta crosswalk for composer.json exists.

| SOMEF metadata category       | SOMEF metadata field                 | COMPOSER.JSON value    |
|-------------------------------|--------------------------------------|------------------------|
| **authors**                   |  authors.value                       |     authors.name |
| **authors**                   |  authors.name                        |     authors.name |
| **authors**                   |  authors.email                       |     authors.email                  |
| **authors**                   |  authors.homepage                    |     authors.homepage                   |
| **authors**                   |  authors.role                        |    authors.role                  |
| **code_repository**           |  code_repository.value               |     repository or repository.url           |
| **description**               |   description.value                  |   description                       |
| **has_package_field**         | has_package_field.value              |   composer.json        |
| **homepage**                  |   homepage.value                     |   homepage                    |
| **keywords**                  |  keywords.value                      |     keywords         |
| **license**                   |  license.value                       |    license                 |
| **license**                   |  license.spdx_id                     |   license(name:value)   -> license.value if spdx_id               |
| **license**                   |  license.name                        |   license(name:value)   -> license.name           |
| **package_id**                |   package_id.value                   |   name                        |
| **requirements**              |  requirements.value                  |   require.name require.version or require-dev.name require-dev.version       |
| **requirements**              |  requirements.name                   |   require.name or require-dev.name           |
| **requirements**              |  requirements.version                |     require.version or require-dev.version            |
| **requirements**              |  requirements.dependency_type        |     require = runtime or require-dev = dev            |
| **version**                   |   version.value                      |   version                    |
| **version**                   |   version.tag                        |   version                   |