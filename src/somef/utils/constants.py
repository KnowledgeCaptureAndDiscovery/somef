from enum import Enum
import os
from pathlib import Path

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
# These are two of the most common ones for Python, but it may be expanded
REGEXP_PYPI = "[![PyPI]"
REGEXP_PYPI_2 = "[![Latest PyPI version]"
REGEXP_COLAB = "https://colab.research.google.com/drive"
# needed to cleanup bibtext files.
REGEXP_BIBTEX = r'\@[a-zA-Z]+\{[.\n\S\s]+?[author|title][.\n\S\s]+?[author|title][.\n\S\s]+?\n\}'
REGEXP_DOI = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
REGEXP_LINKS = r"\[(.*?)?\]\(([^)]+)\)"
REGEXP_IMAGES = r"!\[(.*?)?\]\((.*?)?\)"
REGEXP_ISSN = r'issn\s*=\s*{([\d-]+)}'
REGEXP_YEAR = r'year\s*=\s*{(\d{4})}'
REGEXP_MONTH = r'month\s*=\s*{(\d{1,2})}'
REGEXP_PAGES = r'pages\s*=\s*{([\d-]+)}'

# Project Homepage badge'
REGEXP_PROJECT_HOMEPAGE = r'\[\!\[Project homepage\]([^\]]+)\]\(([^)]+)\)'

# Redthedocs badges'
# REGEXP_READTHEDOCS_BADGES = r"https?://[^\s]*readthedocs\.org/projects/[^\s]*/badge/\?version=[^\s]*(?:.|\n)*?:target:\s*(https?://[^\s]+)"
# REGEXP_READTHEDOCS_BADGES = r"https?://readthedocs\.org/projects/[^/\s]+/badge/\?version=[^)\s]+"
REGEXP_READTHEDOCS_BADGES = (
    r"https?://readthedocs\.org/projects/[^/\s]+/badge/\?version=[^)\s]+"
    r"(?:.|\n)*?:target:\s*(https?://[^\s]+)"  # rst
    r"|" 
    r"\((https?://readthedocs\.org/projects/[^/\s]+/[^)\s]+)\)"  # md
)
# For natural language citation
REGEXP_DOI_NATURAL = r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+'
REGEXP_YEAR_NATURAL = r'\b(19|20)\d{2}\b'
REGEXP_URL_NATURAL = r'https?://[^\s]+'
REGEXP_AUTHOR_NATURAL = r'^[A-Za-z\s,]+et al\.?'
REGEXP_TITLE_NATURAL = r'["“](.+?)["”]'

#License spdx
REGEXP_APACHE = r'(?i)apache\s+license\s*,?\s*version\s*2\.0'
REGEXP_GPL3 = r'(?i)gnu\s+general\s+public\s+license\s*,?\s*version\s*3\.0'
REGEXP_MIT = r'(?i)mit\s+license'
REGEXP_BSD2 = r'(?i)(bsd\s*-?\s*2-?clause(?:\s*license)?|redistribution\s+and\s+use\s+in\s+source\s+and\s+binary\s+forms)'
REGEXP_BSD3 = r'(?i)bsd\s+3-clause\s+license'
REGEXP_BOOST = r'(?i)boost\s+software\s+license\s*,?\s*version\s*1\.0'
REGEXP_CC0 = r'(?i)creative\s+commons\s+zero\s+v?1\.0\s+universal'
REGEXP_EPL2 = r'(?i)eclipse\s+public\s+license\s*,?\s*version\s*2\.0'
REGEXP_AGPL3 = r'(?i)gnu\s+affero\s+general\s+public\s+license\s*(?:v(?:ersion)?\.?\s*3(?:\.0)?)'
REGEXP_GPL2 = r'(?i)gnu\s+general\s+public\s+license\s*,?\s*version\s*2\.0'
REGEXP_LGPL1 = r'(?i)gnu\s+lesser\s+general\s+public\s+license\s*,?\s*version\s*1\.0'
REGEXP_MPL2 = r'(?i)mozilla\s+public\s+license\s*,?\s*version\s*2\.0'
REGEXP_UNLICENSE = r'(?i)the\s+unlicense'

# Detect organization in authors.md
REGEXP_LTD_INC = r'\b(inc|ltd|llc|corporation)([.,]|\b)'

# Detect duplicate all kind of dois. 
REGEXP_ALL_DOIS = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'

