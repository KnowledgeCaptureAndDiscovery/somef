import logging
import os
import re
import urllib
import yaml
import lxml.etree
from rdflib import Graph
from urllib.parse import urlparse
from .utils import constants, markdown_utils
from . import extract_ontologies, extract_workflows
from .process_results import Result
from chardet import detect
from .parser.pom_xml_parser import parse_pom_file
from .parser.package_json_parser import parse_package_json_file

def process_repository_files(repo_dir, metadata_result: Result, repo_type, owner="", repo_name="",
                             repo_default_branch="", ignore_test_folder=True):
    """
    Method that given a folder, it recognizes whether there are notebooks, dockerfiles, docs, script files or
    ontologies.
    Parameters
    ----------
    @param repo_dir: path to the dir to analyze
    @param metadata_result: JSON object gathering the metadata found by SOMEF
    @param repo_type: GITHUB, GITLAB or LOCAL
    @param owner: owner of the repo (only for github/gitlab repos)
    @param repo_name: repository name (only for github/gitlab repos)
    @param repo_default_branch: branch (only for github/gitlab repos)
    @param ignore_test_folder: flag to ignore the contents of test folders (e.g., licenses)

    Returns
    -------
    @return: text of the main readme and a JSON dictionary (filtered_resp) with the findings in files
    """
    text = ""
    try:
        for dir_path, dir_names, filenames in os.walk(repo_dir):
            repo_relative_path = os.path.relpath(dir_path, repo_dir)
            # if this is a test folder, we ignore it (except for the root repo)
            if ignore_test_folder and repo_relative_path != "." and "test" in repo_relative_path.lower():
                # skip this file if it's in a test folder, or inside one
                continue
            for filename in filenames:
                file_path = os.path.join(repo_relative_path, filename)
                # ignore image files that may have  correct name
                if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or \
                        filename.lower().endswith(".svg") or filename.lower().endswith(".png") or \
                        filename.lower().endswith(".gif"):
                    continue
                if filename == "Dockerfile" or filename.lower() == "docker-compose.yml":
                    docker_url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir,
                                               repo_relative_path, filename)
                    if filename == "Dockerfile":
                        format_file = constants.FORMAT_DOCKERFILE
                    else:
                        format_file = constants.FORMAT_DOCKER_COMPOSE
                    metadata_result.add_result(constants.CAT_HAS_BUILD_FILE,
                                               {
                                                   constants.PROP_VALUE: docker_url,
                                                   constants.PROP_TYPE: constants.URL,
                                                   constants.PROP_FORMAT: format_file
                                               },
                                               1,
                                               constants.TECHNIQUE_FILE_EXPLORATION, docker_url)
                if filename.lower().endswith(".ipynb"):
                    notebook_url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir,
                                                 repo_relative_path, filename)
                    metadata_result.add_result(constants.CAT_EXECUTABLE_EXAMPLE,
                                               {
                                                   constants.PROP_VALUE: notebook_url,
                                                   constants.PROP_TYPE: constants.URL,
                                                   constants.PROP_FORMAT: constants.FORMAT_JUPYTER_NB
                                               },
                                               1,
                                               constants.TECHNIQUE_FILE_EXPLORATION, notebook_url)
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
                                    logging.error(f"{type(err).__name__} was raised: {err} Trying other encodings...")
                                    text = data_file_text.decode(detect(data_file_text)["encoding"])
                                if repo_type == constants.RepositoryType.GITHUB:
                                    readme_url = convert_to_raw_user_content_github(filename, owner,
                                                                                    repo_name,
                                                                                    repo_default_branch)
                                    metadata_result.add_result(constants.CAT_README_URL,
                                                               {
                                                                   constants.PROP_VALUE: readme_url,
                                                                   constants.PROP_TYPE: constants.URL
                                                               },
                                                               1,
                                                               constants.TECHNIQUE_FILE_EXPLORATION)
                        except ValueError:
                            logging.error("README Error: error while reading file content")
                            logging.error(f"{type(err).__name__} was raised: {err}")
                if "LICENCE" == filename.upper() or "LICENSE" == filename.upper() or "LICENSE.MD" == filename.upper():
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_LICENSE)
                if "CODE_OF_CONDUCT" == filename.upper() or "CODE_OF_CONDUCT.MD" == filename.upper():
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_COC)
                if "CONTRIBUTING" == filename.upper() or "CONTRIBUTING.MD" == filename.upper():
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_CONTRIBUTING_GUIDELINES)
                if "ACKNOWLEDGMENT" in filename.upper() or "ACKNOWLEDGEMENT.MD" == filename.upper():
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_ACKNOWLEDGEMENT)
                if "CONTRIBUTORS" == filename.upper() or "CONTRIBUTORS.MD" == filename.upper():
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_CONTRIBUTORS)
                if "INSTALL" in filename.upper() and filename.upper().endswith("MD"):
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_INSTALLATION)
                # TO DO: double-check the formats and create a proper publication object (issue 207)
                if "CITATION" == filename.upper() or "CITATION.BIB" == filename.upper():
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_CITATION,
                                                               constants.FORMAT_BIB)
                if "CITATION.CFF" == filename.upper():       
                    metadata_result = get_file_content_or_link(repo_type, file_path, owner, repo_name,
                                                               repo_default_branch,
                                                               repo_dir, repo_relative_path, filename, dir_path,
                                                               metadata_result, constants.CAT_CITATION,
                                                               constants.FORMAT_CFF)
                if filename.endswith(".sh"):
                    sh_url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir,
                                           repo_relative_path, filename)
                    metadata_result.add_result(constants.CAT_HAS_SCRIPT_FILE,
                                               {
                                                   constants.PROP_VALUE: sh_url,
                                                   constants.PROP_TYPE: constants.URL
                                               }, 1, constants.TECHNIQUE_FILE_EXPLORATION
                                               )
                if filename.endswith(".ttl") or filename.endswith(".owl") or filename.endswith(".nt") or filename. \
                        endswith(".xml"):
                    uri = extract_ontologies.is_file_ontology(os.path.join(repo_dir, file_path))
                    if uri is not None:
                        onto_url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir,
                                                 repo_relative_path, filename)
                        metadata_result.add_result(constants.CAT_ONTOLOGIES,
                                                   {
                                                       constants.PROP_VALUE: onto_url,
                                                       constants.PROP_TYPE: constants.URL
                                                   }, 1, constants.TECHNIQUE_FILE_EXPLORATION
                                                   )
                if filename.endswith(".ga") or filename.endswith(".cwl") or filename.endswith(".nf") or (
                        filename.endswith(".snake") or filename.endswith(
                    ".smk") or "Snakefile" == filename_no_ext) or filename.endswith(".knwf") or filename.endswith(
                    ".t2flow") or filename.endswith(".dag") or filename.endswith(".kar") or filename.endswith(
                    ".wdl"):
                    analysis = extract_workflows.is_file_workflow(os.path.join(repo_dir, file_path))
                    if analysis:
                        workflow_url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch,
                                                     repo_dir, repo_relative_path, filename)
                        metadata_result.add_result(constants.CAT_WORKFLOWS,
                                                   {
                                                       constants.PROP_VALUE: workflow_url,
                                                       constants.PROP_TYPE: constants.URL
                                                   }, 1, constants.TECHNIQUE_FILE_EXPLORATION)
                ################################### PACKAGE ##################################
                if filename.lower() == "pom.xml":
                    logging.info(f"############### Processing package file: {filename} ############### ")
                    metadata_result = parse_pom_file(os.path.join(dir_path, filename), metadata_result)
                    
                    build_file_url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir,
                                                  repo_relative_path, filename)
                    metadata_result.add_result(constants.CAT_HAS_BUILD_FILE,
                                              {
                                                  constants.PROP_VALUE: build_file_url,
                                                  constants.PROP_TYPE: constants.URL,
                                                  constants.PROP_FORMAT: constants.FORMAT_POM
                                              },
                                              1,
                                              constants.TECHNIQUE_FILE_EXPLORATION, build_file_url)

                elif filename.lower() == "package.json":
                    logging.info(f"############### Processing package file: {filename} ###############")
                    metadata_result = parse_package_json_file(os.path.join(dir_path, filename), metadata_result)
                    
                    build_file_url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir,
                                                    repo_relative_path, filename)
                    metadata_result.add_result(constants.CAT_HAS_BUILD_FILE,
                                                {
                                                    constants.PROP_VALUE: build_file_url,
                                                    constants.PROP_TYPE: constants.URL,
                                                    constants.PROP_FORMAT: constants.FORMAT_NPM
                                                },
                                                1,
                                                constants.TECHNIQUE_FILE_EXPLORATION, build_file_url)
                ################################### PACKAGE ##################################
                
            # TO DO: Improve this a bit, as just returning the docs folder is not that informative
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
                                docs_url = f"https://github.com/{owner}/{repo_name}/tree/{urllib.parse.quote(repo_default_branch)}/{docs_path}"
                            elif repo_type == constants.RepositoryType.GITLAB:
                                docs_url = f"https://gitlab.com/{owner}/{repo_name}/-/tree/{urllib.parse.quote(repo_default_branch)}/{docs_path}"
                            else:
                                docs_url = os.path.join(repo_dir, docs_path)
                            # docs.append(docs_url)
                            metadata_result.add_result(constants.CAT_DOCUMENTATION,
                                                       {
                                                           constants.PROP_VALUE: docs_url,
                                                           constants.PROP_TYPE: constants.URL
                                                       }, 1, constants.TECHNIQUE_FILE_EXPLORATION
                                                       )
                            break
        return text, metadata_result
    except TypeError:
        logging.error("Error when opening the repository files")
        return None, None


