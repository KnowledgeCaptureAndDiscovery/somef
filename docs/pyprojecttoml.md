The following metadata fields can be extracted from a pyproject.toml file.   
These fields are defined in the [pyproject.toml specification](https://packaging.python.org/en/latest/guides/writing-pyproject-toml), and are mapped according to the [CodeMeta crosswalk for python](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| Software metadata category  |    SOMEF metadata JSON path    | PYPROJECT.TOML metadata file field     |
|--------------------------------|-----------------------------|----------------------------------------|
| authors - value                   |  authors[i].result.value       |     authors.name                  |
| authors - email                   |  authors[i].result.email       |     authors.email                  |
| authors - name                   |  authors[i].result.name        |     authors.name                |
| authors - url                   |  authors[i].result.url         |     authors.url               |
| code_repository           |  code_repository[i].result.value  |  project.urls.repository or tool.poetry.repository |
| description               |  description[i].result.value |  project.description or tool.poetry.description                |
| documentation             |  documentation[i].result.value  |  project.urls.documentation or tool.poetry.documentation |
| download_url              |  download_url[i].result.value    |  project.urls.download or tool.poetry.download|        
| license - value                   |  license[i].result.value  |   license.file or license.type or license                   |
| license - name                   |  license[i].result.name    |  license.name           *(1)*   |
| license - spdx id                   |  license[i].result.spdx_id |    license.identifier if "spdx.org/licenses/   *(1)* |  
| has_package_file          |  has_package_file[i].result.value    |   URL of the pyproject.toml file      |
| homepage                  |  homepage[i].result.value          |   project.homepage or tool.poetry.homepage     |
| issue_tracker             |  issue_tracker[i].result.value              |  projects.urls.issue or tool.poetry.issue |
| keywords                  |  keywords[i].result.value          |     keywords                 |
| package_id                |  package_id[i].result.value |   project.name or tool.poetry.name  |
| readme_url                |  readme_url[i].result.value                   |  projects.urls.readme or tool.poetry.readme|
| related_documentation     |  download_url[i].result.value          |  projects.urls or tool.poetry |  
| requirements - value              | requirements[i].result.value  |   dependencies(name=version) or build-system.requires[i] *(2)*   |
| requirements - name              |  requirements[i].result.name   |   dependencies(name=version) -> dependencies.name or build-system.requires[i] parsing -> name  *(2)*     |
| requirements - version              |  requirements[i].result.version   | dependencies[i](name=version) -> dependencies.version or build-system.requires[i] parsing -> version *(2)*   |
| runtime_platform - value         |  runtime_platform[i].result.value |  depeendencies or requires-python -> version  *(3)*  |
| runtime_platform - name          |  runtime_platform[i].result.name |   depeendencies or requires-python -> name   *(3)* |
| version - value                   |  version[i].result.value |  project.version or tool.poetry.version |
| version - tag                  |  version[i].result.tag                            |     project.version or tool.poetry.version                            |

---

*(1)*  
- Look for the name and spdx_id in a local dictionary with all licenses

*(2)*  
- Examples: allows formats
```
dependencies = [
    "astropy",
    "ctapipe",
    "ctaplot",
    "dl1_data_handler",
    "h5py",
........

[tool.poetry.dependencies]
    python = ">=3.9,<=3.13"
    bs4 = "^0.0.1"
........

[build-system]
    requires = ["poetry-core>=1.1.10"]
```

- If it is possible we obtain name and version
    'value' : 'python>=3.9,<=3.13' 
    'name' : 'python'  
    'version' : '>=3.9,<=3.13'  

*(3)*
- Always "Python" and version if exists.
- Examenple:
```
requires-python = ">=3.11"

or

[tool.poetry.dependencies]
    python = ">=3.9,<=3.13"

or

[dependencies]
    python = ">=3.9,<=3.13"

```
