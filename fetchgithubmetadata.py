#!/usr/bin/python3
#fetchmetadata.py
# This module takes a URL to a github and collects the following data:
# repo name, small description, keywords
import sys
import argparse
from urllib.parse import urlparse
import requests
import json
import pprint

auth2token_header = {}
with open('config.json') as fh:
    auth2token_header = json.load(fh)
## Parse command line arguments
argparser = argparse.ArgumentParser(description="Fetch Github repository metadata.")
argparser.add_argument("repo_url", help="URL of the Github repository")
argparser.add_argument("-o", "--output", help="output file")
argv = argparser.parse_args()

pp = pprint.PrettyPrinter()
## Parse input URL
url = urlparse(argv.repo_url)
if url.netloc != 'github.com':
    sys.exit("Error: repository must come from github")
_, owner, repo_name = url.path.split('/')
print("Owner: {} Repo name: {}".format(owner, repo_name))
general_resp = requests.get("https://api.github.com/repos/" + owner + "/" + repo_name, headers=auth2token_header).json()

#pp.pprint(general_resp)
## Remove extraneous data
keep_keys = ('description', 'name', 'owner', 'license', 'languages_url')
filtered_resp = {k: general_resp[k] for k in keep_keys}

## Condense owner information
filtered_resp['owner'] = filtered_resp['owner']['login']
# condense license information
filtered_resp['license'] = {k: filtered_resp['license'][k] for k in ('name', 'url')}
# get keywords / topics
topics_headers = {
    'Accept': 'application/vnd.github.mercy-preview+json'
}
topics_headers.update(auth2token_header)
topics_resp = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/topics', headers=topics_headers).json()
filtered_resp['topics'] = topics_resp['names']

## get languages
filtered_resp['languages'] = list(requests.get(filtered_resp['languages_url']).json().keys())
del filtered_resp['languages_url']

## get default README
filtered_resp['readme_url'] = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/readme', headers=topics_headers).json()['html_url']


## get releases
releases_list = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/releases', headers=auth2token_header).json()
#pp.pprint(releases_list)
releases_list = map(lambda release : {'tag_name': release['tag_name'], 'name': release['name'], 'author_name': release['author']['login'], 'body': release['body'], 'tarball_url': release['tarball_url'], 'zipball_url': release['zipball_url'], 'html_url':release['html_url'], 'url':release['url']}, releases_list)
#pp.pprint(list(releases_list))
filtered_resp['releases'] = list(releases_list)
## pretty output to STDOUT

pp.pprint(filtered_resp)

if argv.output:
    with open(argv.output, 'w') as outfile:
        json.dump(filtered_resp, outfile)
