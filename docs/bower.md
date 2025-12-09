The following metadata fields can be extracted from a bower.json file.   
These fields are defined in the [Bower specification](https://github.com/bower/spec/blob/master/json.md), currently at version **4.0.0**, and are mapped according to the [CodeMeta crosswalk for bower.json](https://github.com/codemeta/codemeta/blob/master/crosswalks/NodeJS.csv).

| Software metadata category  | SOMEF metadata JSON path              | BOWER.JSON metadata file field     |
|-----------------------------|---------------------------------------|---------------------|
| **authors**                 |     authors[i].result.value           |     authors[]         |
| **description**             |     description[i].result.value       |     description     |
| **has_package_file**        |     has_package_file[i].result.value  |   URL of the bower.json file   |
| **homepage**                |     homepage[i].result.value          |     homepage |
| **license**                 |     license[i].result.value           |     license |
| **name**                    |     name[i].result.value              |     name  |
| **keywords**                |     keywords[i].result.value          |     keywords |
| **requirements**            |     requirements[i].result.value      | "dependencies": {"paq":"version"}  -> paq: version    *(1)* | 
| **requirements**            |     requirements[i].result.name       | "dependencies": {"paq":"version"}  -> paq       |        
| **requirements**            |     requirements[i].result.version    | "dependencies": {"paq":"version"}  -> version |
| **requirements**            |     requirements[i].result.dependency_type            | dependencies -> runtime , devDependencies -> dev |
| **version**                 |     version[i].result.value           | version |


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