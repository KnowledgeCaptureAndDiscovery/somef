The following metadata fields can be extracted from a gemspec file.   
These fields are defined in the [Ruby Gems specification](https://guides.rubygems.org/specification-reference/) currently at version **2.0**, and are mapped according to the [CodeMeta crosswalk for ruby gems](https://github.com/codemeta/codemeta/blob/master/crosswalks/Ruby%20Gem.csv).

| SOMEF metadata category       | Expected value type            |       SOMEF metadata field  | .gemspec metadata field               |
|-------------------------------|-------------------------------|-----------------------------|------------------------------|
| **authors**                   |  Agent (authors[i].result is of type Agent) | authors[i].result.value   |   gem.authors    *(1)*    |
| **description**               |  String (description[i].result is of type String)|   description[i].resultvalue   |   description   *(2)* |
| **has_package_file**         |  Url(has_package_file[i].result is of type Url) |  has_package_file[i].result.value    |  URL of the filename.gemspec file      |
| **homepage**                  |  Url (homepage[i].result is of type String)|   homepage[i].result.value   |  homepage *(3)*   |
| **license**                   |  License (license[i].result is of type License)|   license[i].result.value   |   license/licenses  *(4)*   |
| **license**                   |  License (license[i].result is of type License)|   license[i].result.spdx_id   |   license/licenses *(4)* spdx_id   |
| **license**                   |  License (license[i].result is of type License)|   license[i].result.name   |    llicense/licenses name  *(4)*  |
| **package_id**                |  String (package_id[i].result is of type String)|   package_id[i].result.value   |   name  *(5)*   |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.value                  |   requirements/add_dependency/add_development_dependency    name:version   *(6)*    |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.name                   |  requirements/add_dependency/add_development_dependency   name    *(6)*      |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.version                |     requirements/add_dependency/add_development_dependency  version     *(6)*      |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.development_type               |     add_dependency -> runtime     *(6)*     |
| **requirements**              |  Software_application (requirements[i].result is of type Software_application) |   requirements[i].result.development_type               |     add_development_dependency -> dev      *(6)*    |

---

*(1)*  
- Regex: `r'gem\.author[s]?\s*=\s*(?P<value>"[^"]*"|\[[^\]]*\])'`  
- Example: 
```
  s.authors     = [
    "André Arko", "Samuel Giddins", "Colby Swandale", "Hiroshi Shibata"
  ]
```
```
  s.author    = "Daniel Garijo"
```

*(2)*  
- Regex: `r'gem\.description\s*=\s*%q{([^}]+)}|gem\.description\s*=\s*["\']([^"\']+)["\']'`  


*(3)*  
- Regex: `r'gem\.homepage\s*=\s*["\']([^"\']+)["\']`  
- Example: `s.homepage    = "https://bundler.io"`
- Result: `https://bundler.io`

*(4)* 
- Regex: `r'gem\.license[s]?\s*=\s*["\']([^"\']+)["\']'` 
- if license with spdx_id: 
``` 
    name
    value
    spdx_id
```
- if not just value
- Example:   `gem.license       = 'MIT'`
- Result: `MIT`

*(5)* 
- Regex: `r'gem\.name\s*=\s*["\']([^"\']+)["\']`
- Example:   `gem.name          = "bootstrap-datepicker-rails"`
- Resutl: `bootstrap-datepicker-rails`

*(5)* 
- Regex1: `r'gem\.requirements\s*=\s*(\[.*?\])'`
- Example:
```
spec.requirements = [
  "Java Development Kit (JDK) 1.6 or newer is required.",
  "The environment variable JAVA_HOME must be correctly defined."
]

```
- Result: `["Java Development Kit (JDK) 1.6 or newer is required.","The environment variable JAVA_HOME must be correctly defined."]`
- Regex2: `r'gem\.add_dependency\s*["\']([^"\']+)["\'](?:\s*,\s*["\']([^"\']+)["\'])?'`
- Regex3: `'gem\.add_development_dependency\s*["\']([^"\']+)["\'](?:\s*,\s*["\']([^"\']+)["\'])?'`
- Example: 
``` 
    gem.add_dependency "railties", ">= 3.0"
    gem.add_development_dependency "bundler", ">= 1.0"
``` 
Result: add_depency --> type runtime; add_development_dependencyd --> type dev 
```
    [{'result': {'value': 'railties: >= 3.0', 'name': 'railties', 'version': '>= 3.0', 'type': 'Software_application', 'dependency_type': 'runtime'}, 'confidence': 1, 'technique': 'code_parser', 'source': 'https://example.org/bootstrap-datepicker-rails.gemspec'}, {'result': {'value': 'bundler: >= 1.0', 'name': 'bundler', 'version': '>= 1.0', 'type': 'Software_application', 'dependency_type': 'dev'}, 'confidence': 1, 'technique': 'code_parser', 'source': 'https://example.org/bootstrap-datepicker-rails.gemspec'}]
```





