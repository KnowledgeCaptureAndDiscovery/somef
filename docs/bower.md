The following metadata fields can be extracted from a bower.json file.   
These fields are defined in the [Bower specification](https://github.com/bower/spec/blob/master/json.md), currently at version **4.0.0**, and are mapped according to the [CodeMeta crosswalk for bower.json](https://github.com/codemeta/codemeta/blob/master/crosswalks/NodeJS.csv).

| SOMEF metadata category | Category describes  | SOMEF metadata field          | BOWER.JSON value    |
|-------------------------|---------------------|-------------------------------|---------------------|
| **authors**             |  String(authors)           |       String.value           |     authors[]         |
| **description**         |  String(description[i].result is of type String)   |       String.value       |     description     |
| **has_package_file**    |  Url(has_package_file[i].result is of type Url)  |       Url.value  |     "bower.json"    |
| **homepage**            |  Url(homepage[i].result is of type Url)                   |       Url.value          |     homepage |
| **license**             |  License(license[i].result is of type License)                 |       License.value           |     license |
| **name**                |  String(name[i].result is of type String)           |     String.value              |     name  |
| **keywords**            |  String(keywords[i].result is of type String)                    |       String.value          |     keywords |
| **requirements**        |   Software_application (requirements[i].result is of type Software_application)                  |       Software_application.value                      | "dependencies": {"paq":"version"}  -> paq: version     | 
| **requirements**        |   Software_application (requirements[i].result is of type Software_application)                |    Software_application.name                       | "dependencies": {"paq":"version"}  -> paq       |        
| **requirements**        |   Software_application (requirements[i].result is of type Software_application)                     |    Software_application.version                    | "dependencies": {"paq":"version"}  -> version |
| **requirements**        |    requirements.dependency_type            | dependencies -> runtime , devDependencies -> dev |
| **version**             |       Release(version[i].result is of type Release)               | Release.value                                    | version |


