import logging
import os
import zipfile
import time
import requests
import sys
import re
from datetime import datetime
from urllib.parse import urlparse, quote
from .utils import constants
from . import configuration
from .process_results import Result
from .regular_expressions import detect_license_spdx
from .parser.codeowners_parser import enrich_github_user

# Constructs a template HTTP header, which:
# - has a key for the authorization token if passed via the authorization argument, otherwise
# - has a key for the authorization token if specified via config, otherwise
# - has not key for the authorization token
def header_template(authorization=None):
    header = {}
    file_paths = configuration.get_configuration_file()
    if authorization is not None:
        header[constants.CONF_AUTHORIZATION] = authorization
    elif constants.CONF_AUTHORIZATION in file_paths.keys():
        header[constants.CONF_AUTHORIZATION] = file_paths[constants.CONF_AUTHORIZATION]
    return header


def is_gitlab(gitlab_server):
    api_url = f"https://{gitlab_server}/api/v4/projects"
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code in [200, 401, 403]: 
            return True
    except requests.RequestException:
        pass
    return False

# the same as requests.get(args).json(), but protects against rate limiting
def rate_limit_get(*args, backoff_rate=2, initial_backoff=1, size_limit_mb=constants.SIZE_DOWNLOAD_LIMIT_MB, **kwargs):
# def rate_limit_get(*args, backoff_rate=2, initial_backoff=1, **kwargs):
    """Function to obtain how many requests we have pending with the GitHub API"""

    """GET request that handles rate limiting and prevents downloading excessively large files"""
    size_limit_bytes = size_limit_mb * 1024 * 1024
    url = args[0] if args else kwargs.get("url")
    if not url:
        raise ValueError("Missing URL in rate_limit_get")
    
    parsed = urlparse(url)
    is_api_request = "api.github.com" in parsed.netloc
    content_length = None
    # just verify size if NOT is a request to api.github.com
    if not is_api_request:
        try:
            head_response = requests.get(url, stream=True, allow_redirects=True, **kwargs)
            content_length = head_response.headers.get("Content-Length")
            if content_length is not None:
                size_bytes = int(content_length)
                print(f"HEAD Content-Length: {size_bytes}")
                if size_bytes > size_limit_bytes:
                    logging.warning(
                        f"Download size {size_bytes} bytes exceeds limit of {size_limit_bytes} bytes. Skipping download."
                    )
                    return None, None
            else:
                # logging.warning(f"Could not determine file size for {url}. Skipping download.")
                # return None, None
                logging.warning(f"No Content-Length header for {url}. Proceeding with download anyway (unable to estimate size).")
        except Exception as e:
            logging.warning(f"HEAD/stream request failed: {e}. Continuing with GET...")

    rate_limited = True
    date = ""
    response = {}
    while rate_limited:
        use_stream = not is_api_request and (content_length is None or int(content_length) > 10 * 1024 * 1024)
        response = requests.get(
            *args,
            timeout=(constants.DOWNLOAD_TIMEOUT_SECONDS, constants.DOWNLOAD_TIMEOUT_SECONDS),
            stream=use_stream,
            **kwargs
        )
        # Detect invalid or insufficient GitHub token 
        if response.status_code == 401: 
            raise Exception("Invalid GitHub token. Run `somef configure` to set a valid token.") 
        if response.status_code == 403: 
            raise Exception("GitHub token lacks required permissions or scopes.")
        
        date = response.headers.get("Date", "")
        # Show rate limit information if available
        if "X-RateLimit-Remaining" in response.headers:
            rate_limit_remaining = response.headers["X-RateLimit-Remaining"]
            epochtime = int(response.headers["X-RateLimit-Reset"])
            date_reset = datetime.fromtimestamp(epochtime)
            logging.info(
                "Remaining GitHub API requests: " + rate_limit_remaining + " ### Next rate limit reset at: " + str(
                    date_reset))
            
            if not use_stream:
                try:
                    json_data = response.json()
                    msg = json_data.get("message", "")
                    if "API rate limit exceeded" in msg:
                        rate_limited = True
                        logging.warning(f"Rate limited. Backing off for {initial_backoff} seconds")
                        time.sleep(initial_backoff)
                        initial_backoff *= backoff_rate
                        continue
                except Exception:
                    pass

        rate_limited = False

    if not is_api_request and use_stream:
        content = bytearray()
        total_read = 0
        chunk_size = 1024 * 1024  # 1 MB
        start_time = time.monotonic()

        try:
            for i, chunk in enumerate(response.iter_content(chunk_size=chunk_size)):
                if not chunk:
                    # logging.debug(f"Chunk {i} empty, continue...")
                    continue

                # logging.debug(f"Chunk read {i}: {len(chunk)} bytes")
                content.extend(chunk)
                total_read += len(chunk)

                # Comprobar límite de tamaño
                if total_read > size_limit_bytes:
                    logging.warning(f"Downloaded content exceeded {size_limit_bytes} bytes. Aborting.")
                    return None, None

                # Comprobar límite de tiempo
                elapsed = time.monotonic() - start_time
                if elapsed > constants.DOWNLOAD_TIMEOUT_SECONDS:
                    logging.warning(f"Download exceeded time limit ({elapsed:.2f}s). Aborting.")
                    return None, None

        except Exception as e:
            logging.warning(f"Error while streaming: {e}")
            return None, None
        
        response._content = bytes(content)

    return response, date


