## Splits a large pdf file to small 10-pages files.

import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_by_pages(input_pdf_path, output_dir, pages_per_split=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_pdf = PdfReader(input_pdf_path)

    total_pages = len(input_pdf.pages)
    num_splits = (total_pages // pages_per_split) + (1 if total_pages % pages_per_split > 0 else 0)

    for i in range(num_splits):
        start_page = i * pages_per_split
        end_page = min((i + 1) * pages_per_split, total_pages)
        output_pdf_path = os.path.join(output_dir, f'split_{i}.pdf')

        writer = PdfWriter()
        for page_num in range(start_page, end_page):
            writer.add_page(input_pdf.pages[page_num])

        with open(output_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)

if __name__ == "__main__":
    input_pdf_path = "pdf/aipc738.pdf"  # Замените на путь к вашему PDF-файлу
    output_dir = "pdf/split"  # Замените на путь к папке, где хотите сохранить разделенные файлы
    pages_per_split = 10

    split_pdf_by_pages(input_pdf_path, output_dir, pages_per_split)
