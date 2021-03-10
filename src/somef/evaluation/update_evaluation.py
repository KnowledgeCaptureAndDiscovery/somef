## Script to update the header evaluation.
## The goal of this script is to re-run the evaluation after doing improvements to SOMEF header analysis

import pandas as pd
import os
from somef.header_analysis import label_header
from datetime import datetime
import csv

output_dir = "../../../experiments/header_analysis/header_evaluation/"
output_header = os.path.join(output_dir, "header_evaluation_new_header_only_annotated.csv")
# output_all = os.path.join(output_dir,"header_evaluation_new_header_content_annotated.csv")

eval_data_header = pd.read_csv(output_header)

# Create predictions for all entries in file
predictions = []
print("Creating predictions for headers in " + output_header)
for index, row in eval_data_header.iterrows():
    header = row["Header"]
    # print(header,label_header(header))
    ps = label_header(header)
    result_to_attach = ""
    for p in ps:
        result_to_attach += p + ";"
    # remove the last ;
    result_to_attach = result_to_attach[:-1]
    predictions.append(result_to_attach.replace("installation", "install").replace("requirement", "requirements")
                       .replace("acknowledgement", "ack"))

eval_data_header.insert(3, "Prediction", predictions, True)

# Save results
eval_data_header.to_csv(
    os.path.join(output_dir, "header_evaluation_predicted_" + datetime.today().strftime('%Y-%m-%d') + ".csv"))

# Save summary
output_summary = os.path.join(output_dir, "header_evaluation_summary_" + datetime.today().strftime('%Y-%m-%d') + ".csv")

summary = {
    "citation": {
        "correct": 0,  # predicted correctly
        "incorrect": 0,  # predicted with an incorrect label
        "miss": 0  # a prediction is not created, but there was one
    },
    "run": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "install": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "download": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "requirements": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "contact": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "description": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "contributor": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "documentation": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "license": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "usage": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "faq": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "support": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    },
    "ack": {
        "correct": 0,
        "incorrect": 0,
        "miss": 0
    }
}

for index, row in eval_data_header.iterrows():
    label_list = str(row["Label"]).split(";")
    if 'nan' in label_list or label_list == ['']:
        label_list = []
    prediction_list = str(row["Prediction"]).split(";")
    if 'nan' in prediction_list or prediction_list == ['']:
        prediction_list = []

    # print(summary["install"]["correct"])
    # print(label_list,prediction_list)

    if label_list:  # label is not empty
        for label in label_list:
            if label != '' and label in summary:  # only look at the desired categories
                if not prediction_list:  # if prediction is empty, miss
                    summary[label]["miss"] = summary[label]["miss"] + 1
                elif label in prediction_list:
                    summary[label]["correct"] = summary[label]["correct"] + 1
        # If there are predictions not in label, then error
        if prediction_list:
            for p in prediction_list:
                if p not in label_list:  # if p in label, it has already been annotated
                    summary[p]["incorrect"] += 1

    else:  # label is empty: There is not annotation: error.
        if prediction_list:
            for p in prediction_list:
                summary[p]["incorrect"] += 1

# Save summary in CSV
print(summary)
print(output_summary)
with open(output_summary, "w") as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["category", "total correct", "total incorrect", "total missed", "precision", "recall"])

    for key in summary:
        writer.writerow([key, f"{summary[key]['correct']}", f"{summary[key]['incorrect']}",
                         summary[key]['miss'],
                         f"{float(summary[key]['correct']) / float(summary[key]['correct'] + summary[key]['incorrect']):.3f}",
                         f"{float(summary[key]['correct']) / float(summary[key]['correct'] + summary[key]['miss']):.3f}"])
