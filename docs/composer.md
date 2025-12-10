The following metadata fields can be extracted from a composer.json file.   
These fields are defined in the [Composer.json specification](https://getcomposer.org/doc/04-schema.md), currently at version **2.8.12**, and are mapped to CodeMeta properties following the internal mapping implemented in the parser, since no dedicated CodeMeta crosswalk for composer.json exists.

| Software metadata category    | SOMEF metadata JSON path          | COMPOSER.JSON metadata file field     |
|-------------------------------|-----------------------------------|-----------------------------------|
| authors - value                  |  authors[i].result.value      |     authors.name |
| authors - name                   |  authors[i].result.name       |     authors.name |
| authors - name                |  authors[i].result email      |     authors.email |
| authors - url                  |  authors[i].result.url   |     authors.homepage |
| authors - role                 |  authors[i].result.role        |    authors.role     |
| code_repository           |  code_repository[i].result.value   |     repository or repository.url           |
| description               |  description[i].result.value  |   description                       |
| has_package_file          |  has_package_file[i].result.value    |   URL of the composer.json file        |
| homepage                  |  homepage[i].result.value          |   homepage                    |
| keywords                  |  keywords[i].result.value  |     keywords         |
| license - value                   |  license[i].result.value  |    license                 |
| license - spdx id                  |  license[i].result.spdx_id |   license(name:value)   -> license.value if spdx_id        |
| license - name                   |  license[i].result.name    |   license(name:value)   -> license.name           |
| package_id                |  package_id[i].result.value   |   name                        |
| requirements - value              |  requirements[i].result.value                  |   require.name require.version or require-dev.name reire-dev.version       |
| requirements - name              |  requirements[i].result.name                   |   require.name or require-dev.name           |
| requirements - version              |  requirements[i].result.version                |     require.version or require-dev.version            |
| requirements - dependency type              |  requirements[i].result.dependency_type        |     require = runtime or require-dev = dev            |
| version - value                   |  version[i].result.value                      |   version                    |
| version - tag                   |  version[i].result.tag                        |   version                   |
