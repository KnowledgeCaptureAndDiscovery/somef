The following metadata fields can be extracted from a cargo.toml file.   
These fields are defined in the [Cargo.toml specification](https://doc.rust-lang.org/cargo/reference/manifest.html), and are mapped according to the [CodeMeta crosswalk for cargo.toml](https://github.com/codemeta/codemeta/blob/master/crosswalks/Cargo.csv).

| SOMEF metadata category       | Expected value type            |       SOMEF metadata field  | CARGO.TOML metadata field                |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.value   |     package.authors      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Aauthors[i].result.name   |     package.authors  *(1)*     |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.email   |    package.authors  *(2)*      |
| **code_repository**           |  Url (code_repository[i].result is of type Url)  | code_repository[i].result.value   |   package.repository      |
| **description**               | String (description[i].result is of type String)|   description[i].result.value   |   package.description   |
| **has_package_file**         |  Url(has_package_file[i].result is of type Url) |  has_package_file[i].result.value    |  URL of the cargo.toml file        |
| **keywords**               | String (keywords[i].result is of type String)|   keywords[i].result.value   |   package.keywords   |
| **license**                   |  License (license[i].result is of type License)|   license[i].result.value   |   package.license    |
| **license**                   |  License (license[i].result is of type License)|   license[i].result.spdx_id   |   package.license *(3)*  |
| **license**                   |  License (license[i].result is of type License)|   license[i].result.name   |   package.license  *(4)*   |
| **package_id**                |  String (package_id[i].result is of type String)|   package_id[i].result.value   |   package.name   |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.value                  |  target.dependencies or depencencies name = version     |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.name                   |  target.dependencies or depencencies name         |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.version                |  target.dependencies or depencencies version             |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.development_type               |   target.dependencies or dependencies (version, git, path, other)         |
| **version**               | Release(version[i].result is of type Release)|   version[i].result.value   |   package.version   |
| **version**               | Release(version[i].result is of type Release)|   version[i].result.tag      |   package.version   |

---

*(1)*  
- Regex: `re.search(r'<([^>]+)>', author_str)`--> look in package.authors, them from init until email init.
- Example: `authors = ["rustdesk <info@rustdesk.com>"]`
- Result: `rustdesk`

*(2)*  
- Regex: `re.search(r'<([^>]+)>', author_str)`--> look in package.authors
- Example: `authors = ["rustdesk <info@rustdesk.com>"]`
- Result: `info@rustdesk.com`

*(3)*, *(4)*  
- Look for expressions in a local dictionary with all the reference and spdx_id
- Example: `license = "Apache-2.0"`
- Result spdx_id: `Apache-2.0`
- Result name: `Apache License 2.0`

