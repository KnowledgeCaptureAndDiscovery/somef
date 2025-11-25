The following metadata fields can be extracted from a setup.py file.   
These fields are defined in the [Setup.py specification](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#setup-args), and are mapped according to the [CodeMeta crosswalk for python](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| SOMEF metadata category       | Expected value type            |       SOMEF metadata field  | SETUP.PY metadata field               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.value   |     author     *(1)*          |
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.email   |  author_email or EMAIL  *(1)*   |
| **code_repository**           |  Url (code_repository[i].result is of type Url)  | code_repository[i].result.value   |   url or URL      |
| **description**               |  String (description[i].result is of type String) |   description[i].result .value  |   description or DESCRIPTION  |
| **keywords**                  |  String(keywords[i].result is of type String)  |   keywords[i].result.value          |     keywords |
| **license**                   |  License(license[i].result is of type License) |   license[i].result.value    |   license          |
| **package_id**                |  String (package_id[i].result is of type String)|   package_id[i].result.value   |   name                        |
| **programming_languages**     |  String(programming_languages[i].result is of type String)  |   programming_languages[i].result.value   |  if classifiers  -> "python" *(2)*  |

---

*(1)*  
- Example: 
```
    author='Colin Raffel',
    author_email='craffel@gmail.com',
```
- Result: `result {'name': 'Colin Raffel', 'email':'craffel@gmail.com'}`

*(2)*  
- Example: 
```
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
    ],
```
- Result: always `"value": "Python"` if 'Programming Language :: Python' in classifiers.