# Detect zenodo latest doi in readme. 
REGEXP_ZENODO_LATEST_DOI = r':target:\s*(https://zenodo\.org/badge/latestdoi/\d+)'
REGEXP_ZENODO_DOI = r'https://zenodo\.org/badge/DOI/\d+'
REGEXP_ZENODO_JSON_LD = r"<script[^>]*type=['\"]application/ld\+json['\"][^>]*>(.*?)</script>"

LICENSES_DICT = {
    "Apache License 2.0": {"regex": REGEXP_APACHE, "spdx_id": "Apache-2.0"},
    "GNU General Public License v3.0": {"regex": REGEXP_GPL3, "spdx_id": "GPL-3.0"},
    "MIT License": {"regex": REGEXP_MIT, "spdx_id": "MIT"},
    "BSD 2-Clause": {"regex": REGEXP_BSD2, "spdx_id": "BSD-2-Clause"},
    "BSD 3-Clause": {"regex": REGEXP_BSD3, "spdx_id": "BSD-3-Clause"},
    "Boost Software License 1.0": {"regex": REGEXP_BOOST, "spdx_id": "BSL-1.0"},
    "Creative Commons Zero v1.0": {"regex": REGEXP_CC0, "spdx_id": "CC0-1.0"},
    "Eclipse Public License 2.0": {"regex": REGEXP_EPL2, "spdx_id": "EPL-2.0"},
    "GNU Affero General Public License v3.0": {"regex": REGEXP_AGPL3, "spdx_id": "AGPL-3.0"},
    "GNU General Public License v2": {"regex": REGEXP_GPL2, "spdx_id": "GPL-2.0"},
    "GNU Lesser General Public License v1.0": {"regex": REGEXP_LGPL1, "spdx_id": "LGPL-1.0"},
    "Mozilla Public License 2.0": {"regex": REGEXP_MPL2, "spdx_id": "MPL-2.0"},
    "The Unlicense": {"regex": REGEXP_UNLICENSE, "spdx_id": "Unlicense"},
}
# Categories recognized by SOMEF (they all start by CAT_
CAT_ASSETS = "assets"
CAT_AUTHORS = "authors"
CAT_APPLICATION_DOMAIN = "application_domain"
CAT_ACKNOWLEDGEMENT = "acknowledgement"
CAT_CITATION = "citation"
CAT_CONTRIBUTORS = "contributors"
CAT_CONTRIBUTING_GUIDELINES = "contributing_guidelines"
CAT_COC = "code_of_conduct"
CAT_CODE_REPOSITORY = "code_repository"
CAT_CONTACT = "contact"
CAT_DATE_CREATED = "date_created"
CAT_DATE_UPDATED = "date_updated"
CAT_DATE_PUBLISHED = "date_published"
CAT_DESCRIPTION = "description"
CAT_DOCUMENTATION = "documentation"
CAT_DOWNLOAD = "download"
CAT_DOWNLOAD_URL = "download_url"
CAT_EXECUTABLE_EXAMPLE = "executable_example"
CAT_FAQ = "faq"
CAT_FORK_COUNTS = "forks_count"
CAT_FORKS_URLS = "forks_url"
CAT_FULL_NAME = "full_name"
CAT_FULL_TITLE = "full_title"
CAT_HOMEPAGE = "homepage"
CAT_HAS_BUILD_FILE = "has_build_file"
CAT_HAS_SCRIPT_FILE = "has_script_file"
CAT_IDENTIFIER = "identifier"
CAT_IMAGE = "images"
CAT_INSTALLATION = "installation"
CAT_INVOCATION = "invocation"
CAT_ISSUE_TRACKER = "issue_tracker"
CAT_KEYWORDS = "keywords"
CAT_LICENSE = "license"
CAT_LOGO = "logo"
CAT_NAME = "name"
CAT_ONTOLOGIES = "ontologies"
CAT_OWNER = "owner"
CAT_PACKAGE_DISTRIBUTION = "package_distribution"
REGEXP_PACKAGE_MANAGER = r"""
    (?P<url>
        https?://
        (?:
            (?:pypi\.python\.org/pypi/[^/\s]+)|
            (?:anaconda\.org/[^/\s]+/[^/\s]+)|
            (?:search\.maven\.org/artifact/[^/\s]+/[^/\s]+(?:/[^/\s]+)?)
        )
    )
"""
CAT_PROGRAMMING_LANGUAGES = "programming_languages"
CAT_README_URL = "readme_url"
CAT_RELATED_DOCUMENTATION = "related_documentation"
CAT_RELATED_PAPERS = "related_papers"
CAT_RELEASES = "releases"
CAT_REQUIREMENTS = "requirements"
CAT_RUN = "run"
CAT_RUNTIME_PLATFORM = "runtime_platform"
CAT_STATUS = "repository_status"
CAT_STARS = "stargazers_count"
CAT_SUPPORT = "support"
CAT_SUPPORT_CHANNELS = "support_channels"
CAT_USAGE = "usage"
CAT_WORKFLOWS = "workflows"
CAT_TYPE = "type"
CAT_PACKAGE_ID = "package_id"
CAT_HAS_PACKAGE_FILE = "has_package_file"
CAT_VERSION = "version"
CAT_CONTINUOUS_INTEGRATION= "continuous_integration"
CAT_FUNDING = "funding"
CAT_DEV_STATUS = "development_status"
CAT_REF_PUBLICATION = "reference_publication"
# Special category: missing categories
CAT_MISSING = "somef_missing_categories"
CAT_HOMEPAGE = "homepage"
# list of those categories to be analyzed with supervised classification.
# supervised_categories = [CAT_DESCRIPTION, CAT_CITATION, CAT_INSTALLATION, CAT_INVOCATION]
# update jan 2025: only description is run, since the installation classifier is a bit noisy.
# we prioritize returning high precision, since some users get confused otherwise.
supervised_categories = [CAT_DESCRIPTION]

