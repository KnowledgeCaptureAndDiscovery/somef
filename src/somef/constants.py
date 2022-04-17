from enum import Enum

categories = ['description', 'citation', 'installation', 'invocation']
# keep_keys = ('description', 'name', 'owner', 'license', 'languages_url', 'forks_url')
# instead of keep keys, we have this table
# it says that we want the key "codeRepository", and that we'll get it from the path "html_url" within the result object

github_crosswalk_table = {
    "codeRepository": "html_url",
    "languages_url": "languages_url",
    "owner": ["owner", "login"],
    "ownerType": ["owner", "type"],  # used to determine if owner is User or Organization
    "dateCreated": "created_at",
    "dateModified": "updated_at",
    "license": "license",
    "description": "description",
    "name": "name",
    "fullName": "full_name",
    "issueTracker": "issues_url",
    "forksUrl": "forks_url",
    "stargazers_count": "stargazers_count",
    "forks_count": "forks_count"
}

release_crosswalk_table = {
    'tagName': 'tag_name',
    'name': 'name',
    'authorName': ['author', 'login'],
    'authorType': ['author', 'type'],
    'body': 'body',
    'tarballUrl': 'tarball_url',
    'zipballUrl': 'zipball_url',
    'htmlUrl': 'html_url',
    'url': 'url',
    'dateCreated': 'created_at',
    'datePublished': "published_at",
}


class RepositoryType(Enum):
    GITHUB = 1
    GITLAB = 2
    LOCAL = 3