def load_gitlab_repository_metadata(repo_metadata: Result, repository_url):
    """
    Function uses the repository_url provided to load required information from gitlab.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    @param repo_metadata: Result object with the metadata found in the repository so far
    @param repository_url: URL of the Gitlab repository to analyze

    Returns
    -------
    @return: Metadata available in GitLab from the target repo, along with its owner, name and default branch
    """
    logging.info(f"Loading Repository {repository_url} Information....")
    # load general response of the repository
    if repository_url[-1] == '/':
        repository_url = repository_url[:-1]
    url = urlparse(repository_url)
    # if url.netloc != 'gitlab.com':
    # if "gitlab" not in url.netloc:
    #     logging.error("Repository must come from Gitlab")
    #     return " ", {}

    path_components = url.path.split('/')

    if len(path_components) < 3:
        logging.error("Gitlab link is not correct.")
        return " ", {}

    owner = path_components[1]
    repo_name = path_components[2]
    if len(path_components) == 4:
        repo_name = repo_name + '/' + path_components[3]

    # could be gitlab.com or some gitlab self-hosted GitLab servers like gitlab.in2p3.fr
    if repository_url.rfind("gitlab.com") > 0:
        project_id = get_project_id(repository_url, False)
        project_api_url = f"https://gitlab.com/api/v4/projects/{project_id}"
    else:
        project_path = url.path.lstrip("/")  # "gammalearn/gammalearn"
        encoded_project_path = quote(project_path, safe="") # Codifica "/" como "%2F"
        # Build url of api to get id
        api_url = f"https://{url.netloc}/api/v4/projects/{encoded_project_path}"
        project_id = get_project_id(api_url, True)
        logging.info(f'Project_id: {project_id}')
        project_api_url = f"https://{url.netloc}/api/v4/projects/{project_id}"
    
    logging.info(f"Downloading {project_api_url}")
    details = requests.get(project_api_url)
    project_details = details.json()
    date = details.headers["date"]

    repo_api_base_url = f"{repository_url}"
    # releases = get_gitlab_releases(project_id, f"https://{url.netloc}")
    all_releases = get_all_gitlab_releases(project_api_url)
    release_list_filtered = [do_crosswalk(release, constants.release_gitlab_crosswalk_table) for release in all_releases]

    for release in release_list_filtered:
        release_obj = {
            constants.PROP_TYPE: constants.RELEASE,
            constants.PROP_VALUE: release.get(constants.PROP_URL, "")
        }
        for category, value in release.items():
            if category != constants.AGENT_TYPE:
                if category == constants.PROP_AUTHOR:                 
                    value = {
                        constants.PROP_NAME: value,
                        constants.PROP_TYPE: release.get(constants.AGENT_TYPE, "Person")
                    }
            tar_gz_entry = None
            zip_gz_entry = None

            if category == "tarball_url" and isinstance(value, list):
                tar_gz_entry = next((item for item in value if item.get("format") == "tar.gz"), None)
            elif category == "zipball_url" and isinstance(value, list):
                zip_gz_entry = next((item for item in value if item.get("format") == "zip"), None)

            if tar_gz_entry:
                value = tar_gz_entry["url"]
            elif zip_gz_entry:
                value = zip_gz_entry["url"]

            if category == constants.CAT_ASSETS:
                assets_release_list_filtered = []
                for source in release[constants.CAT_ASSETS]['sources']:
                    source_asset = {
                        constants.PROP_ENCODING_FORMAT: source[constants.PROP_FORMAT],
                        constants.PROP_CONTENT_URL: source[constants.PROP_URL]
                    }
                    assets_release_list_filtered.append(source_asset)

                for link in release[constants.CAT_ASSETS]['links']:
                    link_asset = {
                        constants.PROP_NAME: link[constants.PROP_NAME],
                        constants.PROP_ENCODING_FORMAT: link["link_type"],
                        constants.PROP_URL: constants.PROP_URL,
                        constants.PROP_CONTENT_URL: link["direct_asset_url"],
                    }
                    assets_release_list_filtered.append(link_asset)

                value = assets_release_list_filtered 
        
            if value: 
                release_obj[category] = value
            else:
                logging.warning(f"Ignoring empty value in release for {category}")

        repo_metadata.add_result(constants.CAT_RELEASES, release_obj, 1, constants.TECHNIQUE_GITLAB_API)


    default_branch = None

    if len(path_components) >= 5:
        if not path_components[4] == "tree":
            logging.error(
                "GitLab link is not correct. \nThe correct format is https://gitlab.com/{owner}/{repo_name}.")

            return " ", {}

        # we must join all after 4, as sometimes tags have "/" in them.
        default_branch = "/".join(path_components[5:])
        ref_param = {"ref": default_branch}

    if 'defaultBranch' in project_details.keys():
        general_resp = {'defaultBranch': project_details['defaultBranch']}
    elif 'default_branch' in project_details.keys():
        general_resp = {'defaultBranch': project_details['default_branch']}
    else:
        logging.error("Could not retrieve information for the GitLab repository")
        return repo_metadata

    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            logging.error("Error: repository name is incorrect")
        else:
            message = general_resp['message']
            logging.error("Error: " + message)

        raise GithubUrlError

    if default_branch is None:
        default_branch = general_resp['defaultBranch']

    repo_metadata.add_result(constants.CAT_CODE_REPOSITORY,
                             {constants.PROP_VALUE: f"https://{url.netloc}/{owner}/{repo_name}/",
                              constants.PROP_TYPE: constants.URL
                              }, 1, constants.TECHNIQUE_GITLAB_API)

    # filtered_resp = do_crosswalk(general_resp, github_crosswalk_table)
    # filtered_resp = {"downloadUrl": f"https://gitlab.com/{owner}/{repo_name}/-/branches"}
    repo_metadata.add_result(constants.CAT_DOWNLOAD_URL,
                             {constants.PROP_VALUE: f"https://{url.netloc}/{owner}/{repo_name}/-/branches",
                              constants.PROP_TYPE: constants.URL
                             }, 1, constants.TECHNIQUE_GITLAB_API)

    # condense license information
    license_result = {constants.PROP_TYPE: constants.URL}
    
    if 'license' in general_resp:
        if "name" in general_resp['license']:
            license_result[constants.PROP_NAME] = general_resp["license"]["name"]
        if "url" in general_resp['license']:
            license_result[constants.PROP_VALUE] = general_resp["license"]["url"]

        # for k in ('name', 'url'):
        #     if k in general_resp['license']:
        #         license_info[k] = general_resp['license'][k]

    # If we didn't find it, look for the license
    if constants.PROP_VALUE not in license_result or license_result[constants.PROP_VALUE] is None:
        # possible_license_url = f"{repository_url}/-/blob/master/LICENSE"
        possible_license_url = f"{repository_url}/-/raw/master/LICENSE"
        license_text_resp = requests.get(possible_license_url)
        if license_text_resp.status_code == 200:
            license_text = license_text_resp.text
            license_result[constants.PROP_VALUE] = possible_license_url
            license_info = detect_license_spdx(license_text, 'JSON')
            if license_info:
                 license_result[constants.PROP_NAME] = license_info['name']
                 license_result[constants.PROP_SPDX_ID] = license_info['spdx_id']

    if constants.PROP_VALUE in license_result:
        repo_metadata.add_result(constants.CAT_LICENSE, license_result, 1, constants.TECHNIQUE_GITLAB_API)

    # get keywords / topics
    # topics_headers = header
    # topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
    # topics_resp, date = rate_limit_get(repo_api_base_url + "/topics",
    #                                   headers=topics_headers)
    topics_resp = {}

    keywords = []
    if 'message' in topics_resp.keys():
        logging.error("Topics Error: " + topics_resp['message'])
    elif topics_resp and 'names' in topics_resp.keys():
        keywords = topics_resp['names']

    if project_details['topics'] is not None:
        keywords = project_details['topics']

    if len(keywords) > 0:
        value = '%s,' % (', '.join(keywords))
        value = value.rstrip(',')
        result = {
            constants.PROP_VALUE: value,
            constants.PROP_TYPE: constants.STRING
        }
        repo_metadata.add_result(constants.CAT_KEYWORDS, result, 1, constants.TECHNIQUE_GITLAB_API)

    # get social features: stargazers_count
    if project_details['star_count'] is not None:
        result = {
            constants.PROP_VALUE: project_details['star_count'],
            constants.PROP_TYPE: constants.NUMBER
        }
        repo_metadata.add_result(constants.CAT_STARS, result, 1, constants.TECHNIQUE_GITLAB_API)

    # get social features: forks_count
    if project_details['forks_count'] is not None:
        repo_metadata.add_result(constants.CAT_FORK_COUNTS, {
            constants.PROP_VALUE: project_details['forks_count'],
            constants.PROP_TYPE: constants.NUMBER
        }, 1, constants.TECHNIQUE_GITLAB_API)

    # get programming languages
    if 'languages_url' in project_details.keys():
        if "message" in project_details['languages_url']:
            logging.error("Languages Error: " + project_details['languages_url']["message"])
        else:
            result = {
                constants.PROP_VALUE: list(project_details['languages_url']),
                constants.PROP_TYPE: constants.STRING
            }
            repo_metadata.add_result(constants.CAT_PROGRAMMING_LANGUAGES, result, 1, constants.TECHNIQUE_GITLAB_API)

    if 'readme_url' in project_details.keys():
        repo_metadata.add_result(constants.CAT_README_URL, {
            constants.PROP_VALUE: project_details['readme_url'],
            constants.PROP_TYPE: constants.URL
        }, 1, constants.TECHNIQUE_GITLAB_API)

    logging.info("Repository information successfully loaded. \n")
    return repo_metadata, owner, repo_name, default_branch


