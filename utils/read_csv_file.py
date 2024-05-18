import csv
from numpy import array

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(array([float(el) for el in row]))
    return array(data)  # Преобразование списка списков в массив NumPy