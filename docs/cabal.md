The following metadata fields can be extracted from a cabal file.   
These fields are defined in the [Cabal specification](https://cabal.readthedocs.io/en/3.10/cabal-package.html), currently at version **3.10** and are mapped according to the [Codemeta crosswalk for cabal](https://github.com/codemeta/codemeta/blob/master/crosswalks/Cabal.csv).

| Software metadata category    |       SOMEF metadata JSON path        | CABAL metadata file field               |
|-------------------------------|---------------------------------------|-----------------------------------------|
| **description**               |   description[i].result.value         |     synopsis / description *(1)*|
| **development_status**        |   development_status[i].result.value  |     stability  |
| **has_package_file**          |   has_package_file[i].result.value    |     URL of the filename.cabal file    |
| **homepage**                  |   homepage[i].result.value            |     homepage  *(2)*  |
| **issue_tracker**             |   issue_tracker[i].result.value       |     bug-reports             |
| **license**                   |   license[i].result.value             |     Regex license  *(3)*  |
| **package_id**                |   package_id[i].value                 |     name  *(4)* |
| **requirements**              |   requirements[i].result.value        |     *(5)*      |
| **requirements**              |   requirements[i].result.name         |     library.build-depends name  *(5.1)*    |
| **requirements**              |   requirements[i].result.version      |     library.build-depends version  *(5.2)*  |   
| **requirements**              |   requirements[i].result.development_type  |    "runtime"         |
| **version**                   |   version[i].result.value             |     version  *(6)*  |
| Software metadata category       |       SOMEF metadata JSON path  | CABAL metadata file field               |
|-------------------------------|-----------------------------|------------------------------|
| description  |   description[i].result.value   |   synopsis or description *(1)*|
| has_package_file         |  has_package_file[i].result.value    |   URL of the filename.cabal file    |
| homepage                  |  homepage[i].result.value   |   homepage  *(2)*  |
| license                   |   license[i].result.value   |    license  *(3)*  |
| package id                |  package_id[i].value   |   name  *(4)* |
| requirements - value              |    requirements[i].result.value  |  library.build-depends *(5)*      |
| requirements - name              |    requirements[i].result.name | library.build-depends name  *(5.1)*    |
| requirements - version             |   requirements[i].result.version | library.build-depends version  *(5.2)*       
| requirements - development type              | requirements[i].result.development_type  |    runtime         |
| version                   |    version[i].result.value   |   version  *(6)*  |

---

*(1)*  
- Regex: `r'description:\s*(.*?)(?=\n\S|\Z)' → group[1]`  
- Example: `description: text description`
- Result: `text description`

*(2)*  
- Regex: `re.search(r'homepage:\s*(.*)' → group[1]`  
- Example: `homepage:            https://github.com/joshuaclayton/unused#readme`
- Result: `https://github.com/joshuaclayton/unused#readme`

*(3)*  
- Regex: `r'license:\s*(.*)' → group[1]`  
- Example: `license:       BSD-3-Clause`
- Result: `BSD-3-Clause`

*(4)*  
- Regex: `r'name:\s*(.*)' → group[1]`  
- Example: `name:                unused`
- Result: `unused`

*(5)*, *(5.1)*, *(5.2)*    

- Regex 1: `r'library\s*\n(.*?)(?=\n\S|\Z)' → group[1]`  --> first look into library
- Regex 2: `r'build-depends:\s*(.*?)(?=\n\s*(?:[A-Za-z0-9_-]+\s*:|if\s|\Z)) ' → group[1]`  --> build-depends into library content
- Regex 3: `r'^([a-zA-Z0-9-_]+)\s*(.*?)$'` --> extract groups for name and version
- Example: 
```
library
  build-depends:
    Cabal-syntax ^>= 3.17,
    array         >= 0.4.0.1  && < 0.6
```
- Result value: `Cabal-syntax ^>= 3.17`
- Result name: `Cabal-syntax`
- Result version: `^>= 3.17`

*(6)*  
- Regex: `r'version:\s*(.*)' → group[1]`  
- Example: `version:             0.10.0.0`
- Result: `0.10.0.0`

