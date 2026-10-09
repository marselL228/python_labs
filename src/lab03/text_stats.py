from src.lib.text import normalize, tokenize, count_freq, top_n
import sys
def main() -> None:
    a = sys.stdin.read()

    norm = normalize(a)
    tokens = tokenize(norm)
    freq = count_freq(tokens)
    totalwords = len(tokens)
    uniqewords = len(freq)

    print(f'Всего слов: {totalwords}')
    print(f'Уникальных слов: {uniqewords}')
    print('Топ-5:')
    for word, count in top_n(freq, 5):
        print(f'{word}:{count}')

if __name__ == '__main__':
    main()
