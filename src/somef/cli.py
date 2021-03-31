# creatJSON.py
# parameters:
## input file: either: url to github repository OR markdown documentation file path
## output file: json with each excerpt marked with all four classification scores

import argparse
import json
import base64
from urllib.parse import urlparse
import sys
import os
from os import path
from pathlib import Path
import requests
from markdown import Markdown
from bs4 import BeautifulSoup
from io import StringIO
import pickle
import pprint
import pandas as pd
import numpy as np
import re
from dateutil import parser as date_parser
import zipfile

from somef.data_to_graph import DataGraph

from . import createExcerpts
from . import header_analysis

import time

import tempfile

import urllib


## Markdown to plain text conversion: begin ##
# code snippet from https://stackoverflow.com/a/54923798
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)


## Markdown to plain text conversion: end ##

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(f"{x} not in range [0.0, 1.0]")
    return x


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
    "forks_url": "forks_url",
    "stargazers_count": "stargazers_count",
    "forks_count": "forks_count"
}

release_crosswalk_table = {
    'tag_name': 'tag_name',
    'name': 'name',
    'author_name': ['author', 'login'],
    'authorType': ['author', 'type'],
    'body': 'body',
    'tarball_url': 'tarball_url',
    'zipball_url': 'zipball_url',
    'html_url': 'html_url',
    'url': 'url',
    'dateCreated': 'created_at',
    'datePublished': "published_at",
}


# the same as requests.get(args).json(), but protects against rate limiting
def rate_limit_get(*args, backoff_rate=2, initial_backoff=1, **kwargs):
    rate_limited = True
    response = {}
    date = ""
    while rate_limited:
        response = requests.get(*args, **kwargs)
        data = response
        date = data.headers["date"]
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


# error when github url is wrong
class GithubUrlError(Exception):
    # print("The URL provided seems to be incorrect")
    pass


def load_repository_metadata(repository_url, header):
    """
    Function uses the repository_url provided to load required information from github.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    repository_url
    header

    Returns
    -------
    Returns the readme text and required metadata
    """
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
        print("Github link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}.")
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

    general_resp, date = rate_limit_get(repo_api_base_url, headers=header)

    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            print("Error: repository name is incorrect")
        else:
            message = general_resp['message']
            print("Error: " + message)

        raise GithubUrlError

    if repo_ref is None:
        repo_ref = general_resp['default_branch']

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

    filtered_resp = do_crosswalk(general_resp, github_crosswalk_table)
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

    if license_info != '':
        filtered_resp['license'] = license_info

    # get keywords / topics
    topics_headers = header
    topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
    topics_resp, date = rate_limit_get(repo_api_base_url + "/topics",
                                       headers=topics_headers)

    if 'message' in topics_resp.keys():
        print("Topics Error: " + topics_resp['message'])
    elif topics_resp and 'names' in topics_resp.keys():
        filtered_resp['topics'] = topics_resp['names']

    # get social features: stargazers_count
    stargazers_info = {}
    if 'stargazers_count' in filtered_resp:
        stargazers_info['count'] = filtered_resp['stargazers_count']
        stargazers_info['date'] = date
    filtered_resp['stargazers_count'] = stargazers_info

    # get social features: forks_count
    forks_info = {}
    if 'forks_count' in filtered_resp:
        forks_info['count'] = filtered_resp['forks_count']
        forks_info['date'] = date
    filtered_resp['forks_count'] = forks_info

    ## get languages
    languages, date = rate_limit_get(filtered_resp['languages_url'])
    if "message" in languages:
        print("Languages Error: " + languages["message"])
    else:
        filtered_resp['languages'] = list(languages.keys())

    del filtered_resp['languages_url']

    # get default README
    readme_info, date = rate_limit_get(repo_api_base_url + "/readme",
                                       headers=topics_headers,
                                       params=ref_param)
    if 'message' in readme_info.keys():
        print("README Error: " + readme_info['message'])
        text = ""
    else:
        readme = base64.b64decode(readme_info['content']).decode("utf-8")
        text = readme
        filtered_resp['readme_url'] = readme_info['html_url']

    # get full git repository
    # todo: maybe it should be optional, as this could take some time?

    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        # download the repo at the selected branch with the link
        repo_archive_url = f"https://github.com/{owner}/{repo_name}/archive/{repo_ref}.zip"
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

        notebooks = []
        dockerfiles = []

        docs = []

        for dirpath, dirnames, filenames in os.walk(repo_dir):
            repo_relative_path = os.path.relpath(dirpath, repo_dir)
            for filename in filenames:
                if filename == "Dockerfile":
                    dockerfiles.append(os.path.join(repo_relative_path, filename))
                if filename.lower().endswith(".ipynb"):
                    notebooks.append(os.path.join(repo_relative_path, filename))

            for dirname in dirnames:
                if dirname.lower() == "docs":
                    if repo_relative_path == ".":
                        docs_path = dirname
                    else:
                        docs_path = repo_relative_path + "/" + dirname

                    docs.append(
                        f"https://github.com/{owner}/{repo_name}/tree/{urllib.parse.quote(repo_ref)}/{docs_path}")
                    print(docs)

        print("NOTEBOOKS:")
        print(notebooks)

        print("DOCKERFILES:")
        print(dockerfiles)

    if len(notebooks) > 0:
        filtered_resp["hasExecutableNotebook"] = [convert_to_raw_usercontent(x, owner, repo_name, repo_ref) for x in
                                                  notebooks]
    if len(dockerfiles) > 0:
        filtered_resp["hasBuildFile"] = [convert_to_raw_usercontent(x, owner, repo_name, repo_ref) for x in dockerfiles]
    if len(docs) > 0:
        filtered_resp["hasDocumentation"] = docs

    ## get releases
    releases_list, date = rate_limit_get(repo_api_base_url + "/releases",
                                         headers=header)

    if isinstance(releases_list, dict) and 'message' in releases_list.keys():
        print("Releases Error: " + releases_list['message'])
    else:
        filtered_resp['releases'] = [do_crosswalk(release, release_crosswalk_table) for release in releases_list]

    print("Repository Information Successfully Loaded. \n")
    return text, filtered_resp


