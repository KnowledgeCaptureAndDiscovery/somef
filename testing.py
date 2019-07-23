# testing.py
# parameters:
## input file: either: url to github repository OR markdown documentation file path
## output file: json with each paragraph marked with all four classification scores

import argparse
import json
import base64
from urllib.parse import urlparse
import sys
import requests
from markdown import markdown
from bs4 import BeautifulSoup

with open('config.json') as fh:
    header = json.load(fh)
header['accept'] = 'application/vnd.github.v3+json'

argparser = argparse.ArgumentParser(description="Fetch Github README, split paragraphs, and run classifiers.")
src = argparser.add_mutually_exclusive_group(required=True)
src.add_argument('--repo_url', help="URL of the Github repository")
src.add_argument('--doc_src', help='path to documentation file')
argparser.add_argument('-m', '--model_src', help='path to pickled model', required=True)
argparser.add_argument('--output', '-o', help="path for output json")
argv = argparser.parse_args()

if (argv.repo_url):
    # repository url given
    url = urlparse(argv.repo_url)
    if url.netloc != 'github.com':
        sys.exit("Error: repository must come from github")
    _, owner, repo_name = url.path.split('/')
    general_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/readme", headers=header).json()
    readme = base64.b64decode(general_resp['content'])
    html = markdown(readme)
    text = ''.join(BeautifulSoup(html, features="html.parser").findAll(text=True))
elif (argv.doc_src):
    # Documentation from already downloaded Markdown file.
    text = ''.join(BeautifulSoup(open(argv.doc_src), features="html.parser").findAll(text=True))
else:
    # undefined behavior
    print("ERROR")
print(text)