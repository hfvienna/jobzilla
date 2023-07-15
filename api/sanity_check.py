import os
import json
import jsonschema
from jsonschema import validate

# Define the JSON schema you expect
schema = {
    "type" : "object",
    "properties" : {
        "company" : {"type" : "string"},
        "title" : {"type" : "string"},
        "fit" : {"type" : ["integer", "null"]},
        "fit_detailed" : {"type" : "string"},
        "dateAdded" : {"type" : "string"},
        "salaryRange" : {"type" : "string"},
        "location" : {"type" : "string"},
    },
}

def count_files(directory):
    num_files = 0
    num_valid_json = 0
    num_valid_schema = 0
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            num_files += 1
            if f.endswith('.json'):
                with open(os.path.join(directory, f)) as json_file:
                    try:
                        data = json.load(json_file)
                        num_valid_json += 1
                        # Validate the loaded JSON against the schema
                        validate(instance=data, schema=schema)
                        num_valid_schema += 1
                    except json.JSONDecodeError:
                        print(f"Invalid JSON file: {f}")
                    except jsonschema.exceptions.ValidationError as ve:
                        print(f"JSON file does not match schema: {f}, {ve}")

    return num_files, num_valid_json, num_valid_schema

directories = [
    "../public/jobs/pdfs",
    "../public/jobs/txts",
    "../public/jobs/JSONs_facts",
    "../public/jobs/JSONs_fits",
]

for directory in directories:
    num_files, num_valid_json, num_valid_schema = count_files(directory)
    print(f"There are {num_files} files in {directory}")
    print(f"There are {num_valid_json} valid JSON files in {directory}")
    print(f"There are {num_valid_schema} valid JSON files that match the schema in {directory}")