def convert_to_raw_usercontent(partial, owner, repo_name, repo_ref):
    return f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/{urllib.parse.quote(partial)}"


## Function takes readme text as input and divides it into excerpts
## Returns the extracted excerpts
def create_excerpts(string_list):
    print("Splitting text into valid excerpts for classification")
    divisions = createExcerpts.split_into_excerpts(string_list)
    print("Text Successfully split. \n")
    return divisions


## Function takes readme text as input and runs the provided classifiers on it
## Returns the dictionary containing scores for each excerpt.
def run_classifiers(excerpts, file_paths):
    score_dict = {}
    if len(excerpts) > 0:
        for category in categories:
            if category not in file_paths.keys():
                sys.exit("Error: Category " + category + " file path not present in config.json")
            file_name = file_paths[category]
            if not path.exists(file_name):
                sys.exit(f"Error: File/Directory {file_name} does not exist")
            print("Classifying excerpts for the category", category)
            classifier = pickle.load(open(file_name, 'rb'))
            scores = classifier.predict_proba(excerpts)
            score_dict[category] = {'excerpt': excerpts, 'confidence': scores[:, 1]}
            print("Excerpt Classification Successful for the Category", category)
        print("\n")

    return score_dict


## Function removes all excerpt lines which have been classified but contain only one word.
## Returns the excerpt to be entered into the predictions
def remove_unimportant_excerpts(excerpt_element):
    excerpt_info = excerpt_element['excerpt']
    excerpt_confidence = excerpt_element['confidence']
    excerpt_lines = excerpt_info.split('\n')
    final_excerpt = {'excerpt': "", 'confidence': [], 'technique': 'Supervised classification'}
    for i in range(len(excerpt_lines) - 1):
        words = excerpt_lines[i].split(' ')
        if len(words) == 2:
            continue
        final_excerpt['excerpt'] += excerpt_lines[i] + '\n';
        final_excerpt['confidence'].append(excerpt_confidence[i])
    return final_excerpt


