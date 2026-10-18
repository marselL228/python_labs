import json
import csv
from pathlib import Path


def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует список словарей из JSON в CSV.
    Порядок колонок определяется первым объектом.
    """
    json_path = Path(json_path)
    csv_path = Path(csv_path)

    if json_path.suffix.lower() != ".json":
        raise ValueError("Входной файл должен иметь расширение .json")

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Выходной файл должен иметь расширение .csv")

    with json_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("JSON должен содержать список словарей")

    fieldnames = list(data[0].keys())

    if not fieldnames:
        raise ValueError("В объектах JSON отсутствуют поля")

    for item in data:
        for key in item:
            if key not in fieldnames:
                fieldnames.append(key)

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON.
    Значения всех полей сохраняются как строки.
    """
    csv_path = Path(csv_path)
    json_path = Path(json_path)

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Входной файл должен иметь расширение .csv")

    if json_path.suffix.lower() != ".json":
        raise ValueError("Выходной файл должен иметь расширение .json")

    with csv_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not any(reader.fieldnames):
            raise ValueError("CSV пустой или не содержит заголовок")

        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Заголовки CSV должны быть уникальными")

        data = list(reader)

    if not data:
        raise ValueError("CSV не содержит данных")

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        