# list with all categories
all_categories = [CAT_APPLICATION_DOMAIN, CAT_ACKNOWLEDGEMENT, CAT_AUTHORS, CAT_CITATION, CAT_CONTRIBUTORS,
                  CAT_CONTRIBUTING_GUIDELINES, CAT_CONTINUOUS_INTEGRATION,
                  CAT_COC, CAT_CODE_REPOSITORY, CAT_CONTACT, CAT_DESCRIPTION, CAT_DATE_CREATED, CAT_DATE_UPDATED,
                  CAT_DOCUMENTATION, CAT_DOWNLOAD, CAT_DOWNLOAD_URL, CAT_EXECUTABLE_EXAMPLE,
                  CAT_FAQ, CAT_FORK_COUNTS, CAT_FORKS_URLS, CAT_FULL_NAME, CAT_FULL_TITLE, CAT_HAS_BUILD_FILE,
                  CAT_HAS_SCRIPT_FILE, CAT_IDENTIFIER, CAT_IMAGE, CAT_INSTALLATION,
                  CAT_INVOCATION, CAT_ISSUE_TRACKER,CAT_HOMEPAGE, CAT_KEYWORDS, CAT_LICENSE, CAT_LOGO, CAT_NAME, CAT_ONTOLOGIES,
                  CAT_OWNER, CAT_PACKAGE_DISTRIBUTION, CAT_HAS_PACKAGE_FILE, CAT_PROGRAMMING_LANGUAGES, CAT_README_URL,
                  CAT_RELATED_DOCUMENTATION, CAT_RELEASES, CAT_RUN, CAT_RUNTIME_PLATFORM, CAT_RELATED_PAPERS,
                  CAT_STATUS, CAT_REQUIREMENTS, CAT_STARS, CAT_SUPPORT, CAT_SUPPORT_CHANNELS, CAT_USAGE,
                  CAT_WORKFLOWS, CAT_TYPE]

# All properties used by SOMEF to label the output JSON
# Provenance:
PROP_PROVENANCE = "somef_provenance"
PROP_SOMEF_VERSION = "somef_version"
PROP_SOMEF_SCHEMA_VERSION = "somef_schema_version"
PROP_DATE = "date"
# for Category:
PROP_CONFIDENCE = "confidence"
PROP_RESULT = "result"
PROP_SOURCE = "source"
PROP_TECHNIQUE = "technique"
# for Result:
PROP_FORMAT = "format"
PROP_TYPE = "type"
AGENT_TYPE = "agent_type"  # Special type needed when objects are nested
PROP_VALUE = "value"
# For Result types
PROP_AUTHOR = "author"
PROP_BROWSER_URL = "browser_download_url"
PROP_CONTENT_TYPE = "content_type"
PROP_DOI = "doi"
PROP_DESCRIPTION = "description"
PROP_DATE_CREATED = "date_created"
PROP_DATE_CREATED_AT = "created_at"
PROP_DATE_PUBLISHED = "date_published"
PROP_DATE_UPDATED = "date_updated"
PROP_HTML_URL = "html_url"
PROP_NAME = "name"
PROP_ORIGINAL_HEADER = "original_header"
PROP_PARENT_HEADER = "parent_header"
PROP_RELEASE_ID = "release_id"
PROP_SIZE = "size"
PROP_SPDX_ID = "spdx_id"
PROP_TAG = "tag"
PROP_URL = "url"
PROP_VERSION = "version"
PROP_ZIPBALL_URL = "zipball_url"
PROP_TARBALL_URL = "tarball_url"
# Publications
PROP_TITLE = "title"
# Assets from releases
# PROP_ASSETS = "assets"
PROP_CONTENT_URL = "content_url"
PROP_ENCODING_FORMAT = "encoding_format"
PROP_UPLOAD_DATE = "upload_date"
PROP_CONTENT_SIZE = "content_size"
PROP_DOWNLOAD_COUNT = "download_count"

