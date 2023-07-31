#    Jobzilla automates job search using a LLM.
#    Copyright (C) 2023  hfvienna, author of Jobzilla

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os
import subprocess
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Directory of the currently running script
src_dir = os.path.dirname(os.path.abspath(__file__))

# Get the path of the currently running Python interpreter
python_interpreter = sys.executable

# List of Python files in the order they should be executed
py_files = [
    "rename_job_posting_pdf_to_add_uuid.py",
    "convert_job_posting_pdf_to_txt.py",
    "extract_job_posting_facts_to_json.py",
    "evaluate_job_fit_from_recruiter_view.py",
    "evaluate_job_fit_from_applicant_view.py",
    "merge_applicant_and_recruiter_views.py",
    "aggregate_jsons_to_table_to_display_ranked_jobs.py",
#    "write_application_letter.py",
    "sanity_check.py",
]

# Run each Python file
for py_file in py_files:
    py_file_path = os.path.join(src_dir, py_file)
    if os.path.isfile(py_file_path):
        logging.info(f"Running {py_file_path}...")
        try:
            subprocess.run([python_interpreter, py_file_path], check=True)
        except subprocess.CalledProcessError as e:
            error_message = f"Error while running {py_file_path}: {e}"
            logging.error(error_message)
            raise
    else:
        logging.error(f"File {py_file_path} does not exist")
        raise FileNotFoundError(f"File {py_file_path} does not exist")
