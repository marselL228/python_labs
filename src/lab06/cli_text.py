
import argparse

from src.lab04.io_txt_csv import read_text
from src.lib.text import normalize, tokenize, count_freq, top_n

def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("--top должен быть больше 0")
    return number


def cat(input_path, number_lines=False):
    """Выводит содержимое файла."""
    text = read_text(input_path)

    for i, line in enumerate(text.splitlines(), start=1):
        if number_lines:
            print(f"{i}\t{line}")
        else:
            print(line)


def stats(input_path, top=5):
    """Выводит самые частые слова."""
    if top < 1:
        raise ValueError("Параметр --top должен быть положительным")

    text = normalize(read_text(input_path))
    frequencies = count_freq(tokenize(text))

    for word, count in top_n(frequencies, top):
        print(f"{word}: {count}")


def cat_main():
    """Точка входа команды cat."""
    parser = argparse.ArgumentParser(description="Вывод содержимого файла")
    parser.add_argument("--input", required=True, help="Входной файл")
    parser.add_argument("-n", action="store_true", help="Нумеровать строки")
    args = parser.parse_args()
    cat(args.input, args.n)


def stats_main():
    """Точка входа команды stats."""
    parser = argparse.ArgumentParser(description="Статистика частоты слов")
    parser.add_argument("--input", required=True, help="Входной файл")
    parser.add_argument("--top", type=positive_int, default=5, help="Количество слов")
    args = parser.parse_args()
    stats(args.input, args.top)


def main():
    """Общий запуск текстовых команд."""
    parser = argparse.ArgumentParser(description="Работа с текстовыми файлами")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True, help="Входной файл")
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats_parser = subparsers.add_parser("stats", help="Подсчитать частоту слов")
    stats_parser.add_argument("--input", required=True, help="Входной файл")
    stats_parser.add_argument("--top", type=positive_int, default=5, help="Количество слов")

    args = parser.parse_args()

    if args.command == "cat":
        cat(args.input, args.n)
    elif args.command == "stats":
        stats(args.input, args.top)


if __name__ == "__main__":
    main()
