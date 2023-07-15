# api/process_jobs_facts.py

import json
import os

from claude import llm

SYSTEM_MESSAGE = """You are an expert job hunter.
You will receive a job description from a company.
Return a JSON of the job with the key-value pairs as in the following example.
Add the empty key value pairs but keep them empty.
Do not invent information. If you don't know, "n/a".
Only use the given information in the job description.
Make the company max two words.
Make the title max 3 words.
Make the date added like in the examples.
Make the salary only one number if no range is given.
If a monthly salary is given, multiply by 12.
If a monthly salary is given in Austria, multiply by 14.
Leave the salary as "Not provided" if you can not find it.
Make the location City, Country or Remote.
Leave the location empty if you can not find it.
{
  "company": "Anthropic",
  "title": "Software Engineer",
  "fit": "",
  "fit_detailed": "",
  "dateAdded": "July 10, 2023",
  "salaryRange": "€120k - €150k",
  "location": "Remote"
},
{
  "company": "Google",
  "title": "Product Manager",
  "fit": "",
  "fit_detailed": "",
  "dateAdded": "July 12, 2023",
  "salaryRange": "€150k - €180k",
  "location": "Mountain View, USA"
},
{
  "company": "Microsoft",
  "title": "Software Engineer",
  "fit": "",
  "fit_detailed": "",
  "dateAdded": "July 14, 2023",
  "salaryRange": "€130k - €160k",
  "location": "Redmond, USA"
}
Only use the given information in the job description and the requirements.
"""


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JOBS_FOLDER = os.path.join(ROOT_DIR, "../public/jobs/txts")
JSON_FOLDER = os.path.join(ROOT_DIR, "../public/jobs/JSONs_facts")


for filename in os.listdir(JOBS_FOLDER):
    if filename.endswith(".txt"):
        json_filename = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(JSON_FOLDER, json_filename)
        
        # Check if JSON file already exists, and if so, skip processing this TXT file
        if os.path.exists(json_path):
            continue

        with open(os.path.join(JOBS_FOLDER, filename)) as f:
            job_text = f.read()

        context = job_text

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
        with open(json_path, "w") as f:
            json.dump(clean_result, f)
