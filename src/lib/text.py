import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True, strip: bool = True) -> str:
    """Нормализует текст."""
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()

    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")

    text = text.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    if strip:
        text = text.strip()

    return text


def tokenize(text: str) -> list[str]:
    """Разбивает текст на слова."""
    text = normalize(text)
    tokens = re.findall(r"\w+(?:-\w+)*", text)
    return tokens


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Подсчитывает частоту каждого слова."""
    freq = {}

    for token in tokens:
        if token in freq:
            freq[token] += 1
        else:
            freq[token] = 1

    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Возвращает n самых частых слов."""
    sort_freq = sorted(
        freq.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return sort_freq[:n]


if __name__ == "__main__":
    k = "-"

    print(k * 5, "NORMALIZE", k * 5)
    print(normalize("ПрИвЕт\nМИр\t"))
    print(normalize("ёжик, Ёлка"))
    print(normalize("Hello\r\nWorld"))
    print(normalize("  двойные  пробелы  "))

    print(k * 10, "TOKENIZE", k * 10)
    print(tokenize("привет мир"))
    print(tokenize("hello,world!!!"))
    print(tokenize("по-настоящему круто"))
    print(tokenize("2025 год"))
    print(tokenize("emoji 😀 не слово"))

    print(k * 15, "COUNT_FREQ + TOP_N", k * 15)
    tokens = ["a", "b", "a", "c", "b", "a"]
    print(count_freq(tokens))
    print(top_n(count_freq(tokens), n=2))
