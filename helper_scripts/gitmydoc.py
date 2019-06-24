#!/usr/bin/python3
# gitmydoc.py
# gitmydoc.py (git [get] my documentation)
import os
import glob
from urllib.parse import urlparse
import pandas as pd
import requests

src_path = '/home/allen/Documents/ISI2019/SM2KG/data/'
dest_path = '/home/allen/Documents/ISI2019/SM2KG/data/repos/'
# Get list of all files in destination directory
collected_READMEs = glob.glob(dest_path + '*.md')
collected_READMEs = list(map(lambda fpath : os.path.split(fpath)[1], collected_READMEs))
#print(collected_READMEs)
# slurp *.csv from source directory
csv_files = glob.glob(src_path + '*.csv')
#print(csv_files)
# get URLs from *.csv and remove duplicate URLs
urls = set()
for csv in csv_files:
    df = pd.read_csv(csv)
    urls = urls|set(df.URL)
# URL processing
for url in urls:
    o = urlparse(url)
    split_path = o.path.split('/')
    owner = ""
    repo = ""
    if len(split_path) == 3: #get default README
        owner = split_path[1]
        repo = split_path[2]
        if repo+"-README.md" in collected_READMEs:
            print("{} by {} already downloaded".format(repo, owner))
            continue
        else:
            request = "https://api.github.com/repos/" + owner + "/" + repo + "/readme"
            print("request: {}".format(request))
            resp = requests.get(request).json()
            download_url=resp['download_url']
            print(download_url)
            readme = requests.get(download_url)

            fh = open(dest_path + repo+"-README.md", 'w')
            fh.write(readme.text)
            fh.close()

# - get default README
# - get specific documentation file
# - get Github Wiki file
# If proposed filename is in list of files in destination directory, continue.
# Else, send request and download to destination directory
