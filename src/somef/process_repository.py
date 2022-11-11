import base64
import logging
import os
import zipfile
import time
import requests
import sys
from datetime import datetime
from urllib.parse import urlparse
from .utils import constants
from . import configuration


# the same as requests.get(args).json(), but protects against rate limiting
def rate_limit_get(*args, backoff_rate=2, initial_backoff=1, **kwargs):
    """Function to obtain how many requests we have pending with the GitHub API"""
    rate_limited = True
    response = {}
    date = ""
    while rate_limited:
        response = requests.get(*args, **kwargs)
        data = response
        date = data.headers["date"]
        rate_limit_remaining = data.headers["x-ratelimit-remaining"]
        epochtime = int(data.headers["x-ratelimit-reset"])
        date_reset = datetime.fromtimestamp(epochtime)
        print("Remaining GitHub API requests: " + rate_limit_remaining + " ### Next rate limit reset at: " + str(
            date_reset))
        response = response.json()
        if 'message' in response and 'API rate limit exceeded' in response['message']:
            rate_limited = True
            print(f"rate limited. Backing off for {initial_backoff} seconds")
            time.sleep(initial_backoff)
            # increase the backoff for next time
            initial_backoff *= backoff_rate
        else:
            rate_limited = False

    return response, date


def load_gitlab_repository_metadata(repository_url):
    """
    Function uses the repository_url provided to load required information from gitlab.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
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
    if url.netloc != 'gitlab.com':
        logging.error("Repository must come from Gitlab")
        return " ", {}

    path_components = url.path.split('/')

    if len(path_components) < 3:
        print("Gitlab link is not correct.")
        return " ", {}

    owner = path_components[1]
    repo_name = path_components[2]
    if len(path_components) == 4:
        repo_name = repo_name + '/' + path_components[3]

    project_id = get_project_id(repository_url)
    project_api_url = f"https://gitlab.com/api/v4/projects/{project_id}"
    print(f"Downloading {project_api_url}")
    details = requests.get(project_api_url)
    project_details = details.json()
    date = details.headers["date"]

    repo_api_base_url = f"{repository_url}"

    default_branch = None

    if len(path_components) >= 5:
        if not path_components[4] == "tree":
            print(
                "GitLab link is not correct. \nThe correct format is https://gitlab.com/{owner}/{repo_name}.")

            return " ", {}

        # we must join all after 4, as sometimes tags have "/" in them.
        default_branch = "/".join(path_components[5:])
        ref_param = {"ref": default_branch}

    print(repo_api_base_url)
    if 'defaultBranch' in project_details.keys():
        general_resp = {'defaultBranch': project_details['defaultBranch']}
    elif 'default_branch' in project_details.keys():
        general_resp = {'defaultBranch': project_details['default_branch']}

    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            print("Error: repository name is incorrect")
        else:
            message = general_resp['message']
            print("Error: " + message)

        raise GithubUrlError

    if default_branch is None:
        default_branch = general_resp['defaultBranch']

    # get only the fields that we want
    def do_crosswalk(data, crosswalk_table):
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

        output = {}
        for codemeta_key, path in crosswalk_table.items():
            value = get_path(data, path)
            if value is not None:
                output[codemeta_key] = value
            else:
                print(f"Error: key {path} not present in gitlab repository")
        return output

    # filtered_resp = do_crosswalk(general_resp, github_crosswalk_table)
    filtered_resp = {"downloadUrl": f"https://gitlab.com/{owner}/{repo_name}/-/branches"}

    # condense license information
    license_info = {}
    if 'license' in filtered_resp:
        for k in ('name', 'url'):
            if k in filtered_resp['license']:
                license_info[k] = filtered_resp['license'][k]

    # If we didn't find it, look for the license
    if 'url' not in license_info or license_info['url'] is None:

        possible_license_url = f"{repository_url}/-/blob/master/LICENSE"
        license_text_resp = requests.get(possible_license_url)

        # todo: It's possible that this request will get rate limited. Figure out how to detect that.
        if license_text_resp.status_code == 200:
            # license_text = license_text_resp.text
            license_info['url'] = possible_license_url

    if license_info != '':
        filtered_resp['license'] = license_info

    # get keywords / topics
    # topics_headers = header
    # topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
    # topics_resp, date = rate_limit_get(repo_api_base_url + "/topics",
    #                                   headers=topics_headers)
    topics_resp = {}

    if 'message' in topics_resp.keys():
        print("Topics Error: " + topics_resp['message'])
    elif topics_resp and 'names' in topics_resp.keys():
        filtered_resp['topics'] = topics_resp['names']

    if project_details['topics'] is not None:
        filtered_resp['topics'] = project_details['topics']

    # get social features: stargazers_count
    stargazers_info = {}
    # if 'stargazers_count' in filtered_resp:
    if project_details['star_count'] is not None:
        stargazers_info['count'] = project_details['star_count']
        stargazers_info['date'] = date
        if 'stargazers_count' in filtered_resp.keys():
            del filtered_resp['stargazers_count']
    filtered_resp['stargazersCount'] = stargazers_info

    # get social features: forks_count
    forks_info = {}
    # if 'forks_count' in filtered_resp:
    if project_details['forks_count'] is not None:
        forks_info['count'] = project_details['forks_count']
        forks_info['date'] = date
        if 'forks_count' in filtered_resp.keys():
            del filtered_resp['forks_count']
    filtered_resp['forksCount'] = forks_info

    # get languages
    languages = {}
    filtered_resp['languages_url'] = "languages_url"
    if "message" in languages:
        print("Languages Error: " + languages["message"])
    else:
        filtered_resp['languages'] = list(languages.keys())

    del filtered_resp['languages_url']

    readme_info = {}
    if 'message' in readme_info.keys():
        print("README Error: " + readme_info['message'])
        # text = ""
    elif 'content' in readme_info:
        readme = base64.b64decode(readme_info['content']).decode("utf-8")
        # text = readme
        filtered_resp['readmeUrl'] = readme_info['html_url']

    if 'readme_url' in project_details:
        # text = get_readme_content(project_details['readme_url'])
        filtered_resp['readmeUrl'] = project_details['readme_url']

    releases_list = {}
    if isinstance(releases_list, dict) and 'message' in releases_list.keys():
        print("Releases Error: " + releases_list['message'])
    else:
        filtered_resp['releases'] = [do_crosswalk(release, constants.release_crosswalk_table) for release in
                                     releases_list]

    print("Repository information successfully loaded. \n")
    return filtered_resp, owner, repo_name, default_branch


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
    repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/archive/{repo_branch}/{repo_name}-{repo_branch}.zip"
    if len(path_components) == 4:
        repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/archive/{repo_branch}/{path_components[3]}.zip"
    print(f"Downloading {repo_archive_url}")
    repo_download = requests.get(repo_archive_url)
    repo_zip = repo_download.content

    repo_zip_file = os.path.join(directory, "repo.zip")
    repo_extract_dir = os.path.join(directory, "repo")

    with open(repo_zip_file, "wb") as f:
        f.write(repo_zip)

    with zipfile.ZipFile(repo_zip_file, "r") as zip_ref:
        zip_ref.extractall(repo_extract_dir)

    repo_folders = os.listdir(repo_extract_dir)
    assert (len(repo_folders) == 1)

    repo_dir = os.path.join(repo_extract_dir, repo_folders[0])
    return repo_dir


def download_readme(owner, repo_name, default_branch, repo_type):
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
    repo_download = requests.get(primary_url)
    if repo_download.status_code == 404:
        logging.error(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        logging.info(f"Trying to download {secondary_url}")
        repo_download = requests.get(secondary_url)
    if repo_download.status_code != 200:
        logging.error(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        return None
    repo_zip = repo_download.content
    text = repo_zip.decode('utf-8')
    return text


def load_online_repository_metadata(repository_url, ignore_api_metadata=False,
                                    repo_type=constants.RepositoryType.GITHUB):
    """
    Function uses the repository_url provided to load required information from GitHub or Gitlab.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    @param repo_type: type of the repository (GITLAB, GITHUB or LOCAL)
    @param ignore_api_metadata: true if you do not want to do an additional request to the target API
    @param repository_url: target repository URL.

    Returns
    -------
    @return: Dictionary with the available metadata from online APIs, its owner, repo name and default branch
    """
    if repo_type == constants.RepositoryType.GITLAB:
        return load_gitlab_repository_metadata(repository_url)
    elif repo_type == constants.RepositoryType.LOCAL:
        logging.warning("Trying to download metadata from a local repository")
        return None

    logging.info(f"Loading Repository {repository_url} Information....")
    # Read from the config file the right token information
    header = {}
    file_paths = configuration.get_configuration_file()
    if 'Authorization' in file_paths.keys():
        header['Authorization'] = file_paths['Authorization']
    header['accept'] = 'application/vnd.github.v3+json'

    # load general response of the repository
    if repository_url[-1] == '/':
        repository_url = repository_url[:-1]
    url = urlparse(repository_url)
    if url.netloc != 'github.com':
        logging.error("Repository must be from Github")
        return " ", {}

    path_components = url.path.split('/')

    if len(path_components) < 3:
        logging.error("Repository link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}.")
        return " ", {}

    owner = path_components[1]
    repo_name = path_components[2]

    repo_api_base_url = f"https://api.github.com/repos/{owner}/{repo_name}"

    default_branch = None

    if len(path_components) >= 5:
        if not path_components[3] == "tree":
            print(
                "Github link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}/tree/{ref}.")

            return " ", {}

        # we must join all after 4, as sometimes tags have "/" in them.
        default_branch = "/".join(path_components[4:])
        ref_param = {"ref": default_branch}

    general_resp = {}
    date = ""
    if not ignore_api_metadata:
        general_resp, date = rate_limit_get(repo_api_base_url, headers=header)

    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            print("Error: Repository name is private or incorrect")
        else:
            message = general_resp['message']
            print("Error: " + message)

        raise GithubUrlError

    if ignore_api_metadata:
        default_branch = 'master'
    elif default_branch is None:
        default_branch = general_resp['default_branch']

    # get only the fields that we want
    def do_crosswalk(data, crosswalk_table):
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

        output = {}
        for codemeta_key, path in crosswalk_table.items():
            value = get_path(data, path)
            if value is not None:
                output[codemeta_key] = value
            else:
                print(f"Error: key {path} not present in github repository")
        return output

    filtered_resp = {}
    if not ignore_api_metadata:
        filtered_resp = do_crosswalk(general_resp, constants.github_crosswalk_table)
        if "issueTracker" in filtered_resp:
            issue_tracker = filtered_resp["issueTracker"]
            issue_tracker = issue_tracker.replace("{/number}", "")
            filtered_resp["issueTracker"] = issue_tracker

    # add download URL
    filtered_resp["downloadUrl"] = f"https://github.com/{owner}/{repo_name}/releases"

    # condense license information
    license_info = {}
    if 'license' in filtered_resp:
        for k in ('name', 'url'):
            if k in filtered_resp['license']:
                license_info[k] = filtered_resp['license'][k]

    # If we didn't find it, look for the license
    if 'url' not in license_info or license_info['url'] is None:

        possible_license_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{default_branch}/LICENSE"
        license_text_resp = requests.get(possible_license_url)

        # todo: It's possible that this request will get rate limited. Figure out how to detect that.
        if license_text_resp.status_code == 200:
            # license_text = license_text_resp.text
            license_info['url'] = possible_license_url

    if len(license_info) > 0:
        filtered_resp['license'] = license_info

    # get keywords / topics
    if 'topics' in general_resp.keys():
        filtered_resp['topics'] = general_resp['topics']
    # else:
    #    topics_headers = header
    #    topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
    #    topics_resp, date = rate_limit_get(repo_api_base_url + "/topics",
    #                                       headers=topics_headers)

    #    if 'message' in topics_resp.keys():
    #        print("Topics Error: " + topics_resp['message'])
    #    elif topics_resp and 'names' in topics_resp.keys():
    #        filtered_resp['topics'] = topics_resp['names']

    # get social features: stargazers_count
    stargazers_info = {}
    if 'stargazers_count' in filtered_resp:
        stargazers_info['count'] = filtered_resp['stargazers_count']
        stargazers_info['date'] = date
        del filtered_resp['stargazers_count']
    if len(stargazers_info.keys()) > 0:
        filtered_resp['stargazersCount'] = stargazers_info

    # get social features: forks_count
    forks_info = {}
    if 'forks_count' in filtered_resp:
        forks_info['count'] = filtered_resp['forks_count']
        forks_info['date'] = date
        del filtered_resp['forks_count']
    if len(forks_info.keys()) > 0:
        filtered_resp['forksCount'] = forks_info

    # get languages
    if not ignore_api_metadata:
        languages, date = rate_limit_get(filtered_resp['languages_url'], headers=header)
        if "message" in languages:
            print("Languages Error: " + languages["message"])
        else:
            filtered_resp['languages'] = list(languages.keys())

        del filtered_resp['languages_url']
        # get releases
        releases_list, date = rate_limit_get(repo_api_base_url + "/releases",
                                             headers=header)
        if isinstance(releases_list, dict) and 'message' in releases_list.keys():
            print("Releases Error: " + releases_list['message'])
        else:
            filtered_resp['releases'] = [do_crosswalk(release, constants.release_crosswalk_table) for release in
                                         releases_list]
    logging.info("Repository information successfully loaded.\n")
    return filtered_resp, owner, repo_name, default_branch


def download_repository_files(owner, repo_name, default_branch, repo_type, target_dir, repo_ref=None):
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

    Returns
    -------
    @return: Path to the folder where files have been downloaded

    """

    if repo_type == constants.RepositoryType.GITHUB:
        return download_github_files(target_dir, owner, repo_name, default_branch)
    elif repo_type == constants.RepositoryType.GITLAB:
        return download_gitlab_files(target_dir, owner, repo_name, default_branch, repo_ref)
    else:
        logging.error("Cannot download files from a local repository!")
        return None


