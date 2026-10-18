
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx

try:
    json_to_csv(
        "data/lab05/samples/people.json",
        "data/lab05/out/people_from_json.csv"
    )

    csv_to_json(
        "data/lab05/samples/people.csv",
        "data/lab05/out/people_from_csv.json"
    )

    csv_to_xlsx(
        "data/lab05/samples/people.csv",
        "data/lab05/out/people.xlsx"
    )

    csv_to_xlsx(
        "data/lab05/samples/cities.csv",
        "data/lab05/out/cities.xlsx"
    )

    print("Все преобразования выполнены успешно!")

except (ValueError, FileNotFoundError, PermissionError) as error:
    print(f"Не удалось выполнить преобразование: {error}")

