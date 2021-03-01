tmp_json = "header_evaluation_tmp.json"

input_dir = "../../experiments/training_corpus/repos"

import os

all_data = {}

print("INSTRUCTIONS:")
print("You will be asked whether an excerpt matches a given value")
print("To say it does, enter 'y' or just press enter. To say it does not, enter 'n'")

for filename in os.listdir(input_dir):
    from somef.cli import cli_get_data
    cli_data = cli_get_data(1.0, doc_src=os.path.join(input_dir, filename))

    def get_yes_or_no():
        while True:
            y_or_n = input("yes or no: ")
            if len(y_or_n) == 0 or y_or_n == "y":
                return True
            elif y_or_n == "n":
                return False

    def evaluate_data(data):

        out_data = {}
        for key, value_array in data.items():
            print(key)

            if isinstance(value_array, list) and len(value_array) > 0:
                print(value_array)
                value = value_array[0]
                if value['technique'] == 'Header extraction':
                    print(f"\n========== is this {key}? ==========\n")
                    print(value['excerpt'])
                    print("\n=======================================")
                    y_or_n = get_yes_or_no()
                    out_data[key] = {
                        "excerpt": value['excerpt'],
                        "correct": y_or_n
                    }

        return out_data

    should_continue = True
    while should_continue:
        all_data[filename] = evaluate_data(cli_data)
        print("Summary:")
        for key, value in all_data[filename].items():
            print(f"{key}: {value['correct']}")
        print("Did you make any mistakes? (entering yes will re-run this repo)")
        should_continue = get_yes_or_no()

    with open(tmp_json, "w") as tmp_save:
        import json
        json.dump(all_data, tmp_save)
        print("saved")