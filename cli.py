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
import requests
from markdown import Markdown
from bs4 import BeautifulSoup
from io import StringIO
import pickle
import pprint
import pandas as pd
import numpy as np
import re

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

categories = ['description','citation','installation','invocation']
keep_keys = ('description', 'name', 'owner', 'license', 'languages_url', 'forks_url')


## Function uses the repository_url provided to load required information from github.
## Information kept from the repository is written in keep_keys.
## Returns the readme text and required metadata
def load_repository_metadata(repository_url):
    print("Loading Repository Information....")
    ## load general response of the repository
    url = urlparse(repository_url)
    if url.netloc != 'github.com':
        sys.exit("Error: repository must come from github")
    _, owner, repo_name = url.path.split('/')
    general_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=header).json() 

    if 'message' in general_resp.keys() and general_resp['message']=="Not Found":
        sys.exit("Error: repository name is incorrect")

    ## Remove extraneous data
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
    
    print("Repository Information Successfully Loaded.")
    return text, filtered_resp

## Function takes readme text as input and divides it into excerpts
## Returns the extracted excerpts
def create_excerpts(text):
    divisions = text.splitlines()
    divisions = [i for i in divisions if i]
    return divisions

## Function takes readme text as input and runs the provided classifiers on it
## Returns the dictionary containing scores for each excerpt.
def run_classifiers(text):
    score_dict={}
    for category in categories:
        excerpts = create_excerpts(text)
        file_name = file_paths[category]
        if file_name=="":
            print('I am here')
            continue
        if not path.exists(file_name):
            sys.exit("Error: File/Directory does not exist")
        print("Classifying excerpts for the catgory",category)
        classifier = pickle.load(open(file_name, 'rb'))
        scores = classifier.predict_proba(excerpts)
        score_dict[category]={'excerpt': excerpts, 'confidence': scores[:,1]}
        print("Excerpt Classification Successful for the Category",category)   
    return score_dict 

## Function takes scores dictionary and a threshold as input 
## Returns predictions containing excerpts with a confidence above the given threshold.
def classify(scores, threshold):
    print("Checking Thresholds for Excerpt Classification.")
    predictions = {}
    for ele in scores.keys():
        print("Running for",ele)
        flag = False
        predictions[ele] = []
        excerpt=""
        confid=[]
        for i in range(len(scores[ele]['confidence'])):
            if scores[ele]['confidence'][i]>=threshold:
                if flag==False:
                    excerpt=excerpt+scores[ele]['excerpt'][i]+' \n'
                    confid.append(scores[ele]['confidence'][i])
                    flag=True
                else:
                    excerpt=excerpt+scores[ele]['excerpt'][i]+' \n'
                    confid.append(scores[ele]['confidence'][i])
            else :
                if flag==True:
                    element = {'excerpt':excerpt,'confidence':confid}
                    predictions[ele].append(element)
                    excerpt=""
                    confid=[]
                    flag=False
        print("Run completed.")
    print("All Excerpts below the given Threshold Removed.")
    return predictions

## Function takes readme text as input and runs a regex parser on it
## Returns a list of bibtex citations
def extract_bibtex(readme_text):
    print("Extracting bibtex citation from readme")
    regex = r'\@[a-zA-z]+\{[.\n\S\s]+?[author|title][.\n\S\s]+?[author|title][.\n\S\s]+?\n\}'
    excerpts = readme_text
    citations = re.findall(regex,excerpts)
    print("Extracting bibtex citation from readme completed.")
    print(citations)
    print(len(citations))
    return citations

## Function takes metadata, readme text predictions, bibtex citations and path to the output file
## Performs some combinations and saves the final json Object in the file
def save_json(git_data, repo_data, citations, outfile):   
    
    for i in git_data.keys():
        if i == 'description':
            if 'description' not in repo_data.keys():
                repo_data['description'] = []
            repo_data['description'].append(git_data[i])
        else:
            repo_data[i] = git_data[i]

    for i in range(len(citations)):
        if 'citation' not in repo_data.keys():
            repo_data['citation'] = []
        repo_data['citation'].append({'excerpt': citations[i]})

    print("Saving json data to",outfile)
    with open(outfile, 'w') as output:
        json.dump(repo_data, output)  

header = {}
with open('config.json') as fh:
    file_paths = json.load(fh)
header['Authorization'] = file_paths['Authorization']
header['accept'] = 'application/vnd.github.v3+json'

argparser = argparse.ArgumentParser(description="Fetch Github README, split paragraphs, run classifiers and output json containing repository information, classified excerpts and confidence.")
src = argparser.add_mutually_exclusive_group(required=True)
src.add_argument('-r', '--repo_url', help="URL of the Github repository")
src.add_argument('-d', '--doc_src', help='path to documentation file')
argparser.add_argument('-o', '--output', help="path for output json", required=True)
argparser.add_argument('-t','--threshold', help="threshold score", type=restricted_float, default=0.5)
argv = argparser.parse_args()

github_data = {}
if (argv.repo_url):
    text, github_data = load_repository_metadata(argv.repo_url)
elif (argv.doc_src):
    # Documentation from already downloaded Markdown file.
    with open(argv.doc_src, 'r') as doc_fh:
        text = unmark(doc_fh.read())

score_dict = run_classifiers(text)

predictions = classify(score_dict, argv.threshold)

citations = extract_bibtex(text)

save_json(github_data, predictions, citations, argv.output)
