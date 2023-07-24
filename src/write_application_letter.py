import logging
import os
import json

from llm_claude import llm

SYSTEM_MESSAGE = """
Assume you are an "expert job hunter".
You have the CV from the applicant and the job posting.
Write a complete application letter to send out to apply for the job.
Only use arguments that you can prove from the CV and cite them with quotes to make it visible which source you cite.
Write that your letter is automatically written using an LLM and a software that the applicant made.
They can see the software under https://github.com/hfvienna/jobzilla and check out their companies ranking at https://jobzillaai.vercel.app/ranking
If the job posting is in German, write the application letter in German only.
If the job posting is in English or any other language, write the application letter in English only.
Sign as the name in the CV (assume you are the person in the CV plus having the skill of an expert job hunter).
Write only things that belong in an application letter and convince the recruiter.
Be concise, your application letter has to fit on one page including date etc.
"""

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JOBS_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/job_postings_renamed_txt")
LETTERS_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/application_letters_txt")
SCORES_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/fits_merged_json")
CV_TXT = os.path.join(ROOT_DIR, "../data/digitaltwin/cv_hfvienna.txt")

# Make sure the application_letters_txt directory exists
os.makedirs(LETTERS_FOLDER, exist_ok=True)

def load_file(path):
    with open(path, 'r') as f:
        return f.read()

def load_json_file(path):
    with open(path, 'r') as f:
        return json.load(f)

for filename in os.listdir(JOBS_FOLDER):
    if not filename.endswith(".txt"):  # Skip non-txt files
        continue

    txt_filename = os.path.splitext(filename)[0] + ".txt"
    txt_path = os.path.join(JOBS_FOLDER, txt_filename)
    output_path = os.path.join(LETTERS_FOLDER, txt_filename)
    score_path = os.path.join(SCORES_FOLDER, txt_filename.replace(".txt", ".json"))

    # Check if the file already exists in the target folder
    if os.path.exists(output_path):
        logging.debug(f"Application letter for {txt_filename} already exists. Skipping.")
        continue

    # Check if the total score is less than 80
    if os.path.exists(score_path):  # Make sure the score file exists
        score_data = load_json_file(score_path)
        total_score = score_data["fit_applicant"] + score_data["fit_recruiter"]
        if total_score < 80:
            logging.debug(f"Total score for {txt_filename} is less than 80. Skipping.")
            continue

    # Load job text
    with open(txt_path) as f:
        job_text = f.read()
        logging.debug(f"Loaded job text: {job_text}")

    cv_text = load_file(CV_TXT)

    # Combine all texts
    context = SYSTEM_MESSAGE + "\n" + job_text + "\n" + "\n" + cv_text
    logging.debug(f"Combined context: {context}")

    result = llm(SYSTEM_MESSAGE, context)
    logging.debug(f"LLM result: {result}")

    # extract the 'completion' part
    completion = result["completion"]
    logging.debug(f"Completion: {completion}")

    # Save result to txt file
    with open(output_path, "w") as f:
        f.write(completion)
        