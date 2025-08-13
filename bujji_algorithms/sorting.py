def bubble_sort(arr):
    """
    Bubble Sort Algorithm
    
    Repeatedly swaps adjacent elements if they are in the wrong order,
    "bubbling" the largest unsorted element to the end each pass.
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    Stability: Stable
    
    Use case: Simple teaching algorithm, small or nearly sorted arrays.
    
    Example:
    >>> bubble_sort([5, 3, 8, 4, 2])
    [2, 3, 4, 5, 8]
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr):
    """
    Selection Sort Algorithm
    
    Selects the minimum element from unsorted portion and swaps it
    with the first unsorted element.
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    Stability: Not stable by default
    
    Use case: Small arrays, scenarios minimizing writes.
    
    Example:
    >>> selection_sort([64, 25, 12, 22, 11])
    [11, 12, 22, 25, 64]
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    """
    Insertion Sort Algorithm
    
    Builds the sorted array one element at a time by inserting each element
    into its proper place in the already sorted portion.
    
    Time Complexity: O(n^2) worst, O(n) best (nearly sorted)
    Space Complexity: O(1)
    Stability: Stable
    
    Use case: Small or nearly sorted arrays.
    
    Example:
    >>> insertion_sort([12, 11, 13, 5, 6])
    [5, 6, 11, 12, 13]
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr


def merge_sort(arr):
    """
    Merge Sort Algorithm
    
    Divide-and-conquer algorithm that splits the array into halves,
    recursively sorts them, and merges sorted halves.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    Stability: Stable
    
    Use case: Large datasets, stable sort, external sorting.
    
    Example:
    >>> merge_sort([12, 11, 13, 5, 6, 7])
    [5, 6, 7, 11, 12, 13]
    """
    if len(arr) <= 1:
        return arr
    
    def merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def quick_sort(arr, low=0, high=None):
    """
    Quick Sort Algorithm
    
    Partition-based sort using a pivot element, recursively sorting
    elements less than and greater than pivot.
    
    Time Complexity: O(n log n) average, O(n^2) worst
    Space Complexity: O(log n) (recursive stack)
    Stability: Not stable
    
    Use case: General-purpose in-place sorting.
    
    Example:
    >>> arr = [10, 7, 8, 9, 1, 5]
    >>> quick_sort(arr)
    [1, 5, 7, 8, 9, 10]
    """
    if high is None:
        high = len(arr) - 1
    
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i + 1
    
    if low < high:
        pi = partition(low, high)
        quick_sort(arr, low, pi-1)
        quick_sort(arr, pi+1, high)
    return arr


def heap_sort(arr):
    """
    Heap Sort Algorithm
    
    Converts array into a max-heap and repeatedly extracts max element,
    sorting the array in-place.
    
    Time Complexity: O(n log n)
    Space Complexity: O(1)
    Stability: Not stable
    
    Use case: In-place sorting with guaranteed O(n log n).
    
    Example:
    >>> heap_sort([12, 11, 13, 5, 6, 7])
    [5, 6, 7, 11, 12, 13]
    """
    def heapify(n, i):
        largest = i
        l = 2*i + 1
        r = 2*i + 2
        
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)
    
    n = len(arr)
    
    # Build max heap
    for i in range(n//2 - 1, -1, -1):
        heapify(n, i)
    
    # Extract elements one by one
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    return arr


def counting_sort(arr, max_value=None):
    """
    Counting Sort Algorithm
    
    Non-comparative sorting for integers with a known small range.
    
    Time Complexity: O(n + k), where k = max value
    Space Complexity: O(k)
    Stability: Stable
    
    Use case: Sorting integers when range is small and known.
    
    Example:
    >>> counting_sort([4, 2, 2, 8, 3, 3, 1])
    [1, 2, 2, 3, 3, 4, 8]
    """
    if not arr:
        return []
    if max_value is None:
        max_value = max(arr)
    
    count = [0] * (max_value + 1)
    for num in arr:
        count[num] += 1
    
    sorted_arr = []
    for num, c in enumerate(count):
        sorted_arr.extend([num] * c)
    return sorted_arr


def radix_sort(arr):
    """
    Radix Sort Algorithm
    
    Non-comparative integer sorting algorithm that sorts numbers digit by digit,
    starting from least significant digit.
    
    Time Complexity: O(d * (n + k)), d = digits, k = base (usually 10)
    Space Complexity: O(n + k)
    Stability: Stable
    
    Use case: Sorting integers or strings with fixed length.
    
    Example:
    >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
    [2, 24, 45, 66, 75, 90, 170, 802]
    """
    if not arr:
        return []
    
    max_num = max(arr)
    exp = 1  # digit position
    
    def counting_sort_exp(arr, exp):
        output = [0] * len(arr)
        count = [0] * 10
        
        for num in arr:
            index = (num // exp) % 10
            count[index] += 1
        
        for i in range(1, 10):
            count[i] += count[i-1]
        
        for i in reversed(range(len(arr))):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
        
        return output
    
    output = arr
    while max_num // exp > 0:
        output = counting_sort_exp(output, exp)
        exp *= 10
    
    return output


def bucket_sort(arr, bucket_size=5):
    """
    Bucket Sort Algorithm
    
    Distributes elements into buckets, sorts each bucket individually,
    then concatenates results.
    
    Time Complexity: Average O(n + k), worst O(n^2)
    Space Complexity: O(n + k)
    Stability: Depends on sorting algorithm used on buckets.
    
    Use case: Uniformly distributed data like floats in [0,1).
    
    Example:
    >>> bucket_sort([0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51])
    [0.23, 0.25, 0.32, 0.42, 0.47, 0.51, 0.52]
    """
    if not arr:
        return []
    
    min_value, max_value = min(arr), max(arr)
    bucket_count = (max_value - min_value) // bucket_size + 1
    
    buckets = [[] for _ in range(int(bucket_count))]
    
    for num in arr:
        index = int((num - min_value) // bucket_size)
        buckets[index].append(num)
    
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))
    return sorted_arr


def shell_sort(arr):
    """
    Shell Sort Algorithm
    
    Generalization of insertion sort that allows swapping distant elements.
    
    Time Complexity: Depends on gap sequence; approx O(n^(3/2)) to O(n log^2 n)
    Space Complexity: O(1)
    Stability: Not stable
    
    Use case: Medium-sized arrays, in-place improvement over insertion sort.
    
    Example:
    >>> shell_sort([12, 34, 54, 2, 3])
    [2, 3, 12, 34, 54]
    """
    n = len(arr)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j-gap] > temp:
                arr[j] = arr[j-gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def real_world_examples():
    """
    Sorting Algorithms Module — Real World Usage Examples
    =====================================================

    1. Bubble Sort
       Scenario:
           Educational purposes or very small datasets.
       Benefit:
           Simple to understand but inefficient for large data.

    2. Selection Sort
       Scenario:
           Small datasets where memory writes are costly.
       Benefit:
           Minimizes swaps, good for memory-constrained environments.

    3. Insertion Sort
       Scenario:
           Nearly sorted data such as live data streams.
       Benefit:
           Very efficient on mostly sorted datasets.

    4. Merge Sort
       Scenario:
           External sorting of large datasets on disk.
       Benefit:
           Stable and O(n log n), suitable for linked lists and large data.

    5. Quick Sort
       Scenario:
           General purpose sorting in-memory.
       Benefit:
           Very fast average case, used widely in standard libraries.

    6. Heap Sort
       Scenario:
           Systems requiring guaranteed O(n log n) worst case.
       Benefit:
           In-place and no extra memory.

    7. Radix Sort
       Scenario:
           Sorting integers or fixed-length strings.
       Benefit:
           Linear time for small range integers.

    8. Counting Sort
       Scenario:
           Sorting small range integers efficiently.
       Benefit:
           Non-comparative, very fast for known limited ranges.

    9. Bucket Sort
       Scenario:
           Uniformly distributed data over a range.
       Benefit:
           Distributes sort workload for faster average sorting.

    10. Shell Sort
       Scenario:
           Medium-sized arrays with some unordered elements.
       Benefit:
           Improved insertion sort for distant elements.

    """
    print(real_world_examples.__doc__)


__all__ = [
    "bubble_sort", "selection_sort", "insertion_sort", "merge_sort",
    "quick_sort", "heap_sort", "radix_sort", "counting_sort",
    "bucket_sort", "shell_sort", "real_world_examples"
]
