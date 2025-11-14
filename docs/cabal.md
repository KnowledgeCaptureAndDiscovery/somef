The following metadata fields can be extracted from a cabal file.   
These fields are defined in the [Cabal specification](https://cabal.readthedocs.io/en/3.10/cabal-package.html), currently at version **3.10**and are mapped according to the [Codemeta crosswalk for cabal](https://github.com/codemeta/codemeta/blob/master/crosswalks/Cabal.csv).

| SOMEF metadata category       | Expected value type            |       SOMEF metadata field  | CABAL metadata field               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **description**               | String (description[i].result is of type String)|   description[i].result.value   |   synopsis / description *(1)*|
| **has_package_file**         |  Url(has_package_file[i].result is of type Url) |  has_package_file[i].result.value    |   URL of the filename.cabal file    |
| **homepage**                  |  Url (homepage[i].result is of type Url)|  homepage[i].result.value   |   homepage  *(2)*  |
| **license**                   |  License (license[i].result is of type License)|   license[i].result.value   |   Regex license  *(3)*  |
| **package_id**                |  String (package_id[i].result is of type String)|   package_id[i].value   |   name  *(4)* |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.value  |   *(5)*      |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.name | library.build-depends name  *(5.1)*    |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.version | library.build-depends version  *(5.2)*       
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) | requirements[i].result.development_type  |    "runtime"         |
| **version**                   |  String (version[i].result is of type String)|   version[i].result.value   |   version  *(6)*  |

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

