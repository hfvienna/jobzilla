import os
import subprocess

# Directory of the currently running script
src_dir = os.path.dirname(os.path.abspath(__file__))

# List of Python files in the order they should be executed
py_files = [
    'rename_job_posting_pdf_to_add_uuid.py',
    'convert_job_posting_pdf_to_txt.py',
    'extract_job_posting_facts_to_json.py',
    'evaluate_job_fit_from_recruiter_view.py',
    'evaluate_job_fit_from_applicant_view.py',
    'merge_applicant_and_recruiter_views.py',
    'aggregate_jsons_to_table_to_display_ranked_jobs.py',
    'sanity_check.py'
]

# Run each Python file
# Run each Python file
for py_file in py_files:
    py_file_path = os.path.join(src_dir, py_file)
    if os.path.isfile(py_file_path):
        print(f'Running {py_file_path}...')
        try:
            subprocess.run(['python3', py_file_path], check=True)
        except subprocess.CalledProcessError:
            print(f"Error occurred while running {py_file_path}")
    else:
        print(f"File {py_file_path} does not exist")
