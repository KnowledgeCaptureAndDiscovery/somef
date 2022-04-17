import base64
import urllib
import os
import tempfile
import re
import zipfile
import time
import requests
import sys

from datetime import datetime
from urllib.parse import urlparse
from . import markdown_utils, extract_ontologies, constants


# the same as requests.get(args).json(), but protects against rate limiting
def rate_limit_get(*args, backoff_rate=2, initial_backoff=1, **kwargs):
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


def load_gitlab_repository_metadata(repository_url, header, readme_only=False):
    """
    Function uses the repository_url provided to load required information from gitlab.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    repository_url: URL of the Gitlab repository to analyze
    header: headers of the repository
    readme_only: flag to indicate whether to process the full repo or just the readme

    Returns
    -------
    Readme text and required metadata
    """
    print(f"Loading Repository {repository_url} Information....")
    # load general response of the repository
    if repository_url[-1] == '/':
        repository_url = repository_url[:-1]
    url = urlparse(repository_url)
    if url.netloc != 'gitlab.com':
        print("Error: repository must come from github")
        return " ", {}

    path_components = url.path.split('/')

    if len(path_components) < 3:
        print("Gitlab link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}.")
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

    repo_ref = None

    if len(path_components) >= 5:
        if not path_components[4] == "tree":
            print(
                "GitLab link is not correct. \nThe correct format is https://gitlab.com/{owner}/{repo_name}.")

            return " ", {}

        # we must join all after 4, as sometimes tags have "/" in them.
        repo_ref = "/".join(path_components[5:])
        ref_param = {"ref": repo_ref}

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

    if repo_ref is None:
        repo_ref = general_resp['defaultBranch']

    if readme_only:
        repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/raw/{repo_ref}/README.md"
        print(f"Downloading {repo_archive_url}")
        repo_download = requests.get(repo_archive_url)
        if repo_download.status_code == 404:
            print(f"Error: Archive request failed with HTTP {repo_download.status_code}")
            repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/raw/master/README.md"
            print(f"Trying to download {repo_archive_url}")
            repo_download = requests.get(repo_archive_url)

        if repo_download.status_code != 200:
            print(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        repo_zip = repo_download.content
        print(repo_zip)
        text = repo_zip.decode('utf-8')
        return text, {}

    ## get only the fields that we want
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
    topics_headers = header
    topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
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

    ## get languages
    # languages, date = rate_limit_get(filtered_resp['languages_url'])
    languages = {}
    filtered_resp['languages_url'] = "languages_url"
    if "message" in languages:
        print("Languages Error: " + languages["message"])
    else:
        filtered_resp['languages'] = list(languages.keys())

    del filtered_resp['languages_url']

    # get default README
    # repo_api_base_url https://api.github.com/dgarijo/Widoco/readme
    # readme_info, date = rate_limit_get(repo_api_base_url + "/readme",
    #                                   headers=topics_headers,
    #                                   params=ref_param)
    readme_info = {}
    if 'message' in readme_info.keys():
        print("README Error: " + readme_info['message'])
        text = ""
    elif 'content' in readme_info:
        readme = base64.b64decode(readme_info['content']).decode("utf-8")
        text = readme
        filtered_resp['readmeUrl'] = readme_info['html_url']

    if 'readme_url' in project_details:
        text = get_readme_content(project_details['readme_url'])
        filtered_resp['readmeUrl'] = project_details['readme_url']

    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        # download the repo at the selected branch with the link
        # https://gitlab.com/unboundedsystems/adapt/-/archive/master/adapt-master.zip
        repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/archive/{repo_ref}/{repo_name}-{repo_ref}.zip"
        if len(path_components) == 4:
            repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/archive/{repo_ref}/{path_components[3]}.zip"
        print(f"Downloading {repo_archive_url}")
        repo_download = requests.get(repo_archive_url)
        repo_zip = repo_download.content

        repo_zip_file = os.path.join(temp_dir, "repo.zip")
        repo_extract_dir = os.path.join(temp_dir, "repo")

        with open(repo_zip_file, "wb") as f:
            f.write(repo_zip)

        with zipfile.ZipFile(repo_zip_file, "r") as zip_ref:
            zip_ref.extractall(repo_extract_dir)

        repo_folders = os.listdir(repo_extract_dir)
        assert (len(repo_folders) == 1)

        repo_dir = os.path.join(repo_extract_dir, repo_folders[0])

        text, filtered_resp = process_repository_files(repo_dir, filtered_resp, constants.RepositoryType.GITLAB,
                                                       owner, repo_name, repo_ref)
    releases_list = {}
    if isinstance(releases_list, dict) and 'message' in releases_list.keys():
        print("Releases Error: " + releases_list['message'])
    else:
        filtered_resp['releases'] = [do_crosswalk(release, constants.release_crosswalk_table) for release in
                                     releases_list]

    print("Repository Information Successfully Loaded. \n")
    return text, filtered_resp


def load_github_repository_metadata(repository_url, header, ignore_github_metadata=False, readme_only=False):
    """
    Function uses the repository_url provided to load required information from Github.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    repository_url
    header

    Returns
    -------
    Returns the readme text and required metadata
    """
    if repository_url.rfind("gitlab.com") > 0:
        return load_gitlab_repository_metadata(repository_url, header, readme_only)

    print(f"Loading Repository {repository_url} Information....")
    ## load general response of the repository
    if repository_url[-1] == '/':
        repository_url = repository_url[:-1]
    url = urlparse(repository_url)
    if url.netloc != 'github.com':
        print("Error: repository must come from github")
        return " ", {}

    path_components = url.path.split('/')

    if len(path_components) < 3:
        print("Repository link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}.")
        return " ", {}

    owner = path_components[1]
    repo_name = path_components[2]

    repo_api_base_url = f"https://api.github.com/repos/{owner}/{repo_name}"

    repo_ref = None
    ref_param = None

    if len(path_components) >= 5:
        if not path_components[3] == "tree":
            print(
                "Github link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}/tree/{ref}.")

            return " ", {}

        # we must join all after 4, as sometimes tags have "/" in them.
        repo_ref = "/".join(path_components[4:])
        ref_param = {"ref": repo_ref}

    print(repo_api_base_url)

    general_resp = {}
    date = ""
    if not ignore_github_metadata or readme_only:
        general_resp, date = rate_limit_get(repo_api_base_url, headers=header)

    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            print("Error: Repository name is private or incorrect")
        else:
            message = general_resp['message']
            print("Error: " + message)

        raise GithubUrlError

    if ignore_github_metadata:
        repo_ref = 'master'
    elif repo_ref is None:
        repo_ref = general_resp['default_branch']

    if readme_only:
        repo_archive_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/README.md"
        print(f"Downloading {repo_archive_url}")
        repo_download = requests.get(repo_archive_url)
        if repo_download.status_code == 404:
            print(f"Error: Archive request failed with HTTP {repo_download.status_code}")
            repo_archive_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/master/README.md"
            print(f"Trying to download {repo_archive_url}")
            repo_download = requests.get(repo_archive_url)

        if repo_download.status_code != 200:
            print(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        repo_zip = repo_download.content

        text = repo_zip.decode('utf-8')
        return text, {}

    ## get only the fields that we want
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
    if not ignore_github_metadata:
        filtered_resp = do_crosswalk(general_resp, constants.github_crosswalk_table)
        if "issueTracker" in filtered_resp:
            issue_tracker = filtered_resp["issueTracker"]
            issue_tracker = issue_tracker.replace("{/number}", "")
            filtered_resp["issueTracker"] = issue_tracker

    # add download URL
    filtered_resp["downloadUrl"] = f"https://github.com/{owner}/{repo_name}/releases"

    ## condense license information
    license_info = {}
    if 'license' in filtered_resp:
        for k in ('name', 'url'):
            if k in filtered_resp['license']:
                license_info[k] = filtered_resp['license'][k]

    ## If we didn't find it, look for the license
    if 'url' not in license_info or license_info['url'] is None:

        possible_license_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/LICENSE"
        license_text_resp = requests.get(possible_license_url)

        # todo: It's possible that this request will get rate limited. Figure out how to detect that.
        if license_text_resp.status_code == 200:
            # license_text = license_text_resp.text
            license_info['url'] = possible_license_url

    if len(license_info) > 0:
        filtered_resp['license'] = license_info

    topics_headers = header
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

    ## get languages
    if not ignore_github_metadata:
        languages, date = rate_limit_get(filtered_resp['languages_url'], headers=header)
        if "message" in languages:
            print("Languages Error: " + languages["message"])
        else:
            filtered_resp['languages'] = list(languages.keys())

        del filtered_resp['languages_url']

    # get default README
    #                                   headers=topics_headers,
    # readme_info, date = rate_limit_get(repo_api_base_url + "/readme",
    #                                   headers=topics_headers,
    #                                   params=ref_param)
    # if 'message' in readme_info.keys():
    #    print("README Error: " + readme_info['message'])
    #    text = ""
    # else:
    #    readme = base64.b64decode(readme_info['content']).decode("utf-8")
    #    text = readme
    #    filtered_resp['readmeUrl'] = readme_info['html_url']

    # get full git repository
    # todo: maybe it should be optional, as this could take some time?

    text = ""
    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

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

        repo_zip_file = os.path.join(temp_dir, "repo.zip")
        repo_extract_dir = os.path.join(temp_dir, "repo")

        with open(repo_zip_file, "wb") as f:
            f.write(repo_zip)

        with zipfile.ZipFile(repo_zip_file, "r") as zip_ref:
            zip_ref.extractall(repo_extract_dir)

        repo_folders = os.listdir(repo_extract_dir)
        assert (len(repo_folders) == 1)

        repo_dir = os.path.join(repo_extract_dir, repo_folders[0])

        text, filtered_resp = process_repository_files(repo_dir, filtered_resp, constants.RepositoryType.GITHUB,
                                                 owner, repo_name, repo_ref)

    # get releases
    if not ignore_github_metadata:
        releases_list, date = rate_limit_get(repo_api_base_url + "/releases",
                                             headers=header)

        if isinstance(releases_list, dict) and 'message' in releases_list.keys():
            print("Releases Error: " + releases_list['message'])
        else:
            filtered_resp['releases'] = [do_crosswalk(release, constants.release_crosswalk_table) for release in
                                         releases_list]

    print("Repository information successfully loaded.\n")
    return text, filtered_resp


def load_local_repository_metadata(local_repo):
    filtered_resp = {}
    repo_dir = os.path.abspath(local_repo)
    text, filtered_resp = process_repository_files(repo_dir, filtered_resp, constants.RepositoryType.LOCAL)
    print("Local Repository Information Successfully Loaded. \n")
    return text, filtered_resp


def get_project_id(repository_url):
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
    readme_url = readme_url.replace("/blob/", "/raw/")
    readme = requests.get(readme_url)
    readme_text = readme.content.decode('utf-8')
    return readme_text


def convert_to_raw_user_content_github(partial, owner, repo_name, repo_ref):
    if partial.startswith("./"):
        partial = partial.replace("./", "")
    if partial.startswith(".\\"):
        partial = partial.replace(".\\", "")
    if partial.find("\\") >= 0:
        partial = re.sub("\\\\", "/", partial)

    return f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/{urllib.parse.quote(partial)}"


def convert_to_raw_user_content_gitlab(partial, owner, repo_name, repo_ref):
    if partial.startswith("./"):
        partial = partial.replace("./", "")
    if partial.startswith(".\\"):
        partial = partial.replace(".\\", "")
    return f"https://gitlab.com/{owner}/{repo_name}/-/blob/{repo_ref}/{urllib.parse.quote(partial)}"


def process_repository_files(repo_dir, filtered_resp, repo_type, owner="", repo_name="", repo_ref=""):
    """
    Method that given a folder, it recognizes whether there are notebooks, dockerfiles, docs, script files or
    ontologies.
    Parameters
    ----------
    repo_dir: path to the dir to analyze
    filtered_resp: JSON object to be completed by this method
    repo_type: GITHUB, GITLAB or LOCAL
    owner: owner of the repo (only for github/gitlab repos)
    repo_name: repository name (only for github/gitlab repos)
    repo_ref: branch (only for github/gitlab repos)

    Returns
    -------
    A JSON object (filtered_resp) with the findings and the text of the readme
    """
    notebooks = []
    dockerfiles = []
    docs = []
    script_files = []
    ontologies = []
    text = ""
    for dir_path, dir_names, filenames in os.walk(repo_dir):
        repo_relative_path = os.path.relpath(dir_path, repo_dir)
        for filename in filenames:
            file_path = os.path.join(repo_relative_path, filename)
            if filename == "Dockerfile" or filename.lower() == "docker-compose.yml":
                if repo_type == constants.RepositoryType.GITHUB:
                    dockerfiles.append(convert_to_raw_user_content_github(file_path, owner, repo_name, repo_ref))
                elif repo_type == constants.RepositoryType.GITLAB:
                    dockerfiles.append(convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_ref))
                else:
                    dockerfiles.append(os.path.join(repo_dir, file_path))

            if filename.lower().endswith(".ipynb"):
                if repo_type == constants.RepositoryType.GITHUB:
                    notebooks.append(convert_to_raw_user_content_github(file_path, owner, repo_name, repo_ref))
                elif repo_type == constants.RepositoryType.GITLAB:
                    notebooks.append(convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_ref))
                else:
                    notebooks.append(os.path.join(repo_dir, file_path))

            if "README" == filename.upper() or "README.MD" == filename.upper():
                if repo_relative_path == ".":
                    try:
                        with open(os.path.join(dir_path, filename), "rb") as data_file:
                            data_file_text = data_file.read()
                            text = data_file_text.decode("utf-8")
                            if repo_type == constants.RepositoryType.GITHUB:
                                filtered_resp['readmeUrl'] = convert_to_raw_user_content_github(filename, owner,
                                                                                                repo_name,
                                                                                                repo_ref)
                    except:
                        print("README Error: error while reading file content")
            if "LICENSE" == filename.upper() or "LICENSE.MD" == filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "rb") as data_file:
                        file_text = data_file.read()
                        filtered_resp["licenseText"] = markdown_utils.unmark(file_text)
                except:
                    # TO DO: try different encodings
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["licenseFile"] = convert_to_raw_user_content_github(filename, owner, repo_name,
                                                                                          repo_ref)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["licenseFile"] = convert_to_raw_user_content_gitlab(filename, owner, repo_name,
                                                                                          repo_ref)
                    else:
                        filtered_resp["licenseFile"] = os.path.join(repo_dir, repo_relative_path, filename)

            if "CODE_OF_CONDUCT" == filename.upper() or "CODE_OF_CONDUCT.MD" == filename.upper():
                if repo_type == constants.RepositoryType.GITHUB:
                    filtered_resp["codeOfConduct"] = convert_to_raw_user_content_github(filename, owner, repo_name,
                                                                                        repo_ref)
                elif repo_type == constants.RepositoryType.GITLAB:
                    filtered_resp["codeOfConduct"] = convert_to_raw_user_content_gitlab(filename, owner, repo_name,
                                                                                        repo_ref)
                else:
                    filtered_resp["codeOfConduct"] = os.path.join(repo_dir, repo_relative_path, filename)

            if "CONTRIBUTING" == filename.upper() or "CONTRIBUTING.MD" == filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["contributingGuidelines"] = markdown_utils.unmark(file_text)
                except:
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["contributingGuidelinesFile"] = convert_to_raw_user_content_github(filename,
                                                                                                         owner,
                                                                                                         repo_name,
                                                                                                         repo_ref)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["contributingGuidelinesFile"] = convert_to_raw_user_content_gitlab(filename,
                                                                                                         owner,
                                                                                                         repo_name,
                                                                                                         repo_ref)
                    else:
                        filtered_resp["contributingGuidelinesFile"] = os.path.join(repo_dir, repo_relative_path,
                                                                                   filename)
            if "ACKNOWLEDGMENT" in filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["acknowledgments"] = markdown_utils.unmark(file_text)
                except:
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["acknowledgmentsFile"] = convert_to_raw_user_content_github(filename, owner,
                                                                                                  repo_name,
                                                                                                  repo_ref)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["acknowledgmentsFile"] = convert_to_raw_user_content_gitlab(filename, owner,
                                                                                                  repo_name,
                                                                                                  repo_ref)
                    else:
                        filtered_resp["acknowledgmentsFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CONTRIBUTORS" == filename.upper() or "CONTRIBUTORS.MD" == filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["contributors"] = markdown_utils.unmark(file_text)
                except:
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["contributorsFile"] = convert_to_raw_user_content_github(filename, owner,
                                                                                               repo_name,
                                                                                               repo_ref)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["contributorsFile"] = convert_to_raw_user_content_gitlab(filename, owner,
                                                                                               repo_name,
                                                                                               repo_ref)
                    else:
                        filtered_resp["contributorsFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CITATION" == filename.upper() or "CITATION.CFF" == filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["citation"] = markdown_utils.unmark(file_text)
                except:
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["citationFile"] = convert_to_raw_user_content_github(filename, owner,
                                                                                           repo_name,
                                                                                           repo_ref)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["citationFile"] = convert_to_raw_user_content_gitlab(filename, owner,
                                                                                           repo_name,
                                                                                           repo_ref)
                    else:
                        filtered_resp["citationFile"] = os.path.join(repo_dir, repo_relative_path, filename)

            if filename.endswith(".sh"):
                if repo_type == constants.RepositoryType.GITHUB:
                    script_files.append(convert_to_raw_user_content_github(file_path, owner, repo_name, repo_ref))
                elif repo_type == constants.RepositoryType.GITLAB:
                    script_files.append(convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_ref))
                else:
                    script_files.append(os.path.join(repo_dir, file_path))

            if filename.endswith(".ttl") or filename.endswith(".owl") or filename.endswith(".nt") or filename. \
                    endswith(".xml"):
                uri = extract_ontologies.is_file_ontology(os.path.join(repo_dir, file_path))
                if uri is not None:
                    # and not any(o['uri'] == uri for o in ontologies): This checks if the onto is not already
                    # there, but we return all ontologies we find right now. Filtering is up to users
                    file_url = ""
                    if repo_type == constants.RepositoryType.GITHUB:
                        file_url = convert_to_raw_user_content_github(file_path, owner, repo_name, repo_ref)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        file_url = convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_ref)
                    else:
                        file_url = os.path.join(repo_dir, file_path)
                    onto = {
                        "uri": uri,
                        "file_url": file_url
                    }
                    ontologies.append(onto)

        for dir_name in dir_names:
            if dir_name.lower() == "docs":
                if repo_relative_path == ".":
                    docs_path = dir_name
                else:
                    if repo_relative_path.find("\\") >= 0:
                        new_repo_relative_path = repo_relative_path.replace("\\", "/")
                        docs_path = os.path.join(new_repo_relative_path, dir_name)
                    else:
                        docs_path = os.path.join(repo_relative_path, dir_name)

                names = os.listdir(os.path.join(repo_dir, docs_path))
                for name in names:
                    if name.lower().endswith(".pdf") or name.lower().endswith(".md") or name.lower().endswith(
                            ".html") or name.lower().endswith(".htm"):
                        if repo_type == constants.RepositoryType.GITHUB:
                            docs.append(
                                f"https://github.com/{owner}/{repo_name}/tree/{urllib.parse.quote(repo_ref)}/{docs_path}")
                        elif repo_type == constants.RepositoryType.GITLAB:
                            docs.append(
                                f"https://gitlab.com/{owner}/{repo_name}/-/tree/{urllib.parse.quote(repo_ref)}/{docs_path}")
                        else:
                            docs.append(os.path.join(repo_dir, docs_path))
                        break

    if len(notebooks) > 0:
        filtered_resp["hasExecutableNotebook"] = notebooks
    if len(dockerfiles) > 0:
        filtered_resp["hasBuildFile"] = dockerfiles
    if len(docs) > 0:
        filtered_resp["hasDocumentation"] = docs
    if len(script_files) > 0:
        filtered_resp["hasScriptFile"] = script_files
    if len(ontologies) > 0:
        filtered_resp["ontologies"] = ontologies
    return text, filtered_resp
