## Script used to create summary statistics on the interactive header evaluation
in_file = "header_evaluation_tmp.json"

full_out_csv = "header_evalution.csv"
summary_csv = "header_evaluation_summary.csv"

with open(in_file, "r") as in_handle:
    import json
    data = json.load(in_handle)

all_keys = [*{key for value in data.values() for key in value.keys()}]

print(all_keys)

with open(full_out_csv, "w") as out_file:
    import csv
    writer = csv.writer(out_file)

    labels = ["repository"] + [x for key in all_keys for x in (key, f"{key} correct")]
    print(labels)
    writer.writerow(labels)

    for repository, repo_data in data.items():
        line = [repository]

        for key in all_keys:
            if key in repo_data:
                line += [repo_data[key]['excerpt'], 'y' if repo_data[key]['correct'] else 'n']
            else:
                line += ['', '']

        writer.writerow(line)

# compute summary statistics

with open(summary_csv, "w") as out_file:
    writer = csv.writer(out_file)

    writer.writerow(["property", "total correct", "total present", "proportion"])

    for key in all_keys:
        count_positive = 0
        count_total = 0
        for repo_data in data.values():
            if key in repo_data:
                count_total += 1
                if repo_data[key]['correct']:
                    count_positive += 1

        writer.writerow([key, f"{count_positive}", f"{count_total}",
                        f"{float(count_positive)/float(count_total):.3f}"])

