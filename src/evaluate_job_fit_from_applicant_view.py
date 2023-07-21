import json
import logging
import os

from llm_claude import llm

SYSTEM_MESSAGE = """
You are an expert job hunter.
You will receive a weighted rankings for requirements from the applicant
as well as a job description from a company as well as a JSON with company facts.
This is an example:
{
  "uuid": 24,
  "company": "ALDI SÜD", 
  "title": "Senior Manager",
  "fit_applicant": null,
  "fit_applicant_detailed": "",
  "fit_recruiter": null,
  "fit_recruiter_detailed": "",
  "date_added": "July 14, 2023",
  "salary_range": "EUR 113k",
  "location": "Salzburg, Austria",
  "email": ""
}
Using the weighted requirements grade the job on a scale from 0-50 so 
that the applicant can make a ranking of all jobs and decide which ones to apply first to.
Think step by step. First grade every category, like salary of the requirements with its maximum being its weighted value and give three reasons for each category.
Then sum up those individual grades to one final grade.
Make the grades for categories full integers.
Make the final grade very exact, so don't round to 25 or 45, just add up the previous values.
Where information is not provided, like salary, take a value that you would expect from benchmark job.
Return a JSON of the job with the key-value pairs.
Put your final grade in "fit_applicant".
Fit is an integer, see example. So just a number between 0 and 50 which you added up.
Put your detailed thinking that leads to the fit in "fit_applicant_detailed".
Leave the other key value pairs as they are.
Only change the fit and fit_detailed in this step, but return the full JSON.
If you are uncertain, just state that.
Make the fit a number between 0 and 50 where 50 is perfect fit.
Your outcome should look like this:
Provide all your detailed reasoning like in the example below.
{
  "uuid": 27,
  "company": "Biotech International",
  "title": "Biotech Data Analyzer",
  "fit_applicant": 38,
  "fit_applicant_detailed": "Intellectual stimulation and challenge 6/10 because innovative biotech diagnostics are intellectually stimulating, however, this is not in the field of AI. Developing sales strategy requires creative thinking, and oncology focus provides complexity. Flexible/remote work arrangements 8/8 because fully remote DACH-based role, flexible hours mentioned, and home office stated. Autonomy and independence 5/7 because VP suggests autonomy but unclear on CCO oversight and leading team indicates some independence. Alignment with interests 5/5 because biotech startup with innovative cancer prevention technology indicates risk tolerance needed. Opportunities to publish research 1/3 because commercial operations less focused on research, could partner with R&D. Compensation level 2/5 because salary range not provided, likely competitive for role but equity details unknown. Work/life balance 5/5 because fully remote, flexible hours, reasonable travel. Impact and meaning 2/2 because cancer prevention diagnostics have big impact and commercial success enables product impact. Collaborative team environment 2/3 because leading commercial team indicates collaboration and cross-functional partnerships mentioned but limited detail on culture. Career advancement prospects 2/2 because startup may enable fast growth but advancement path and trajectory unclear.",
  "fit_recruiter": null,
  "fit_recruiter_detailed": "",
  "date_added": "July 14, 2023",
  "salary_range": "EUR 130k - 160k",
  "location": "Redmond, USA",
  "email": ""
}
Return a JSON that does have both a filled fit integer and a filled fit_detailed with a long explanatory string!
Return a fit for each category that is lower than the max category or that is the max for the category.
In the string use only normal characters and spaces.
If you feel you have to use non-JSON code like tabs then escape it.
"""


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JOBS_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/job_postings_renamed_txt")
JSON_FOLDER_FACTS = os.path.join(ROOT_DIR, "../data/jobs/job_postings_facts_json")
JSON_FOLDER_FITS = os.path.join(ROOT_DIR, "../data/jobs/fits_applicant_json")
REQUIREMENTS_FILE = os.path.join(
    ROOT_DIR, "../data/digitaltwin/weighted_rankings_for_requirements.txt"
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
            logging.debug(f"Loaded JSON facts: {json_facts}")

        # Load job text
        with open(txt_path) as f:
            job_text = f.read()
            logging.debug(f"Loaded job text: {job_text}")

        # Combine all texts
        context = user_message + "\n" + job_text + "\n" + json.dumps(json_facts)
        logging.debug(f"Combined context: {context}")

        result = llm(SYSTEM_MESSAGE, context)
        logging.debug(f"LLM result: {result}")

        # extract the 'completion' part
        completion = result["completion"]
        logging.debug(f"Completion: {completion}")

        # find the start and end of the JSON string
        start = completion.find("{")
        end = completion.rfind("}") + 1
        logging.debug(f"Start and end of JSON string: {start}, {end}")

        # extract and clean the JSON string
        clean_result_str = completion[start:end]
        logging.debug(f"Clean result string: {clean_result_str}")

        # convert the JSON string back to a Python dictionary
        try:
            clean_result_dict = json.loads(clean_result_str)
            logging.debug(f"Clean result dict: {clean_result_dict}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            logging.error(f"JSON string that caused the error: {clean_result_str}")
            continue

        # print the dictionary as a pretty JSON string
        print(json.dumps(clean_result_dict, indent=4))

        # Save result to JSON file
        with open(json_path_fits, "w") as f:
            json.dump(clean_result_dict, f, indent=4)
