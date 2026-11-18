"""CSV-хранилище студентов и CRUD-операции над ним."""

import csv
from collections import Counter
from pathlib import Path
from statistics import mean

from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student

HEADER = list(STUDENT_FIELDS)


def ensure_storage(path) -> None:
    """Создаёт CSV-файл с заголовком, если хранилища ещё нет."""
    storage = Path(path)
    storage.parent.mkdir(parents=True, exist_ok=True)

    if not storage.exists():
        with storage.open("w", encoding="utf-8", newline="") as file:
            csv.DictWriter(file, fieldnames=STUDENT_FIELDS).writeheader()


def load_students(path) -> list[dict]:
    """Загружает записи, а для отсутствующего файла возвращает пустой список."""
    try:
        file = Path(path).open("r", encoding="utf-8", newline="")
    except FileNotFoundError:
        return []

    students = []

    with file:
        reader = csv.DictReader(file, strict=True)
        try:
            if reader.fieldnames is None:
                raise ValueError("В CSV-файле отсутствует заголовок")

            if reader.fieldnames != HEADER:
                raise ValueError(
                    "Заголовок CSV должен быть fio,birthdate,group,gpa"
                )

            for row in reader:
                try:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("неверное количество столбцов")

                    # DictReader возвращает GPA строкой, а ЛР8 ожидает число.
                    row["gpa"] = float(row["gpa"])
                    students.append(student_from_dict(row))
                except ValueError as error:
                    raise ValueError(
                        f"Строка CSV №{reader.line_num}: {error}"
                    ) from error
        except csv.Error as error:
            raise ValueError(f"Нарушен формат CSV: {error}") from error

    return students


def save_students(path, students) -> None:
    """Валидирует записи и целиком перезаписывает CSV-файл."""
    checked_students = []

    for student in students:
        validate_student(student)
        checked_students.append(student_from_dict(student))

    storage = Path(path)
    storage.parent.mkdir(parents=True, exist_ok=True)

    with storage.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=STUDENT_FIELDS)
        writer.writeheader()
        writer.writerows(checked_students)


def add_student(path, student: dict) -> None:
    """Добавляет валидную запись, если такого ФИО ещё нет."""
    validate_student(student)
    checked_student = student_from_dict(student)

    students = load_students(path)
    fio = checked_student["fio"]
    if any(record["fio"] == fio for record in students):
        raise ValueError(f"Запись с таким ФИО уже есть: {fio}")

    students.append(checked_student)
    save_students(path, students)


def list_students(path, sort_by=None) -> list[dict]:
    """Возвращает студентов с необязательной сортировкой."""
    if sort_by not in (None, "fio", "gpa"):
        raise ValueError(
            "sort_by должен быть None, 'fio' или 'gpa'"
        )

    students = load_students(path)

    if sort_by is None:
        return students

    return sorted(students, key=lambda student: student[sort_by])


def find_students(path, substr: str) -> list[dict]:
    """Ищет подстроку в ФИО без учёта регистра."""
    query = substr.casefold()

    return [
        student
        for student in load_students(path)
        if query in student["fio"].casefold()
    ]


def remove_student(path, fio: str) -> int:
    """Удаляет все записи с точно указанным ФИО."""
    students = load_students(path)
    remaining = [
        student
        for student in students
        if student["fio"] != fio
    ]

    removed_count = len(students) - len(remaining)
    if removed_count:
        save_students(path, remaining)

    return removed_count


def update_student(path, fio: str, **fields) -> bool:
    """Обновляет первую запись с указанным ФИО."""
    unknown_fields = set(fields) - set(STUDENT_FIELDS)

    if unknown_fields:
        unknown = sorted(unknown_fields)[0]
        raise KeyError(f"Неизвестное поле: {unknown}")

    students = load_students(path)

    for index, student in enumerate(students):
        if student["fio"] == fio:
            updated = student.copy()
            updated.update(fields)

            validate_student(updated)
            students[index] = student_from_dict(updated)
            save_students(path, students)

            return True

    return False


def stats(path) -> dict:
    """Считает статистику по GPA, группам и пяти лучшим студентам."""
    students = load_students(path)
    gpas = [student["gpa"] for student in students]
    top = sorted(students, key=lambda student: (-student["gpa"], student["fio"]))[:5]

    return {
        "count": len(students),
        "min_gpa": min(gpas, default=None),
        "max_gpa": max(gpas, default=None),
        "avg_gpa": mean(gpas) if gpas else None,
        "groups": dict(Counter(student["group"] for student in students)),
        "top_5_students": [
            {"fio": student["fio"], "gpa": student["gpa"]} for student in top
        ],
    }
