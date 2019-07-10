#!/usr/bin/python3
# minegithubrepodescriptions.py

import os
import sys
import requests
import json
import traceback
import csv
from printprogressbar import printProgressBar

output_corpus = 'data/repos_summary.csv'

## read auth key
auth2token_header = {}
with open('config.json') as configfh:
    auth2token_header = json.load(configfh)
    configfh.close()

try:
    f = open(output_corpus, 'r+')
    f.seek(0, os.SEEK_END)     # seek to end of file
    while f.read(1) != "\n":   # Until EOL is found...
        f.seek(f.tell() - 2, os.SEEK_SET) # ...jump back the read byte plus one more.
        #f.seek(-2, 1)
    last = f.readline()         # Read last line.
    id, _ = [x.strip('\"') for x in last.split(',')]
    id = int(id)
    f.seek(0, os.SEEK_END)
except (FileNotFoundError, ValueError):
    # FileNotFoundError: file does not exist yet
    # ValueError: no downloaded entries yet
    # restart from scratch: create or overwrite existing file
    traceback.print_exc()
    print("Creating file...")
    f = open(output_corpus, 'w')
    csv_writer = csv.writer(f, dialect='unix')
    csv_writer.writerow(['id', 'description'])
    id = 0
else:
    csv_writer = csv.writer(f, dialect='unix')
requests_remaining = 1
while requests_remaining > 0:
#    print(id)
    reporequest = requests.get("https://api.github.com/repositories", params={'since':id}, headers=auth2token_header)
#    print(reporequest.request)
    requests_remaining = int(reporequest.headers['X-RateLimit-Remaining'])
    total_requests = int(reporequest.headers['X-RateLimit-Limit'])
    #print(reporequest.json())
    for repo in reporequest.json():
        repo_id = repo['id']
        repo_description = repo['description']
        print("ID: {}, Description: {}".format(repo_id, repo_description))
        if (repo_description):
            csv_writer.writerow([repo_id, repo_description])
        printProgressBar(total_requests-requests_remaining, total_requests, prefix = '% of used requests', suffix = 'done')
    id = repo_id
