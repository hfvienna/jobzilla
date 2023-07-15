# api/process_job_fit.py

import json
import os

from claude import llm

SYSTEM_MESSAGE = """
You are an expert job hunter.
You will receive a weighted rankings for requirements from the applicant
as well as a job description from a company as well as a JSON with company facts.
This is an example:
{
  "company": "ALDI SÜD", 
  "title": "Senior Manager",
  "fit": null,
  "fit_detailed": "",
  "dateAdded": "July 14, 2023",
  "salaryRange": "EUR 113k",
  "location": "Salzburg, Austria"
}
Using the weighted requirements grade the job on a scale from 0-100 so 
that the applicant can make a ranking of all jobs and decide which ones to apply first to.
Think step by step. First grade every category, like salary of the requirements with its maximum being its weighted value and give three reasons for each category.
Do not repeat the weights as "weight" or the number to not confuse them with your grades.
Like in the sample below, grades are provided, but not again the weights.
Only write grade for each category.
Then sum up those individual grades to one final grade.
Make the final grade very exact, so don't round to 65 or 75, just add up the previous values.
Where information is not provided, like salary, take a value that you would expect from benchmark job.
Return a JSON of the job with the key-value pairs.
Put your final grade in "fit".
Fit is an integer, see example. So just a number between 0 and 100 which you added up.
Put your detailed thinking that leads to the fit in "fit_detailed".
Leave the other key value pairs as they are.
DO NOT CHANGE ANYTHING ELSE THAN THE fit and fit_detailed in this step, but return the full JSON.
Do not invent information.
Make the fit a number between 0 and 100 where 100 is perfect fit.
Your outcome should look like this:
Provide all your detailed reasoning and not just "reason 1", "reason", do it like in the example below.
{
  "company": "Biotech International",
  "title": "Biotech Data Analyzer",
  "fit": 68,
  "fit_detailed": "Intellectual stimulation and challenge 5 because innovative biotech diagnostics are intellectually stimulating, however, this is not in the field of AI. developing sales strategy requires creative thinking, and oncology focus provides complexity. Flexible/remote work arrangements 15 because fully remote DACH-based role, flexible hours mentioned, and home office stated. Autonomy and independence 10 because VP suggests autonomy but unclear on CCO oversight and leading team indicates some independence. Alignment with interests 10 because biotech startup with innovative cancer prevention technology indicates risk tolerance needed. Opportunities to publish research 2 because commercial operations less focused on research, could partner with R&D. Compensation level 5 because salary range not provided, likely competitive for role but equity details unknown. Work/life balance 10 because fully remote, flexible hours, reasonable travel. Impact and meaning 5 because cancer prevention diagnostics have big impact and commercial success enables product impact. Collaborative team environment 3 because leading commercial team indicates collaboration and cross-functional partnerships mentioned but limited detail on culture. Career advancement prospects 3 because startup may enable fast growth but advancement path and trajectory unclear.",
  "dateAdded": "July 14, 2023",
  "salaryRange": "EUR 130k - 160k",
  "location": "Redmond, USA"
}
Do not return a JSON that does not have both a filled fit integer and a filled fit_detailed with a long explanatory string!
Do not repeat the weights. We know them, we just want the resulting grade for each category.
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
        clean_result_str = completion[start:end]

        # convert the JSON string back to a Python dictionary
        clean_result_dict = json.loads(clean_result_str)

        # print the dictionary as a pretty JSON string
        print(json.dumps(clean_result_dict, indent=4))

        # Save result to JSON file
        with open(json_path_fits, "w") as f:
            json.dump(clean_result_dict, f, indent=4)