# Format:
FORMAT_BIB = "bibtex"
FORMAT_CFF = "cff"
FORMAT_JUPYTER_NB = "jupyter_notebook"
FORMAT_DOCKERFILE = "dockerfile"
FORMAT_DOCKER_COMPOSE = "docker_compose"
FORMAT_READTHEDOCS = "readthedocs"
FORMAT_WIKI = "wiki"
# Package types
FORMAT_PYTHON_SETUP_PY = "setup.py"
FORMAT_POM_XML = "pom.xml"
FORMAT_PYPROJECT_TOML = "pyproject.toml"
FORMAT_PACKAGE_JSON = "package.json"


# Result types: data types
STRING = "String"
URL = "Url"
DATE = "Date"
NUMBER = "Number"
TEXT_EXCERPT = "Text_excerpt"
FILE_DUMP = "File_dump"

# Result types: entities (complex objects)
AGENT = "Agent"
RELEASE = "Release"
LICENSE = "License"
PUBLICATION = "Publication"
LANGUAGE = "Programming_language"
SOFTWARE_APPLICATION = "Software_application"
SCHOLARLY_ARTICLE = "Scholarly_article"

# Different techniques
TECHNIQUE_SUPERVISED_CLASSIFICATION = "supervised_classification"
TECHNIQUE_HEADER_ANALYSIS = "header_analysis"
TECHNIQUE_REGULAR_EXPRESSION = "regular_expression"
TECHNIQUE_FILE_EXPLORATION = "file_exploration"
TECHNIQUE_CODE_CONFIG_PARSER = "code_parser"
TECHNIQUE_GITHUB_API = "GitHub_API"
TECHNIQUE_GITLAB_API = "GitLab_API"
TECHNIQUE_HEURISTICS = "software_type_heuristics"

# GitHub properties
GITHUB_DOMAIN = "github.com"
GITHUB_ACCEPT_HEADER = "application/vnd.github.v3+json"
GITHUB_API = "https://api.github.com/repos"

# Software Heritage
SWH_ROOT = "https://archive.softwareheritage.org/"
REGEXP_SWH = r'\[\!\[SWH\]([^\]]+)\]\(([^)]+)\)'
REGEXP_SWH_ANCHOR = r"anchor=(swh:1:[a-z]+:[a-f0-9]{40})"
REGEXP_SWH_ALL_IDENTIFIERS = r"(swh:1:[a-z]+:[a-f0-9]{40})"
# Spdx url
SPDX_BASE = "https://spdx.org/licenses/"

# Codeowners file
CODEOWNERS_FILE = "CODEOWNERS"

# Crosswalk to retrieve easily contents of interest from the GitHub response
github_crosswalk_table = {
    CAT_CODE_REPOSITORY: "html_url",
    "languages_url": "languages_url",
    CAT_OWNER: ["owner", "login"],
    AGENT_TYPE: ["owner", "type"],  # used to determine if owner is User or Organization
    CAT_DATE_CREATED: "created_at",
    CAT_DATE_UPDATED: "updated_at",
    CAT_LICENSE: "license",
    CAT_DESCRIPTION: "description",
    CAT_NAME: "name",
    CAT_FULL_NAME: "full_name",
    CAT_ISSUE_TRACKER: "issues_url",
    CAT_FORKS_URLS: "forks_url",
    CAT_STARS: "stargazers_count",
    CAT_KEYWORDS: "topics",
    CAT_FORK_COUNTS: "forks_count",
    CAT_HOMEPAGE: "homepage"
}

