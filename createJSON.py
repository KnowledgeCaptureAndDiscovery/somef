# creatJSON.py
# parameters:
## input file: either: url to github repository OR markdown documentation file path
## output file: json with each paragraph marked with all four classification scores

import argparse
import json
import base64
from urllib.parse import urlparse
import sys
import os
from os import path
import requests
from markdown import Markdown
from bs4 import BeautifulSoup
from io import StringIO
import pickle
import pprint
import pandas as pd
import numpy as np

with open('config.json') as fh:
    header = json.load(fh)
header['accept'] = 'application/vnd.github.v3+json'

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

def load_repository_information(repository_url):
    ## load general response of the repository
    url = urlparse(argv.repo_url)
    if url.netloc != 'github.com':
        sys.exit("Error: repository must come from github")
    _, owner, repo_name = url.path.split('/')
    general_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=header).json() 

    if 'message' in general_resp.keys() and general_resp['message']=="Not Found":
        sys.exit("Error: repository name is incorrect")

    ## Remove extraneous data
    keep_keys = ('description', 'name', 'owner', 'license', 'languages_url', 'forks_url')
    filtered_resp = {k: general_resp[k] for k in keep_keys}

    ## Condense owner information
    if filtered_resp['owner'] and 'login' in filtered_resp['owner'].keys():
        filtered_resp['owner'] = filtered_resp['owner']['login']
    
    ## condense license information
    license_info = {}
    for k in ('name', 'url'):
        if filtered_resp['license'] and k in filtered_resp['license'].keys():
            license_info[k] = filtered_resp['license'][k]
    filtered_resp['license'] = license_info
    
    # get keywords / topics
    topics_headers = {}
    topics_headers.update(header)
    topics_headers = {'accept': 'application/vnd.github.mercy-preview+json'}
    topics_resp = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/topics', headers=topics_headers).json()
    if topics_resp and 'names' in topics_resp.keys():
        filtered_resp['topics'] = topics_resp['names']

    ## get languages
    filtered_resp['languages'] = list(requests.get(filtered_resp['languages_url']).json().keys())
    del filtered_resp['languages_url']

    ## get default README
    readme_info = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/readme', headers=topics_headers).json()
    readme = base64.b64decode(readme_info['content']).decode("utf-8")
    text = unmark(readme)
    filtered_resp['readme_url'] = readme_info['html_url']

    ## get releases
    releases_list = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/releases', headers=header).json()
    releases_list = map(lambda release : {'tag_name': release['tag_name'], 'name': release['name'], 'author_name': release['author']['login'], 'body': release['body'], 'tarball_url': release['tarball_url'], 'zipball_url': release['zipball_url'], 'html_url':release['html_url'], 'url':release['url']}, releases_list)
    filtered_resp['releases'] = list(releases_list)

    return text, filtered_resp

def run_classifiers(path_to_models, text):
    score_dict={}
    if(not path.exists(path_to_models)):
        sys.exit("Error: File/Directory does not exist")
    if(path.isfile(path_to_models)):
        classifier = pickle.load(open(path_to_models, 'rb'))
        classifier_name = os.path.basename(argv.model_src)
        excerpts = text.splitlines()
        excerpts = [i for i in excerpts if i]
        scores = classifier.predict_proba(excerpts)
        score_dict={'excerpt': excerpts, classifier_name: scores[:,1]}
    else :
        for file in os.listdir(argv.model_src):
            classifier = pickle.load(open(argv.model_src+'/'+file, 'rb'))
            classifier_name = os.path.basename(file)
            excerpts = text.splitlines()
            excerpts = [i for i in excerpts if i]
            scores = classifier.predict_proba(excerpts)
            if 'excerpt' not in score_dict.keys():
                score_dict={'excerpt': excerpts, classifier_name: scores[:,1]}
            else :
                score_dict[classifier_name]=scores[:,1]
    return score_dict 

def classify_into_one(scores, threshold):
    results = pd.DataFrame(scores)
    col = results[results.columns[1:]].idxmax(axis=1)
    maxval = results[results.columns[1:]].max(axis=1)
    pred = np.column_stack((results['excerpt'],col,maxval))
    pred = pred[pred[:,2] >= threshold]
    predictions = {'description.sk':[],'invocation.sk':[],'installation.sk':[],'citation.sk':[]}
    curr=""
    excerpt=""
    for ele in range(len(pred)):
        if curr=="":
            excerpt=excerpt+pred[ele][0]+' \n'
            curr = pred[ele][1]
        elif curr==pred[ele][1]:
            excerpt=excerpt+pred[ele][0]+' \n'
        else :
            predictions[pred[ele][1]].append(excerpt)
            excerpt = pred[ele][0]+' \n'
            curr = pred[ele][1]
    return predictions

def synthRepoData(git_data, repo_data, outfile):   
    
    for i in git_data.keys():
        if(i == 'description'):
            repo_data['description.sk'].append(git_data[i])
        else:
            repo_data[i] = git_data[i]

    with open(outfile, 'w') as output:
        json.dump(repo_data, output)  


argparser = argparse.ArgumentParser(description="Fetch Github README, split paragraphs, and run classifiers.")
src = argparser.add_mutually_exclusive_group(required=True)
src.add_argument('--repo_url', help="URL of the Github repository")
src.add_argument('--doc_src', help='path to documentation file')
argparser.add_argument('-m', '--model_src', help='path to pickled model', required=True)
argparser.add_argument('--output', '-o', help="path for output json", required=True)
argparser.add_argument('--threshold', '-t', help="threshold score", type=restricted_float, default=0.5)
argv = argparser.parse_args()

if (argv.repo_url):
    text, github_data = load_repository_information(argv.repo_url)
elif (argv.doc_src):
    # Documentation from already downloaded Markdown file.
    with open(argv.doc_src, 'r') as doc_fh:
        text = unmark(doc_fh.read())

score_dict = run_classifiers(argv.model_src, text)

predictions = classify_into_one(score_dict, argv.threshold)

synthRepoData(github_data, predictions, argv.output)
