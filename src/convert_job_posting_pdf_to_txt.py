import logging
import os
from pathlib import Path

from PyPDF2 import PdfReader

logging.basicConfig(filename="extraction.log", level=logging.DEBUG)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__)).split("/src")[0]
INPUT_FOLDER = os.path.join(ROOT_DIR, "data/jobs/job_postings_renamed_pdf")
OUTPUT_FOLDER = os.path.join(ROOT_DIR, "data/jobs/job_postings_renamed_txt")

def get_processed_files(log_file):
    # Check if the log file exists, if not, create it
    if not os.path.exists(log_file):
        open(log_file, 'a').close()

    with open(log_file, 'r') as f:
        return f.read().splitlines()

def log_processed_file(log_file, file_name):
    with open(log_file, 'a') as f:
        f.write(file_name + '\n')

def extract_pdf_text():
    log_file = 'convert_job_posting_pdf_to_txt.log'
    processed_files = get_processed_files(log_file)
    
    input_pdf_paths = list(Path(INPUT_FOLDER).glob("*.pdf"))
    unprocessed_pdf_paths = [path for path in input_pdf_paths if path.name not in processed_files]

    if not unprocessed_pdf_paths:
        logging.error(f"No unprocessed PDFs found in input folder {INPUT_FOLDER}")
    else:
        logging.info(f"{len(unprocessed_pdf_paths)} unprocessed PDFs found in input folder")

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for pdf_path in unprocessed_pdf_paths:
        try:
            pdf = PdfReader(str(pdf_path))
        except Exception as e:
            logging.exception(f"Error opening PDF {pdf_path}: {e}")
            continue

        text = ""

        for page in pdf.pages:
            text += page.extract_text()

        output_path = os.path.join(
            OUTPUT_FOLDER, os.path.basename(os.path.splitext(pdf_path)[0] + ".txt")
        )

        try:
            with open(output_path, "w") as f:
                f.write(text)
                logging.info(f"Text extracted to {output_path}")
        except Exception as e:
            logging.exception(f"Error writing to {output_path}: {e}")
        else:
            log_processed_file(log_file, pdf_path.name)

    logging.info("PDF extraction complete")


if __name__ == "__main__":
    extract_pdf_text()
