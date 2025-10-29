The following metadata fields can be extracted from a requirements file.   
These fields are defined in the [Requirements specification](https://pip.pypa.io/en/stable/reference/requirements-file-format/), currently at version **25.2**, and are mapped according to the [CodeMeta crosswalk for requirements files](https://github.com/codemeta/codemeta/blob/master/crosswalks/Python%20Distutils%20(PyPI).csv).

| SOMEF metadata category       | Category describes            |       SOMEF metadata field  |REQUIREMENTS.TXT value       
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  Software_application.value  |  line |
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  Software_application.name   |  regex line -> name   |
| **requirements**         |  Software_application (requirements[i].result is of type Software_application) |  Software_application.version| regex line -> version |
| **runtime_platform**     | String (runtime_platform[i].result is of type String)  |   String.value |  regex version if Python |
| **runtime_platform**     | String (runtime_platform[i].result is of type String) |   String.name |   "Python"   |

