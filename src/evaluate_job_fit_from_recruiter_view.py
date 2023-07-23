import json
import os

from llm_claude import llm

SYSTEM_MESSAGE = """
You are an expert recruiter.
You will receive a weighted rankings for requirements from the recruiters
as well as a job description from a company as well as a JSON with company facts as well as the CV of the applicant.
This is an example:
{
  "uuid": 17,
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
Using the weighted requirements from the recruiter grade the applicant on a scale from 0-50 so 
that the recruiter can make a ranking of all applicants and decide which one to make an offer to.
Think step by step. First grade every category, like relevant skills and experience with its maximum being its weighted value and give three reasons for each category.
To make sure the information is correct, cite your source for every supporting from the cv.
Then sum up those individual grades to one final grade.
Make the final grade very exact, so don't round to 35 or 45, just add up the previous values.
Make all values/grades integers.
Where information is not provided, take a value that you would expect from benchmark applicant.
Return a JSON of the job with the key-value pairs.
Put your final grade in "fit_recruiter".
fit_recruiter is an integer, see example. So just a number between 0 and 50 which you added up.
Put your detailed thinking that leads to the fit in "fit_recruiter_detailed".
Leave the other key value pairs as they are.
Only change fit_recruiter and fit_recruiter_detailed in this step
Return the full JSON.
If you don't know something, say you don't know.
Make the fit a number between 0 and 50 where 50 is perfect fit.
Only take information you can prove in the CV.
Your outcome should look like this:
Provide all your detailed reasoning like in the example below.
Leave the uuid as is.
{
  "uuid": 18,
  "company": "Biotech International",
  "title": "Biotech Data Analyzer",
  "fit_applicant": null,
  "fir_applicant_detailed": "",
  "fit_recruiter": 43,
  "fit_recruiter_detailed": "Relevant Skills and Experience: 9/10 - Has strong technical skills in AI/ML and software engineering. Industrial experience is limited but has worked on data science projects. Educational Qualifications: 5/5 - Has a relevant master's degree in computer science/engineering. Cultural Fit: 6/7 - Seems capable of working in an innovative, fast-paced research environment. Fits the desire for collaborative teamwork. Communication Skills: 7/7 - Can communicate technical details clearly in English and German. Writing skills evidenced by publications. Problem-Solving Ability: 4/5 - Analytical skills evidenced by academic projects and publications. More details on specific industrial problems solved would be beneficial. Adaptability: 4/5 - Academic and consulting background suggests ability to adapt, but more evidence in industrial research settings would be better. Initiative and Motivation: 4/4 - Shows initiative through founding a company and pursuing research. More evidence of drive in a research role would help. Teamwork: 2/3 - Collaborated with cross-functional teams on projects. More emphasis on teamwork capabilities would be better. Leadership Potential: 2/3 - Limited evidence, but research leadership potential could likely be developed over time. Total: 43/50 In summary, the candidate has a strong technical background but is relatively junior. Cultural fit seems decent and they have potential, but more proven industrial research experience would strengthen their candidacy. I would recommend an interview to further assess motivation and fit.",
  "date:added": "July 14, 2023",
  "salary_range": "EUR 130k - 160k",
  "location": "Redmond, USA",
  "email": "biotech@hr.com"
}
Ensure that for every category the grade is smaller that the category weight.
Only give full points.
So, for leadership potential for example, only the following are possible 0/3, 1/3, 2/3, 3/3.
Return a JSON that does have both a filled fit_recruiter and a filled fit_recruiter_detailed with a long explanatory string!
Only add human readable non-code text.
Put citations in round brackets.
To make sure the information is correct, cite your source for every supporting from the cv abbreviated to 5 words per supporting argument.
Be super specific, like research experience, proven by "Paper in conference ECIS"
The CV is delimited from the other text by the delimiter #### .
Only take information between #### as source and reason for your grade.
Answer in English.
The job requirements are delimited by XXXX .
Make your total ranking lower or the same as category max.
Only arguments from the CV count as only they apply to the applicant.
The job description is only to be used to check for what this recruiter look for, not what the applicant offers.
The applicant does not have the criteria from the job description unless stated in or infered from the CV.
In the string use only normal characters and spaces.
If you feel you have to use non-JSON code like tabs then escape it.
"""


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JOBS_TXTS = os.path.join(ROOT_DIR, "../data/jobs/job_postings_renamed_txt")
CV_TXT = os.path.join(ROOT_DIR, "../data/digitaltwin/cv_hfvienna.txt")
JSON_FACTS = os.path.join(ROOT_DIR, "../data/jobs/job_postings_facts_json")
JSON_FITS = os.path.join(ROOT_DIR, "../data/jobs/fits_recruiter_json")
REQUIREMENTS_FILE = os.path.join(ROOT_DIR, "../data/jobs/weighted_rankings_for_recruiters.txt")

def load_file(file_path):
    with open(file_path) as f:
        return f.read()

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def process_files():
    user_message = load_file(REQUIREMENTS_FILE)

    for filename in os.listdir(JSON_FACTS):
        if filename.endswith(".json"):
            json_filename_fits = os.path.splitext(filename)[0] + ".json"
            json_path_fits = os.path.join(JSON_FITS, json_filename_fits)

            if os.path.exists(json_path_fits):
                print(f"Skipping {filename} because {json_filename_fits} already exists.")
                continue

            txt_filename = os.path.splitext(filename)[0] + ".txt"
            job_txt_path = os.path.join(JOBS_TXTS, txt_filename)
            cv_txt_path = os.path.join(CV_TXT)

            json_facts = load_json(os.path.join(JSON_FACTS, filename))
            job_text = load_file(job_txt_path)
            cv_text = load_file(cv_txt_path)

            context = user_message + "\n" + "XXXX" + job_text + "XXXX" + "\n" + cv_text + "\n" + json.dumps(json_facts) + "\n" + SYSTEM_MESSAGE
            #repeat of system message to increase prompt visibility

            result = llm(SYSTEM_MESSAGE, context)
            completion = result["completion"]
            start = completion.find("{")
            end = completion.rfind("}") + 1

            clean_result_str = completion[start:end]
            print(clean_result_str)  # Add this line to print the string
            try:
                clean_result_dict = json.loads(clean_result_str)
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")

            save_json(json_path_fits, clean_result_dict)

if __name__ == "__main__":
    process_files()