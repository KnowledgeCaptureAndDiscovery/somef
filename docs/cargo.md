The following metadata fields can be extracted from a cargo.toml file.   
These fields are defined in the [Cargo.toml specification](https://doc.rust-lang.org/cargo/reference/manifest.html), and are mapped according to the [CodeMeta crosswalk for cargo.toml](https://github.com/codemeta/codemeta/blob/master/crosswalks/Cargo.csv).

| Software metadata category        |      SOMEF metadata JSON path  | CARGO.TOML metadata file field                |
|-------------------------------|--------------------------------------------|------------------------------|
| **authors**                   |   authors[i].result.value   |     package.authors      |
| **authors**                   |   authors[i].result.name   |     package.authors  *(1)*     |
| **authors**                   |   authors[i].result.email   |    package.authors  *(2)*      |
| **code_repository**           |   code_repository[i].result.value   |   package.repository      |
| **description**               |   description[i].result.value   |   package.description   |
| **has_package_file**          |   has_package_file[i].result.value    |  URL of the cargo.toml file        |
| **keywords**                  |   keywords[i].result.value   |   package.keywords   |
| **license**                   |   license[i].result.value   |   package.license    |
| **license**                   |   license[i].result.spdx_id   |   package.license *(3)*  |
| **license**                   |   license[i].result.name   |   package.license  *(4)*   |
| **package_id**                |   package_id[i].result.value   |   package.name   |
| **requirements**              |   requirements[i].result.value                  |  target.dependencies or depencencies name = version     |
| **requirements**              |   requirements[i].result.name                   |  target.dependencies or depencencies name         |
| **requirements**              |   requirements[i].result.version                |  target.dependencies or depencencies version             |
| **requirements**              |   requirements[i].result.development_type               |   target.dependencies or dependencies (version, git, path, other)         |
| **version**                   |    version[i].result.value   |   package.version   |
| **version**                   |   version[i].result.tag      |   package.version   |

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

