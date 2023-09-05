import csv

def filter_csv(input_file, output_file):
    rows_with_commas = []
    
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if ',' in ','.join(row):  # Проверяем, содержит ли строка хотя бы одну запятую
                rows_with_commas.append(row)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows_with_commas)

if __name__ == "__main__":
    input_csv_file = "data(2).csv"   # Замените на путь к вашему входному CSV-файлу
    output_csv_file = "data.csv" # Замените на путь, по которому хотите сохранить результат

    filter_csv(input_csv_file, output_csv_file)