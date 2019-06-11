#!/usr/bin/python3
# githubrepo2readme.py
# Takes a github repo url from stdin and downloads the README.md of the repo. Assumes url is valid.

import sys
import re
import requests

for line in sys.stdin:
    url = line.strip()
    regex=re.compile('((git@|http(s)?:\/\/)([\w\.@]+)(\/|:))([\w,\-,\_]+)\/([\w,\-,\_]+)(.git){0,1}((\/){0,1})')
    owner = regex.findall(url)[0][5]
    repo = regex.findall(url)[0][6]
#    print("Owner: {}, repo name: {}".format(owner, repo))
    request = "https://api.github.com/repos/" + owner + "/" + repo + "/readme"
    print("request: {}".format(request))
    resp = requests.get(request).json()
    download_url=resp['download_url']
    print(download_url)
    readme = requests.get(download_url)

    fh = open(repo+"-README.md", 'w')
    fh.write(readme.text)
    fh.close()

