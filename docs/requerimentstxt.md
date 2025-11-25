The following metadata fields can be extracted from a requirements file.   
These fields are defined in the [Requirements specification](https://pip.pypa.io/en/stable/reference/requirements-file-format/), currently at version **25.2**, and are mapped according to the [CodeMeta crosswalk for requirements files](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| SOMEF metadata category       | Expected value type            |       SOMEF metadata field  |REQUIREMENTS.TXT metadata field  |   
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  requirements[i].result.value  |  *(1)*  |
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  requirements[i].result.name   |  *(1)*    |
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  requirements[i].result.version| *(1)*   |
| **runtime_platform**     | String (runtime_platform[i].result is of type String)  |   runtime_platform[i].result.value | if Python *(1)* |
| **runtime_platform**     | String (runtime_platform[i].result is of type String) |   runtime_platform[i].result.name |   "Python"   |


---

*(1)*  
- Example: `docstring_parser==0.7`
- Result: 
```
value : docstring_parser==0.7
name : docstring_parser=
version : 0.7
```

*(2)*
- Always "Python" and version if exists.
- Example: `python= ">=3.11"`