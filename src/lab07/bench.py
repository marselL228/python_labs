import multiprocessing as mp
import random
import timeit
from pathlib import Path

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

def measure(action):
    times = timeit.repeat(action, number=1, repeat=3)
    return min(times)

def sort_worker(connection, fn, data):
    """Измеряет сортировку три раза."""
    try:
        for _ in range(3):
            seconds = timeit.timeit(lambda: fn(data), number=1)
            connection.send((True, seconds))
    except Exception as error:
        connection.send((False, str(error)))
    finally:
        connection.close()


def timed_sort(fn, data, limit=60):
    """Возвращает минимум времени или отметку о превышении лимита."""
    context = mp.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=sort_worker, args=(sender, fn, data))
    times = []

    try:
        process.start()
        sender.close()

        for _ in range(3):
            if not receiver.poll(limit):
                return f"> {limit:g} s"

            success, value = receiver.recv()

            if not success:
                raise RuntimeError(value)

            times.append(value)

        return min(times)
    finally:
        if process.pid is not None:
            if process.is_alive():
                process.terminate()

            process.join()

        receiver.close()
        sender.close()

def bench_sorts(n):
    data = [random.randint(-100_000, 100_000) for _ in range(n)]
    rows = []

    for fn in (bubble_sort, insertion_sort, selection_sort, sorted):
        seconds = timed_sort(fn, data)
        rows.append(("sort", n, fn.__name__, seconds))

    return rows


def bench_search():
    n = 100_000
    data = [random.randint(-100_000, 100_000) for _ in range(n)]
    queries = [random.randint(-100_000, 100_000) for _ in range(10_000)]

    preparation = measure(lambda: sorted(data))
    rows = [("search_prepare", n, "sorted", preparation)]
    sorted_data = sorted(data)

    for fn, values in ((linear_search, data), (binary_search, sorted_data)):
        seconds = measure(lambda: [fn(values, x) for x in queries])
        rows.append(("search_10000_queries", n, fn.__name__, seconds))

    return rows


def bench_two_sum(n):
    data = [random.randint(0, 100) for _ in range(n - 2)]
    data += [1000, 2000]
    target = 3000
    rows = []

    for fn in (two_sum_brute, two_sum_fast):
        seconds = measure(lambda: fn(data, target))
        rows.append(("two_sum", n, fn.__name__, seconds))

    return rows


def main():
    random.seed(42)
    rows = []

    for n in (1000, 10_000, 100_000):
        print(f"Сортировки: n={n}", flush=True)
        rows.extend(bench_sorts(n))

    print("Поиск: 10 000 запросов", flush=True)
    rows.extend(bench_search())

    for n in (1000, 10_000):
        rows.extend(bench_two_sum(n))

    root = Path(__file__).resolve().parents[2]
    path = root / "data" / "lab07" / "bench.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(rows, path, header=("task", "n", "impl", "seconds"))

    print(f"{'task':<23} {'n':>7} {'impl':<17} {'seconds':>12}")

    for task, n, impl, seconds in rows:
        value = f"{seconds:.6f}" if isinstance(seconds, float) else seconds
        print(f"{task:<23} {n:>7} {impl:<17} {value:>12}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, EOFError) as error:
        print(f"Ошибка бенчмарка: {error}")
        raise SystemExit(1)
