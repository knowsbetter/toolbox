# This script converts part numbers and chapters cross-reference
# from pdf to csv file.

import pdfplumber
import csv

def read_refs(file_name: str, from_page: int = 0, to_page: int = 0):
    """Reads pdf index file to a dictionary with {'part_number': [chapter_list]} structure."""
    temp = []
    with pdfplumber.open(file_name) as pdf:
        for page in pdf.pages:
            temp += page.extract_table()[1]
    return temp

def write_to_csv(data: dict, file_name: str):
    """Writes dictionary to a csv file with 'file_name'"""
    with open(file_name, 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for key, value in data.items():
            csv_writer.writerow([key] + value)

def convert_table_to_dict(t: list):
    for_db = {}
    current_pn = ""
    skip_line = False
    for i in range(0, len(table), 2):
        for line in table[i].split('\n'):
            if (' ' not in line) or ('*' in line):
                if '*' not in line:
                    if not skip_line:
                        current_pn = line
                        for_db[current_pn] = []
                    else:
                        current_pn += line
                        for_db[current_pn] = []
                        skip_line = False
                else:
                    first_space_index = line.index(' ')
                    current_pn = line[:first_space_index]
                    skip_line = True
            elif not skip_line:
                first_space_index = line.index(' ')
                line = line[:first_space_index] + '-' + line[first_space_index+1:]
                for_db[current_pn].append(line)
    return for_db

for i in range(407):
    print(f'File #{i} is converting...')
    table = read_refs(f'pdf/split/split_{i}.pdf')
    db_dict = convert_table_to_dict(table)
    write_to_csv(db_dict, 'data.csv')