###min_max
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if len(nums) == 0:
        raise ValueError('Пустой список')
    min_num = nums[0]
    max_num = nums[0]
    for num in nums:
        if num < min_num:
            min_num = num
        if num > max_num:
            max_num = num
    return min_num, max_num

#print(min_max([3, -1, 5, 5, 0]))
#print(min_max([42]))
#print(min_max([-5, -2, -9]))
#print(min_max([1.5, 2, 2.0, -3.1]))
#print(min_max([]))

###unique sorted
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    a = []
    for num in nums:
        if num not in a:
            a.append(num)
    for i in range(1, len(a)):
        b = a[i]
        j = i - 1
        while j >= 0 and a[j] > b:
            a[j + 1] = a[j]
            j -= 1
            a[j + 1] = b
    return a

#print(unique_sorted([3, 1, 2, 1, 3]))
#print(unique_sorted([]))
#print(unique_sorted([-1, -1, 0, 2, 2]))
#print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))


###flatten
def flatten(mat: list[list | tuple]) -> list:
    if len(mat) == 0:
        raise ValueError('Пустая матрица')
    if all(isinstance(x, (list, tuple)) for x in mat):
        return [a for i in mat for a in i]
    else:
        raise TypeError("строка не строка строк матрицы")
print(flatten([[1, 2], [3, 4]]))
print(flatten([[1, 2], (3, 4, 5)]))
print(flatten([[1], [], [2, 3]]))
print(flatten([[1, 2], "ab"]))