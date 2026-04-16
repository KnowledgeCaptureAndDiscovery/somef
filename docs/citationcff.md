The following metadata fields can be extracted from a CITATION.cff file. 
These fields are defined in the [CITATION.cff specification](https://citation-file-format.github.io/), currently at version [1.2.0](https://github.com/citation-file-format/citation-file-format/releases/tag/1.2.0), and are mapped according to the [CodeMeta crosswalk](https://github.com/codemeta/codemeta/tree/master/crosswalks).

| Software metadata category | SOMEF metadata JSON path | CITATION.cff metadata file field |
|----------------------------|---------------------------------------|---------------------|
| citation - authors - name | citation[i].result.authors[j].name | authors / preferred-citation.authors |
| citation - authors - family_name | citation[i].result.authors[j].family_name | authors.family-names |
| citation - authors - given_name | citation[i].result.authors[j].given_name | authors.given-names |
| citation - authors - url | citation[i].result.authors[j].url | authors.orcid |
| citation - doi | citation[i].result.doi | doi / preferred-citation.doi |
| citation - datePublished | citation[i].result.datePublished | date-released |
| citation - is_preferred_citation | citation[i].result.is_preferred_citation | "True" if from preferred-citation. Omitted otherwise|
| citation - journal | citation[i].result.journal | preferred-citation.journal |
| citation - year | citation[i].result.year | preferred-citation.year |
| citation - pages | citation[i].result.pages | preferred-citation.pages |
| citation - title | citation[i].result.title | title / preferred-citation.title |
| citation - type | citation[i].result.type | type / preferred-citation.type *(1)* |
| license - value | license[i].result.value | license |
| license - spdx_id | license[i].result.spdx_id | license |
| license - name | license[i].result.name | license  |

---

*(1)* 
For the CFF main block, the type is mapped to SoftwareApplication. For the preferred-citation block, it is mapped to ScholarlyArticle.

