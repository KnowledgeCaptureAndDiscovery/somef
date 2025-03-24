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
# r"!\[[^\]]*\]\((.*?)?\)"

# Categories recognized by SOMEF (they all start by CAT_
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
CAT_PROGRAMMING_LANGUAGES = "programming_languages"
CAT_README_URL = "readme_url"
CAT_RELATED_DOCUMENTATION = "related_documentation"
CAT_RELATED_PAPERS = "related_papers"
CAT_RELEASES = "releases"
CAT_RUN = "run"
CAT_STATUS = "repository_status"
CAT_REQUIREMENTS = "requirements"
CAT_STARS = "stargazers_count"
CAT_SUPPORT = "support"
CAT_SUPPORT_CHANNELS = "support_channels"
CAT_USAGE = "usage"
CAT_WORKFLOWS = "workflows"
CAT_TYPE = "type"
CAT_PACKAGE_FILE = "package_file"
# Special category: missing categories
CAT_MISSING = "somef_missing_categories"

# list of those categories to be analyzed with supervised classification.
# supervised_categories = [CAT_DESCRIPTION, CAT_CITATION, CAT_INSTALLATION, CAT_INVOCATION]
# update jan 2025: only description is run, since the installation classifier is a bit noisy.
# we prioritize returning high precision, since some users get confused otherwise.
supervised_categories = [CAT_DESCRIPTION]

# list with all categories
all_categories = [CAT_APPLICATION_DOMAIN, CAT_ACKNOWLEDGEMENT, CAT_CITATION, CAT_CONTRIBUTORS,
                  CAT_CONTRIBUTING_GUIDELINES,
                  CAT_COC, CAT_CODE_REPOSITORY, CAT_CONTACT, CAT_DESCRIPTION, CAT_DATE_CREATED, CAT_DATE_UPDATED,
                  CAT_DOCUMENTATION, CAT_DOWNLOAD, CAT_DOWNLOAD_URL, CAT_EXECUTABLE_EXAMPLE,
                  CAT_FAQ, CAT_FORK_COUNTS, CAT_FORKS_URLS, CAT_FULL_NAME, CAT_FULL_TITLE, CAT_HAS_BUILD_FILE,
                  CAT_HAS_SCRIPT_FILE, CAT_IDENTIFIER, CAT_IMAGE, CAT_INSTALLATION,
                  CAT_INVOCATION, CAT_ISSUE_TRACKER, CAT_KEYWORDS, CAT_LICENSE, CAT_LOGO, CAT_NAME, CAT_ONTOLOGIES,
                  CAT_OWNER, CAT_PACKAGE_DISTRIBUTION, CAT_PROGRAMMING_LANGUAGES, CAT_README_URL,
                  CAT_RELATED_DOCUMENTATION, CAT_RELEASES, CAT_RUN,
                  CAT_STATUS, CAT_REQUIREMENTS, CAT_STARS, CAT_SUPPORT, CAT_SUPPORT_CHANNELS, CAT_USAGE]

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
PROP_DOI = "doi"
PROP_DESCRIPTION = "description"
PROP_DATE_CREATED = "date_created"
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
PROP_ZIPBALL_URL = "zipball_url"
PROP_TARBALL_URL = "tarball_url"
# Publications
PROP_TITLE = "title"

# Format:
FORMAT_BIB = "bibtex"
FORMAT_CFF = "cff"
FORMAT_JUPYTER_NB = "jupyter_notebook"
FORMAT_DOCKERFILE = "dockerfile"
FORMAT_DOCKER_COMPOSE = "docker_compose"
FORMAT_READTHEDOCS = "readthedocs"
FORMAT_WIKI = "wiki"
FORMAT_POM = "pom.xml"
FORMAT_NPM = "npm"

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

# Spdx url
SPDX_BASE = "https://spdx.org/licenses/"
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
    CAT_FORK_COUNTS: "forks_count"
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
}

# TO DO: Assess run and download.
categories_files_header = [CAT_INSTALLATION, CAT_CITATION, CAT_ACKNOWLEDGEMENT, "run", "download", CAT_REQUIREMENTS,
                           CAT_CONTACT, CAT_DESCRIPTION, CAT_CONTRIBUTORS, CAT_DOCUMENTATION, CAT_LICENSE, CAT_USAGE,
                           CAT_FAQ, CAT_SUPPORT, CAT_IDENTIFIER, CAT_HAS_BUILD_FILE, CAT_EXECUTABLE_EXAMPLE]

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