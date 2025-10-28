The following metadata fields can be extracted from a DESCRIPTION file.   
These fields are defined in the [DESCRIPTON specification](https://r-pkgs.org/description.html), and are mapped according to the [CodeMeta crosswalk for DESCRIPTION files based in R Package](https://github.com/codemeta/codemeta/blob/master/crosswalks/R%20Package%20Description.csv).

| SOMEF metadata category       | Category describes        | SOMEF metadata field          | DESCRIPTION file    |
|-------------------------------|---------------------------|-------------------------------|---------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value      |  Regex 'Authors:'   regex firsname + regex lastname |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email      |  Regex 'Authors:'   regex email |
| **code_repository**           |  Url (code_repository[i].result is of type Url)  | Url.value   |  Regex 'URL:'  if github.com or gitlab.com      |
| **description**               |  String (description[i].result is of type String)|   String.value   |   Regex 'Description:'    |
| **has_package_field**         |  Url(has_package_file[i].result is of type Url) |  Url.value    |   "DESCRIPTION"        |
| **hompage**           |  Url (homepage[i].result is of type Url)  | Url.value   |  Regex 'URL:'  if not (github.com or gitlab.com)     |
| **issue_tracker**           |  Url (issue_tracker[i].result is of type Url)  | Url.value   |  Regex 'BugReports:'    |
| **license**                  |  String (license[i].result is of type String)|   String.value   |   Regex 'License:'    |
| **package_id**                |  String (package_id[i].result is of type String)|   String.value   |   Regex 'Package:'    |
| **version**                  |  String (version[i].result is of type String)|   String.value   |   Regex 'Version:'    |


