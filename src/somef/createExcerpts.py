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

## Function takes readme text as input and divides it into excerpts
## Returns the extracted excerpts
def split_into_excerpts(string_list):
	divisions = []
	for text in string_list:
		if text:
			divisions = divisions + unmark(text).splitlines()
	divisions = [i for i in divisions if i]
	return divisions