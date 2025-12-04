## This script extracts headers which will be used in the evaluation.
## This script does not annotate anything. The annotation has to be performed by hand.
input_dir = "../../../experiments/training_corpus/repos"
output ="../../../experiments/header_analysis/header_evaluation/header_evaluation_new.csv"

import os
import pandas as pd
from .header_analysis import extract_header_content

df_all = pd.DataFrame ({}, columns = ['Repo','Header','Content'])
print(df_all)
for filename in os.listdir(input_dir):
    print("Analyzing " + filename)
    with open(os.path.join(input_dir, filename), "r") as data_file:
        file_text = data_file.read()
        df_result = extract_header_content(file_text)
        df_result.insert(0,"Repo",filename)
        df_all = df_all.append(df_result)
        #print(df_result)
df_all.to_csv(output)
