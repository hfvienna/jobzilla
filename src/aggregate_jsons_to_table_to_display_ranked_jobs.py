#    Jobzilla automates job search using a LLM.
#    Copyright (C) 2023  hfvienna, author of Jobzilla

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

data = load_job_data("../data/jobs/fits_merged_json")  # Load job data

# Convert "fit_applicant" and "fit_recruiter" to numeric, coerce errors (invalid values) to NaN, then fill with 0
data['fit_applicant'] = pd.to_numeric(data['fit_applicant'], errors='coerce').fillna(0)
data['fit_recruiter'] = pd.to_numeric(data['fit_recruiter'], errors='coerce').fillna(0)

# Calculate total fit as the sum of applicant and recruiter fits
data['fit_total'] = data['fit_applicant'] + data['fit_recruiter']

# Drop the 'email' column
if 'email' in data.columns:
    data = data.drop(columns=['email'])

print(data)  # Print the DataFrame

df_sorted = data.sort_values("fit_total", ascending=False)  # Sort by total fit

# Convert the DataFrame to a list of dictionaries and save to JSON
with open("../app/job_table.json", "w") as f:
    json.dump(df_sorted.to_dict(orient="records"), f, indent=4)
