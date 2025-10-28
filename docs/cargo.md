The following metadata fields can be extracted from a cargo.toml file.   
These fields are defined in the [Cargo.toml specification](https://doc.rust-lang.org/cargo/reference/manifest.html), and are mapped according to the [CodeMeta crosswalk for cargo.toml](https://github.com/codemeta/codemeta/blob/master/crosswalks/Cargo.csv).

| SOMEF metadata category       | Category describes            |       SOMEF metadata field  | CARGO.TOML value               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value   |     package.authors regex name      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.name   |     package.authors regex name      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email   |     package.authors regex email      |
| **code_repository**           |  Url (code_repository[i].result is of type Url)  | Url.value   |   package.repository      |
| **description**               | String (description[i].result is of type String)|   String.value   |   package.description   |
| **has_package_field**         |  Url(has_package_file[i].result is of type Url) |  Url.value    |  "Cargo.toml"            |
| **keywords**               | String (keywords[i].result is of type String)|   String.value   |   package.keywords   |
| **license**                   |  License (license[i].result is of type License)|   License.value   |   package.license    |
| **license**                   |  License (license[i].result is of type License)|   License.spdx_id   |   package.license regex spdx_id   |
| **license**                   |  License (license[i].result is of type License)|   License.name   |   package.license  regex name   |
| **package_id**                |  String (package_id[i].result is of type String)|   String.value   |   package.name   |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.value                  |  target.dependencies or  depencencies name = version     |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.name                   |  target.dependencies or depencencies name         |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.version                |  target.dependencies or depencencies version             |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.development_type               |   target.dependencies  or dependencies (version, git, path, other)         |
| **version**               | Release(version[i].result is of type Release)|   Release.value   |   package.version   |
| **version**               | Release(version[i].result is of type Release)|   Release.tag      |   package.version   |

