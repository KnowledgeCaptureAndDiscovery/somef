import os
import re
import urllib
from .utils import constants ,markdown_utils
from . import extract_ontologies
from chardet import detect


def process_repository_files(repo_dir, filtered_resp, repo_type, owner="", repo_name="", repo_default_branch=""):
    """
    Method that given a folder, it recognizes whether there are notebooks, dockerfiles, docs, script files or
    ontologies.
    Parameters
    ----------
    @param repo_dir: path to the dir to analyze
    @param filtered_resp: JSON object to be completed by this method
    @param repo_type: GITHUB, GITLAB or LOCAL
    @param owner: owner of the repo (only for github/gitlab repos)
    @param repo_name: repository name (only for github/gitlab repos)
    @param repo_default_branch: branch (only for github/gitlab repos)

    Returns
    -------
    @return: text of the main readme and a JSON dictionary (filtered_resp) with the findings in files
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
                    dockerfiles.append(convert_to_raw_user_content_github(file_path, owner, repo_name, repo_default_branch))
                elif repo_type == constants.RepositoryType.GITLAB:
                    dockerfiles.append(convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_default_branch))
                else:
                    dockerfiles.append(os.path.join(repo_dir, file_path))

            if filename.lower().endswith(".ipynb"):
                if repo_type == constants.RepositoryType.GITHUB:
                    notebooks.append(convert_to_raw_user_content_github(file_path, owner, repo_name, repo_default_branch))
                elif repo_type == constants.RepositoryType.GITLAB:
                    notebooks.append(convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_default_branch))
                else:
                    notebooks.append(os.path.join(repo_dir, file_path))

            filename_no_ext = os.path.splitext(filename)[0]
            # this will take into account README, README.MD, README.TXT, README.RST
            if "README" == filename_no_ext.upper():
                if repo_relative_path == ".":
                    try:
                        with open(os.path.join(dir_path, filename), "rb") as data_file:
                            data_file_text = data_file.read()
                            try:
                                text = data_file_text.decode("utf-8")
                            except UnicodeError as err:
                                print(f"{type(err).__name__} was raised: {err} Trying other encodings...")
                                text = data_file_text.decode(detect(data_file_text)["encoding"])
                            if repo_type == constants.RepositoryType.GITHUB:
                                filtered_resp['readmeUrl'] = convert_to_raw_user_content_github(filename, owner,
                                                                                                repo_name,
                                                                                                repo_default_branch)
                    except ValueError:
                        print("README Error: error while reading file content")
                        print(f"{type(err).__name__} was raised: {err}")

            if "LICENSE" == filename.upper() or "LICENSE.MD" == filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "rb") as data_file:
                        file_text = data_file.read()
                        filtered_resp["licenseText"] = markdown_utils.unmark(file_text)
                except:
                    # TO DO: try different encodings
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["licenseFile"] = convert_to_raw_user_content_github(filename, owner, repo_name,
                                                                                          repo_default_branch)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["licenseFile"] = convert_to_raw_user_content_gitlab(filename, owner, repo_name,
                                                                                          repo_default_branch)
                    else:
                        filtered_resp["licenseFile"] = os.path.join(repo_dir, repo_relative_path, filename)

            if "CODE_OF_CONDUCT" == filename.upper() or "CODE_OF_CONDUCT.MD" == filename.upper():
                if repo_type == constants.RepositoryType.GITHUB:
                    filtered_resp["codeOfConduct"] = convert_to_raw_user_content_github(filename, owner, repo_name,
                                                                                        repo_default_branch)
                elif repo_type == constants.RepositoryType.GITLAB:
                    filtered_resp["codeOfConduct"] = convert_to_raw_user_content_gitlab(filename, owner, repo_name,
                                                                                        repo_default_branch)
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
                                                                                                         repo_default_branch)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["contributingGuidelinesFile"] = convert_to_raw_user_content_gitlab(filename,
                                                                                                         owner,
                                                                                                         repo_name,
                                                                                                         repo_default_branch)
                    else:
                        filtered_resp["contributingGuidelinesFile"] = os.path.join(repo_dir, repo_relative_path,
                                                                                   filename)
            if "ACKNOWLEDGMENT" in filename.upper() or "ACKNOWLEDGEMENT" in filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["acknowledgement"] = markdown_utils.unmark(file_text)
                except ValueError:
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["acknowledgmentsFile"] = convert_to_raw_user_content_github(filename, owner,
                                                                                                  repo_name,
                                                                                                  repo_default_branch)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["acknowledgmentsFile"] = convert_to_raw_user_content_gitlab(filename, owner,
                                                                                                  repo_name,
                                                                                                  repo_default_branch)
                    else:
                        filtered_resp["acknowledgmentsFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CONTRIBUTORS" == filename.upper() or "CONTRIBUTORS.MD" == filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["contributors"] = markdown_utils.unmark(file_text)
                except ValueError:
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["contributorsFile"] = convert_to_raw_user_content_github(filename, owner,
                                                                                               repo_name,
                                                                                               repo_default_branch)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["contributorsFile"] = convert_to_raw_user_content_gitlab(filename, owner,
                                                                                               repo_name,
                                                                                               repo_default_branch)
                    else:
                        filtered_resp["contributorsFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CITATION" == filename.upper() or "CITATION.CFF" == filename.upper() or "CITATION.BIB" == filename.upper():
                try:
                    with open(os.path.join(dir_path, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["citation"] = markdown_utils.unmark(file_text)
                except ValueError:
                    if repo_type == constants.RepositoryType.GITHUB:
                        filtered_resp["citationFile"] = convert_to_raw_user_content_github(filename, owner,
                                                                                           repo_name,
                                                                                           repo_default_branch)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        filtered_resp["citationFile"] = convert_to_raw_user_content_gitlab(filename, owner,
                                                                                           repo_name,
                                                                                           repo_default_branch)
                    else:
                        filtered_resp["citationFile"] = os.path.join(repo_dir, repo_relative_path, filename)

            if filename.endswith(".sh"):
                if repo_type == constants.RepositoryType.GITHUB:
                    script_files.append(convert_to_raw_user_content_github(file_path, owner, repo_name, repo_default_branch))
                elif repo_type == constants.RepositoryType.GITLAB:
                    script_files.append(convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_default_branch))
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
                        file_url = convert_to_raw_user_content_github(file_path, owner, repo_name, repo_default_branch)
                    elif repo_type == constants.RepositoryType.GITLAB:
                        file_url = convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_default_branch)
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
                                f"https://github.com/{owner}/{repo_name}/tree/{urllib.parse.quote(repo_default_branch)}/{docs_path}")
                        elif repo_type == constants.RepositoryType.GITLAB:
                            docs.append(
                                f"https://gitlab.com/{owner}/{repo_name}/-/tree/{urllib.parse.quote(repo_default_branch)}/{docs_path}")
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


def convert_to_raw_user_content_github(partial, owner, repo_name, repo_ref):
    """Converts GitHub paths into raw.githubuser content URLs, accessible by users"""
    if partial.startswith("./"):
        partial = partial.replace("./", "")
    if partial.startswith(".\\"):
        partial = partial.replace(".\\", "")
    if partial.find("\\") >= 0:
        partial = re.sub("\\\\", "/", partial)

    return f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/{urllib.parse.quote(partial)}"


def convert_to_raw_user_content_gitlab(partial, owner, repo_name, repo_ref):
    """Converts GitLab paths into raw.githubuser content URLs, accessible by users"""
    if partial.startswith("./"):
        partial = partial.replace("./", "")
    if partial.startswith(".\\"):
        partial = partial.replace(".\\", "")
    return f"https://gitlab.com/{owner}/{repo_name}/-/blob/{repo_ref}/{urllib.parse.quote(partial)}"
