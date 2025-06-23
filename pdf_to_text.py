import os
import sys
import argparse
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image


base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

tesseract_path = os.path.join(base_dir, 'tesseract_ocr', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

poppler_bin_path = r'poppler\Library\bin'

def extract_text_from_pdf(pdf_path, output_dir, poppler_path=None):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_dir = os.path.join(output_dir, base_name)
    os.makedirs(pdf_output_dir, exist_ok=True)

    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
    except Exception as e:
        print(f"[ERROR] Failed to open PDF: {pdf_path}. {e}")
        return

    for page_num in range(num_pages):
        text_path = os.path.join(pdf_output_dir, f'page_{page_num + 1}.txt')
        ocr_text_path = os.path.join(pdf_output_dir, f'ocr_page_{page_num + 1}.txt')

        page = reader.pages[page_num]
        extracted_text = page.extract_text() or ""

        # Save extracted text (if any)
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)

        # Convert this page to image
        images = convert_from_path(
            pdf_path,
            first_page=page_num + 1,
            last_page=page_num + 1,
            poppler_path=poppler_path
        )

        for image in images:
            ocr_text = pytesseract.image_to_string(image)
            with open(ocr_text_path, 'a', encoding='utf-8') as ocr_file:
                ocr_file.write(ocr_text)

def main():
    # parser = argparse.ArgumentParser(description="Convert PDFs in a folder to text using OCR")
    # parser.add_argument('--input', required=True, help='Input folder containing PDFs')
    # parser.add_argument('--output', required=True, help='Output folder for text files')
    # parser.add_argument('--poppler', help='(Optional) Path to Poppler bin directory (Windows only)')

    print('Convert PDFs in a folder to text using OC')
    input_folder = input("Enter the folder directory to be converted:\n").strip()
    output_folder = 'outputted_txt'

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            print(f"[INFO] Processing: {filename}")
            extract_text_from_pdf(pdf_path, output_folder, poppler_bin_path)

if __name__ == '__main__':
    main()
