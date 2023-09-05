import csv

filename = 'server/templates/static/data.csv'
output_filename = 'server/templates/static/data1.csv'

output_file = open(output_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(output_file)

with open(filename, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    current_key = ''
    current_combined_row = []

    for row in csv_reader:
        if len(row) > 1:
            key = row[0]
            if key != current_key:
                if current_combined_row:
                    csv_writer.writerow(current_combined_row)
                current_key = key
                current_combined_row = row
            else:
                current_combined_row.extend(row[1:])

    if current_combined_row:
        csv_writer.writerow(current_combined_row)

output_file.close()
