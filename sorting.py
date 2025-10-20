import random
import time
import sys
 
# Increase recursion limit for large quicksorts
sys.setrecursionlimit(10000)
 
# Track memory and recursion depth
merge_sort_memory = 0
quick_sort_recursion_depth = 0
max_quick_sort_recursion_depth = 0
 
 
# ----------------- Sorting Algorithms -----------------
 
# Bubble Sort (O(1) space)
def bubble_sort(array):
    n = len(array)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
 
 
# Insertion Sort (O(1) space)
def insertion_sort(array):
    n = len(array)
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
 
 
# Merge Sort (O(n) space)
def merge_sort(array):
    global merge_sort_memory
    if len(array) <= 1:
        return array
 
    mid = len(array) // 2
    left = array[:mid]
    right = array[mid:]
 
    # Simulate extra memory used
    merge_sort_memory += len(left) + len(right)
 
    left = merge_sort(left)
    right = merge_sort(right)
 
    return merge(left, right)
 
 
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
 
 
# QuickSort (O(log n) space)
def quick_sort(array, left, right):
    global quick_sort_recursion_depth, max_quick_sort_recursion_depth
 
    if left < right:
        quick_sort_recursion_depth += 1
        max_quick_sort_recursion_depth = max(max_quick_sort_recursion_depth, quick_sort_recursion_depth)
 
        pivot = partition(array, left, right)
        quick_sort(array, left, pivot - 1)
        quick_sort(array, pivot + 1, right)
 
        quick_sort_recursion_depth -= 1
 
 
def partition(array, left, right):
    pivot = array[right]
    i = left - 1
    for j in range(left, right):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[right] = array[right], array[i + 1]
    return i + 1
 
 
# ----------------- Helpers -----------------
 
def generate_random_array(size):
    return [random.randint(1, 10000) for _ in range(size)]
 
 
def measure_time_and_space(sort_method, array, description):
    global merge_sort_memory, max_quick_sort_recursion_depth
    merge_sort_memory = 0
    max_quick_sort_recursion_depth = 0
 
    start_time = time.time()
 
    if description == "Merge Sort":
        sort_method(array)
    elif description == "QuickSort":
        sort_method(array, 0, len(array) - 1)
    else:
        sort_method(array)
 
    elapsed_time = (time.time() - start_time) * 1000  # ms
    print(f"{description} took {elapsed_time:.2f} ms")
 
    if description == "Merge Sort":
        print(f"Memory used by Merge Sort: {merge_sort_memory} elements (O(n) space)")
    elif description == "QuickSort":
        print(f"Max recursion depth of QuickSort: {max_quick_sort_recursion_depth} (O(log n) space on average)")
 
 
# ----------------- Main -----------------
 
if __name__ == "__main__":
    sizes = [100, 1000, 50000]
 
    for size in sizes:
        print(f"\nArray Size: {size}")
 
        random_array = generate_random_array(size)
 
        measure_time_and_space(bubble_sort, random_array.copy(), "Bubble Sort")
        measure_time_and_space(insertion_sort, random_array.copy(), "Insertion Sort")
        measure_time_and_space(lambda arr: merge_sort(arr), random_array.copy(), "Merge Sort")
        measure_time_and_space(quick_sort, random_array.copy(), "QuickSort")