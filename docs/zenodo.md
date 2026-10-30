When analyzing a Zenodo deposit via ``--doi``, SOMEF retrieves metadata from the Zenodo API 
(``https://zenodo.org/api/records/{id}``). The ``--doi`` flag accepts several input 
The following metadata fields can be extracted from a `.zenodo.json` file.   
These fields are defined in the [Zenodo metadata schema for GitHub releases](https://help.zenodo.org/docs/github/describe-software/zenodo-json) and are mapped according to the [CodeMeta crosswalk for Zenodo](https://codemeta.github.io/crosswalk/zenodo/) and [csv CodeMeta crosswalk for Zenodo](https://github.com/codemeta/codemeta/blob/master/crosswalks/Zenodo.csv)

| Software metadata category  | SOMEF metadata JSON path              | .ZENODO.JSON metadata file field     |
|-----------------------------|---------------------------------------|----------------------------------------|
| author - value              |   author[i].result.value              |   creators.name *(1)*                  |
| author - name               |   author[i].result.name               |   creators.name *(1)*                  |
| author - given name         |   author[i].result.given_name         |   creators.name, only if "Family, Given" format *(1)* |
| author - last name          |   author[i].result.last_name          |   creators.name, only if "Family, Given" format *(1)* |
| author - affiliation        |   author[i].result.affiliation        |   creators.affiliation                 |
| author - identifier         |   author[i].result.identifier         |   creators.orcid *(2)*                 |
| contributor - value         |   contributor[i].result.value         |   contributors.name *(1)*              |
| contributor - name          |   contributor[i].result.name          |   contributors.name *(1)*              |
| contributor - given name    |   contributor[i].result.given_name    |   contributors.name, only if "Family, Given" format *(1)* |
| contributor - last name     |   contributor[i].result.last_name     |   contributors.name, only if "Family, Given" format *(1)* |
| contributor - affiliation   |   contributor[i].result.affiliation   |   contributors.affiliation             |
| contributor - identifier    |   contributor[i].result.identifier    |   contributors.orcid *(2)*             |
| date_published              |   date_published[i].result.value      |   publication_date                     |
| description                 |   description[i].result.value         |   description *(3)*                    |
| keywords                    |   keywords[i].result.value            |   keywords                             |
| license - value             |   license[i].result.value             |   license (string or license.id)       |
| license - name              |   license[i].result.name              |   license, if recognized *(4)*         |
| license - spdx id           |   license[i].result.spdx_id           |   license, if recognized *(4)*         |
| license - identifier        |   license[i].result.identifier        |   license, if recognized *(4)*         |
| name                        |   name[i].result.value                |   title                                |
| version                     |   version[i].result.value             |   version                              |

---

*(1)*
Zenodo usually writes names as `Family, Given`. In that case SOMEF splits the name into `given_name` and `last_name`, and `value` and `name` are returned as `Given Family`. If the name has no comma (for example `Serah Njambi`, a username or an organization) it is not split, and only `value` and `name` are returned.
- Example:
```
"creators": [
  {
    "name": "Frey, Matthias",
    "affiliation": "University of St Andrews",
    "orcid": "0000-0002-7842-0051"
  }
]
```

*(2)*
The ORCID is returned as a URL (`https://orcid.org/<orcid>`). If the file already contains the full URL, it is kept as it is.

*(3)*
Zenodo descriptions may contain HTML. SOMEF removes the HTML tags and returns plain text.

*(4)*
Zenodo uses its own lowercase license identifiers (for example `mit` or `apache-2.0`). The original value is always kept in `value`. SOMEF also tries to recognize the license: if it is recognized, `name`, `spdx_id` and `identifier` (SPDX URL) are added. If it is not recognized, only `value` is returned.
- Example:
```
"license": {"id": "apache-2.0"}
```
returns
```
"value": "apache-2.0",
"name": "Apache License 2.0",
"spdx_id": "Apache-2.0",
"identifier": "https://spdx.org/licenses/Apache-2.0"
```

## Analyzing Zenodo deposits with `--doi`

When analyzing a Zenodo deposit via `--doi`, SOMEF retrieves metadata from the Zenodo API 
(`https://zenodo.org/api/records/{id}`). The `--doi` flag accepts several input 
formats and extracts the following categories (if present):

| SOMEF category | Description | Source |
|---|---|---|
| ``full_title`` | Title of the Zenodo record | Zenodo API |
| ``authors`` | creators (given and family name, ORCID if available) | Zenodo API |
| ``contributors`` | contributors | Zenodo API |
| ``license`` | License of the record, mapped to SPDX (e.g. ``MIT``) | Zenodo API |
| ``version`` | Version of the deposit | Zenodo API |
| ``date_published`` | Publication date | Zenodo API |
| ``code_repository`` | Related repository URL (GitHub/GitLab/Codeberg/Bitbucket) | ``related_identifiers`` in metadata |
| ``keywords`` | Keywords from the record | Zenodo API |
| ``description`` | Description of the deposit | Zenodo API |
| ``download_url`` | files of the deposit | Zenodo API |
| ``identifier`` | The DOI of the record | Zenodo API |

### Accepted input formats

The ``--doi`` flag accepts the following forms of Zenodo DOIs or record URLs:

* ``10.5281/zenodo.X`` – bare DOI
* ``https://doi.org/10.5281/zenodo.X`` – DOI via resolver
* ``https://zenodo.org/records/X`` – record URL (with ``/record/X`` also supported)

If the Zenodo record contains ``related_identifiers`` pointing to a GitHub/GitLab/Codeberg/Bitbucket 
repository, SOMEF will also extract the ``code_repository`` category with the corresponding URL and tag.
| `full_title` | Title of the Zenodo record | Zenodo API |
| `authors` | creators (given and family name, ORCID if available) | Zenodo API |
| `contributors` | contributors | Zenodo API |
| `license` | License of the record, mapped to SPDX (e.g. `MIT`) | Zenodo API |
| `version` | Version of the deposit | Zenodo API |
| `date_published` | Publication date | Zenodo API |
| `code_repository` | Related repository URL (GitHub/GitLab/Codeberg/Bitbucket) | `related_identifiers` in metadata |
| `keywords` | Keywords from the record | Zenodo API |
| `description` | Description of the deposit | Zenodo API |
| `download_url` | files of the deposit | Zenodo API |
| `identifier` | The DOI of the record | Zenodo API |

### Accepted input formats

The `--doi` flag accepts the following forms of Zenodo DOIs or record URLs:

* `10.5281/zenodo.X` – bare DOI
* `https://doi.org/10.5281/zenodo.X` – DOI via resolver
* `https://zenodo.org/records/X` – record URL (with `/record/X` also supported)

If the Zenodo record contains `related_identifiers` pointing to a GitHub/GitLab/Codeberg/Bitbucket 
repository, SOMEF will also extract the `code_repository` category with the corresponding URL and tag.

If the record does not point to a source repository, SOMEF stops with an error.

### Source repository and deposit files

With ``--doi``, SOMEF downloads and analyzes the source repository found in the record, at the
tag of the deposit if available, as it does in the git-based modes. The files of the Zenodo deposit
itself are not downloaded or processed: they are only listed in the ``download_url`` category.

### Enrichment via ``-e``

When the ``-e`` / ``--enrichment`` flag is used, SOMEF makes additional requests to external
services (OpenAlex, OpenAIRE, Zenodo) to complete the metadata, for example the ``openaire_id``
(or ``openalex_id``) and the Software Heritage identifier (``swhid``) of the DOI of the record,
ORCIDs of authors, and project information for funding.

### Example

```bash
somef describe --doi 10.5281/zenodo.22943101 -o output.json
```
With `--doi`, SOMEF downloads and analyzes the source repository found in the record, at the
tag of the deposit if available, as it does in the git-based modes. The files of the Zenodo deposit
itself are not downloaded or processed: they are only listed in the `download_url` category.
