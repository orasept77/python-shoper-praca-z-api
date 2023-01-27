import csv

# Идентификаторы продуктов, которые нужно выбрать
product_ids = [123, 456, 789, ...]

# Открытие файла csv для чтения
with open('products.csv', 'r') as csv_file:
    # Создание читателя csv
    reader = csv.reader(csv_file)
    # Проход по всем строкам файла
    for row in reader:
        # Если первый столбец строки содержит идентификатор продукта
        if row[0] in product_ids:
            # Вывод информации о продукте
            print(row)