The following metadata fields can be extracted from a setup.py file.   
These fields are defined in the [Setup.py specification](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#setup-args), and are mapped according to the [CodeMeta crosswalk for python](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| Software metadata category    |       SOMEF metadata JSON path  | SETUP.PY metadata file field  |
|-------------------------------|------------------------------|------------------------------|
| **authors**                   |  authors[i].result.value   |     author     *(1)*          |
| **authors**                   |  authors[i].result.email   |  author_email or EMAIL  *(1)*   |
| **code_repository**           |  code_repository[i].result.value   |   url or URL      |
| **description**               |  description[i].result .value  |   description or DESCRIPTION  |
| **keywords**                  |  keywords[i].result.value          |     keywords |
| **license**                   |  license[i].result.value    |   license          |
| **package_id**                |  package_id[i].result.value   |   name                        |
| **programming_languages**     |  programming_languages[i].result.value   |  if classifiers  -> "python" *(2)*  |

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