# Mapping for releases
release_crosswalk_table = {
    PROP_TAG: 'tag_name',
    PROP_NAME: 'name',
    PROP_AUTHOR: ['author', 'login'],
    AGENT_TYPE: ['author', 'type'],
    PROP_DESCRIPTION: 'body',
    PROP_TARBALL_URL: 'tarball_url',
    PROP_ZIPBALL_URL: 'zipball_url',
    PROP_HTML_URL: 'html_url',
    PROP_URL: 'url',
    PROP_RELEASE_ID: 'id',
    PROP_DATE_CREATED: 'created_at',
    PROP_DATE_PUBLISHED: "published_at",
    CAT_ASSETS: "assets"
}

release_gitlab_crosswalk_table = {
    PROP_TAG: 'tag_name',
    PROP_NAME: 'name',
    PROP_AUTHOR: ['author', 'username'],
    PROP_DESCRIPTION: 'description',
    PROP_TARBALL_URL: ['assets', 'sources'],
    PROP_ZIPBALL_URL: ['assets', 'sources'],
    PROP_HTML_URL: ['_links', 'self'],
    PROP_URL: ['_links', 'self'],
    PROP_RELEASE_ID: 'tag_name',
    PROP_DATE_CREATED: 'created_at',
    PROP_DATE_PUBLISHED: "released_at",
    CAT_ASSETS: "assets"
}

release_assets_github = {
    PROP_URL: "url",
    PROP_NAME: "name",
    PROP_SIZE: "size",
    PROP_BROWSER_URL: "browser_download_url",
    PROP_CONTENT_TYPE: "content_type",
    PROP_DATE_CREATED_AT: "created_at",
    PROP_DOWNLOAD_COUNT: "download_count"
}

# Minimum percentage of total bytes a programming language must have to be considered relevant in CodeMeta file.
MINIMUM_PERCENTAGE_LANGUAGE_PROGRAMMING = 10

# TO DO: Assess run and download.
categories_files_header = [CAT_INSTALLATION, CAT_CITATION, CAT_ACKNOWLEDGEMENT, "run", "download", CAT_REQUIREMENTS,
                           CAT_CONTACT, CAT_DESCRIPTION, CAT_CONTRIBUTORS, CAT_DOCUMENTATION, CAT_LICENSE, CAT_USAGE,
                           CAT_FAQ, CAT_SUPPORT, CAT_IDENTIFIER, CAT_HAS_BUILD_FILE, CAT_EXECUTABLE_EXAMPLE, CAT_KEYWORDS]

# Config to materialize with yarrrml.yml.
MAPPING_CONFIG = """
                    [DataSource1]
                    mappings: $PATH
                    file_path: $DATA
                 """
                 
# Config to materialize with rml.ttl.
MAPPING_CONFIG_DICT = """
                    [DataSource1]
                    mappings: $PATH
                 """
       
# YML by default          
# mapping_path = str(Path(__file__).parent.parent) + os.path.sep + "mapping" + os.path.sep + "yarrrml.yml"
 
mapping_path = str(Path(__file__).parent.parent) + os.path.sep + "mapping" + os.path.sep + "rml.ttl"

AUX_RELEASES_IDS = "releases_ids"

class RepositoryType(Enum):
    GITHUB = 1
    GITLAB = 2
    LOCAL = 3

# Media/script/non-software sets
workflow_extensions=('.ga','.cwl','.nf','.knwf','.t2flow','.dag','.kar','.wdl',".smk",".snake")
code_extensions = (".jl",".sql",".ddl",".psql",".mysql",".oracle",".plsql",".py",".java",".jar",".bash",".sh",".cs",".dll",".cpp",".c",".php",".phtml",".ps1",".rs",".go",".kt",".rb",".pl",".lua",".dart",".groovy",".asm",".swift",".R",".r")
ontology_extensions=(".rdf",".ttl",".owl",".nt",".owl2",".nq",".n3",".rdfs") 
media_files=(".mp4",".mp3",".wav",".bmp",".gif",".png",".jpeg",".jpg",".svg",".webp",".xls",".xlsx",".ico",".webm",".wmv",".txt")

# Folders ignored in process_files.py/process_repository_files
IGNORED_DIRS = {"test", "tests", "node_modules", "venv", "__pycache__"}

SIZE_DOWNLOAD_LIMIT_MB = 200
DOWNLOAD_TIMEOUT_SECONDS = 120


