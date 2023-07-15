import ast
import json
import os

import pandas as pd


def load_job_data(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as f:
                job_str = f.read().strip(
                    '"'
                )  # Read the file as a string and remove leading/trailing quotes
                job_str = ast.literal_eval(f'"{job_str}"')  # Unescape the JSON string
                try:
                    job = json.loads(job_str)  # Parse the JSON string
                except json.JSONDecodeError as e:
                    print("JSONDecodeError: ", e.doc, e.pos)
                data.append(job)
    return pd.DataFrame(data)  # Convert list of dicts to DataFrame


data = load_job_data("../public/jobs/JSONs")  # Load job data

print(data)  # Print the DataFrame

df_sorted = data.sort_values("fit", ascending=False)  # Sort by fit
df_sorted.to_json("../app/job_table.json", orient="records")  # Save DataFrame to JSON
