import csv
import sys
from pathlib import Path
from typing import Iterable, Sequence

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """
    Читает текстовый файл целиком и возвращает его содержимое
    как одну строку.

    По умолчанию файл читается в кодировке UTF-8. Если нужен другой
    формат кодировки, можно передать его явно, например:
        read_text("data/input.txt", encoding="cp1251")

    Если файл не найден - функция не перехватывает ошибку,
    а даёт ей "всплыть" наружу как FileNotFoundError.
    Если кодировка не подходит к содержимому файла - аналогично
    всплывает UnicodeDecodeError.
    
    Если файл пустой - возвращается пустая строка "".
    """
    p = Path(path)
    return p.read_text(encoding=encoding)


def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    """
    Записывает строки rows в CSV-файл path с разделителем ",".

    Если указан header - он записывается первой строкой файла.
    Если длины строк или заголовка не совпадают, возникает ValueError.
    """
    p = Path(path)
    rows = list(rows)

    try:
        if rows:
            expected_length = len(rows[0])

            for r in rows:
                if len(r) != expected_length:
                    raise ValueError("Все строки должны иметь одинаковую длину")

        else:
            expected_length = len(header) if header is not None else None

        if header is not None and expected_length is not None:
            if len(header) != expected_length:
                raise ValueError("Длина заголовка должна совпадать с длиной строк")

    except ValueError:
        raise

    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        if header is not None:
            w.writerow(header)

        for r in rows:
            w.writerow(r)


if __name__ == '__main__':
    print(read_text('data/lab_04/input.txt'))

    write_csv([("word", "count"), ("test", 3)], "data/lab_04/check.csv")
    print('csv создан')
