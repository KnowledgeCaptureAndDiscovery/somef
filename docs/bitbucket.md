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
| `download_url` | *(built from URL)*| Built as `{html_url}/downloads` |
| `issue_tracker` | *(built from URL)* | Built as `{html_url}/issues` when `has_issues` is true |
| `programming_languages` | `language` | Single string, not a dictionary with sizes |
| `releases` | `/refs/tags` | Bitbucket has no dedicated releases endpoint; uses the tags endpoint |
| `stargazers_count` | *(not available)* | Bitbucket does not have a stargazers feature |
| `forks_count` | *(not available)* | Bitbucket does not expose fork counts in its API |


### Authentication

Bitbucket uses HTTP Basic authentication. The token is encoded as
`base64(email:token)` and sent as the `Authorization` header.
Provide both the Bitbucket app password and your Atlassian account email
via `--bitbucket-token` and `--bitbucket-email`, or by running `somef configure`.

### Archive download

Repository archives are downloaded from:
`https://bitbucket.org/{owner}/{repo}/get/{branch}.zip`

Bitbucket archive URLs typically include a `Content-Length` header, so the size limit check
can be performed before downloading.

### Limitations

- **No stargazers**: Bitbucket does not have a stargazers feature.
- **No forks count**: Bitbucket does not expose fork counts in its API.
- **Tags-only releases**: Bitbucket has no dedicated releases endpoint.
  SOMEF uses the `/refs/tags` endpoint instead, which does not include release
  descriptions or assets.
- **Programming languages**: Bitbucket returns only a single language string,
  without byte counts per language.
- **CODEOWNERS enrichment**: Not supported for Bitbucket, as the platform does not
  expose a public user API.
- **Rate limits**: Unauthenticated requests are limited to 60 requests/hour.
  Authenticated requests (via `bitbucket-token` and `bitbucket-email` ) have higher limits) have higher limits.
  Create an app password at `https://bitbucket.org/account/settings/api-tokens/`
  with `read:repository:bitbucket` and `read:account` scopes.