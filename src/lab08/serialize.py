"""Сохранение и загрузка студентов. Политика ошибок: strict."""

import csv
import json
from pathlib import Path

from .models import STUDENT_FIELDS, student_from_dict, student_to_dict


def students_to_json(students: list[dict], path) -> None:
    """Проверяет все записи, затем сохраняет JSON в UTF-8."""
    data = [student_to_dict(student) for student in students]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, allow_nan=False)
        file.write("\n")


def students_from_json(path) -> list[dict]:
    """При первой битой записи выдаёт ValueError с её номером."""
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("В корне JSON должен быть массив студентов")
    students = []
    for number, item in enumerate(data, start=1):
        try:
            students.append(student_from_dict(item))
        except ValueError as error:
            raise ValueError(f"Запись №{number}: {error}") from error
    return students


def students_from_csv(path) -> list[dict]:
    """Преобразует строковый gpa из CSV в число перед валидацией."""
    students = []
    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != list(STUDENT_FIELDS):
            raise ValueError("Заголовок CSV должен быть fio,birthdate,group,gpa")
        for number, row in enumerate(reader, start=2):
            try:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("неверное количество столбцов")
                row["gpa"] = float(row["gpa"])
                students.append(student_from_dict(row))
            except ValueError as error:
                raise ValueError(f"Строка CSV №{number}: {error}") from error
    return students
