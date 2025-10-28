The following metadata fields can be extracted from a gemspec file.   
These fields are defined in the [Ruby Gems specification](https://guides.rubygems.org/specification-reference/) currently at version **2.0**, and are mapped according to the [CodeMeta crosswalk for ruby gems](https://github.com/codemeta/codemeta/blob/master/crosswalks/Ruby%20Gem.csv).

| SOMEF metadata category       | Category describes            |       SOMEF metadata field  | .gemspec value               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value   |     Regex gem authors        |
| **description**               |  String (description[i].result is of type String)|   String.value   |   Regex gem description    |
| **has_package_field**         |  Url(has_package_file[i].result is of type Url) |  Url.value    |   filename.gemspec       |
| **homepage**                  |  Url (homepage[i].result is of type String)|   Url.value   |   Regex gem homepage    |
| **license**                   |  License (license[i].result is of type License)|   License.value   |   Regex gem license    |
| **license**                   |  License (license[i].result is of type License)|   License.spdx_id   |   Regex gem license spdx_id   |
| **license**                   |  License (license[i].result is of type License)|   License.name   |   Regex gem license name   |
| **package_id**                |  String (package_id[i].result is of type String)|   String.value   |   Regex gem name    |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.value                  |   Regex gem add_dependency add_development_dependency   name:version       |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.name                   |  Regex gem add_dependency add_development_dependency   name         |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.version                |     Regex gem add_dependency add_development_dependency version           |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.development_type               |     Regex gem add_dependency -> runtime          |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   Software_application.development_type               |     Regex gem add_development_dependency -> dev          |