def download_gitlab_files(directory, owner, repo_name, repo_branch, repo_ref):
    """
    Download all repository files from a GitHub repository
    Parameters
    ----------
    @param repo_branch: Branch of the repo we are analysing
    @param repo_ref: link to the repo
    @param repo_name: name of the repo
    @param owner: owner of the GitLab repo
    @param directory: directory where to extract all downloaded files
    Returns
    -------
    @rtype: string
    @return: path of the folder where the files have been downloaded
    """
    url = urlparse(repo_ref)
    path_components = url.path.split('/')

    repo_archive_url = f"https://{url.netloc}/{owner}/{repo_name}/-/archive/{repo_branch}/{repo_name}-{repo_branch}.zip"
    if len(path_components) == 4:
            repo_archive_url = f"https://{url.netloc}/{owner}/{repo_name}/-/archive/{repo_branch}/{path_components[3]}.zip"

    logging.info(f"Downloading {repo_archive_url}")
    repo_download = requests.get(repo_archive_url)
    repo_zip = repo_download.content

    repo_zip_file = os.path.join(directory, "repo.zip")
    repo_extract_dir = os.path.join(directory, "repo")

    with open(repo_zip_file, "wb") as f:
        f.write(repo_zip)

    with zipfile.ZipFile(repo_zip_file, "r") as zip_ref:
        zip_ref.extractall(repo_extract_dir)

    repo_folders = os.listdir(repo_extract_dir)
    if len(repo_folders) == 1:
        repo_dir = os.path.join(repo_extract_dir, repo_folders[0])
        return repo_dir
    else:
        logging.error("Error when processing GitLab repository")
        return None


