# OpenAlex API Mapping

When the enrichment flag (`-e` / `--enrichment`) is enabled, SOMEF integrates with the **OpenAlex API** to resolve and complete scholarly publication data and missing author identities.

## Citation Enrichment
If OpenAIRE fails to resolve a publication's DOI, SOMEF queries OpenAlex as a fallback to fetch the publication's unique ID.

| SOMEF Property | Source API Function | Description |
| :--- | :--- | :--- |
| `openalex_id` | `get_openalex_id(doi)` | The unique OpenAlex URL identifier assigned to the publication. |

## Author/Contributor Enrichment
For extracted authors or contributors who lack a structured identifier, SOMEF searches OpenAlex by name to retrieve their professional ORCID.

| SOMEF Property | Source API Function | Description |
| :--- | :--- | :--- |
| `identifier` | `search_openalex_author(name)` | The author's verified ORCID URL (used as fallback when missing in local files). |