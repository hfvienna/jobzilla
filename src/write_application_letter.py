import logging
import os
import json

from llm_claude import llm

SYSTEM_MESSAGE = """
Assume you are an expert job hunter.
You have the CV from the applicant and the job posting.
Write a complete application letter to send out to apply for the job.
Only use arguments that you can prove from the CV and cite them with quotes to make it visible which source you cite.
Write that your letter is automatically written using an LLM and a software that the applicant made.
They can see the software under github.com/hfvienna/jobzilla and check out their companies ranking at jobzillaai.vercel.com
"""

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JOBS_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/job_postings_renamed_txt")
LETTERS_FOLDER = os.path.join(ROOT_DIR, "../data/jobs/application_letters_txt")
CV_TXT = os.path.join(ROOT_DIR, "../data/digitaltwin/cv_hfvienna.txt")

# Make sure the application_letters_txt directory exists
os.makedirs(LETTERS_FOLDER, exist_ok=True)

def load_file(path):
    with open(path, 'r') as f:
        return f.read()

for filename in os.listdir(JOBS_FOLDER):
    txt_filename = os.path.splitext(filename)[0] + ".txt"
    txt_path = os.path.join(JOBS_FOLDER, txt_filename)
    
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
    output_path = os.path.join(LETTERS_FOLDER, txt_filename)
    with open(output_path, "w") as f:
        f.write(completion)
