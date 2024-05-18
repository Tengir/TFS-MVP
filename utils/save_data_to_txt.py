def save_data_to_txt(data, filename):
    try:
        with open(f"{filename}.txt", "w") as file:
            for row in data:
                row_str = "[" + ", ".join(map(str, row)) + "]"
                file.write(row_str + "\n")
        print(f"Данные успешно сохранены в файл {filename}.txt")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")