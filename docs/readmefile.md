The following metadata fields can be extracted from a readme.md file.   
Unlike others files formats (pom, cargo, cabal...), README documents do not follow a formal specification. They are free‑form text files, usually written in markdown or restructuredtext, and their structure varies widely across projects. SOMEF applies heuristics to identify common sections (e.g., Title, Description, Installation, Usage, License...) and extracts metadata accordingly.

| Software metadata category     |    SOMEF metadata JSON path            | README.MD metadata file field     |
|--------------------------------|----------------------------------------|----------------------------------------|
| acknowledgement                |     acknowledgement[i].result.value      |  hearders with acknowledgement        |
| citation                       |     citation[i].result.value      |  headers with citation, reference, cite. Extract bibtext  **(1)**       |
| contact                       |     contact[i].result.value      |  headers with contact       |
| contributing_guidelines                      |     contributing_guidelines[i].result.value      |  headers with contributing     |
| contributors                       |     contributors[i].result.value      |  headers with contributor      |
| description                       |     description[i].result.value      |  headers with description, introduction, basics, initiation, overview      |
| documentation                  |     documentation[i].result.value      |  github or gitlab url documentation **(2)**, headers with documentation, readthedocs same name project, readthedocs in badges, wiki links in badges and text       |
| download                       |     download[i].result.value      |  headers with download       |
| executable_example                      |     executable_example[i].result.value      |  extracts Binder from badgets   **(3)**    |
| faq                       |     faq[i].result.value      |  headers with faq, errors, problems   |
| full_title                       |     full_title[i].result.value      |  extract full title   **(4)** |
| homepage                       |     homepage[i].result.value      |  homepage from badgets  **(5)**  |
| identifier                    |     idenfier[i].result.value         |     extract from badgets directly or get from zenodo with latest doi **(6)**, swh identifiers **(7)**         |
| images                       |     images[i].result.value      |  other images in the README apart from the logo   |
| installation                      |     installation[i].result.value      |  headers with installation, install, setup, prepare, preparation, manual, guide       |
| license                       |     license[i].result.value      |  headers with license      |
| logo                       |     logo[i].result.value      |   look images in badges and text **(8)**  |
| package_distribution                       |    package_distribution[i].result.value      |  Pypi or latest Pypi version in badges   **(9)**   |
| related_documentation                  |     dorelated_documentationumentation[i].result.value      |   readthedocs diferent name project     |
| run                       |     run[i].result.value      |  headers with run, execute       |
| readme_url                     |     readme_url[i].result.value         |     url in raw githubuser content **(10)**         |
| related_papers                   |     related_papers[i].result.value         |    look for arXiv reference in all the text **(11)**       |
| repository_status                       |     repository_status[i].result.value      |  badges with Project status **(12)**  |
| requirements                     |     requirements[i].result.value      |  headers with requirement, prerequisite, dependency, dependent      |
| support                       |     support[i].result.value      |  headers with support, help, report   |
| support_channels               |     support_channels[i].result.value      |  extract information of gitter, reddit and discord in badges and text  **(13)**  |
| usage                       |     usage[i].result.value      |  headers with usage, example, implement, implementation, demo, tutorial, start, started      |


------

**(1)** 
- Example:
```bib
@inproceedings{garijo2017widoco,
  title={WIDOCO: a wizard for documenting ontologies},
  author={Garijo, Daniel},
  booktitle={International Semantic Web Conference},
  pages={94--102},
  year={2017},
  organization={Springer, Cham},
  doi = {10.1007/978-3-319-68204-4_9},
  funding = {USNSF ICER-1541029, NIH 1R01GM117097-01},
  url={http://dgarijo.com/papers/widoco-iswc2017.pdf}
}
```
- Result:
```
{
    "result": {
        "value": "@inproceedings{garijo2017widoco,\n    url = {http://dgarijo.com/papers/widoco-iswc2017.pdf},\n    funding = {USNSF ICER-1541029, NIH 1R01GM117097-01},\n    doi = {10.1007/978-3-319-68204-4_9},\n    organization = {Springer, Cham},\n    year = {2017},\n    pages = {94--102},\n    booktitle = {International Semantic Web Conference},\n    author = {Garijo, Daniel},\n    title = {WIDOCO: a wizard for documenting ontologies},\n}",
        "type": "Text_excerpt",
        "format": "bibtex",
        "doi": "10.1007/978-3-319-68204-4_9",
        "title": "WIDOCO: a wizard for documenting ontologies",
        "author": "Garijo, Daniel",
        "url": "http://dgarijo.com/papers/widoco-iswc2017.pdf"
    },
}
```


