When analyzing a Zenodo deposit via ``--doi``, SOMEF retrieves metadata from the Zenodo API 
(``https://zenodo.org/api/records/{id}``). The ``--doi`` flag accepts several input 
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