def get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir, repo_relative_path,
                  filename):
    """
    Function to return the URL (or path if not possible) of a given file
    Parameters
    ----------
    repo_type
    file_path
    owner
    repo_name
    repo_default_branch
    repo_dir
    repo_relative_path
    filename

    Returns
    -------

    """
    if repo_type == constants.RepositoryType.GITHUB:
        return convert_to_raw_user_content_github(file_path, owner, repo_name, repo_default_branch)
    elif repo_type == constants.RepositoryType.GITLAB:
        return convert_to_raw_user_content_gitlab(file_path, owner, repo_name, repo_default_branch)
    else:
        return os.path.join(repo_dir, repo_relative_path, filename)


def get_file_content_or_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir, repo_relative_path,
                             filename, dir_path, metadata_result: Result, category, format_result=""):
    """
    This method will return to the JSON file the contents of the file or its link if it cannot process the contents
    Parameters
    ----------
    repo_type
    file_path
    owner
    repo_name
    repo_default_branch
    repo_dir
    repo_relative_path
    filename
    dir_path
    metadata_result
    category
    format_result

    Returns
    -------
    @returns String with the file content or url link to the file
    """
    url = get_file_link(repo_type, file_path, owner, repo_name, repo_default_branch, repo_dir, repo_relative_path,
                        filename)
    # do not add result if a file under the same category exist. Only for license, citation, COC, contribution, README
    replace = False
    results = metadata_result.results
    try:
        if category in results:
            # check category exists, using the file exploration technique, and retrieve source
            if category in [constants.CAT_CITATION, constants.CAT_LICENSE, constants.CAT_COC, constants.CAT_README_URL,
                            constants.CAT_CONTRIBUTING_GUIDELINES]:
                for entry in results[category]:
                    if (constants.PROP_SOURCE in entry and
                            entry[constants.PROP_TECHNIQUE] is constants.TECHNIQUE_FILE_EXPLORATION):
                        new_file_path = extract_directory_path(url)
                        existing_path = extract_directory_path(entry[constants.PROP_SOURCE])
                        if new_file_path.startswith(existing_path):
                            # the existing file is higher, ignore this one
                            return metadata_result
                        else:
                            # replace result in hierarchy (below)
                            replace = True
                        break
    except Exception as e:
        logging.warning("Error when trying to determine if redundant files exist " + str(e))
    try:
        with open(os.path.join(dir_path, filename), "r") as data_file:
            file_text = data_file.read()

            result = {
                constants.PROP_VALUE: file_text,
                constants.PROP_TYPE: constants.FILE_DUMP
            }
            
            # Properties extraction from cff
            if format_result == 'cff':
                yaml_content = yaml.safe_load(file_text)
                preferred_citation = yaml_content.get("preferred-citation", {})

                title = preferred_citation.get("title", None)
                doi = preferred_citation.get("doi", None)
                url_citation = preferred_citation.get("url", None) 
                authors = preferred_citation.get("authors", [])

                if url:
                    final_url = url_citation
                elif doi:
                    final_url = f"https://doi.org/{doi}"

                author_names = ", ".join(
                    f"{a.get('given-names', '').strip()} {a.get('family-names', '').strip()}".strip()
                    for a in authors if a.get('given-names') and a.get('family-names')
                ) or None  

                if title:
                    result[constants.PROP_TITLE] = title
                if author_names:
                    result[constants.PROP_AUTHOR] = author_names
                if final_url:
                    result[constants.PROP_URL] = final_url
                if doi:
                    result[constants.PROP_DOI] = doi   

            if format_result != "":
                result[constants.PROP_FORMAT] = format_result

            if replace:
                metadata_result.edit_hierarchical_result(category, result, 1, constants.TECHNIQUE_FILE_EXPLORATION, url)
            else:
                metadata_result.add_result(category, result, 1, constants.TECHNIQUE_FILE_EXPLORATION, url)
    except:
        if replace:
            metadata_result.edit_hierarchical_result(category,
                                                     {
                                                         constants.PROP_VALUE: url,
                                                         constants.PROP_TYPE: constants.URL
                                                     }, 1, constants.TECHNIQUE_FILE_EXPLORATION)
        else:
            metadata_result.add_result(category,
                                       {
                                           constants.PROP_VALUE: url,
                                           constants.PROP_TYPE: constants.URL
                                       }, 1, constants.TECHNIQUE_FILE_EXPLORATION)
    return metadata_result


def extract_directory_path(path):
    """
    Method to extract a directorr or URL path without the file name
    Parameters
    ----------
    path: file path

    Returns
    -------
    the URL/file path without the name of the file
    """
    if os.path.exists(path):
        return os.path.dirname(os.path.abspath(path))
    else:
        return os.path.dirname(urlparse(path).path)


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
