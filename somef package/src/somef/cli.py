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
from somef import createExcerpts
from somef import header_analysis

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
def load_repository_metadata(repository_url, header):
    print("Loading Repository Information....")
    ## load general response of the repository
    if repository_url[-1]=='/':
        repository_url = repository_url[:-1] 
    url = urlparse(repository_url)
    if url.netloc != 'github.com':
        sys.exit("Error: repository must come from github")
    if len(url.path.split('/')) != 3:
        sys.exit("Github link is not correct. \nThe correct format is https://github.com/owner/repo_name.")
    _, owner, repo_name = url.path.split('/')
    general_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=header).json() 

    if 'message' in general_resp.keys() and general_resp['message']=="Not Found":
        sys.exit("Error: repository name is incorrect")

    if 'message' in general_resp.keys():
        message = general_resp['message']
        sys.exit("Error: "+message)

    ## Remove extraneous data
    filtered_resp = {}
    for k in keep_keys:
        if k not in general_resp.keys():
            sys.exit("Error: key "+k+" not present in github repository")
        filtered_resp[k] = general_resp[k]

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
    topics_headers = header
    topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
    topics_resp = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/topics', headers=topics_headers).json()
    if 'message' in topics_resp.keys():
        sys.exit("Error: "+topics_resp['message'])
    if topics_resp and 'names' in topics_resp.keys():
        filtered_resp['topics'] = topics_resp['names']

    ## get languages
    filtered_resp['languages'] = list(requests.get(filtered_resp['languages_url']).json().keys())
    del filtered_resp['languages_url']

    ## get default README
    readme_info = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/readme', headers=topics_headers).json()
    if 'message' in readme_info.keys():
        sys.exit("Error: "+general_resp['message'])
    readme = base64.b64decode(readme_info['content']).decode("utf-8")
    text = readme
    filtered_resp['readme_url'] = readme_info['html_url']

    ## get releases
    releases_list = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/releases', headers=header).json()
    if isinstance(releases_list,dict) and 'message' in releases_list.keys():
        sys.exit("Error: "+general_resp['message'])        
    releases_list = map(lambda release : {'tag_name': release['tag_name'], 'name': release['name'], 'author_name': release['author']['login'], 'body': release['body'], 'tarball_url': release['tarball_url'], 'zipball_url': release['zipball_url'], 'html_url':release['html_url'], 'url':release['url']}, releases_list)
    filtered_resp['releases'] = list(releases_list)
    
    print("Repository Information Successfully Loaded. \n")
    return text, filtered_resp

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
    score_dict={}
    for category in categories:
        if category not in file_paths.keys():
            sys.exit("Error: Category " + category + " file path not present in config.json")
        file_name = file_paths[category]
        if not path.exists(file_name):
            sys.exit("Error: File/Directory does not exist")
        print("Classifying excerpts for the catgory",category)
        classifier = pickle.load(open(file_name, 'rb'))
        scores = classifier.predict_proba(excerpts)
        score_dict[category]={'excerpt': excerpts, 'confidence': scores[:,1]}
        print("Excerpt Classification Successful for the Category",category)
    print("\n")   
    return score_dict 

## Function removes all excerpt lines which have been classified but contain only one word.
## Returns the excerpt to be entered into the predictions
def remove_unimportant_excerpts(excerpt_element):
    excerpt_info = excerpt_element['excerpt']
    excerpt_confidence = excerpt_element['confidence']
    excerpt_lines = excerpt_info.split('\n')
    final_excerpt = {'excerpt':"",'confidence':[]}
    for i in range(len(excerpt_lines)-1):
        words = excerpt_lines[i].split(' ')
        if len(words)==2:
            continue
        final_excerpt['excerpt'] += excerpt_lines[i]+'\n';
        final_excerpt['confidence'].append(excerpt_confidence[i])
    return final_excerpt

## Function takes scores dictionary and a threshold as input 
## Returns predictions containing excerpts with a confidence above the given threshold.
def classify(scores, threshold):
    print("Checking Thresholds for Classified Excerpts.")
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
                    element = remove_unimportant_excerpts({'excerpt':excerpt,'confidence':confid})
                    if len(element['confidence'])!=0:
                        predictions[ele].append(element)
                    excerpt=""
                    confid=[]
                    flag=False
        print("Run completed.")
    print("All Excerpts below the given Threshold Removed. \n")
    return predictions

