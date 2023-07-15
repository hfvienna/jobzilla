# api/process_jobs.py

import json
import os

from claude import llm

SYSTEM_MESSAGE = """You are an expert job hunter.
You will receive a weighted rankings for requirements from the applicant
as well as a job description from a company.
Using the weighted requirements grade the job on a scale from 0-100 so 
that the applicant can make a ranking of all jobs and decide which ones to apply first to.
Return a JSON of the job with the key-value pairs as in the following example.
Do not invent information. If you don't know, write don't know.
Only use the given information in the job description and the requirements.
Make the company max two words.
Make the title max 3 words.
Make the fit a number between 0 and 100 where 100 is perfect fit.
Make the date added like in the examples
Make the salary only one number if no range is given.
Leave the salary as "Not provided" if you can not find it.
Make the location City, Country or Remote.
Leave the location empty if you can not find it.
{
  "company": "Anthropic",
  "title": "Software Engineer",
  "fit": 95,
  "dateAdded": "July 10, 2023",
  "salaryRange": "€120k - €150k",
  "location": "Remote"
},
{
  "company": "Google",
  "title": "Product Manager",
  "fit": 75,
  "dateAdded": "July 12, 2023",
  "salaryRange": "€150k - €180k",
  "location": "Mountain View, USA"
},
{
  "company": "Microsoft",
  "title": "Software Engineer",
  "fit": 98,
  "dateAdded": "July 14, 2023",
  "salaryRange": "€130k - €160k",
  "location":
  "city": "Redmond, USA"
}
Only use the given information in the job description and the requirements.
"""


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_FOLDER = os.path.join(ROOT_DIR, "../public/jobs/JSONs")
JOBS_FOLDER = os.path.join(ROOT_DIR, "../public/jobs/txts")
REQUIREMENTS_FILE = os.path.join(
    ROOT_DIR, "../public/digitaltwin/weighted_rankings_for_requirements.txt"
)

with open(REQUIREMENTS_FILE) as f:
    user_message = f.read()

for filename in os.listdir(JOBS_FOLDER):
    if filename.endswith(".txt"):
        with open(os.path.join(JOBS_FOLDER, filename)) as f:
            job_text = f.read()

        context = user_message + "\n" + job_text

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
    json_filename = os.path.splitext(filename)[0] + ".json"
    json_path = os.path.join(JSON_FOLDER, json_filename)

    with open(json_path, "w") as f:
        json.dump(clean_result, f)
