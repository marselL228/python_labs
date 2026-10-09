###ЛР3
import re
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True, strip: bool = True) -> str:
    if casefold == True:
        text = text.casefold()
    else:
        text = text.lower()
    if yo2e == True: text = text.replace('ё', 'е').replace('Ё','Е')
    if '\t' in text or '\n' in text or '\r' in text:
        text = text.replace('\t',' ').replace('\r',' ').replace('\n',' ')
    text = re.sub(r'\s+', ' ', text)
    if strip == True: text = text.strip()
    return text
k = '-' 
print(k * 5, 'NORMALIZE', k * 5)
print(normalize('ПрИвЕт\nМИр\t'))
print(normalize('ёжик, Ёлка'))
print(normalize('Hello\r\nWorld'))
print(normalize('  двойные  пробелы  '))
print(k*20)

def tokenize(text: str) -> list[str]:
    text = normalize(text)
    tokens = re.findall(r'\w+(?:-\w+)*', text)
    return tokens
print(k * 10, 'TOKENIZE', k * 10)
print(tokenize('привет мир'))
print(tokenize('hello,world!!!'))
print(tokenize('по-настоящему круто'))
print(tokenize('2025 год'))
print(tokenize('emoji 😀 не слово'))
print(k*30)

def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}
    for token in tokens:
        if token in freq:
            freq[token] += 1
        else:
            freq[token] = 1
    return freq
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    sort_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sort_freq[:n]
print(k * 15, 'COUNT_FREQ + TOP_N', k * 15)
print(count_freq(['a','b','a','c','b','a']))
print(top_n(count_freq(['a','b','a','c','b','a']), n=2))
print(count_freq(['bb','aa','bb','aa','cc']))
print(top_n(count_freq(['bb','aa','bb','aa','cc']), n=2))
print(k*54)
