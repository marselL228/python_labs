
import random

from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast


def check_sorting(fn, trials=100):
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        original = list(nums)
        result = fn(nums)

        assert result == sorted(nums), f"{fn.__name__} ошибься на {nums}: {result}"
        assert nums == original, f"{fn.__name__} изменил исходный список"


def check_search(trials=100):
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        x = random.randint(-110, 110)

        # Проверка линейного поиска
        result = linear_search(nums, x)
        expected = nums.index(x) if x in nums else -1

        assert result == expected, f"linear_search ошиблась на {nums}, искали {x}: {result}"

        # Проверка бинарного поиска
        sorted_nums = sorted(nums)
        result = binary_search(sorted_nums, x)

        if x in sorted_nums:
            assert result != -1 and sorted_nums[result] == x, (
                f"binary_search ошиблась на {sorted_nums}, искали {x}: {result}"
            )
        else:
            assert result == -1, f"binary_search нашла отсутствующий элемент {x}"


def check_two_sum(trials=100):
    cases = [
        ([], 0),
        ([5], 10),
        ([1, 2], 10),
        ([3, 3], 6),
        ([-3, 1, 4], 1),
    ]

    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        target = random.randint(-200, 200)

        cases.append((nums, target))

    for nums, target in cases:
        brute = two_sum_brute(nums, target)
        fast = two_sum_fast(nums, target)

        assert (brute is None) == (fast is None), (
            f"Алгоритмы расходятся: nums={nums}, target={target}, "
            f"brute={brute}, fast={fast}"
        )

        for result in (brute, fast):
            if result is not None:
                i, j = result

                assert 0 <= i < j < len(nums), (
                    f"Некорректные индексы: {result}, nums={nums}"
                )

                assert nums[i] + nums[j] == target, (
                    f"Неверная сумма: nums={nums}, "
                    f"target={target}, result={result}"
                )


if __name__ == "__main__":
    random.seed(42)

    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn)

    check_search()
    check_two_sum()

    print("OK")