def download_readme(owner, repo_name, default_branch, repo_type, authorization):
    """
    Method that given a repository owner, name and default branch, it downloads the readme content only.
    The readme is assumed to be README.md
    Parameters
    ----------
    @param owner: owner of the repository
    @param repo_name: name of the repository to target
    @param default_branch: branch to address
    @param repo_type: see constants.RepositoryType to see types (mostly Github, Gitlab)

    Returns
    -------
    @return: text with the contents of the readme file
    """
    if repo_type is constants.RepositoryType.GITLAB:
        primary_url = f"https://gitlab.com/{owner}/{repo_name}/-/raw/{default_branch}/README.md"
        secondary_url = f"https://gitlab.com/{owner}/{repo_name}/-/raw/master/README.md"
    elif repo_type is constants.RepositoryType.GITHUB:
        primary_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{default_branch}/README.md"
        secondary_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/master/README.md"
    else:
        logging.error("Repository type not supported")
        return None
    logging.info(f"Downloading {primary_url}")

    repo_download, date = rate_limit_get(primary_url, headers=header_template(authorization))

    if repo_download is None:
        logging.warning(f"Repository archive skipped due to size limit: {constants.SIZE_DOWNLOAD_LIMIT_MB} MB or content-lenght none")
        return None   
    if repo_download.status_code == 404:
        logging.error(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        logging.info(f"Trying to download {secondary_url}")
        repo_download, date = rate_limit_get(secondary_url, headers=header_template(authorization))
        if repo_download is None:
            logging.warning(f"Repository archive skipped due to size limit: {constants.SIZE_DOWNLOAD_LIMIT_MB} MB or content-lenght none")
            return None      
    if repo_download.status_code != 200:
        logging.error(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        return None
    repo_zip = repo_download.content
    text = repo_zip.decode('utf-8')
    return text


def load_online_repository_metadata(repository_metadata: Result, repository_url, ignore_api_metadata=False,
                                    repo_type=constants.RepositoryType.GITHUB, authorization=None, reconcile_authors=False):
    """
    Function uses the repository_url provided to load required information from GitHub or Gitlab.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    @param repository_metadata: Result object to store the findings by SOMEF. This is the returned object
    @param repo_type: type of the repository (GITLAB, GITHUB or LOCAL)
    @param ignore_api_metadata: true if you do not want to do an additional request to the target API
    @param repository_url: target repository URL.
    @param authorization: GitHub authorization token
    @param reconcile_authors: flag to indicate if additional should be extracted from certain files as codeowners. More request.

    Returns
    -------
    @return: Result object with the available metadata from online APIs plus its owner, repo name and default branch
    """
    if repo_type == constants.RepositoryType.GITLAB:
        return load_gitlab_repository_metadata(repository_metadata, repository_url)
    elif repo_type == constants.RepositoryType.LOCAL:
        logging.warning("Trying to download metadata from a local repository")
        return None

    logging.info(f"Loading Repository {repository_url} Information....")

    # Create template header with optional authorization token
    header = header_template(authorization)
    header['accept'] = constants.GITHUB_ACCEPT_HEADER

    # load general response of the repository
    if repository_url[-1] == '/':
        repository_url = repository_url[:-1]
    url = urlparse(repository_url)

    if url.netloc != constants.GITHUB_DOMAIN:
        logging.error("Repository must be from Github")
        return repository_metadata, "", "", ""

    path_components = url.path.split('/')

    if len(path_components) < 3:
        logging.error("Repository link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}.")
        return repository_metadata, "", "", ""

    owner = path_components[1]
    repo_name = path_components[2]
    repo_api_base_url = f"{constants.GITHUB_API}/{owner}/{repo_name}"
    default_branch = None

    if len(path_components) >= 5:
        # if not path_components[3] == "tree":
        if path_components[3] not in ["tree", "blob"]:
            logging.error(f"Github link is not correct. \n"
                f"The correct format is https://github.com/{owner}/{repo_name}/tree/... \n"
                f"or  https://github.com/{owner}/{repo_name}/blob/....")
            return repository_metadata, "", "", ""

        # we must join all after 4, as sometimes tags have "/" in them.
        # default_branch = "/".join(path_components[4:])
        default_branch = path_components[4]
        # ref_param = {"ref": default_branch}

    general_resp = {}
    date = ""
    if not ignore_api_metadata:
        general_resp_raw, date = rate_limit_get(repo_api_base_url, headers=header)
        if general_resp_raw is None:
            logging.warning(f"Repository archive skipped due to size limit: {constants.SIZE_DOWNLOAD_LIMIT_MB} MB or content-lenght none")
            return repository_metadata, "", "", ""
        
        general_resp = general_resp_raw.json()
 
    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            logging.error("Error: Repository name is private or incorrect")
        else:
            message = general_resp['message']
            logging.error("Error: " + message)

        raise GithubUrlError

    if ignore_api_metadata:
        default_branch = 'master'
    elif default_branch is None:
        default_branch = general_resp['default_branch']

    # filter the general response with only the fields we are interested in, mapping them to our keys
    filtered_resp = {}
    if not ignore_api_metadata:
        filtered_resp = do_crosswalk(general_resp, constants.github_crosswalk_table)
    # add download URL
    filtered_resp[constants.CAT_DOWNLOAD_URL] = f"https://github.com/{owner}/{repo_name}/releases"

    for category, value in filtered_resp.items():
        value_type = constants.STRING
        maintainer_data = {}
        if category in constants.all_categories:
            if category == constants.CAT_ISSUE_TRACKER:
                value = value.replace("{/number}", "")
            if category == constants.CAT_OWNER:
                if reconcile_authors:
                    print("Enriching owner information from codeowners...")
                    user_info = enrich_github_user(owner)
                    if user_info:
                        if user_info.get("name"):
                            maintainer_data["name"] = user_info.get("name")
                        if user_info.get("company"):
                            maintainer_data["affiliation"] = user_info.get("company")
                        if user_info.get("email"):
                            maintainer_data["email"] = user_info.get("email")

                value_type = filtered_resp[constants.AGENT_TYPE]
            if category == constants.CAT_KEYWORDS:
                # we concatenate all keywords in a list, as the return value is always a single object
                value = '%s,' % (', '.join(value))
                value = value.rstrip(',')
            if category in [constants.CAT_CODE_REPOSITORY, constants.CAT_ISSUE_TRACKER,
                            constants.CAT_DOWNLOAD_URL, constants.CAT_FORKS_URLS, constants.CAT_HOMEPAGE]:
                value_type = constants.URL
            if category in [constants.CAT_DATE_CREATED, constants.CAT_DATE_UPDATED]:
                value_type = constants.DATE
            if category in [constants.CAT_FORK_COUNTS, constants.CAT_STARS]:
                value_type = constants.NUMBER
            if category == constants.CAT_LICENSE:
                result = {
                    constants.PROP_VALUE: value["url"],
                    constants.PROP_TYPE: constants.LICENSE,
                    constants.PROP_NAME: value["name"],
                    constants.PROP_URL: value["url"]
                }
                if "spdx_id" in value.keys():
                    result[constants.PROP_SPDX_ID] = value["spdx_id"]
            elif category == constants.CAT_OWNER:
                result = {
                    constants.PROP_VALUE: value,
                    constants.PROP_TYPE: value_type
                }
                if maintainer_data.get("name"):
                    result[constants.PROP_NAME] = maintainer_data["name"]
                if maintainer_data.get("affiliation"):
                    result[constants.PROP_AFFILIATION] = maintainer_data["affiliation"]
                if maintainer_data.get("email"):
                    result[constants.PROP_EMAIL] = maintainer_data["email"]
            else:
                result = {
                    constants.PROP_VALUE: value,
                    constants.PROP_TYPE: value_type
                }

            if (result['value']):
                repository_metadata.add_result(category, result, 1, constants.TECHNIQUE_GITHUB_API)
    # get languages
    if not ignore_api_metadata:
        languages_raw, date = rate_limit_get(filtered_resp['languages_url'], headers=header)
        
        languages = languages_raw.json()
        if "message" in languages:
            logging.error("Error while retrieving languages: " + languages["message"])
        else:
            filtered_resp['languages'] = list(languages.keys())
            for l, s in languages.items():
                result = {
                    constants.PROP_VALUE: l,
                    constants.PROP_NAME: l,
                    constants.PROP_TYPE: constants.LANGUAGE,
                    constants.PROP_SIZE: s,
                }
                repository_metadata.add_result(constants.CAT_PROGRAMMING_LANGUAGES, result, 1,
                                               constants.TECHNIQUE_GITHUB_API)

        # get releases
        # releases_list_raw, date = rate_limit_get(repo_api_base_url + "/releases",
        #                                          headers=header)
        releases_list = get_all_paginated_results(repo_api_base_url + "/releases", headers=header)
        # releases_list = releases_list_raw.json()
        # if isinstance(releases_list, dict) and 'message' in releases_list.keys():
        #     logging.error(f"Releases Error: {releases_list['message']}")
        # else:
        release_list_filtered = [do_crosswalk(release, constants.release_crosswalk_table) for release in
                                    releases_list]
        
        for release in release_list_filtered:
            release_obj = {
                constants.PROP_TYPE: constants.RELEASE,
                constants.PROP_VALUE: release[constants.PROP_URL]
            }
            for category, value in release.items():
                if category != constants.AGENT_TYPE:
                    if category == constants.PROP_AUTHOR:
                        value = {
                            constants.PROP_NAME: value,
                            constants.PROP_TYPE: release[constants.AGENT_TYPE]
                        }
                    if value != "":
                        release_obj[category] = value
                    else:
                        logging.warning("Ignoring empty value in release for " + category)

                    if category == constants.CAT_ASSETS:
                        assets_release_list_filtered = [do_crosswalk(assets, constants.release_assets_github) for assets in
                                    release[constants.CAT_ASSETS]]
                        
                        key_mapping = {
                            constants.PROP_BROWSER_URL: constants.PROP_CONTENT_URL,
                            constants.PROP_SIZE: constants.PROP_CONTENT_SIZE,
                            constants.PROP_CONTENT_TYPE: constants.PROP_ENCODING_FORMAT,
                            constants.PROP_DATE_CREATED_AT: constants.PROP_UPLOAD_DATE
                        }

                        assets_release_list_filtered = [
                            {key_mapping.get(k, k): v for k, v in asset.items()} for asset in assets_release_list_filtered
                        ]

                        release_obj[category] = assets_release_list_filtered

            repository_metadata.add_result(constants.CAT_RELEASES, release_obj, 1,
                                            constants.TECHNIQUE_GITHUB_API)
    logging.info("Repository information successfully loaded.\n")
    return repository_metadata, owner, repo_name, default_branch


def get_path(obj, path):
    if isinstance(path, list) or isinstance(path, tuple):
        if len(path) == 1:
            path = path[0]
        else:
            return get_path(obj[path[0]], path[1:])

    if obj is not None and path in obj:
        return obj[path]
    else:
        return None


def do_crosswalk(data, crosswalk_table):
    output = {}

    for somef_key, path in crosswalk_table.items():
        value = get_path(data, path)
        if value is not None:
            output[somef_key] = value
        else:
            logging.error(f"Error: key {path} not present in github repository")
    return output


def download_repository_files(owner, repo_name, default_branch, repo_type, target_dir, repo_ref=None,
                              authorization=None):
    """
    Given a repository, this method will download its files and return the readme text
    Parameters
    ----------
    @param repo_type: type of the repo (github, gitlab or local)
    @param default_branch: branch to download files from
    @param repo_name: name of the repo
    @param owner: owner of the repo
    @param target_dir: directory where to download files
    @param repo_ref: URL of the target repository (needed in some specific repos)
    @param authorization: GitHub authorization token

    Returns
    -------
    @return: Path to the folder where files have been downloaded

    """

    if repo_type == constants.RepositoryType.GITHUB:
        return download_github_files(target_dir, owner, repo_name, default_branch, authorization)
    elif repo_type == constants.RepositoryType.GITLAB:
        return download_gitlab_files(target_dir, owner, repo_name, default_branch, repo_ref)
    else:
        logging.error("Cannot download files from a local repository!")
        return None


def download_github_files(directory, owner, repo_name, repo_ref, authorization):
    """
    Download all repository files from a GitHub repository
    Parameters
    ----------
    repo_ref: link to branch of the repo
    repo_name: name of the repo
    owner: GitHub owner
    directory: directory where to extract all downloaded files
    authorization: GitHub authorization token

    Returns
    -------
    path to the folder where all files have been downloaded
    """
    # download the repo at the selected branch with the link
    repo_archive_url = f"https://github.com/{owner}/{repo_name}/archive/{repo_ref}.zip"
    logging.info(f"Downloading {repo_archive_url}")
    repo_download, date = rate_limit_get(repo_archive_url, headers=header_template(authorization))

    if repo_download is None:
        logging.warning(f"Repository archive skipped due to size limit: {constants.SIZE_DOWNLOAD_LIMIT_MB} MB or not content lenght.")
        return None
    
    if repo_download.status_code == 404:
        logging.error(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        repo_archive_url = f"https://github.com/{owner}/{repo_name}/archive/main.zip"
        logging.info(f"Trying to download {repo_archive_url}")
        repo_download, date = rate_limit_get(repo_archive_url, headers=header_template(authorization))
        if repo_download is None:
            logging.warning(f"Repository archive skipped due to size limit: {constants.SIZE_DOWNLOAD_LIMIT_MB} MB or not content lenght.")
            return None
        
    if repo_download.status_code != 200:
        sys.exit(f"Error: Archive request failed with HTTP {repo_download.status_code}")

    repo_zip = repo_download.content

    repo_name_full = owner + "_" + repo_name
    repo_zip_file = os.path.join(directory, repo_name_full + ".zip")
    repo_extract_dir = os.path.join(directory, repo_name_full)

    with open(repo_zip_file, "wb") as f:
        f.write(repo_zip)

    try:
        with zipfile.ZipFile(repo_zip_file, "r") as zip_ref: 
            zip_ref.extractall(repo_extract_dir) 
    except zipfile.BadZipFile: 
        logging.error("Downloaded archive is not a valid zip (repo may be empty)") 
        return None
    
    repo_folders = os.listdir(repo_extract_dir)
    if not repo_folders: 
        logging.warning("Repository archive is empty") 
        return None

    repo_dir = os.path.join(repo_extract_dir, repo_folders[0])
    return repo_dir


def get_project_id(repository_url,self_hosted):
    """
    Function to download a repository, given its URL
    Parameters:
    -------
    repository_url = url repository
    self_hosted = boolean that indicate if there es gitlab.com or a self hosted server
    -------
    """

    logging.info(f"Downloading {repository_url}")
    response = requests.get(repository_url)
    project_id = "-1"

    if self_hosted:
        if response.status_code == 200:
            projects = response.json()
            if isinstance(projects, dict) and "id" in projects:
                project_id = projects["id"]
        elif response.status_code in [401, 403]:
            logging.error("Access denied. Authentication may be required.")
        else:
            logging.error(f"Unexpected error. Status code: {response.status_code}")
    else:
        response_str = str(response.content.decode('utf-8'))
        init = response_str.find('\"project_id\":')
    
        start = init + len("\"project_id\":")
        if init >= 0:
            end = 0
            end_bracket = response_str.find("}", start)
            comma = response_str.find(",", start)
            if comma != -1 and comma < end_bracket:
                end = comma
            else:
                end = end_bracket
            if end >= 0:
                project_id = response_str[start:end]
    return project_id

def get_all_gitlab_releases(repo_api_base_url):
    all_releases = []
    page = 1

    while True:
        url = f"{repo_api_base_url}/releases?page={page}&per_page=100"
        logging.info(f"Getting releases from: {url}")
        response = requests.get(url)
        logging.info(f"Response: {response.status_code}")
        content_type = response.headers.get("Content-Type", "")
        if response.status_code != 200 or "application/json" not in content_type:
            logging.error(f"Error in response or not JSON: {response.text}")
            break 

        try:
            releases = response.json()
        except requests.exceptions.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}. Response: {response.text}")
            break

        if not releases:
            break 

        all_releases.extend(releases)

        # check if more pages
        next_page = response.headers.get("X-Next-Page")
        if not next_page:
            break  # No more pages

        page = int(next_page)

    if not all_releases:
        logging.warning("Not releseases found.")
        return []
    

    # release_list_filtered = [
    #     {
    #         "url": release.get("description"),
    #         "name": release.get("name"),
    #         "tag_name": release.get("tag_name"),
    #         "date": release.get("released_at"),
    #     }
    #     for release in all_releases
    # ]
    # print(release_list_filtered)
    return all_releases

def get_gitlab_releases(project_id, base_url):
    """
        Retrieves the releases of a GitLab repository without authentication.
        
        :param project_id: ID of the project in GitLab
        :param base_url: Base URL of the GitLab where the project is hosted (e.g., https://gitlab.in2p3.fr)
        :return: List of releases with relevant information
    """
    releases_url = f"{base_url}/api/v4/projects/{project_id}/releases"

    logging.info(f"Getting releases from: {releases_url}")

    response = requests.get(releases_url)
    
    if response.status_code != 200:
        logging.error(f"Error getting releases: {response.text}")
        return []

    releases_list = response.json()
    
    release_list_filtered = [
        {
            "url": release.get("description"),
            "name": release.get("name"),
            "tag_name": release.get("tag_name"),
            "date": release.get("released_at"),
        }
        for release in releases_list
    ]
    
    return release_list_filtered

# error when github url is wrong
class GithubUrlError(Exception):
    pass


def get_readme_content(readme_url):
    """Function to retrieve the content of a readme file given its URL (github)"""
    readme_url = readme_url.replace("/blob/", "/raw/")
    readme = requests.get(readme_url)
    readme_text = readme.content.decode('utf-8')
    return readme_text

def get_all_paginated_results(base_url, headers, per_page=100):
    """
    Retrieve all paginated results from a GitHub API endpoint.
    
    Parameters:
        base_url (str): The base API URL (without ?page or ?per_page).
        headers (dict): Headers to send (e.g. for authentication).
        per_page (int): Number of results per page (default=100, GitHub max).
    
    Returns:
        list: A combined list with all the items across all pages.
    """
    all_results = []
    page = 1

    while True:
        url = f"{base_url}?per_page={per_page}&page={page}"
        response, _ = rate_limit_get(url, headers=headers)

        if response.status_code != 200:
            logging.warning(f"GitHub API error on page {page}: {response.status_code}")
            break

        page_data = response.json()
        if not page_data:
            break  # No more results

        all_results.extend(page_data)
        page += 1

    return all_results
