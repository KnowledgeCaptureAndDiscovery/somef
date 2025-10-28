The following metadata fields can be extracted from a cabal file.   
These fields are defined in the [Cabal specification](https://cabal.readthedocs.io/en/3.10/cabal-package.html), currently at version **3.10**and are mapped according to the [Codemeta crosswalk for cabal](https://github.com/codemeta/codemeta/blob/master/crosswalks/Cabal.csv).

| SOMEF metadata category       | Category describes            |       SOMEF metadata field  | CABAL file value               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **has_package_field**         |  Url(has_package_file[i].result is of type Url) |  Url.value    |   filename.cabal       |
| **package_id**                |  String (package_id[i].result is of type String)|   String.value   |   Regex name    |
| **version**                   |  String (version[i].result is of type String)|   String.value   |   Regex version    |
| **description**               | String (description[i].result is of type String)|   String.value   |   Regex description   |
| **homepage**                  |  Url (homepage[i].result is of type String)|   Url.value   |   Regex homepage    |
| **license**                   |  License (license[i].result is of type License)|   License.value   |   Regex license    |
| **license**                   |  License (license[i].result is of type License)|   License.spdx_id   |   Regex license spdx_id   |
| **license**                   |  License (license[i].result is of type License)|   License.name   |   Regex license name   |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.value  |   Regex library build-depends name:version       |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.name                   |  Regex library build-depends name       |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.version                |     Regex library build-depends version          |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |  Software_application development_type               |    "runtime"         |

