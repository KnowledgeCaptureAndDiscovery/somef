The following metadata fields can be extracted from a gemspec file.   
These fields are defined in the [Ruby Gems specification](https://guides.rubygems.org/specification-reference/) currently at version **2.0**, and are mapped according to the [CodeMeta crosswalk for ruby gems](https://github.com/codemeta/codemeta/blob/master/crosswalks/Ruby%20Gem.csv).

| Software metadata category    |   SOMEF metadata JSON path     | .gemspec metadata file field               |
|-------------------------------|--------------------------------|--------------------------------------|
| authors                  |  authors[i].result.value   |   gem.authors    *(1)*    |
| description              |  description[i].resultvalue   |   description   *(2)* |
| has_package_file          |  has_package_file[i].result.value    |  URL of the filename.gemspec file      |
| homepage                  |  homepage[i].result.value   |  homepage *(3)*   |
| license - value                   |  license[i].result.value   |   license/licenses  *(4)*   |
| license - spdx id                   |  license[i].result.spdx_id   |   license/licenses *(4)* spdx_id   |
| license - name                   |  license[i].result.name   |    llicense/licenses name  *(4)*  |
| package_id                |  package_id[i].result.value   |   name  *(5)*   |
| requirements - value              |  requirements[i].result.value                  |   requirements/add_dependency/add_development_dependency    name:version   *(6)*    |
| requirements - name              |  requirements[i].result.name                   |  requirements/add_dependency/add_development_dependency   name    *(6)*      |
| requirements - version             |  requirements[i].result.version                |     requirements/add_dependency/add_development_dependency  version     *(6)*      |
| requirements - development type             |  requirements[i].result.development_type               |     add_dependency -> runtime     *(6)*     |
| requirements - development type                |  requirements[i].result.development_type               |     add_development_dependency -> dev      *(6)*    |

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