def download_github_files(directory, owner, repo_name, repo_ref):
    """
    Download all repository files from a GitHub repository
    Parameters
    ----------
    repo_ref: link to branch of the repo
    repo_name: name of the repo
    owner: GitHub owner
    directory: directory where to extract all downloaded files

    Returns
    -------
    path to the folder where all files have been downloaded
    """
    # download the repo at the selected branch with the link
    repo_archive_url = f"https://github.com/{owner}/{repo_name}/archive/{repo_ref}.zip"
    print(f"Downloading {repo_archive_url}")
    repo_download = requests.get(repo_archive_url)
    if repo_download.status_code == 404:
        print(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        repo_archive_url = f"https://github.com/{owner}/{repo_name}/archive/main.zip"
        print(f"Trying to download {repo_archive_url}")
        repo_download = requests.get(repo_archive_url)

    if repo_download.status_code != 200:
        sys.exit(f"Error: Archive request failed with HTTP {repo_download.status_code}")
    repo_zip = repo_download.content

    repo_name_full = owner + "_" + repo_name
    repo_zip_file = os.path.join(directory, repo_name_full + ".zip")
    repo_extract_dir = os.path.join(directory, repo_name_full)

    with open(repo_zip_file, "wb") as f:
        f.write(repo_zip)

    with zipfile.ZipFile(repo_zip_file, "r") as zip_ref:
        zip_ref.extractall(repo_extract_dir)

    repo_folders = os.listdir(repo_extract_dir)
    # assert (len(repo_folders) == 1)

    repo_dir = os.path.join(repo_extract_dir, repo_folders[0])

    return repo_dir
    #return process_repository_files(repo_dir, filtered_resp, constants.RepositoryType.GITHUB,
    #                                owner, repo_name, repo_ref)


# def load_local_repository_metadata(local_repo):
#     """Function to apply somef to a local repository (already downloaded)"""
#     filtered_resp = {}
#     repo_dir = os.path.abspath(local_repo)
#     text, filtered_resp = process_repository_files(repo_dir, filtered_resp, constants.RepositoryType.LOCAL)
#     print("Local repository information successfully loaded. \n")
#     return text, filtered_resp


def get_project_id(repository_url):
    """Function to download a repository, given its URL"""
    print(f"Downloading {repository_url}")
    response = requests.get(repository_url)
    response_str = str(response.content.decode('utf-8'))
    init = response_str.find('\"project_id\":')
    project_id = "-1"
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


# error when github url is wrong
class GithubUrlError(Exception):
    # print("The URL provided seems to be incorrect")
    pass


def get_readme_content(readme_url):
    """Function to retrieve the content of a readme file given its URL (github)"""
    readme_url = readme_url.replace("/blob/", "/raw/")
    readme = requests.get(readme_url)
    readme_text = readme.content.decode('utf-8')
    return readme_text


