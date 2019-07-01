#!/usr/bin/python3
#fetchmetadata.py
# This module takes a URL to a github and collects the following data:
# repo name, small description, keywords
import sys
import argparse
from urllib.parse import urlparse
import requests
import json

argparser = argparse.ArgumentParser(description="Fetch Github repository metadata.")
argparser.add_argument("repo_url", help="URL of the Github repository")
argv = argparser.parse_args()

#url = urlparse(argv.repo_url).path.split('/')
url = urlparse(argv.repo_url)
if url.netloc != 'github.com':
    sys.exit("Error: repository must come from github")
_, owner, repo_name = url.path.split('/')
print("Owner: {} Repo name: {}".format(owner, repo_name))
general_resp = requests.get("https://api.github.com/repos/" + owner + "/" + repo_name).json()
#print(general_resp)
keep_keys = ('description', 'name', 'owner', 'license', 'language', 'languages_url', 'releases_url')
filtered_resp = {k: general_resp[k] for k in keep_keys}
filtered_resp['owner'] = filtered_resp['owner']['login']
topics_headers = {
    'Accept': 'application/vnd.github.mercy-preview+json',
}
topics_resp = requests.get('https://api.github.com/repos/' + owner + "/" + repo_name + '/topics', headers=topics_headers).json()
filtered_resp['topics'] = topics_resp['names']
resp_json = json.dumps(filtered_resp)
print(resp_json)
