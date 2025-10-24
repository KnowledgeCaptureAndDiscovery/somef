The following metadata fields can be extracted from a setup.py file.   
These fields are defined in the [Setup.py specification](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#setup-args), and are mapped according to the [CodeMeta crosswalk for python](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| SOMEF metadata category       | Category describes            |       SOMEF metadata field  | SETUP.PY value               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value   |     author                  |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email   |     author_email or EMAIL    |
| **code_repository**           |  Url (code_repository[i].result is of type Url)  | Url.value   |   url or URL      |
| **description**               |  String (description[i].result is of type String) |   String.value  |   description or DESCRIPTION  |
| **keywords**                  |  String(keywords[i].result is of type String)  |   String.value          |     keywords |
| **license**                   |  License(license[i].result is of type License) |   License.value    |   license          |
| **package_id**                |  String (package_id[i].result is of type String)|   String.value   |   name                        |
| **programming_languages**     |  String(programming_languages[i].result is of type String)  |   String.value   |  if classifiers  -> "python" |

