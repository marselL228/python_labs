"""Консольная CRUD-утилита для CSV-хранилища студентов."""

import argparse
import json
import sys

from src.lab08.models import format_student, student_from_dict
from src.lab09 import group

DEFAULT_DB = "data/lab09/students.csv"


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер с подкомандами CRUD."""
    parser = argparse.ArgumentParser(
        description="CRUD-утилита для базы студентов"
    )
    parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help="путь к CSV-хранилищу",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_parser = subparsers.add_parser(
        "add",
        help="добавить студента",
    )
    add_parser.add_argument("--fio", required=True)
    add_parser.add_argument("--birthdate", required=True)
    add_parser.add_argument("--group", required=True)
    add_parser.add_argument("--gpa", required=True)

    list_parser = subparsers.add_parser(
        "list",
        help="вывести всех студентов",
    )
    list_parser.add_argument(
        "--sort",
        choices=("fio", "gpa"),
    )

    find_parser = subparsers.add_parser(
        "find",
        help="найти студентов по подстроке в ФИО",
    )
    find_parser.add_argument("--q", required=True)

    remove_parser = subparsers.add_parser(
        "remove",
        help="удалить студентов по ФИО",
    )
    remove_parser.add_argument("--fio", required=True)

    update_parser = subparsers.add_parser(
        "update",
        help="обновить данные студента",
    )
    update_parser.add_argument("--fio", required=True)
    update_parser.add_argument("--birthdate")
    update_parser.add_argument("--group")
    update_parser.add_argument("--gpa")

    subparsers.add_parser("stats", help="вывести статистику по студентам и группам")

    return parser


def print_students(students: list[dict]) -> None:
    """Печатает по одной записи студента на строку."""
    for student in students:
        print(format_student(student))


def main() -> int:
    """Выполняет выбранную подкоманду."""
    args = build_parser().parse_args()

    try:
        if args.command == "add":
            student = student_from_dict(
                {
                    "fio": args.fio,
                    "birthdate": args.birthdate,
                    "group": args.group,
                    "gpa": float(args.gpa),
                }
            )

            group.add_student(args.db, student)
            print(f"Добавлен: {format_student(student)}")

        elif args.command == "list":
            students = group.list_students(
                args.db,
                sort_by=args.sort,
            )
            print_students(students)

        elif args.command == "find":
            students = group.find_students(args.db, args.q)
            print_students(students)

        elif args.command == "remove":
            removed_count = group.remove_student(
                args.db,
                args.fio,
            )
            print(f"Удалено записей: {removed_count}")

        elif args.command == "update":
            fields = {
                name: value
                for name, value in (
                    ("birthdate", args.birthdate),
                    ("group", args.group),
                    (
                        "gpa",
                        float(args.gpa)
                        if args.gpa is not None
                        else None,
                    ),
                )
                if value is not None
            }

            if not fields:
                raise ValueError(
                    "не указаны поля для обновления"
                )

            if group.update_student(
                args.db,
                args.fio,
                **fields,
            ):
                print(f"Обновлена запись: {args.fio}")
            else:
                print(
                    f"Студент не найден: {args.fio}",
                    file=sys.stderr,
                )
                return 1

        elif args.command == "stats":
            print(json.dumps(group.stats(args.db), ensure_ascii=False, indent=2))

    except (KeyError, OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
    
