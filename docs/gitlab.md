When analyzing a GitLab repository, SOMEF uses the [GitLab REST API](https://docs.gitlab.com/ee/api/projects.html)
(`GET /api/v4/projects/{project_id}`) to retrieve metadata. The table below shows how GitLab API
fields map to SOMEF categories:

| SOMEF category | GitLab API field | Notes |
|---|---|---|
| `code_repository` | *(built from URL)* | `https://{host}/{project_path}/` |
| `download_url` | *(built from URL)* | `https://{host}/{project_path}/-/branches` |
| `defaultBranch` | `default_branch` | Also checks `defaultBranch` (legacy key) |
| `description` | `description` | |
| `name` | `name` | |
| `full_name` | `path_with_namespace` | |
| `owner` | `owner.username` | `agent_type` deduced from `namespace.kind` ("group" → Organization, "user" → Person) |
| `date_created` | `created_at` | |
| `date_updated` | `last_activity_at` | |
| `issue_tracker` | *(built from URL)* | `https://{host}/{project_path}/-/issues` |
| `license` | `license` | `name` and `url` with SPDX detection. Falls back to fetching raw LICENSE file |
| `keywords` | `topics` | |
| `stargazers_count` | `star_count` | Called `star_count` in GitLab |
| `forks_count` | `forks_count` | |
| `programming_languages` | `languages` | Only language names (keys), no byte counts |
| `readme_url` | `readme_url` | |
| `releases` | `/projects/{id}/releases` | Paginated via `X-Next-Page`, mapped via `release_gitlab_crosswalk_table` |


### Self-hosted GitLab instances

SOMEF supports self-hosted GitLab instances (e.g., `gitlab.in2p3.fr`). The project path is
URL-encoded and used to query the instance's API at `https://{host}/api/v4/projects/{encoded_path}`.
SOMEF detects self-hosted instances by checking if the URL contains `gitlab.com`.

### Archive download

Repository archives are downloaded from:
`https://{host}/{project_path}/-/archive/{branch}/{repo_name}-{branch}.zip`

GitLab archive URLs typically include a `Content-Length` header, so the size limit check
can be performed before downloading.

### Enrichment via CODEOWNERS

When `--reconcile_authors` (`-ra`) is enabled, SOMEF fetches additional user details
(name, organization, public email) from `GET {server_url}/api/v4/users?username={username}`
for the repository owner and for each CODEOWNERS entry. Self-hosted instances use their
own API endpoint; `gitlab.com` uses the standard `https://gitlab.com/api/v4/users`.

### Limitations

- **Release assets**: GitLab releases include sources (tar.gz, zip) and links, but do not
  provide `download_count` or `content_size` like GitHub.