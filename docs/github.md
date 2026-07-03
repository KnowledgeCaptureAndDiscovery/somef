When analyzing a GitHub repository, SOMEF uses the [GitHub REST API](https://docs.github.com/en/rest/repos/repos)
(`GET /repos/{owner}/{repo}`) to retrieve metadata. The table below shows how GitHub API
fields map to SOMEF categories:

| SOMEF category | GitHub API field | Notes |
|---|---|---|
| `code_repository` | `html_url` | |
| `owner` | `owner.login` | `agent_type` is extracted from `owner.type` (User or Organization) |
| `date_created` | `created_at` | |
| `date_updated` | `updated_at` | |
| `license` | `license` | Nested object with `spdx_id`, `name`, `url` |
| `description` | `description` | |
| `name` | `name` | |
| `full_name` | `full_name` | Format: `{owner}/{repo}` |
| `issue_tracker` | `issues_url` | The `{/number}` suffix is stripped |
| `forks_url` | `forks_url` | |
| `stargazers_count` | `stargazers_count` | |
| `keywords` | `topics` | |
| `forks_count` | `forks_count` | |
| `homepage` | `homepage` | |
| `programming_languages` | `languages` | Additional GET to `/repos/{owner}/{repo}/languages`. Returns a dictionary with byte counts per language |
| `releases` | `/repos/{owner}/{repo}/releases` | Paginated results, mapped via `release_crosswalk_table` |
| `download_url` | *(constructed)* | Built as `https://github.com/{owner}/{repo}/releases` |

### Archive download

SOMEF downloads the repository archive from `https://github.com/{owner}/{repo}/archive/{ref}.zip`.
GitHub archive URLs do not include a `Content-Length` header, so SOMEF uses a streaming check:
it reads the response in 1 MB chunks and aborts if the total exceeds the configured size limit
(see `--download-limit`).

If the ref name is ambiguous (a branch and a tag share the same name), GitHub returns
HTTP 300. SOMEF handles this by trying the following fallback URLs in order:

1. `https://github.com/{owner}/{repo}/archive/{ref}.zip` (short form)
2. `https://github.com/{owner}/{repo}/archive/refs/heads/{ref}.zip` (explicit branch)
3. `https://github.com/{owner}/{repo}/archive/refs/tags/{ref}.zip` (explicit tag)
4. `https://github.com/{owner}/{repo}/archive/main.zip` (legacy rename fallback)

### Limitations

- **Private repositories**: SOMEF cannot access private repositories without a valid token.


### Enrichment via CODEOWNERS

When `--reconcile_authors` (`-ra`) is enabled, SOMEF fetches additional user details
(name, company, email) from `GET https://api.github.com/users/{username}` for the
repository owner and for each CODEOWNERS entry.