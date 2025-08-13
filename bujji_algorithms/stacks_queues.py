class Stack:
    """
    Stack (LIFO) data structure.

    Methods:
    - push(value)
    - pop()
    - peek()
    - is_empty()
    - size()
    - clear()
    - to_list()
    - display()

    Usage:

    >>> s = Stack()
    >>> s.push(10)
    >>> s.push(20)
    >>> s.peek()
    20
    >>> s.pop()
    20
    >>> len(s)
    1
    >>> list(s)
    [10]
    """
    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def clear(self):
        self._data.clear()

    def to_list(self):
        return self._data[::-1]

    def display(self):
        print("Stack (top -> bottom):")
        for elem in reversed(self._data):
            print(elem)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return reversed(self._data)


class Queue:
    """
    Queue (FIFO) data structure.

    Methods:
    - enqueue(value)
    - dequeue()
    - peek()
    - is_empty()
    - size()
    - clear()
    - to_list()
    - display()

    Usage:

    >>> q = Queue()
    >>> q.enqueue(1)
    >>> q.enqueue(2)
    >>> q.peek()
    1
    >>> q.dequeue()
    1
    >>> len(q)
    1
    """
    def __init__(self):
        self._data = []

    def enqueue(self, value):
        self._data.append(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def clear(self):
        self._data.clear()

    def to_list(self):
        return self._data[:]

    def display(self):
        print("Queue (front -> rear):")
        for elem in self._data:
            print(elem)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


class CircularQueue:
    """
    Circular Queue with fixed capacity.

    Methods:
    - enqueue(value)
    - dequeue()
    - peek()
    - is_empty()
    - is_full()
    - size()
    - clear()
    - to_list()
    - display()

    Usage:

    >>> cq = CircularQueue(3)
    >>> cq.enqueue(10)
    >>> cq.enqueue(20)
    >>> cq.dequeue()
    10
    >>> cq.enqueue(30)
    >>> list(cq)
    [20, 30]
    """
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._data = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0

    def enqueue(self, value):
        if self.is_full():
            raise OverflowError("enqueue on full circular queue")
        self._data[self._rear] = value
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty circular queue")
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty circular queue")
        return self._data[self._front]

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def size(self):
        return self._size

    def clear(self):
        self._data = [None] * self._capacity
        self._front = 0
        self._rear = 0
        self._size = 0

    def to_list(self):
        result = []
        idx = self._front
        for _ in range(self._size):
            result.append(self._data[idx])
            idx = (idx + 1) % self._capacity
        return result

    def display(self):
        print("CircularQueue (front -> rear):")
        print(" -> ".join(str(x) for x in self.to_list()))

    def __len__(self):
        return self._size

    def __iter__(self):
        idx = self._front
        count = 0
        while count < self._size:
            yield self._data[idx]
            idx = (idx + 1) % self._capacity
            count += 1


class Deque:
    """
    Deque (Double-Ended Queue) data structure.

    Methods:
    - append(value)        # add right end
    - appendleft(value)    # add left end
    - pop()                # remove from right end
    - popleft()            # remove from left end
    - peek_right()
    - peek_left()
    - is_empty()
    - size()
    - clear()
    - to_list()
    - display()

    Usage:

    >>> d = Deque()
    >>> d.append(1)
    >>> d.appendleft(0)
    >>> d.pop()
    1
    >>> d.popleft()
    0
    """
    def __init__(self):
        self._data = []

    def append(self, value):
        self._data.append(value)

    def appendleft(self, value):
        self._data.insert(0, value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty deque")
        return self._data.pop()

    def popleft(self):
        if self.is_empty():
            raise IndexError("popleft from empty deque")
        return self._data.pop(0)

    def peek_right(self):
        if self.is_empty():
            raise IndexError("peek_right from empty deque")
        return self._data[-1]

    def peek_left(self):
        if self.is_empty():
            raise IndexError("peek_left from empty deque")
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def clear(self):
        self._data.clear()

    def to_list(self):
        return self._data[:]

    def display(self):
        print("Deque (left -> right):")
        print(" <-> ".join(str(x) for x in self._data))

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


import heapq

class PriorityQueue:
    """
    Priority Queue data structure.

    Methods:
    - push(priority, value)
    - pop()                # returns value with lowest priority
    - peek()
    - is_empty()
    - size()
    - clear()
    - to_list()            # returns sorted list without altering PQ
    - display()

    Usage:

    >>> pq = PriorityQueue()
    >>> pq.push(2, "low")
    >>> pq.push(1, "high")
    >>> pq.pop()
    'high'
    """
    def __init__(self):
        self._heap = []

    def push(self, priority, value):
        heapq.heappush(self._heap, (priority, value))

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._heap)[1]

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        return self._heap[0][1]

    def is_empty(self):
        return len(self._heap) == 0

    def size(self):
        return len(self._heap)

    def clear(self):
        self._heap.clear()

    def to_list(self):
        # Return values sorted by priority (lowest first)
        return [v for p, v in sorted(self._heap)]

    def display(self):
        print("PriorityQueue (lowest priority first):")
        for p, v in sorted(self._heap):
            print(f"Priority: {p}, Value: {v}")

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        # Iterate values sorted by priority
        for _, v in sorted(self._heap):
            yield v


def real_world_examples():
    """
    Stacks & Queues Module — Real World Usage Examples
    ==================================================

    1. Stack
       Scenario:
           Undo functionality in a text editor storing previous states.
       If Using Python List:
           - List append/pop works but may cause resizing overhead.
       If Using Stack:
           - Optimized for LIFO operations.
       Production Benefit:
           Ideal for LIFO needs with clear API.

    2. Queue
       Scenario:
           Print job scheduling where first job submitted is printed first.
       If Using Python List:
           - Inefficient to pop front (O(n)).
       If Using Queue:
           - Efficient FIFO operations.
       Production Benefit:
           Perfect for FIFO task management.

    3. CircularQueue
       Scenario:
           Fixed-size buffer for streaming data like audio samples.
       If Using Python List:
           - Manual index wrap-around required.
       If Using CircularQueue:
           - Automatically manages circular buffer indexing.
       Production Benefit:
           Efficient fixed capacity buffer.

    4. Deque
       Scenario:
           Browser tabs where users can open/close tabs from both ends.
       If Using Python List:
           - Inefficient insertions/removals at front.
       If Using Deque:
           - O(1) insertions/removals at both ends.
       Production Benefit:
           Great for double-ended queue operations.

    5. PriorityQueue
       Scenario:
           Task scheduling with priority-based execution.
       If Using Python List:
           - Manual sorting needed on each insertion.
       If Using PriorityQueue:
           - Automatically maintains heap order.
       Production Benefit:
           Perfect for prioritized job queues.

    """
    print(real_world_examples.__doc__)


def list_classes():
    """
    List all available stack and queue classes in the stacks_queues module.
    """
    print(", ".join(__all__[:-1]))


__all__ = [
    "Stack",
    "Queue",
    "CircularQueue",
    "Deque",
    "PriorityQueue",
    "real_world_examples",
    "list_classes",
]
