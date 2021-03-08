## This script extracts headers which
input_dir = "../../../experiments/training_corpus/repos"

import os
from somef.header_analysis import extract_header_content,extract_categories_using_headers

for filename in os.listdir(input_dir):
    print("Analyzing " + filename)
    with open(os.path.join(input_dir, filename), "r") as data_file:
        file_text = data_file.read()
        print(extract_header_content(file_text))