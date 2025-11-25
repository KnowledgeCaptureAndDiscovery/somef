The following metadata fields can be extracted from a bower.json file.   
These fields are defined in the [Bower specification](https://github.com/bower/spec/blob/master/json.md), currently at version **4.0.0**, and are mapped according to the [CodeMeta crosswalk for bower.json](https://github.com/codemeta/codemeta/blob/master/crosswalks/NodeJS.csv).

| SOMEF metadata category | Expected value type  | SOMEF metadata field          | BOWER.JSON metadata field     |
|-------------------------|---------------------|-------------------------------|---------------------|
| **authors**             |  Agent (authors[i].result is of type Agent)         |       authors[i].result.value           |     authors[]         |
| **description**         |  String(description[i].result is of type String)   |       description[i].result.value       |     description     |
| **has_package_file**    |  Url(has_package_file[i].result is of type Url)  |       has_package_file[i].result.value  |   URL of the bower.json file   |
| **homepage**            |  Url(homepage[i].result is of type Url)                   |       homepage[i].result.value          |     homepage |
| **license**             |  License(license[i].result is of type License)                 |      license[i].result.value           |     license |
| **name**                |  String(name[i].result is of type String)           |     name[i].result.value              |     name  |
| **keywords**            |  String(keywords[i].result is of type String)                    |       keywords[i].result.value          |     keywords |
| **requirements**        |   Software_application (requirements[i].result is of type Software_application) |  requirements[i].result.value  | "dependencies": {"paq":"version"}  -> paq: version    *(1)* | 
| **requirements**        |   Software_application (requirements[i].result is of type Software_application) |    requirements[i].result.name  | "dependencies": {"paq":"version"}  -> paq       |        
| **requirements**        |   Software_application (requirements[i].result is of type Software_application)  |    requirements[i].result.version | "dependencies": {"paq":"version"}  -> version |
| **requirements**        |   Software_application (requirements[i].result is of type Software_application)  |  requirements[i].result.dependency_type            | dependencies -> runtime , devDependencies -> dev |
| **version**             |       Release(version[i].result is of type Release)               | version[i].result.value   | version |


---

*(1)*  

- Example: 
```
  "dependencies": {
    "jquery": "^3.1.1",
    "bootstrap": "^3.3.7",
    "moment": "^2.17.1",
    "components-font-awesome": "^4.7.0",
    "font-awesome": "^4.7.0",
    "materialize": "^0.97.8"
  }
  ```
  First item results:
  - Result value: "jquery: ^3.1.1"
  - Result name": "jquery"
  - Result version": "^3.1.1"
  - Result dependency_type": "runtime" because it is "dependencies"s