import os
import PyPDF2
import csv

def extract_bookmarks(pdf_file):
    bookmarks = []

    def traverse_bookmarks(bookmark_list, pdf_reader):
        for item in bookmark_list:
            if isinstance(item, list):
                traverse_bookmarks(item, pdf_reader)
            else:
                if not item.title.startswith('PA'):
                    bookmarks.append(f'{item.title};{pdf_reader.get_destination_page_number(item)+1}')

    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt("")  # If the PDF has a password, provide it here
        traverse_bookmarks(pdf_reader.outline, pdf_reader)

    return bookmarks

def write_to_csv(data: list, file_name: str):
    """Writes dictionary to a csv file with 'file_name'"""
    with open(file_name, 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\n')
        csv_writer.writerow(data)

def index_all_files(directory, output_file):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        file_path = os.path.join(directory, pdf_file)
        bookmarks = extract_bookmarks(file_path)
        print(pdf_file)
        write_to_csv(bookmarks, output_file)

if __name__ == "__main__":
    pdf_directory = "aipc"
    output_csv_file = "bookmarks.csv"
    index_all_files(pdf_directory, output_csv_file)