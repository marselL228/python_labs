def bubble_sort(nums):
    """пузырьком"""
    """Новый список, отсортированный по возрастанию. Исходный не меняется."""
    result = nums.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


 
 
def insertion_sort(nums):
    """вставками"""
    """Тот же контракт, что у bubble_sort."""
    result = nums.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and key < result[j]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result
 
 
def selection_sort(nums):
    """выбором"""
    """Тот же контракт, что у bubble_sort."""
    result = nums.copy()
    for i in range(len(result)):
        min_idx = i
        for j in range(i + 1, len(result)):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result
    