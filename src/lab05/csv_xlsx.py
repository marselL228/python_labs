import csv
from pathlib import Path
from openpyxl import Workbook


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    try:
        csv_path = Path(csv_path)
        xlsx_path = Path(xlsx_path)

        if csv_path.suffix.lower() != ".csv":
            raise ValueError("Входной файл должен быть CSV")

        if xlsx_path.suffix.lower() != ".xlsx":
            raise ValueError("Выходной файл должен быть XLSX")

        with csv_path.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        if not rows or not rows[0] or not any(cell.strip() for cell in rows[0]):
            raise ValueError("CSV пустой или не содержит заголовок")

        if len(rows) < 2:
            raise ValueError("CSV не содержит строк с данными")

        xlsx_path.parent.mkdir(parents=True, exist_ok=True)

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Sheet1"

        for row in rows:
            worksheet.append(row)

        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                if cell.value is not None:
                    max_length = max(max_length, len(str(cell.value)))

            worksheet.column_dimensions[column_letter].width = max(
                8, max_length + 2
            )

        workbook.save(xlsx_path)
        workbook.close()

    except FileNotFoundError:
        print(f"Ошибка: файл {csv_path} не найден")
        raise
    except PermissionError:
        print("Ошибка: нет доступа к файлу")
        raise
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise

        