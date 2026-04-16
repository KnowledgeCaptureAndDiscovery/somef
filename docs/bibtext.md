The following metadata fields can be extracted from a BibTeX *.bib file. 
These fields are defined in the [BibTeX specification](https://www.bibtex.org/Format/), and are mapped according to the [CodeMeta crosswalk for BibTeX](https://github.com/codemeta/codemeta/blob/master/crosswalks/BibTeX.csv).

| Software metadata category | SOMEF metadata JSON path | BibTeX metadata file field |
|----------------------------|---------------------------------------|---------------------|
| citation - value | citation[i].result.value | Full BibTeX entry (reconstructed) |
| citation - author | citation[i].result.author | author |
| citation - doi | citation[i].result.doi | doi |
| citation - title | citation[i].result.title | title |
| citation - url | citation[i].result.url | url |
| citation - format | citation[i].result.format | Fixed to "bibtex" |