When analyzing a Bitbucket repository, SOMEF uses the [Bitbucket Cloud API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/)
(`GET /2.0/repositories/{workspace}/{repo_slug}`) to retrieve metadata. The table below shows how Bitbucket API
fields map to SOMEF categories:

| SOMEF category | Bitbucket API field | Notes |
|---|---|---|
| `name` | `slug` | |
| `description` | `description` | |
| `full_name` | `full_name` | Format: `{workspace}/{slug}` |
| `code_repository` | `links.html.href` | |
| `owner` | `owner.nickname` | Falls back to `owner.username` for team workspaces |
| `date_created` | `created_on` | |
| `date_updated` | `updated_on` | |
| `homepage` | `website` | |
| `forks_url` | `links.forks.href` | |
| `download_url` | *(constructed)* | Built as `{html_url}/downloads` |
| `issue_tracker` | *(constructed)* | Built as `{html_url}/issues` when `has_issues` is true |
| `programming_languages` | `language` | Single string, not a dictionary with sizes |
| `releases` | `/refs/tags` | Bitbucket has no dedicated releases endpoint; uses the tags endpoint |
| `stars` | *(not available)* | Bitbucket does not have a stargazers feature |
| `forks_count` | *(not available)* | Bitbucket does not expose fork counts in its API |