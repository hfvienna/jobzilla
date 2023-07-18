import os
from PyPDF2 import PdfReader

def convert_pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    with open(txt_path, 'w') as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    pdf_path = os.path.join('..', 'public', 'digitaltwin', 'cv_hfvienna.pdf')
    txt_path = os.path.join('..', 'public', 'digitaltwin', 'cv_hfvienna.txt')
    convert_pdf_to_txt(pdf_path, txt_path)
    