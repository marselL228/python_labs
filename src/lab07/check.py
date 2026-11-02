
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
    for _ in range(trials):
        n = random.randint(2, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]

        # Создаём сумму двух разных элементов
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

        while i == j:
            j = random.randint(0, n - 1)

        target = nums[i] + nums[j]

        # Проверяем оба алгоритма
        for fn in (two_sum_brute, two_sum_fast):
            result = fn(nums, target)

            assert result is not None, f"{fn.__name__} не нашла пару в {nums}"

            first, second = result

            assert first != second and nums[first] + nums[second] == target, (
                f"{fn.__name__} вернула неправильную пару: {result}, список: {nums}"
            )


if __name__ == "__main__":
    random.seed(42)

    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn)

    check_search()
    check_two_sum()

    print("OK")
