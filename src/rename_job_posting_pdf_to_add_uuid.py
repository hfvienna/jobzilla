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
import shutil
import uuid

# Set up logging
logging.basicConfig(filename="logging_job_processing.log", level=logging.INFO)

# Maximum filename length
MAX_FILENAME_LENGTH = 100

# Ensure the log file exists
log_file_path = "rename_job_posting_pdf_to_add_uuid.log"
if not os.path.exists(log_file_path):
    open(log_file_path, "a").close()

# Read the log file
with open(log_file_path, "r") as f:
    handled_files = f.read().splitlines()

# Directory to check for PDFs
inbox_dir = "../data/jobs/job_postings_inbox_pdf"
renamed_dir = "../data/jobs/job_postings_renamed_pdf"

# Make sure the renamed directory exists
if not os.path.exists(renamed_dir):
    os.makedirs(renamed_dir)

# Iterate over each file in the directory
for filename in os.listdir(inbox_dir):
    # If we have not handled this file before
    if filename not in handled_files:
        # Generate a UUID
        file_uuid = uuid.uuid4()

        # Copy the file to the renamed directory with its original name
        shutil.copy(
            os.path.join(inbox_dir, filename),
            os.path.join(renamed_dir, filename),
        )

        # Store the original filename before truncation
        original_filename = filename

        # Truncate the filename if it's too long
        if len(filename) > MAX_FILENAME_LENGTH:
            # Keep the extension of the file
            ext = filename.split(".")[-1]
            filename = (
                filename[: MAX_FILENAME_LENGTH - len(ext) - 1] + "." + ext
            )

        # Rename the copied file using the new (potentially truncated) filename
        new_filename = f"{file_uuid}_{filename}"
        os.rename(
            os.path.join(renamed_dir, original_filename),
            os.path.join(renamed_dir, new_filename),
        )

        # Log that we have handled this file
        with open(log_file_path, "a") as f:
            f.write(
                original_filename + "\n"
            )  # Log the original filename, not the new one
        logging.info(
            f"Copied, renamed file: {original_filename} to {new_filename}"
        )
    else:
        logging.info(f"File: {filename} already processed")
