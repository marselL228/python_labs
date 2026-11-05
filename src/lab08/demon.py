"""Запуск из корня репозитория: python -m src.lab08.demo."""

from datetime import date
from pathlib import Path

from .models import format_student, make_student, student_age, update_student
from .serialize import students_from_csv, students_from_json, students_to_json


def main():
    data = Path(__file__).resolve().parents[2] / "data" / "lab08"
    print("ЛР8. Модель Student без классов\n")
    students = students_from_json(data / "students_input.json")
    for student in students:
        print(format_student(student))
    students_to_json(students, data / "students_output.json")
    restored = students_from_json(data / "students_output.json")
    print("\nJSON туда-обратно:", students == restored)
    print("Создан файл data/lab08/students_output.json")

    print("\nПроверка неверной даты:")
    try:
        students_from_json(data / "students_bad.json")
    except ValueError as error:
        print(error)
    print("\nПроверка gpa = 7:")
    try:
        make_student("Иванов Иван Иванович", "2007-09-20", "БИВТ-26-6-5", 7)
    except ValueError as error:
        print(error)

    student = students[0]
    print("\nВозраст до дня рождения:", student_age(student, date(2026, 9, 19)))
    print("Возраст в день рождения:", student_age(student, date(2026, 9, 20)))
    updated = update_student(student, gpa=4.8)
    print("\nОбновление GPA:", student["gpa"], "->", updated["gpa"])
    print("Новая запись — отдельный словарь:", updated is not student)
    print("Студентов из CSV:", len(students_from_csv(data / "students_input.csv")))


if __name__ == "__main__":
    main()