**(2)** 
- Example if github:
```
f"https://github.com/{owner}/{repo_name}/tree/{urllib.parse.quote(repo_default_branch)}/{docs_path}"
```
- Example if gitlab:
```
f"https://{domain_gitlab}/{owner}/{repo_name}/-/tree/{urllib.parse.quote(repo_default_branch)}/{docs_path}"
```

**(3)** 
- Example: `[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/user/repo/HEAD)`
- Result: `"value": "https://mybinder.org/v2/gh/user/repo/HEAD"`

**(4)** 
- Example: `# WIzard for DOCumenting Ontologies (WIDOCO)`
- Result:
```
"full_title": [
  {
    "result": {
      "type": "String",
      "value": "WIzard for DOCumenting Ontologies (WIDOCO)"
    },
    "confidence": 1,
    "technique": "regular_expression",
    "source": "https://raw.githubusercontent.com/dgarijo/Widoco/master/README.md"
  }
]
```

**(5)** 
- Example: `[![Project homepage](https://img.shields.io/badge/homepage-project-blue)](https://myproject.org)`
- Result: `"value": "https://myproject.org"`


**(6)** 
- Example: `[![DOI](https://zenodo.org/badge/11427075.svg)](https://doi.org/10.5281/zenodo.11093793)`
- Result: `"value": "https://doi.org/10.5281/zenodo.11093793"`

**(7)** 
- Example: `[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:40d462bbecefc3a9c3e810567d1f0d7606e0fae7/)](https://archive.softwareheritage.org/swh:1:dir:40d462bbecefc3a9c3e810567d1f0d7606e0fae7;origin=...)`
- Result: ` "value": "https://archive.softwareheritage.org/swh:1:dir:40d462bbecefc3a9c3e810567d1f0d7606e0fae7",`


**(8)** 
- Example: `![Logo](src/main/resources/logo/logo2.png)`
- Result: `"value": "https://raw.githubusercontent.com/dgarijo/Widoco/master/src/main/resources/logo/logo2.png"``

**(9)** 
- Example: `[![PyPI](https://badge.fury.io/py/somef.svg)](https://badge.fury.io/py/somef) `
- Result: `"value": "https://pypi.org/project/somef"`


**(10)** 
- Example: 
```
[Yulun Zhang](http://yulunzhang.com/), [Yapeng Tian](http://yapengtian.org/), [Yu Kong](http://www1.ece.neu.edu/~yukong/), [Bineng Zhong](https://scholar.google.de/citations?user=hvRBydsAAAAJ&hl=en), and [Yun Fu](http://www1.ece.neu.edu/~yunfu/), "Residual Dense Network for Image Super-Resolution", CVPR 2018 (spotlight), [[arXiv]](https://arxiv.org/abs/1802.08797) 
```
- Result: `"value": "https://arxiv.org/abs/1802.08797"`


**(11)** 
- Example:
```
f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/{urllib.parse.quote(partial)}" 
```

**(12)** 
- Example:
```
 [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) 
```
- Result:
```
"value": "https://www.repostatus.org/#active",
"description": "Active \u2013 The project has reached a stable, usable state and is being actively developed."
```

**(13)** 
- Example:
```
[![Gitter chat](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/myproject/community)
[Reddit](https://www.reddit.com/r/myproject)
[Discord](https://discord.com/invite/xyz789)
```
- Result:
```
"value": "https://gitter.im/myproject/community"
....
"value": "https://www.reddit.com/r/myproject"
.....
"value": "https://discord.com/invite/xyz789"
```