## Function takes scores dictionary and a threshold as input
## Returns predictions containing excerpts with a confidence above the given threshold.
def classify(scores, threshold):
    print("Checking Thresholds for Classified Excerpts.")
    predictions = {}
    for ele in scores.keys():
        print("Running for", ele)
        flag = False
        predictions[ele] = []
        excerpt = ""
        confid = []
        for i in range(len(scores[ele]['confidence'])):
            if scores[ele]['confidence'][i] >= threshold:
                if flag == False:
                    excerpt = excerpt + scores[ele]['excerpt'][i] + ' \n'
                    confid.append(scores[ele]['confidence'][i])
                    flag = True
                else:
                    excerpt = excerpt + scores[ele]['excerpt'][i] + ' \n'
                    confid.append(scores[ele]['confidence'][i])
            else:
                if flag == True:
                    element = remove_unimportant_excerpts({'excerpt': excerpt, 'confidence': confid})
                    if len(element['confidence']) != 0:
                        predictions[ele].append(element)
                    excerpt = ""
                    confid = []
                    flag = False
        print("Run completed.")
    print("All Excerpts below the given Threshold Removed. \n")
    return predictions


def extract_categories_using_header(repo_data):
    """
    Function that adds category information extracted using header information
    Parameters
    ----------
    repo_data data to use the header analysis

    Returns
    -------
    Returns json with the information added.
    """
    print("Extracting information using headers")
    # this is a hack because if repo_data is "" this errors out
    if len(repo_data) == 0:
        return {}, []
    try:
        header_info, string_list = header_analysis.extract_categories_using_headers(repo_data)
        print("Information extracted. \n")
        return header_info, string_list
    except:
        print("Error while extracting headers: ", sys.exc_info()[0])
        return {}, [repo_data]


def extract_bibtex(readme_text) -> object:
    """
    Function takes readme text as input (cleaned from markdown notation) and runs a regex expression on top of it.
    Returns list of bibtex citations
    """
    regex = r'\@[a-zA-Z]+\{[.\n\S\s]+?[author|title][.\n\S\s]+?[author|title][.\n\S\s]+?\n\}'
    citations = re.findall(regex, readme_text)
    print("Extraction of bibtex citation from readme completed. \n")
    return citations


def extract_dois(readme_text) -> object:
    """
    Function that takes the text of a readme file and searches if there are any DOIs badges.
    Parameters
    ----------
    readme_text Text of the readme

    Returns
    -------
    DOIs/identifiers associated with this software component
    """
    # regex = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
    # regex = r'\[\!\[DOI\]\(.+\)\]\(([^)]+)\)'
    regex = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
    dois = re.findall(regex, readme_text)
    print("Extraction of DOIS from readme completed.\n")
    # print(dois)
    return dois


def extract_binder_links(readme_text) -> object:
    """
    Function that does a regex to extract binder links used as reference in the readme.
    There could be multiple binder links for one reprository
    Parameters
    ----------
    readme_text

    Returns
    -------
    Links with binder notebooks/scripts that are ready to be executed.
    """
    regex = r'\[\!\[Binder\]([^\]]+)\]\(([^)]+)\)'
    binder_links = re.findall(regex, readme_text)
    print("Extraction of Binder links from readme completed.\n")
    # print(dois)
    return binder_links


def extract_title(unfiltered_text):
    """
    Function to extract a title based on the first header in the readme file
    Parameters
    ----------
    unfiltered_text

    Returns
    -------
    Full title of the repo (if found)
    """
    underline_header = re.findall('.+[\n]={3,}[\n]', unfiltered_text)
    # header declared with ====
    if len(underline_header) != 0:
        title = re.split('.+[=]+[\n]+', unfiltered_text)[0].strip()
    else:
        # The first occurrence is assumed to be the title.
        title = re.findall(r'#.+', unfiltered_text)[0]
        # Remove initial #
        title = title[1:].strip()
    return title


