When analyzing a Codeberg repository, SOMEF uses the [Codeberg API](https://codeberg.org/api/v1/swagger)
(`GET /api/v1/repos/{owner}/{repo}`) to retrieve metadata. The table below shows how Codeberg API
fields map to SOMEF categories:

| SOMEF category | Codeberg API field | Notes |
|---|---|---|
| `code_repository` | `html_url` | |
| `owner` | `owner.login` | |
| `full_name` | `full_name` | Format: `{owner}/{repo}` |
| `name` | `name` | |
| `description` | `description` | |
| `date_created` | `created_at` | |
| `date_updated` | `updated_at` | |
| `stargazers_count` | `stars_count` | Called `stars_count` in Codeberg |
| `forks_count` | `forks_count` | |
| `homepage` | `website` | Called `website` in Codeberg, `homepage` in GitHub |
| `download_url` | *(built from URL)* | `https://codeberg.org/{owner}/{repo}/releases` |
| `keywords` | `topics` | |
| `issue_tracker` | *(built from URL)* | `{html_url}/issues` |
| `license` | *(content API)* | *1* |
| `programming_languages` | `languages_url` | Additional GET request to the languages endpoint, returns byte counts per language |
| `releases` | `/repos/{owner}/{repo}/releases` | Additional GET request, mapped via `release_codeberg_crosswalk_table` |

For releases, the field mapping is identical to GitHub. The only differences are that Codeberg
uses `attachments` instead of `assets` for release files, and it does not provide
`author.type` (`AGENT_TYPE`) for release authors.


--------------- 

*1*
Extracted by fetching the LICENSE file via `GET /api/v1/repos/{owner}/{repo}/contents/{filename}` (tries `LICENSE`, `LICENSE.md`, `LICENCE`, `COPYING`). The content is base64-decoded and analyzed with `detect_license_spdx()` to obtain the SPDX identifier, name and URL.

### Archive download

Repository archives are downloaded from:
`https://codeberg.org/{owner}/{repo}/archive/{branch}.zip`

Codeberg archive URLs typically include a `Content-Length` header, so the size limit check
can be performed before downloading.

### Enrichment via CODEOWNERS

When `--reconcile_authors` (`-ra`) is enabled, SOMEF fetches additional user details
(full name, email) from `GET https://codeberg.org/api/v1/users/{username}` for the
repository owner and for each CODEOWNERS entry.

### Limitations

- **Rate limits**: Unauthenticated requests are limited to 60 requests/hour. Authenticated
  requests (via `codeberg-token`) have higher limits. Create a token at
  `https://codeberg.org/user/settings/applications`.
- **License detection**: Codeberg does not provide a `license` field in the repository
  API response. SOMEF falls back to fetching LICENSE/COPYING files directly via the
  content API.