## Function adds category information extracted using header information
## Returns json with the information added.
def extract_categories_using_header(repo_data):
    print("Extracting information using headers")
    header_info, string_list = header_analysis.extract_categories_using_headers(repo_data)
    print("Information extracted. \n")
    return header_info, string_list

## Function takes readme text as input and runs a regex parser on it
## Returns a list of bibtex citations
def extract_bibtex(readme_text):
    print("Extracting bibtex citation from readme")
    regex = r'\@[a-zA-z]+\{[.\n\S\s]+?[author|title][.\n\S\s]+?[author|title][.\n\S\s]+?\n\}'
    excerpts = readme_text
    citations = re.findall(regex,excerpts)
    print("Extracting bibtex citation from readme completed. \n")
    return citations

## Function takes the predictions using header information, classifier and bibtek parser
## Returns a combined predictions
def merge(header_predictions, predictions, citations):
    print("Merge prediction using header information, classifier and bibtek parser")
    for i in range(len(citations)):
        if 'citation' not in predictions.keys():
            predictions['citation'] = []
        predictions['citation'].insert(0,{'excerpt': citations[i],'confidence': [1.0]})

    for headers in header_predictions:
        if headers not in predictions.keys():
            predictions[headers] = header_predictions[headers]
        else :
            for h in header_predictions[headers]:
                predictions[headers].insert(0,h)
    print("Merging successful. \n")
    return predictions

## Function takes metadata, readme text predictions, bibtex citations and path to the output file
## Performs some combinations and saves the final json Object in the file
def save_json(git_data, repo_data, outfile):   
    
    for i in git_data.keys():
        if i == 'description':
            if 'description' not in repo_data.keys():
                repo_data['description'] = []
            repo_data['description'].append({'excerpt': git_data[i],'confidence': [1.0]})
        else:
            repo_data[i] = {'excerpt': git_data[i],'confidence': [1.0]}

    print("Saving json data to",outfile)
    with open(outfile, 'w') as output:
        json.dump(repo_data, output)  


## Function runs all the required components of the cli for a repository
def run_cli(repo_url, threshold, output):
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
    text, github_data = load_repository_metadata(repo_url, header)
    unfiltered_text = text
    header_predictions, string_list = extract_categories_using_header(unfiltered_text)
    text = unmark(text)
    excerpts = create_excerpts(string_list)
    score_dict = run_classifiers(excerpts, file_paths)
    predictions = classify(score_dict, threshold)
    citations = extract_bibtex(text)
    predictions = merge(header_predictions, predictions, citations)
    save_json(github_data, predictions, output)

## Function runs all the required components of the cli on a given document file
def run_cli_document(doc_src, threshold, output):
    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
    ).expanduser()
    if credentials_file.exists():
        with credentials_file.open("r") as fh:
            file_paths = json.load(fh)
    else:
        sys.exit("Error: Please provide a config.json file.")
    if 'Authorization' in file_paths.keys():
        header['Authorization'] = file_paths['Authorization']
    header['accept'] = 'application/vnd.github.v3+json'
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
    predictions = merge(header_predictions, predictions, citations)
    save_json(github_data, predictions, output)

if __name__=='__main__':
    argparser = argparse.ArgumentParser(description="Fetch Github README, split paragraphs, run classifiers and output json containing repository information, classified excerpts and confidence.")
    src = argparser.add_mutually_exclusive_group(required=True)
    src.add_argument('-r', '--repo_url', help="URL of the Github repository")
    src.add_argument('-d', '--doc_src', help='path to documentation file')
    argparser.add_argument('-o', '--output', help="path for output json", required=True)
    argparser.add_argument('-t','--threshold', help="threshold score", type=restricted_float, default=0.5)
    argv = argparser.parse_args()
    if argv.repo_url:
        run_cli(argv.repo_url, argv.threshold, argv.output)
    elif argv.doc_src:
        run_cli_document(argv.doc_src, argv.threshold, argv.output)
    else :
        sys.exit("Either repository url or document path should be provided.")
