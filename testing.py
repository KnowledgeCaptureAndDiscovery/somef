# testing.py
# parameters:
## input file: either: url to github repository OR markdown documentation file path
## output file: json with each paragraph marked with all four classification scores

import argparse

auth2token_header = {}
with open('config.json') as fh:
    auth2token_header = json.load(fh)

