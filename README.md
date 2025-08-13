# bujji_algorithms

A **memory-efficient** Data Structures & Algorithms library for Python —  
designed with clean, readable code and production-friendly implementations.

## 🚀 Features
- **Arrays Module** – Static, Dynamic, Sparse, Circular, Bit-packed arrays & more.
- **Sorting Algorithms** – From Bubble Sort to Quick Sort, Counting Sort, Radix Sort, and more.
- **String Algorithms** – Palindrome checks, pattern matching (KMP, Rabin-Karp, Z-Algorithm, Manacher’s).
- **Math Algorithms** – Prime checks, GCD/LCM, Sieve of Eratosthenes, Fibonacci (iterative & matrix), modular arithmetic.
- **Trees** – Binary Tree, BST, AVL Tree, Red-Black Tree, Segment Tree, Fenwick Tree, Trie.
- **Graphs** – Adjacency List/Matrix, Directed/Undirected, Weighted Graphs.
- **Heaps** – Min Heap, Max Heap, and D-ary Heap.

All implementations:
- **Memory-conscious** (minimal overhead, avoids Python list bloat where possible)
- **Documented** with clear docstrings and usage examples
- **Tested** with comprehensive scripts for correctness & edge cases

---

## 📦 Installation
```bash
pip install bujji_algorithms
````

*(Coming soon to PyPI — for now, clone and use locally)*

---

## 🛠 Example Usage

### Sorting Example

```python
from bujji_algorithms import sorting

arr = [5, 3, 8, 1, 2]
sorted_arr = sorting.quick_sort(arr)
print(sorted_arr)  # [1, 2, 3, 5, 8]
```

### String Algorithm Example

```python
from bujji_algorithms import string_algorithms as sa

print(sa.is_palindrome("racecar"))  # True
print(sa.kmp_search("ababcabcabababd", "ababd"))  # [10]
```

### Math Algorithm Example

```python
from bujji_algorithms import math_algorithms as ma

print(ma.is_prime(97))  # True
print(ma.gcd(48, 18))   # 6
```

---

## 📂 Modules Overview

### 1. Arrays

* `StaticArray` – Fixed-size, contiguous storage.
* `DynamicArray` – Auto-resizing array with controlled growth.
* `TwoDArray` – Row-major 2D array.
* `SparseMatrix` – Space-efficient storage for sparse data.
* `CircularArray` – Fixed-size, overwriting buffer.
* `BitArray` – Compact storage for boolean values.
* `ColumnMajor2DArray` – Optimized for column operations.
* `ImmutableArray` – Read-only array for constants.

### 2. Sorting

* Bubble Sort, Selection Sort, Insertion Sort
* Merge Sort, Quick Sort, Heap Sort
* Counting Sort, Radix Sort, Bucket Sort, Shell Sort

### 3. String Algorithms

* Palindrome Check
* Anagram Detection
* Rabin-Karp
* KMP (Knuth-Morris-Pratt)
* Z-Algorithm
* Longest Palindromic Substring
* Manacher’s Algorithm
* String Compression

### 4. Math Algorithms

* Prime Check
* GCD / LCM
* Sieve of Eratosthenes
* Fast Exponentiation
* Modular Inverse
* Fibonacci (iterative, DP, matrix)

### 5. Trees

* Binary Tree
* Binary Search Tree (BST)
* AVL Tree
* Red-Black Tree
* Segment Tree
* Fenwick Tree (Binary Indexed Tree)
* Trie

### 6. Graphs

* Adjacency List
* Adjacency Matrix
* Directed / Undirected Graph
* Weighted Graph

### 7. Heaps

* Min Heap
* Max Heap
* D-ary Heap

---

## 🧪 Testing

Every algorithm has a dedicated test script.
Run all tests with:

```bash
pytest tests/
```

Or run a specific test, e.g.:

```bash
python tests/test_sorting.py
```

---

## 📜 License

MIT License © 2025

---

**Made with ❤️ for developers who care about clean, efficient algorithms.**