def merge(header_predictions, predictions, citations, dois, binder_links, long_title):
    """
    Function that takes the predictions using header information, classifier and bibtex/doi parser
    Parameters
    ----------
    header_predictions extraction of common headers and their contents
    predictions predictions from classifiers (description, installation instructions, invocation, citation)
    citations (bibtex citations)
    dois identifiers found in readme (Zenodo DOIs)

    Returns
    -------
    Combined predictions and results of the extraction process
    """
    print("Merge prediction using header information, classifier and bibtex and doi parsers")
    if long_title:
        predictions['long_title'] = {'excerpt': long_title, 'confidence': [1.0],
                                     'technique': 'Regular expression'}
    for i in range(len(citations)):
        if 'citation' not in predictions.keys():
            predictions['citation'] = []
        predictions['citation'].insert(0, {'excerpt': citations[i], 'confidence': [1.0],
                                           'technique': 'Regular expression'})
    if len(dois) != 0:
        predictions['identifier'] = []
        for identifier in dois:
            # The identifier is in position 1. Position 0 is the badge id, which we don't want to export
            predictions['identifier'].insert(0, {'excerpt': identifier[1], 'confidence': [1.0],
                                                 'technique': 'Regular expression'})
    if len(binder_links) != 0:
        predictions['executable_example'] = []
        for notebook in binder_links:
            # The identifier is in position 1. Position 0 is the badge id, which we don't want to export
            predictions['executable_example'].insert(0, {'excerpt': notebook[1], 'confidence': [1.0],
                                                         'technique': 'Regular expression'})
    for headers in header_predictions:
        if headers not in predictions.keys():
            predictions[headers] = header_predictions[headers]
        else:
            for h in header_predictions[headers]:
                predictions[headers].insert(0, h)
    print("Merging successful. \n")
    return predictions


## Function takes metadata, readme text predictions, bibtex citations and path to the output file
## Performs some combinations
def format_output(git_data, repo_data):
    print("formatting output")
    for i in git_data.keys():
        # print(i)
        # print(git_data[i])
        if i == 'description':
            if 'description' not in repo_data.keys():
                repo_data['description'] = []
            if git_data[i] != "":
                repo_data['description'].append(
                    {'excerpt': git_data[i], 'confidence': [1.0], 'technique': 'GitHub API'})
        else:
            if i == 'hasExecutableNotebook' or i == 'hasBuildFile' or i == 'hasDocumentation':
                repo_data[i] = {'excerpt': git_data[i], 'confidence': [1.0], 'technique': 'File Exploration'}
            elif git_data[i] != "" and git_data[i] != []:
                repo_data[i] = {'excerpt': git_data[i], 'confidence': [1.0], 'technique': 'GitHub API'}
    return repo_data


# saves the final json Object in the file
def save_json_output(repo_data, outfile, pretty=False):
    print("Saving json data to", outfile)
    with open(outfile, 'w') as output:
        if pretty:
            json.dump(repo_data, output, sort_keys=True, indent=2)
        else:
            json.dump(repo_data, output)

    ## Function takes metadata, readme text predictions, bibtex citations and path to the output file


## Performs some combinations and saves the final json Object in the file
def save_json(git_data, repo_data, outfile):
    repo_data = format_output(git_data, repo_data)
    save_json_output(repo_data, outfile)


def save_codemeta_output(repo_data, outfile, pretty=False):
    def data_path(path):
        return DataGraph.resolve_path(repo_data, path)

    def format_date(date_string):
        date_object = date_parser.parse(date_string)
        return date_object.strftime("%Y-%m-%d")

    latest_release = None
    releases = data_path(["releases", "excerpt"])

    if releases is not None and len(releases) > 0:
        latest_release = releases[0]
        latest_pub_date = date_parser.parse(latest_release["datePublished"])
        for index in range(1, len(releases)):
            release = releases[index]
            pub_date = date_parser.parse(release["datePublished"])

            if pub_date > latest_pub_date:
                latest_release = release
                latest_pub_date = pub_date

    def release_path(path):
        return DataGraph.resolve_path(latest_release, path)

    code_repository = data_path(["codeRepository", "excerpt"])

    author_name = data_path(["owner", "excerpt"])

    # do the descriptions

    def average_confidence(x):
        confs = x["confidence"]

        if len(confs) > 0:
            return sum(confs) / len(confs)
        else:
            return 0

    descriptions = data_path(["description"])
    descriptions.sort(key=lambda x: (average_confidence(x) + (1 if x["technique"] == "GitHub API" else 0)),
                      reverse=True)
    descriptions_text = [x["excerpt"] for x in descriptions]

    published_date = ""
    try:
        published_date = format_date(release_path(["datePublished"]))
    except:
        print("Published date is not available")

    codemeta_output = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
        "license": data_path(["license", "excerpt", "url"]),
        "codeRepository": "git+" + code_repository + ".git",
        "dateCreated": format_date(data_path(["dateCreated", "excerpt"])),
        "dateModified": format_date(data_path(["dateModified", "excerpt"])),
        "downloadUrl": data_path(["downloadUrl", "excerpt"]),
        "issueTracker": code_repository + "/issues",
        "name": data_path(["name", "excerpt"]),
        "version": release_path(["tag_name"]),
        "description": descriptions_text,
        "releaseNotes": release_path(["body"]),
        "keywords": data_path(["topics", "excerpt"]),
        "programmingLanguage": data_path(["languages", "excerpt"]),
        "softwareRequirements": data_path(["requirement", "excerpt"]),
        "author": [
            {
                "@type": "Person",
                "@id": "https://github.com/" + author_name
            }
        ]
    }
    if published_date != "":
        codemeta_output["datePublished"] = published_date

    pruned_output = {}

    for key, value in codemeta_output.items():
        if not (value is None or ((isinstance(value, list) or isinstance(value, tuple)) and len(value) == 0)):
            pruned_output[key] = value

    # now, prune out the variables that are None

    save_json_output(pruned_output, outfile, pretty=pretty)


