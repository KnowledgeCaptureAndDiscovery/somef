The following metadata fields can be extracted from a Pyproject.toml file with Julia.   
These fields are defined in the [Julia projects specification](https://docs.julialang.org/en/v1/) currently at version **1.12**, and are mapped according to the [CodeMeta crosswalk for julia projects](https://github.com/codemeta/codemeta/blob/master/crosswalks/Julia%20Project.csv).

| Software metadata category    |    SOMEF metadata JSON path  | julia pyproject.toml metadata file field               |
|-------------------------------|--------------------------------|---------------------------------------------------|
| authors - name                 |   authors[i].result.name   |     authors    *(1)*    |
| authors - email                   |   authors[i].result.email   |     authors    *(1)*    |
| package_id                |   package_id[i].result.value   |   name   |
| has_package_file          |   has_package_file[i].result.value    |  URL of the Project.toml file      |
| identifier                |   identifier[i].result .value  | uuid                    |
| package_id                |   package_id[i].result.value   |   name                      |
| requirements              |   requirements[i].result.value               |     deeps       |
| runtime_platform - value          |   runtime_platform[i].result.value |  properties  compat  |
| runtime_platform - name          |   runtime_platform[i].result.name |   compat    |
| version                   |   version[i].result .value  | version                    |


---


*(1)*  
- Regex: `r'^(.+?)\s*<(.+?)>$''`  
- Example: 
```
authors = [
    "Author1 <author1@example.com>",
   ....
    ]

```
- Result: 
```
"name": "Author1",
"email": "author1@example.com",
```

