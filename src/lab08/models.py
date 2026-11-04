"""Запись Student: обычный словарь с фиксированными полями."""

from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def make_student(fio, birthdate, group, gpa) -> dict:
    """Проверяет поля и создаёт новую запись студента."""
    if not isinstance(fio, str) or not fio.strip():
        raise ValueError("fio: нужна непустая строка")
    if not isinstance(group, str) or not group.strip():
        raise ValueError("group: нужна непустая строка")
    if not isinstance(birthdate, str):
        raise ValueError("birthdate: нужна строка YYYY-MM-DD")
    try:
        birthday = date.fromisoformat(birthdate)
    except ValueError:
        raise ValueError("birthdate: нужна существующая дата YYYY-MM-DD") from None
    if birthday.isoformat() != birthdate:
        raise ValueError("birthdate: нужен формат YYYY-MM-DD")
    if birthday > date.today():
        raise ValueError("birthdate: дата рождения не может быть в будущем")
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise ValueError("gpa: нужно число, не bool")
    if not 0 <= gpa <= 5:
        raise ValueError("gpa: средний балл должен быть от 0 до 5")
    return {
        "fio": fio.strip(),
        "birthdate": birthdate,
        "group": group.strip(),
        "gpa": float(gpa),
    }


def validate_student(rec: dict) -> None:
    """Проверяет набор ключей и значения, не изменяя словарь."""
    if not isinstance(rec, dict):
        raise ValueError("Student: нужен словарь")
    if set(rec) != set(STUDENT_FIELDS):
        raise ValueError("Student: нужны ровно ключи fio, birthdate, group, gpa")
    make_student(rec["fio"], rec["birthdate"], rec["group"], rec["gpa"])


def student_age(rec: dict, today=None) -> int:
    """Считает полные годы с учётом дня рождения."""
    validate_student(rec)
    if today is None:
        today = date.today()
    birthday = date.fromisoformat(rec["birthdate"])
    age = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1
    return age


def format_student(rec: dict) -> str:
    """Выводит фамилию с инициалами, группу, возраст и средний балл."""
    validate_student(rec)
    parts = rec["fio"].split()
    initials = "".join(part[0] + "." for part in parts[1:])
    name = parts[0]
    if initials:
        name += " " + initials
    age = student_age(rec)
    if 11 <= age % 100 <= 14:
        word = "лет"
    elif age % 10 == 1:
        word = "год"
    elif age % 10 in (2, 3, 4):
        word = "года"
    else:
        word = "лет"
    return f"{name} ({rec['group'].strip()}), {age} {word}, GPA {rec['gpa']:.2f}"


def student_to_dict(rec: dict) -> dict:
    """Возвращает отдельную копию проверенной записи."""
    validate_student(rec)
    return rec.copy()


def student_from_dict(d: dict) -> dict:
    """Берёт нужные поля; лишние поля входного объекта игнорируются."""
    if not isinstance(d, dict):
        raise ValueError("Student: нужен словарь")
    for field in STUDENT_FIELDS:
        if field not in d:
            raise ValueError(f"Student: отсутствует поле {field}")
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])


def update_student(rec: dict, **fields) -> dict:
    """Создаёт изменённую запись, сохраняя исходную."""
    result = student_to_dict(rec)
    for field, value in fields.items():
        if field not in STUDENT_FIELDS:
            raise KeyError(f"Неизвестное поле: {field}")
        result[field] = value
    validate_student(result)
    return student_from_dict(result)
