import logging
import os
import PyPDF2

from pathlib import Path
from PyPDF2 import PdfReader 

logging.basicConfig(filename='extraction.log', level=logging.DEBUG)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__)).split('/api')[0]
INPUT_FOLDER = os.path.join(ROOT_DIR, 'public/jobs/pdfs')
OUTPUT_FOLDER = os.path.join(ROOT_DIR, 'public/jobs/txts')  

def extract_pdf_text():

  input_pdf_paths = list(Path(INPUT_FOLDER).glob('*.pdf'))

  if not input_pdf_paths:
    logging.error(f'No PDFs found in input folder {INPUT_FOLDER}')
  else:
    logging.info(f'{len(input_pdf_paths)} PDFs found in input folder')
  
  if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

  for pdf_path in input_pdf_paths:

    try:
      pdf = PdfReader(str(pdf_path))
    except Exception as e:
      logging.exception(f'Error opening PDF {pdf_path}: {e}')
      continue

    text = ""

    for page in pdf.pages:
      text += page.extract_text()

    output_path = os.path.join(OUTPUT_FOLDER, os.path.basename(os.path.splitext(pdf_path)[0] + ".txt"))
    
    try:
        with open(output_path, 'w') as f:
            f.write(text)
            logging.info(f'Text extracted to {output_path}')
    except Exception as e:
      logging.exception(f'Error writing to {output_path}: {e}')

  logging.info('PDF extraction complete')

if __name__ == '__main__':
  extract_pdf_text()