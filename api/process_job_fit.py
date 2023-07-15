# api/process_jobs.py

import json
import os

from claude import llm

SYSTEM_MESSAGE = """
You are an expert job hunter.
You will receive a weighted rankings for requirements from the applicant
as well as a job description from a company as well as a JSON with company facts.
This is an example:
"{\n  \"company\": \"Anton Paar\",  \n  \"title\": \"AI Manager\",\n  \"fit\": \"\",\n  \"fit_detailed\": \"\",\n  \"dateAdded\": \"July 10, 2023\",\n  \"salaryRange\": \"\u20ac120k - \u20ac150k\",\n  \"location\": \"Graz, Austria\"\n}"
Using the weighted requirements grade the job on a scale from 0-100 so 
that the applicant can make a ranking of all jobs and decide which ones to apply first to.
Think step by step. First grade every category, like salary of the requirements with its maximum being its weighted value and give three reasons for each category.
Then sum up those individual grades to one final grade.
Where information is not provided, like salary, take a value that you would expect from benchmark job.
Return a JSON of the job with the key-value pairs.
Put your final grade in "fit".
Put your detailed thinking that leads to the fit in "fit_detailed".
Leave the other key value pairs as they are.
Do not invent information.
Make the fit a number between 0 and 100 where 100 is perfect fit.
Your outcome should look like this:
{
  "company": "Microsoft",
  "title": "Software Engineer",
  "fit": "85",
  "fit_detailed": "Put here all your thinking, like intellectual stimulation 15 because reason 1, 2 ,3, impact 3 because reason 1, reason 2, reason 3, so the final grade adds up to this 85",
  "dateAdded": "July 14, 2023",
  "salaryRange": "€130k - €160k",
  "location": "Redmond, USA"
}
Do not return a JSON that does not have both a filled fit and a filled fit_detailed!
"""


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JOBS_FOLDER = os.path.join(ROOT_DIR, "../public/jobs/txts")
JSON_FOLDER_FACTS = os.path.join(ROOT_DIR, "../public/jobs/JSONs_facts")
JSON_FOLDER_FITS = os.path.join(ROOT_DIR, "../public/jobs/JSONs_fits")
REQUIREMENTS_FILE = os.path.join(
    ROOT_DIR, "../public/digitaltwin/weighted_rankings_for_requirements.txt"
)

with open(REQUIREMENTS_FILE) as f:
    user_message = f.read()

for filename in os.listdir(JSON_FOLDER_FACTS):
    if filename.endswith(".json"):
        json_filename_fits = os.path.splitext(filename)[0] + ".json"
        json_path_fits = os.path.join(JSON_FOLDER_FITS, json_filename_fits)
        
        # Check if JSON file already exists in JSON_FOLDER_FITS, and if so skip
        if os.path.exists(json_path_fits):
            continue

        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(JOBS_FOLDER, txt_filename)

        # Load job facts JSON
        with open(os.path.join(JSON_FOLDER_FACTS, filename)) as f:
            json_facts = json.load(f)

        # Load job text
        with open(txt_path) as f:
            job_text = f.read()

        # Combine all texts
        context = user_message + "\n" + job_text + "\n" + json.dumps(json_facts)

        result = llm(SYSTEM_MESSAGE, context)

        # extract the 'completion' part
        completion = result["completion"]

        # find the start and end of the JSON string
        start = completion.find("{")
        end = completion.rfind("}") + 1

        # extract and clean the JSON string
        clean_result = completion[start:end]

        print(clean_result)

        # Save result to JSON file
        with open(json_path_fits, "w") as f:
            json.dump(clean_result, f)

