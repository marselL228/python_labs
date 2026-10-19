import argparse

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def json2csv(input_path, output_path):
    """Преобразует JSON в CSV."""
    json_to_csv(input_path, output_path)
    print(f"Успешная конвертация JSON в CSV! Файл сохранён: {output_path}")


def csv2json(input_path, output_path):
    """Преобразует CSV в JSON."""
    csv_to_json(input_path, output_path)
    print(f"Успешная конвертация CSV в JSON! Файл сохранён: {output_path}")


def csv2xlsx(input_path, output_path):
    """Преобразует CSV в XLSX."""
    csv_to_xlsx(input_path, output_path)
    print(f"Успешная конвертация CSV в XLSX! Файл сохранён: {output_path}")


def make_parser(description):
    """Создаёт парсер аргументов для команды конвертации."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input", required=True, help="Входной файл")
    parser.add_argument("--output", required=True, help="Выходной файл")
    return parser


def json2csv_main():
    args = make_parser("Преобразование JSON в CSV").parse_args()
    json2csv(args.input, args.output)


def csv2json_main():
    args = make_parser("Преобразование CSV в JSON").parse_args()
    csv2json(args.input, args.output)


def csv2xlsx_main():
    args = make_parser("Преобразование CSV в XLSX").parse_args()
    csv2xlsx(args.input, args.output)


def main():
    """Общий запуск команд конвертации."""
    parser = argparse.ArgumentParser(description="Конвертация файлов")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command, description in [
        ("json2csv", "Преобразовать JSON в CSV"),
        ("csv2json", "Преобразовать CSV в JSON"),
        ("csv2xlsx", "Преобразовать CSV в XLSX"),
    ]:
        subparser = subparsers.add_parser(command, help=description)
        subparser.add_argument("--input", required=True, help="Входной файл")
        subparser.add_argument("--output", required=True, help="Выходной файл")

    args = parser.parse_args()

    if args.command == "json2csv":
        json2csv(args.input, args.output)
    elif args.command == "csv2json":
        csv2json(args.input, args.output)
    elif args.command == "csv2xlsx":
        csv2xlsx(args.input, args.output)


if __name__ == "__main__":
    main()
    