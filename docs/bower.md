The following metadata fields can be extracted from a bower.json file.   
These fields are defined in the [Bower specification](https://github.com/bower/spec/blob/master/json.md), currently at version **4.0.0**, and are mapped according to the [CodeMeta crosswalk for bower.json](https://github.com/codemeta/codemeta/blob/master/crosswalks/NodeJS.csv).

| SOMEF metadata category       | SOMEF metadata field                 | BOWER.JSON value    |
|-------------------------|--------------------------------------------|---------------------|
| **authors**             |  authors.name                              |     author.name     |
| **authors**             |  authors.email                             |    author.email                            |
| **description**         | description                                | description |
| **has_package_file**    | bower.json                                 |
| **homepage**            | homepage                                   |   url |
| **license**             | license                                    |     license |
| **name**                | name                                       | name  |
| **keywords**            | keywords                                   |  keywords |
| **requirements**        |    requirements.value                      | "dependencies": {"paq":"version"}  -> paq: version     | 
| **requirements**        |    requirements.name                       | "dependencies": {"paq":"version"}  -> paq       |        
| **requirements**        |    requirements.version                    | "dependencies": {"paq":"version"}  -> version
| **requirements**        |    requirements.dependency_type            | dependencies -> runtime , devDependencies -> dev | 
| **version**             | version                                    | version |

