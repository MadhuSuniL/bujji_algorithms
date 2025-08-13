"""
Heaps Module
============

Implements:
    - MinHeap
    - MaxHeap
    - DAryHeap

All heaps are implemented using arrays (Python lists) for efficiency.
"""

class MinHeap:
    """
    MinHeap — Binary Heap where the smallest element is always at the root.
    
    Use Case:
        Priority scheduling systems where the smallest value should be processed first.
    
    Methods:
        insert(value)     → Add an element to the heap.
        extract_min()     → Remove and return the smallest element.
        peek_min()        → Return smallest element without removing.
        build_heap(data)  → Build heap from iterable.
        is_empty()        → Return True if heap is empty.
        to_list()         → Return heap elements as a list.
    """
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def to_list(self):
        return list(self.heap)

    def peek_min(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        self._swap(0, len(self.heap) - 1)
        min_value = self.heap.pop()
        self._heapify_down(0)
        return min_value

    def build_heap(self, iterable):
        self.heap = list(iterable)
        for i in reversed(range(len(self.heap) // 2)):
            self._heapify_down(i)

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


class MaxHeap:
    """
    MaxHeap — Binary Heap where the largest element is always at the root.
    
    Use Case:
        Leaderboards or priority queues where the largest value has priority.
    """
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def to_list(self):
        return list(self.heap)

    def peek_max(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        self._swap(0, len(self.heap) - 1)
        max_value = self.heap.pop()
        self._heapify_down(0)
        return max_value

    def build_heap(self, iterable):
        self.heap = list(iterable)
        for i in reversed(range(len(self.heap) // 2)):
            self._heapify_down(i)

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] > self.heap[parent]:
            self._swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left
        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right
        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


class DAryHeap:
    """
    DAryHeap — Generalized heap where each node can have `d` children.
    
    By default, it is a Min-Heap.
    
    Use Case:
        Faster decrease-key operations in algorithms like Dijkstra's (when d > 2).
    """
    def __init__(self, d=2):
        if d < 2:
            raise ValueError("d must be >= 2")
        self.d = d
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def to_list(self):
        return list(self.heap)

    def peek(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        self._swap(0, len(self.heap) - 1)
        min_value = self.heap.pop()
        self._heapify_down(0)
        return min_value

    def build_heap(self, iterable):
        self.heap = list(iterable)
        for i in reversed(range(len(self.heap) // self.d + 1)):
            self._heapify_down(i)

    def _heapify_up(self, index):
        parent = (index - 1) // self.d
        while index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            index = parent
            parent = (index - 1) // self.d

    def _heapify_down(self, index):
        smallest = index
        for k in range(1, self.d + 1):
            child = self.d * index + k
            if child < len(self.heap) and self.heap[child] < self.heap[smallest]:
                smallest = child
        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


def real_world_examples():
    """
    Heaps Module — Real World Usage Examples
    ========================================

    1. MinHeap:
        - Task scheduling where earliest deadline is highest priority.
        - Example: CPU job scheduling.

    2. MaxHeap:
        - Leaderboards, extracting top scores.
        - Example: Gaming leaderboards.

    3. DAryHeap:
        - Graph algorithms like Dijkstra's for large branching factors.
        - Example: Network routing in telecom.
    """
    print(real_world_examples.__doc__)


def list_classes():
    print(", ".join(__all__[:-2]))


__all__ = ["MinHeap", "MaxHeap", "DAryHeap", "real_world_examples", "list_classes"]
