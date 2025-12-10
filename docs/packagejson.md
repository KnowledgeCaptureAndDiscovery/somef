The following metadata fields can be extracted from a package.json file.   
These fields are defined in the [Package.json specification](https://docs.npmjs.com/cli/v10/configuring-npm/package-json), currently at version **10.9.4**, and are mapped according to the [CodeMeta crosswalk for package.json](https://github.com/codemeta/codemeta/blob/master/crosswalks/NodeJS.csv).

| Software metadata category    |  SOMEF metadata JSON path                | PACKAGE.JSON metadata file field     |
|-------------------------------|----------------------------------------|---------------------  |
| authors - value                   |    authors[i].result.value                |       author.name    |
| authors - email                   |    authors[i].result.email                |       author.email  |
| authors - url                   |    authors[i].result.url                  |       author.url  |
| authors - name                  |    authors[i].result.name                 |       author.name  |
| code_repository           |    code_repository[i].result.value         |    repository/repository.url/repository.directory  *(1)*|
| description               |    description[i].result.value               | description            |
| has_package_file          |    has_package_file[i].result.value   |  URL of the package.json file   |
| homepage                  |    homepage[i].result.value                       | homepage               |
| issue_tracker             |    issue_tracker[i].result.value           | bugs or bugs.url        *(2)*           |
| keywords                  |    keywords[i].result.value                     |        keywords               |
| license                   |    license[i].result.value       |     license or license.type          *(3)*             |
| package_id               |    package_id[i].result.value                |         name          |
| requirements - value              |    requirements[i].result.value              | dependencies/devDependencies     name@sversion      *(4)*          |
| requirements - name              |    requirements[i].result.name           | dependencies/devDependencies     name   *(4)*                |
| requirements - version              |    requirements[i].result.version         | dependencies/devDependencies       version          *(4)*            |
| runtime_platform - value          |    runtime_platform[i].result.value      | engines(package:version) -> version  *(5)*  |
| runtime_platform - name          |    runtime_platform[i].result.name         engines(package:version) -> package *(5)* |
| version                   |    version[i].result.value               | version               |

---

*(1)*  
- Example: 
```
"repository": "npm/npm",

or

"repository": {
"type": "git",
"url": "git+https://github.com/npm/cli.git"
}

or 

"repository": {
"type": "git",
"directory": "workspaces/libnpmpublish"
}
```

*(2)*  
- Example: 
```
"bugs": {
"url": "https://github.com/npm/cli/issues"
}

or

"bugs": "https://github.com/npm/cli/issues"

```

*(2)*  
- Example: 
```
 "license": "Artistic-2.0"

 or

 "license" : {
    "type" : "ISC",
    "url" : "https://opensource.org/licenses/ISC"
  }
  ```
- Result: `Artistic-2.0" or "ISC" (license.type)`

*(3)*  
- Fist part of item -> name; second part --> version
- Example: 
```
  "devDependencies": 
    "foo": "1.0.0 - 2.9999.9999",
    ...
```
Resutl:
```{'result': {'value': 'foo@1.0.0 - 2.9999.9999', 'name': 'foo', 'version': '1.0.0 - 2.9999.9999', 'type': 'Software_application'}, 'confidence': 1, 'technique': 'code_parser', 'source': 'http://example.com/package_neors.json'}```

*(5)*  
- Example: 
```
  "engines": {
    "node": ">=0.10.3 <15"
    }
```
- Result: `"name": "Node", "version": "">=0.10.3 <15"`