The following metadata fields can be extracted from a AUTHORS file.   
These fields are defined in the [Authors file specification](https://opensource.google/documentation/reference/releasing/authors/), and are mapped according to the [CodeMeta crosswalk for AUTHORS files](https://github.com/codemeta/codemeta/blob/master/crosswalks/codemeta-V2.csv).

| SOMEF metadata category       | Category describes            |       SOMEF metadata field  | AUTHORS file value               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|  
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.value   |    regex name      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.name   |     regex name      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.email   |    regex email      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.given_name   | regex from name if type person      |
| **authors**                   |  Agent (authors[i].result is of type Agent) | Agent.last_name   |     regex from name if type person     |
