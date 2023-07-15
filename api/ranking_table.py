import ast
import json
import os

import pandas as pd


def load_job_data(directory):
    data = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".json"):
            with open(file_path, "r") as f:
                job_str = f.read().strip('"')  # Read the file as a string and remove leading/trailing quotes
                job_str = ast.literal_eval(f'"{job_str}"')  # Unescape the JSON string
                try:
                    job = json.loads(job_str)  # Parse the JSON string
                    data.append(job)
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError in file {filename}: ", e.doc, e.pos)
#                    os.remove(file_path)  # Delete the problematic file
                    print(f"Deleted file {filename} due to JSONDecodeError")
    return pd.DataFrame(data)  # Convert list of dicts to DataFrame



data = load_job_data("../public/jobs/JSONs_fits")  # Load job data

# Fill missing fit values with 0
data['fit'] = data['fit'].fillna(0)

# Convert "fit" to numeric, coerce errors (invalid values) to NaN, then fill with 0
data['fit'] = pd.to_numeric(data['fit'], errors='coerce').fillna(0)

print(data)  # Print the DataFrame

df_sorted = data.sort_values("fit", ascending=False)  # Sort by fit
df_sorted.to_json("../app/job_table.json", orient="records")  # Save DataFrame to JSON