def cli_get_data(threshold, repo_url=None, doc_src=None):
    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
    ).expanduser()
    if credentials_file.exists():
        with credentials_file.open("r") as fh:
            file_paths = json.load(fh)
    else:
        sys.exit("Error: Please provide a config.json file.")
    header = {}
    if 'Authorization' in file_paths.keys():
        header['Authorization'] = file_paths['Authorization']
    header['accept'] = 'application/vnd.github.v3+json'
    if repo_url is not None:
        assert (doc_src is None)
        try:
            text, github_data = load_repository_metadata(repo_url, header)
        except GithubUrlError:
            return None
    else:
        assert (doc_src is not None)
        if not path.exists(doc_src):
            sys.exit("Error: Document does not exist at given path")
        with open(doc_src, 'r') as doc_fh:
            text = doc_fh.read()
        github_data = {}

    unfiltered_text = text
    header_predictions, string_list = extract_categories_using_header(unfiltered_text)
    text = unmark(text)
    excerpts = create_excerpts(string_list)
    score_dict = run_classifiers(excerpts, file_paths)
    predictions = classify(score_dict, threshold)
    citations = extract_bibtex(text)
    dois = extract_dois(unfiltered_text)
    binder_links = extract_binder_links(unfiltered_text)
    title = extract_title(unfiltered_text)
    predictions = merge(header_predictions, predictions, citations, dois, binder_links, title)
    return format_output(github_data, predictions)


# Function runs all the required components of the cli on a given document file
def run_cli_document(doc_src, threshold, output):
    return run_cli(threshold=threshold, output=output, doc_src=doc_src)


# Function runs all the required components of the cli for a repository
def run_cli(*,
            threshold=0.8,
            repo_url=None,
            doc_src=None,
            in_file=None,
            output=None,
            graph_out=None,
            graph_format="turtle",
            codemeta_out=None,
            pretty=False
            ):
    multiple_repos = in_file is not None
    if multiple_repos:
        with open(in_file, "r") as in_handle:
            # get the line (with the final newline omitted) if the line is not empty
            repo_list = [line[:-1] for line in in_handle if len(line) > 1]

        # convert to a set to ensure uniqueness (we don't want to get the same data multiple times)
        repo_set = set(repo_list)

        repo_data = [cli_get_data(threshold, repo_url=repo_url) for repo_url in repo_set]

    else:
        if repo_url:
            repo_data = cli_get_data(threshold, repo_url=repo_url)
        else:
            repo_data = cli_get_data(threshold, doc_src=doc_src)

    if output is not None:
        save_json_output(repo_data, output, pretty=pretty)

    if graph_out is not None:
        print("Generating Knowledge Graph")
        data_graph = DataGraph()
        if multiple_repos:
            for repo in repo_data:
                data_graph.add_somef_data(repo)
        else:
            data_graph.add_somef_data(repo_data)

        print("Saving Knowledge Graph ttl data to", graph_out)
        with open(graph_out, "wb") as out_file:
            out_file.write(data_graph.g.serialize(format=graph_format))

    if codemeta_out is not None:
        save_codemeta_output(repo_data, codemeta_out, pretty=pretty)
