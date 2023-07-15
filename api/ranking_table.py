import json
import os
import pandas as pd

def load_job_data(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as f:
                try:
                    job = json.load(f)  # Load the JSON directly into a Python dictionary
                    data.append(job)
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError in file {filename}: ", e.doc, e.pos)
    return pd.DataFrame(data)  # Convert list of dicts to DataFrame

data = load_job_data("../public/jobs/JSONs_fits")  # Load job data

# Fill missing fit values with 0
data['fit'] = data['fit'].fillna(0)

# Convert "fit" to numeric, coerce errors (invalid values) to NaN, then fill with 0
data['fit'] = pd.to_numeric(data['fit'], errors='coerce').fillna(0)

# Drop the 'email' column
if 'email' in data.columns:
    data = data.drop(columns=['email'])

print(data)  # Print the DataFrame

df_sorted = data.sort_values("fit", ascending=False)  # Sort by fit

# Convert the DataFrame to a list of dictionaries and save to JSON
with open("../app/job_table.json", "w") as f:
    json.dump(df_sorted.to_dict(orient="records"), f, indent=4)
