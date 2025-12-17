
SOMEF recognizes the programming languages used in a software repository by inspecting
well-known configuration files, dependency descriptors and executable artifacts.
To know more about the extraction details for each type of file, click on it.



| Language  | Supported Files |
|-----------|----------------------------|
| Haskell | [`*.cabal`](./cabal.md) |  
| Java | [`pom.xml`](./pom.md) | 
| JavaScript | [`package.json`](./packagejson.md), [`bower.json`](./bower.md) | 
| Julia | [`Project.toml`](./julia.md) | 
| PHP | [`composer.json`](./composer.md) |  
| Python | [`setup.py`](./setuppy.md), [`pyproject.toml`](./pyprojecttoml.md), [`requirements.txt`](./requirementstxt.md) | 
| R | [`DESCRIPTION`](./description.md) | 
| Ruby | [`*.gemspec`](./gemspec.md) |  
| Rust | [`Cargo.toml`](./cargo.md) |  
 
---

SoMEF also detects the following files to recognize build instructions, workflows or executable examples:


| Language  | Supported Files                    | Software metadata category  |
|-----------|------------------------------------|-----------------------------|
| Docker    |  `Dockerfile`, `docker-compose.yml` | has_built_file
| Jupyter Notebook |  `*.ipynb`                | executable_example |
| Ontologies | `*.ttl`, `*.owl`, `*.nt`, `*.xml`, `*.jsonld` | ontologies |
| Shell |  `*.sh`                                | has_script_file   |
| YAML |  `*.yml`, `*.yaml` | continuous_integration, workflows


