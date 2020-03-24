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

## Function takes readme text as input and divides it into excerpts
## Returns the extracted excerpts
def split_into_excerpts(text):
    divisions = text.splitlines()
    divisions = [i for i in divisions if i]
    return divisions