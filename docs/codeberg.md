When analyzing a Codeberg repository, SOMEF uses the [Codeberg API](https://codeberg.org/api/v1/swagger) 
(`GET /api/v1/repos/{owner}/{repo}`) to retrieve metadata. The table below shows how Codeberg API 
fields map to SOMEF categories:

| SOMEF category | Codeberg API field | Notes |
|---|---|---|
| `name` | `name` | |
| `description` | `description` | |
| `code_repository` | `html_url` | |
| `owner` | `owner.login` | |
| `date_created` | `created_at` | |
| `date_updated` | `updated_at` | |
| `stars` | `stars_count` | In GitHub this field is `stargazers_count` |
| `forks_count` | `forks_count` | |
| `homepage` | `website` | In GitHub this field is `homepage` |
| `keywords` | `topics` | |
| `issue_tracker` | *(constructed)* | Built as `{html_url}/issues` |
| `license` | *(content API)* | *1* |
| `programming_languages` | `languages_url` | Additional GET request to the languages endpoint |
| `releases` | `/repos/{owner}/{repo}/releases` | Additional GET request |

For releases, the field mapping is identical to GitHub. The only differences are that Codeberg 
uses `attachments` instead of `assets` for release files, and it does not provide 
`author.type` (`AGENT_TYPE`) for release authors.

--------------- 

*1*
Extracted by fetching the LICENSE file via `GET /api/v1/repos/{owner}/{repo}/contents/{filename}` (tries `LICENSE`, `LICENSE.md`, `LICENCE`, `COPYING`). The content is base64-decoded and analyzed with `detect_license_spdx()` to obtain the SPDX identifier, name and URL. Technique: `Codeberg_API`.