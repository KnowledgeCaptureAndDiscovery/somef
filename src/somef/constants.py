from enum import Enum

# constants about SOMEF configuration
CONF_AUTHORIZATION = "Authorization"
CONF_DESCRIPTION = "description"
CONF_INVOCATION = "invocation"
CONF_INSTALLATION = "installation"
CONF_CITATION = "citation"
CONF_BASE_URI = "base_uri"
CONF_DEFAULT_BASE_URI = "https://w3id.org/okn/i/"

__DEFAULT_SOMEF_CONFIGURATION_FILE__ = "~/.somef/config.json"

# constants with regular expressions. Right now this has room for becoming more efficient
REGEXP_BINDER = r'\[\!\[Binder\]([^\]]+)\]\(([^)]+)\)'
REGEXP_READTHEDOCS = r'http[s]?://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]+.readthedocs.io/'
REGEXP_REDDIT = "(https://www.reddit.com/r/"
REGEXP_DISCORD = "(https://discord.com/invite/"
REGEXP_GITTER = "[![Gitter chat]"
REGEXP_PYPI = "[![PyPI]"
REGEXP_COLAB = "https://colab.research.google.com/drive"
REGEXP_BIBTEX = r'\@[a-zA-Z]+\{[.\n\S\s]+?[author|title][.\n\S\s]+?[author|title][.\n\S\s]+?\n\}'
REGEXP_DOI = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
REGEXP_LINKS = r"\[(.*?)?\]\(([^)]+)\)"
REGEXP_IMAGES = r"!\[(.*?)?\]\((.*?)?\)"
                #r"!\[[^\]]*\]\((.*?)?\)"


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
