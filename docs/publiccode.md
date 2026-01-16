The following metadata fields can be extracted from a publiccode.yml file.   
These fields are defined in the [PublicCode specification](https://yml.publiccode.tools/), currently at version **0.5.0**, and are mapped according to the [CodeMeta crosswalk for publiccode.yml](https://codemeta.github.io/crosswalk/publiccode/) and [csv CodeMeta crosswalk for publiccode.yml](https://github.com/codemeta/codemeta/blob/master/crosswalks/publiccode.csv)

| Software metadata category  | SOMEF metadata JSON path              | PUBLICCODE.YML metadata file field     |
|-----------------------------|---------------------------------------|----------------------------------------|
| application_domain          |   application_domain[i].result.value  | categories or description.[lang].genericName *(1)*  |  
| code_repository             |   code_repository[i].result.value     |     url                      |  
| date_published              |   date_published[i].result.value      |    releaseDate                |  
| date_updated                |   date_updated[i].result.value        |    releaseDate                | 
| description                 |   description[i].result.value         |     description.[lang].shortDescription or description.[lang].longDescription *(2)*   |  
| development_status          |   development_status[i].result.value  |    developmentStatus                | 
| has_package_file            |   has_package_file[i].result.value    |     URL of the publiccode.yml file    |
| keywords                    |   keywords[i].result.value            |     description.[lang].features     *(3)*                |  
| license - value             |   license[i].result.value             |   legal.license    *(4)* |
| license - spdx id           |   license[i].result.spdx_id           |   legal.license extract spdx id  *(4)*|
| license - name              |   license[i].result.name              |   legal.license extract name  *(4)*  | 
| name                        |   name[i].result.value                |     name or description.[lang].localisedName     *(5)*                 |  
| requirements - value        |   requirements[i].result.value        |  dependsOn.open / dependsOn.proprietary / dependsOn.hardware  name + version *(6)*          |  
| requirements - name         |   requirements[i].result.name         |    dependsOn.open / dependsOn.proprietary / dependsOn.hardware  name      *(6)*         |  
| requiriments - version      |   requirements[i].result.version      |  dependsOn.open / dependsOn.proprietary / dependsOn.hardware   more than one label of version *(6)*     |
| runtime_platform            |   runtime_platform[i].result.value    |    platforms                |  
| version                     |   version[i].result.value             |    softwareVersion                |  

---

*(1)* 
- Example:
```
categories:
  - data-collection
  - it-development
```
or
```
description:
  nl:
    genericName: API component
```

*(2)* 
- Example:
```
description:
  nl:
    shortDescription: API voor het beheren van objecten
    longDescription: >
      De **Objecten API** heeft als doel om uiteenlopende objecten eenvoudig te kunnen
      registreren en ontsluiten in een gestandaardiseerd formaat. De Objecten API kan
      ....`_.

  en:
    shortDescription: API to manage objects
    longDescription: >
      The **Objects API** aims to easily store various objects and make them available in
      standardized format. The Objects API can be used by any organization to manage
      relevant objects. An organization can also choose to use the Objects API to
      ....`_.
```

*(3)* 
- Example:
```
description:
  nl:
    features:
      - Objecten API
      - Minimalistische objecten beheerinterface
  en:
    features:
      - Objects API
      - Minimalistic object management interface
```


*(4)* 
- Look for expressions in a local dictionary with all the reference and spdx_id
- Example:
```
legal:
  license: AGPL-3.0-or-later
  mainCopyrightOwner: City of Chicago
  repoOwner: City of Chicago
```
-Result:
```
'result': 
    {'value': 'AGPL-3.0-or-later', 
    'spdx_id': 'AGPL-3.0', 
    'name': 'GNU Affero General Public License v3.0', 
    'type': 'License'},

```

*(5)* 
- Example:
`name: Medusa`
or
```
description:
  en:
    localisedName: Medusa
```


*(6)* 
- Examples:
```
dependsOn:
  open:
    - name: Objecttypes API
      optional: false
      version: '1.0'
    - name: MySQL
      versionMin: "1.1"
      versionMax: "1.3"
      optional: true
    - name: PostgreSQL
      versionMin: "14.0"
      optional: true
```

- Result PostgreSQL:
```
    "result": {
        "value": "PostgreSQL>=14.0",
        "name": "PostgreSQL",
        "version": ">=14.0",
        "type": "Software_application",
        "dependency_type": "runtime"
    },
```


