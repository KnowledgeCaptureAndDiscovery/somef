## Script to update the header evaluation.
import pandas as pd
from somef.header_analysis import label_header
output_header ="../../../experiments/header_analysis/header_evaluation/header_evaluation_new_header_only.csv"
output_all ="../../../experiments/header_analysis/header_evaluation/header_evaluation_new_header_content.csv"

eval_data_header = pd.read_csv(output_header)
# remove long_title and ack. long_title is a regular expression and ack is not yet supported
for index,row in eval_data_header.iterrows():
    print(label_header(row["Header"]))
    #print(index, row)