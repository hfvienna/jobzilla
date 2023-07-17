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
        "email" : {"type" : "string"},
    },
}

def count_files(directory):
    num_files = 0
    num_valid_json = 0
    num_valid_schema = 0
    invalid_json_files = []
    invalid_schema_files = []
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
                        # If the 'fit_detailed' key contains "", print the JSON
                        if directory == "../public/jobs/JSONs_fits" and '""' in data.get('fit_detailed', ''):
                            print(f"JSON from file {f} with '\"\"' in 'fit_detailed': {data}")
                    except json.JSONDecodeError:
                        print(f"Invalid JSON file: {f}")
                        invalid_json_files.append(f)
                    except jsonschema.exceptions.ValidationError as ve:
                        print(f"JSON file does not match schema: {f}, {ve}")
                        invalid_schema_files.append(f)

    return num_files, num_valid_json, num_valid_schema, invalid_json_files, invalid_schema_files

directories = [
    "../public/jobs/pdfs",
    "../public/jobs/txts",
    "../public/jobs/JSONs_facts",
    "../public/jobs/JSONs_fits",
]

for directory in directories:
    num_files, num_valid_json, num_valid_schema, invalid_json_files, invalid_schema_files = count_files(directory)
    print(f"There are {num_files} files in {directory}")
    print(f"There are {num_valid_json} valid JSON files in {directory}")
    print(f"There are {num_valid_schema} valid JSON files that match the schema in {directory}")
    print(f"Invalid JSON files: {invalid_json_files}")
    print(f"JSON files that do not match the schema: {invalid_schema_files}")
