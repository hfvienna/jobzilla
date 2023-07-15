import os
import json

def count_files(directory):
    num_files = 0
    num_valid_json = 0
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            num_files += 1
            if f.endswith('.json'):
                with open(os.path.join(directory, f)) as json_file:
                    try:
                        json.load(json_file)
                        num_valid_json += 1
                    except json.JSONDecodeError:
                        print(f"Invalid JSON file: {f}")
    return num_files, num_valid_json

directories = [
    "../public/jobs/pdfs",
    "../public/jobs/txts",
    "../public/jobs/JSONs_facts",
    "../public/jobs/JSONs_fits",
]

for directory in directories:
    num_files, num_valid_json = count_files(directory)
    print(f"There are {num_files} files in {directory}")
    print(f"There are {num_valid_json} valid JSON files in {directory}")
