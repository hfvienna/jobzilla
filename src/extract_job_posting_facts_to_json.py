import os
import json
import uuid
from datetime import datetime
from llm_claude import llm

SYSTEM_MESSAGE = """You are an expert job hunter.
You will receive a job description from a company.
Return a JSON of the job with the key-value pairs as in the following example.
Add the empty key value pairs but keep them empty.
So fit will be an integer and is therefore null.
fit_detailed will be a string and is therefore ""
Do not invent information. If you don't know, "n/a".
Only use the given information in the job description.
Make the company max two words.
Make the title max 3 words.
Make the date added like in the examples.
Make the salary only one number if no range is given.
Do not add any unicode in the salary, just integers, k for thousand - for range and the text EUR or USD for currency. 
If a monthly salary is given, multiply by 12.
If a monthly salary is given in Austria, multiply by 14.
Leave the salary as "Not provided" if you can not find it.
Make the location City, Country or Remote.
Leave the location empty if you can not find it.
When you find an email, add it in email, otherwise leave it "".
Leave the uuid at null.
Leave the date_added at "".
{
  "uuid": null,
  "company": "Anthropic",
  "title": "Software Engineer",
  "fit_applicant": null,
  "fit_applicant_detailed": "",
  "fit_recruiter": null,
  "fit_recruiter_detailed": "",
  "date_added": "July 10, 2023",
  "salary_range": "USD 120k - 150k",
  "location": "Remote"
  "email": hr@anthropic.org
},
{
  "uuid": null,
  "company": "Google",
  "title": "Product Manager",
  "fit_applicant": null,
  "fit_applicant_detailed": "",
  "fit_recruiter": null,
  "fit_recruiter_detailed": "",
  "date_added": "",
  "salary_range": "EUR 150k - 180k",
  "location": "Mountain View, USA"
  "email": ""
},
{
  "uuid": null,
  "company": "Microsoft",
  "title": "Software Engineer",
  "fit_applicant": null,
  "fit_applicant_detailed": "",
  "fit_recruiter": null,
  "fit_recruiter_detailed": "",
  "date_added": "",
  "salary_range": "EUR 133k",
  "location": "Redmond, USA"
  "email": ""
}
Only use the given information in the job description and the requirements.
Do not return any Unicode. Just write USD or EUR ; never u20ac.
Do not return monthly salaries! If a salary is below 10.000, then calculate the yearly salary.
For all yearly salaries, round to the next 1000 up or down and always use k instead of xx.xxx
Do not leave space(s) between integer and k. Do leave a space, however, between currency and integer.
"""


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JOBS_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/job_postings_renamed_txt")
JSON_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/job_postings_facts_json")

for filename in os.listdir(JOBS_FOLDER):
    if filename.endswith(".txt"):
        json_filename = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(JSON_FOLDER, json_filename)
        
        if os.path.exists(json_path):
            continue

        with open(os.path.join(JOBS_FOLDER, filename)) as f:
            job_text = f.read()

        context = job_text

        try:
            result = llm(SYSTEM_MESSAGE, context)
            completion = result["completion"]
            start = completion.find("{")
            end = completion.rfind("}") + 1
            clean_result = completion[start:end]

            dict_result = json.loads(clean_result)

            # Extract the UUID from the filename
            file_uuid = filename.split('_')[0]
            dict_result['uuid'] = file_uuid

            # Get the creation date of the file
            stat = os.stat(os.path.join(JOBS_FOLDER, filename))
            creation_time = stat.st_birthtime
            creation_date = datetime.fromtimestamp(creation_time)

            # Add the creation date to the dictionary
            dict_result['date_added'] = creation_date.strftime('%B %d, %Y')

            with open(json_path, "w") as f:
                json.dump(dict_result, f, indent=4)
        except json.JSONDecodeError:
            print(f"Failed to process file: {filename}")