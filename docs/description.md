The following metadata fields can be extracted from a DESCRIPTION file.   
These fields are defined in the [DESCRIPTON specification](https://r-pkgs.org/description.html), and are mapped according to the [CodeMeta crosswalk for DESCRIPTION files based in R Package](https://github.com/codemeta/codemeta/blob/master/crosswalks/R%20Package%20Description.csv).

| Software metadata category    | SOMEF metadata JSON path          | DESCRIPTION metadata file field    |
|-------------------------------|---------------------------------|---------------------|
| authors                   |   authors[i].result.value      |  Authors *(1)*  |
| authors                   |   authors[i].result.email      | Authors *(2)*  |
| code_repository          |   code_repository[i].result.value   |     URL *(3)* |
| description               |   description[i].result.value   |    Description *(3)*  |
| has_package_file          |   has_package_file[i].result.value    |  URL of the DESCRIPTION file       |
| homepage                  |   homepage[i].result.value   |  URL    *(3)*   |
| issue_tracker            |   issue_tracker[i].result.value   | BugReports  *(5)*   |
| license                   |   license[i].result.value   | License   *(6)*   |
| package_id                |   package_id[i].result.value   |   Package   *(6)*    |
| version                   |   version[i].result.value   |   Version  *(7)*   |

---

*(1)*, *(2)* , 
- Regex 1: `r'Authors@R:\s*c\(([\s\S]*?)\)\s*$' → group[1]`  
- Regex 2: `find in group[1] all persons and extract first name (or organition), last name and email`
- Example: 
```
        Authors@R: c(
            person("Hadley", "Wickham", , "hadley@posit.co", role = "aut",
                comment = c(ORCID = "0000-0003-4757-117X")),
            person("Winston", "Chang", role = "aut",
                comment = c(ORCID = "0000-0002-1576-2126"))
        )
```

- Result: 
```
{'result': {'value': 'Hadley Wickham', 'type': 'Agent', 'email': 'hadley@posit.co'}, 'confidence': 1, 'technique': 'code_parser', 'source': 'https://example.org/DESCRIPTION'}, {'result': {'value': 'Winston Chang', 'type': 'Agent'}, 'confidence': 1, 'technique': 'code_parser', 'source': 'https://example.org/DESCRIPTION'}
```

*(3)*
- Regex: `'URL:\s*([^\n]+(?:\n\s+[^\n]+)*)'`
- if github.com or gitlab.com  --> code_repository
- if not  --> homepage

- Example: 
```
URL: https://ggplot2.tidyverse.org,
        https://github.com/tidyverse/ggplot2
```

- Result code_repository: `'result': {'value': 'https://github.com/tidyverse/tidyverse', 'type': 'Url'}`
- Result hompeage: `'result': {'value': 'https://tidyverse.tidyverse.org', 'type': 'Url'}}`


*(3)*
- Regex: `r'Description:\s*([^\n]+(?:\n\s+[^\n]+)*)', content)`
- Example: 
```Description: A system for 'declaratively' creating graphics, based on "The
    Grammar of Graphics". You provide the data, tell 'ggplot2' how to map
    variables to aesthetics, what graphical primitives to use, and it
    takes care of the details.
```
- Result: 
```
A system for 'declaratively' creating graphics, based on "The
    Grammar of Graphics". You provide the data, tell 'ggplot2' how to map
    variables to aesthetics, what graphical primitives to use, and it
    takes care of the details.
```

*(5)*
- Regex: `'BugReports:\s*([^\n]+)'`
- Example: `BugReports: https://github.com/tidyverse/ggplot2/issues`
- Result: `https://github.com/tidyverse/ggplot2/issues`

*(5)*
- Regex: `r'License:\s*([^\n]+)'``
- Example: `License: MIT + file LICENSE`
- Result: `MIT + file LICENSE`

*(6)*
- Regex: `r'Package:\s*([^\n]+)`
- Example: `Package: ggplot2`
- Result: `ggplot2`

*(6)*
- Regex: `r'Version:\s*([^\n]+)'`
- Example: `Version: 2.0.0.9000`
- Result: `2.0.0.9000`
