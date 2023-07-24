import os
import json

def count_files(directory):
    num_files = 0
    num_high_fit = 0
    for f in os.listdir(directory):
        if f.startswith('.') or f.endswith('.DS_Store'):  # Skip hidden files and .DS_Store files
            continue
        if os.path.isfile(os.path.join(directory, f)):
            num_files += 1
            if f.endswith('.json'):
                with open(os.path.join(directory, f)) as json_file:
                    data = json.load(json_file)
                    # Calculate the total fit
                    total_fit = (data.get('fit_applicant', 0) or 0) + (data.get('fit_recruiter', 0) or 0)
                    if total_fit >= 80:
                        num_high_fit += 1
    return num_files, num_high_fit

directories = [
    "../data/jobs/job_postings_inbox_pdf",
    "../data/jobs/job_postings_renamed_pdf",
    "../data/jobs/job_postings_renamed_txt",
    "../data/jobs/job_postings_facts_json",
    "../data/jobs/fits_recruiter_json",
    "../data/jobs/fits_applicant_json",
    "../data/jobs/fits_merged_json",
    "../data/jobs/application_letters_txt"
]

for directory in directories:
    num_files, num_high_fit = count_files(directory)
    print(f"There are {num_files} files in {directory}")
    if directory.endswith("fits_merged_json"):
        print(f"There are {num_high_fit} jobs with a fit score of 80 or higher in {directory}")
