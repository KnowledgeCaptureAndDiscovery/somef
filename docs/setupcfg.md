The following metadata fields can be extracted from a setup.cfg file.   
These fields are defined in the [setuptools declarative configuration specification](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html), and are mapped according to the [CodeMeta crosswalk for Python Distutils](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| Software metadata category  |    SOMEF metadata JSON path    | SETUP.CFG metadata file field     |
|--------------------------------|-----------------------------|----------------------------------------|
| author - value                   |  author[i].result.value       |     metadata.author                  |
| author - email                   |  author[i].result.email       |     metadata.author_email            |
| author - name                   |  author[i].result.name        |     metadata.author                |
| code_repository           |  code_repository[i].result.value  |  project_urls (source, repository, code) |
| description               |  description[i].result.value |  metadata.description                |
| documentation             |  documentation[i].result.value  |  project_urls (Documentation, docs) |       
| license - value                   |  license[i].result.value  |   metadata.license or metadata.license_files                   |
| license - name                   |  license[i].result.name    |  metadata.license           *(1)*   |
| license - spdx id                   |  license[i].result.spdx_id |    metadata.license if "spdx.org/licenses/"   *(1)* |  
| has_package_file          |  has_package_file[i].result.value    |   URL of the setup.cfg file      |
| homepage                  |  homepage[i].result.value          |   metadata.url or project_urls (Homepage)     |
| keywords                  |  keywords[i].result.value          |     metadata.keywords                 |
| package_id                |  package_id[i].result.value |   metadata.name  |
| requirements - value              | requirements[i].result.value  |   options.install_requires or options.setup_requires *(2)*   |
| requirements - name              |  requirements[i].result.name   |   options.install_requires or options.setup_requires -> name  *(2)*     |
| requirements - version              |  requirements[i].result.version   | options.install_requires or options.setup_requires -> version *(2)*   |
| runtime_platform - value         |  runtime_platform[i].result.value |  options.python_requires -> "Python" + version  *(3)*  |
| runtime_platform - name          |  runtime_platform[i].result.name |   options.python_requires -> "Python"  *(3)* |
| runtime_platform - version          |  runtime_platform[i].result.version |   options.python_requires  *(3)* |
| version - value                   |  version[i].result.value |  metadata.version |
| version - tag                  |  version[i].result.tag                            |     metadata.version                            |

---

*(1)*  
- Look for the name and spdx_id in a local dictionary with all licenses.

*(2)*  
- Examples of requirements
```
[options]
install_requires =
    astropy
    ctapipe >= 0.12
    h5py ~= 3.1.0
    
setup_requires =
    setuptools >= 40.6.0
    wheel

```

*(3)*  
- Example:
```
python_requires = >= 3.10.0
```
