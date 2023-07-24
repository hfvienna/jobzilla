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
    pdf_path = os.path.join('..', 'data', 'digitaltwin', 'cv_hfvienna.pdf')
    txt_path = os.path.join('..', 'data', 'digitaltwin', 'cv_hfvienna.txt')
    convert_pdf_to_txt(pdf_path, txt_path)
    