# OpenAIRE and Zenodo API Mapping

When the enrichment flag (`-e` / `--enrichment`) is enabled, SOMEF integrates with the **OpenAIRE** and **Zenodo** APIs to fetch project context, funding background, and ecosystem identifiers.

## Funding Enrichment (OpenAIRE)

These fields are injected into the **Funding** category when a matching grant or project is reconciled via OpenAIRE keywords or grant identifiers.

| SOMEF Property | Source API Field | Description |
| :--- | :--- | :--- |
| `project_code` | `code` | The official project or grant code assigned by the funding body. |
| `project_title` | `title` | The full title of the funded research project. |
| `project_acronym` | `acronym` | The official acronym of the project. |
| `grant_id` | `callidentifier` | Unique identifier for the specific call or grant agreement. |

## Identifier Enrichment (OpenAIRE & Zenodo)

When processing repository identifiers or DOIs found in citations, SOMEF resolves them against OpenAIRE to construct an explore landing page link. Additionally, if the DOI belongs to Zenodo, SOMEF queries the Zenodo API to extract its corresponding Software Heritage identifier (`swhid`).

| SOMEF Property | Source API / Function | Description |
| :--- | :--- | :--- |
| `openaire_id` | `get_openaire_id(doi)` | Direct link to the OpenAIRE explore page dedicated to this artifact. |
| `swhid` | `get_zenodo_swhid(doi)` | The Software Heritage Identifier (SWHID) associated with a Zenodo record. |