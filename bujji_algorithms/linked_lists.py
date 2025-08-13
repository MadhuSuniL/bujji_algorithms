import random

class SinglyNode:
    """Node for Singly Linked List."""
    __slots__ = ['value', 'next']
    def __init__(self, value=None):
        self.value = value
        self.next = None


class DoublyNode:
    """Node for Doubly Linked List."""
    __slots__ = ['value', 'next', 'prev']
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None


class SinglyNode:
    """Node for Singly Linked List."""
    __slots__ = ['value', 'next']
    def __init__(self, value=None):
        self.value = value
        self.next = None


class SkipListNode:
    """Node for SkipList."""
    __slots__ = ['value', 'forwards']

    def __init__(self, value=None, level=0):
        self.value = value
        self.forwards = [None] * (level + 1)


class SinglyLinkedList:
    """
    Singly Linked List implementation.

    Each node contains a value and a pointer to the next node.
    Supports efficient appends, prepends, and traversal.

    Usage:
    >>> sll = SinglyLinkedList()
    >>> sll.append(1)
    >>> sll.prepend(0)
    >>> sll.insert(1, 0.5)  # Insert 0.5 at index 1
    >>> sll.to_list()
    [0, 0.5, 1]
    >>> sll.display()
    0 -> 0.5 -> 1 -> None
    >>> sll.remove(0.5)
    True
    >>> len(sll)
    2
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        """Add value at the end."""
        new_node = SinglyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def prepend(self, value):
        """Add value at the start."""
        new_node = SinglyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1

    def insert(self, index, value):
        """Insert value at specified index."""
        if index < 0 or index > self.length:
            raise IndexError("Index out of bounds")
        if index == 0:
            self.prepend(value)
            return
        if index == self.length:
            self.append(value)
            return
        new_node = SinglyNode(value)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.length += 1

    def remove(self, value):
        """Remove first node with the given value. Returns True if removed."""
        if not self.head:
            raise ValueError("List is empty")
        current = self.head
        prev = None
        while current:
            if current.value == value:
                if prev is None:
                    self.head = current.next
                    if current == self.tail:
                        self.tail = None
                else:
                    prev.next = current.next
                    if current == self.tail:
                        self.tail = prev
                self.length -= 1
                return True
            prev = current
            current = current.next
        raise ValueError(f"Value {value} not found")

    def find(self, value):
        """Return the first node with the given value or None."""
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def clear(self):
        """Clear the list."""
        self.head = None
        self.tail = None
        self.length = 0

    def to_list(self):
        """Return a Python list of all values."""
        return list(iter(self))

    def display(self):
        """Print the list values in readable format."""
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        print(" -> ".join(values) + " -> None")

    def __iter__(self):
        """Iterator over values."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __len__(self):
        """Return length of the list."""
        return self.length


class DoublyNode:
    """Node for Doubly Linked List."""
    __slots__ = ['value', 'next', 'prev']
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    Doubly Linked List implementation.

    Each node contains a value and pointers to both previous and next nodes,
    allowing bidirectional traversal.

    Usage:
    >>> dll = DoublyLinkedList()
    >>> dll.append(1)
    >>> dll.prepend(0)
    >>> dll.insert(1, 0.5)
    >>> dll.to_list()
    [0, 0.5, 1]
    >>> dll.display()
    0 <-> 0.5 <-> 1 <-> None
    >>> dll.remove(0.5)
    True
    >>> list(reversed(dll))
    [1, 0]
    >>> len(dll)
    2
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        """Add value at the end."""
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def prepend(self, value):
        """Add value at the start."""
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1

    def insert(self, index, value):
        """Insert value at specified index."""
        if index < 0 or index > self.length:
            raise IndexError("Index out of bounds")
        if index == 0:
            self.prepend(value)
            return
        if index == self.length:
            self.append(value)
            return
        new_node = DoublyNode(value)
        current = self.head
        for _ in range(index):
            current = current.next
        prev_node = current.prev
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = current
        current.prev = new_node
        self.length += 1

    def remove(self, value):
        """Remove first node with the given value. Returns True if removed."""
        current = self.head
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.length -= 1
                return True
            current = current.next
        raise ValueError(f"Value {value} not found")

    def find(self, value):
        """Return the first node with the given value or None."""
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def clear(self):
        """Clear the list."""
        self.head = None
        self.tail = None
        self.length = 0

    def to_list(self):
        """Return a Python list of all values."""
        return list(iter(self))

    def display(self):
        """Print the list values in readable format."""
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        print(" <-> ".join(values) + " <-> None")

    def __iter__(self):
        """Iterator over values forward."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __reversed__(self):
        """Iterator over values backward."""
        current = self.tail
        while current:
            yield current.value
            current = current.prev

    def __len__(self):
        """Return length of the list."""
        return self.length


class CircularSinglyLinkedList:
    """
    Circular Singly Linked List.

    Similar to singly linked list, but last node points back to the head,
    forming a circular structure.

    Usage:
    >>> cll = CircularSinglyLinkedList()
    >>> cll.append(1)
    >>> cll.prepend(0)
    >>> cll.to_list()
    [0, 1]
    >>> cll.display()
    0 -> 1 -> (back to head)
    >>> cll.remove(0)
    True
    >>> len(cll)
    1
    """

    def __init__(self):
        self.tail = None
        self.length = 0
        self.head = None

    def append(self, value):
        """Add value at the end."""
        new_node = SinglyNode(value)
        if not self.tail:
            self.tail = new_node
            new_node.next = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def prepend(self, value):
        """Add value at the start."""
        new_node = SinglyNode(value)
        if not self.tail:
            self.tail = new_node
            new_node.next = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
        self.length += 1

    def remove(self, value):
        """Remove first node with the given value. Returns True if removed."""
        if not self.tail:
            raise ValueError("List is empty")
        current = self.tail.next
        prev = self.tail
        for _ in range(self.length):
            if current.value == value:
                if self.length == 1:
                    self.tail = None
                else:
                    prev.next = current.next
                    if current == self.tail:
                        self.tail = prev
                self.length -= 1
                return True
            prev = current
            current = current.next
        raise ValueError(f"Value {value} not found")

    def find(self, value):
        """Return the first node with the given value or None."""
        if not self.tail:
            return None
        current = self.tail.next
        for _ in range(self.length):
            if current.value == value:
                return current
            current = current.next
        return None

    def clear(self):
        """Clear the list."""
        self.tail = None
        self.length = 0

    def to_list(self):
        """Return a Python list of all values."""
        return list(iter(self))

    def display(self):
        """Print the list values in readable format."""
        if not self.tail:
            print("Empty list")
            return
        values = []
        current = self.tail.next
        for _ in range(self.length):
            values.append(str(current.value))
            current = current.next
        print(" -> ".join(values) + " -> (back to head)")

    def __iter__(self):
        """Iterator over values once around the circle."""
        if not self.tail:
            return
        current = self.tail.next
        for _ in range(self.length):
            yield current.value
            current = current.next

    def __len__(self):
        """Return length of the list."""
        return self.length


class CircularDoublyLinkedList:
    """
    Circular Doubly Linked List.

    Last node points to the head and head.prev points back to the tail,
    forming a doubly linked circular structure.

    Usage:
    >>> cdll = CircularDoublyLinkedList()
    >>> cdll.append(1)
    >>> cdll.prepend(0)
    >>> cdll.to_list()
    [0, 1]
    >>> cdll.display()
    0 <-> 1 <-> (back to head)
    >>> cdll.remove(0)
    True
    >>> list(reversed(cdll))
    [1]
    >>> len(cdll)
    1
    """

    def __init__(self):
        self.tail = None
        self.length = 0
        self.head = None
        

    def append(self, value):
        """Add value at the end."""
        new_node = DoublyNode(value)
        if not self.tail:
            new_node.next = new_node.prev = new_node
            self.tail = new_node
        else:
            head = self.tail.next
            new_node.prev = self.tail
            new_node.next = head
            self.tail.next = new_node
            head.prev = new_node
            self.tail = new_node
        self.length += 1

    def prepend(self, value):
        """Add value at the start."""
        new_node = DoublyNode(value)
        if not self.tail:
            new_node.next = new_node.prev = new_node
            self.tail = new_node
        else:
            head = self.tail.next
            new_node.next = head
            new_node.prev = self.tail
            head.prev = new_node
            self.tail.next = new_node
        self.length += 1

    def remove(self, value):
        """Remove first node with the given value. Returns True if removed."""
        if not self.tail:
            raise ValueError("List is empty")
        current = self.tail.next
        for _ in range(self.length):
            if current.value == value:
                if self.length == 1:
                    self.tail = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self.tail:
                        self.tail = current.prev
                self.length -= 1
                return True
            current = current.next
        raise ValueError(f"Value {value} not found")

    def find(self, value):
        """Return the first node with the given value or None."""
        if not self.tail:
            return None
        current = self.tail.next
        for _ in range(self.length):
            if current.value == value:
                return current
            current = current.next
        return None

    def clear(self):
        """Clear the list."""
        self.tail = None
        self.length = 0

    def to_list(self):
        """Return a Python list of all values."""
        return list(iter(self))

    def display(self):
        """Print the list values in readable format."""
        if not self.tail:
            print("Empty list")
            return
        values = []
        current = self.tail.next
        for _ in range(self.length):
            values.append(str(current.value))
            current = current.next
        print(" <-> ".join(values) + " <-> (back to head)")

    def __iter__(self):
        """Iterator over values forwards once around the circle."""
        if not self.tail:
            return
        current = self.tail.next
        for _ in range(self.length):
            yield current.value
            current = current.next

    def __reversed__(self):
        """Iterator over values backwards once around the circle."""
        if not self.tail:
            return
        current = self.tail
        for _ in range(self.length):
            yield current.value
            current = current.prev

    def __len__(self):
        """Return length of the list."""
        return self.length


class SkipList:
    """
    Skip List: probabilistic data structure with multiple levels.

    Supports fast search, insertion, and deletion in O(log n) expected time.

    Usage:
    >>> sl = SkipList()
    >>> sl.insert(3)
    >>> sl.insert(7)
    >>> sl.insert(5)
    >>> sl.search(5) is not None
    True
    >>> sl.remove(7)
    True
    >>> list(sl)
    [3, 5]
    >>> sl.display()
    SkipList Levels:
    Level 3: ...
    Level 2: ...
    Level 1: ...
    Level 0: 3 -> 5
    """

    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = SkipListNode(None, self.max_level)
        self.level = 0
        self.length = 0

    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, value):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in reversed(range(self.level + 1)):
            while current.forwards[i] and current.forwards[i].value < value:
                current = current.forwards[i]
            update[i] = current

        current = current.forwards[0]

        if current is None or current.value != value:
            lvl = self.random_level()
            if lvl > self.level:
                for i in range(self.level + 1, lvl + 1):
                    update[i] = self.header
                self.level = lvl
            new_node = SkipListNode(value, lvl)
            for i in range(lvl + 1):
                new_node.forwards[i] = update[i].forwards[i]
                update[i].forwards[i] = new_node
            self.length += 1

    def remove(self, value):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in reversed(range(self.level + 1)):
            while current.forwards[i] and current.forwards[i].value < value:
                current = current.forwards[i]
            update[i] = current

        current = current.forwards[0]

        if current and current.value == value:
            for i in range(self.level + 1):
                if update[i].forwards[i] != current:
                    break
                update[i].forwards[i] = current.forwards[i]

            while self.level > 0 and self.header.forwards[self.level] is None:
                self.level -= 1
            self.length -= 1
            return True
        return False

    def search(self, value):
        current = self.header
        for i in reversed(range(self.level + 1)):
            while current.forwards[i] and current.forwards[i].value < value:
                current = current.forwards[i]
        current = current.forwards[0]
        if current and current.value == value:
            return current
        return None

    def clear(self):
        self.header = SkipListNode(None, self.max_level)
        self.level = 0
        self.length = 0

    def display(self):
        print("SkipList Levels:")
        for i in reversed(range(self.level + 1)):
            current = self.header.forwards[i]
            level_nodes = []
            while current:
                level_nodes.append(str(current.value))
                current = current.forwards[i]
            print(f"Level {i}: {' -> '.join(level_nodes)}")

    def to_list(self):
        """Return sorted list of values."""
        return list(iter(self))

    def __iter__(self):
        current = self.header.forwards[0]
        while current:
            yield current.value
            current = current.forwards[0]

    def __len__(self):
        return self.length


def real_world_examples():
    """
    Linked Lists Module — Real World Usage Examples
    ===============================================

    1. SinglyLinkedList
       Scenario:
           Implementing a simple task scheduler with a list of jobs where traversal
           is always forward and minimal overhead is desired.
       If Using Python List:
           - Insertions/deletions in middle are costly (O(n)).
           - Memory overhead for dynamic resizing.
       If Using SinglyLinkedList:
           - Efficient insertions and deletions at the front or known nodes.
       Production Benefit:
           Useful for simple forward-only linear collections with frequent insertions/deletions.

    2. DoublyLinkedList
       Scenario:
           Browser history navigation allowing forward and backward traversal.
       If Using Python List:
           - Back and forth traversal possible but inefficient insertion/deletion in middle.
       If Using DoublyLinkedList:
           - Bi-directional traversal, easy insertion/removal from both ends.
       Production Benefit:
           Great for navigation structures or where both directions are needed.

    3. CircularSinglyLinkedList
       Scenario:
           Multiplayer game turn rotation where after last player, the first player plays.
       If Using Python List:
           - Need manual modulo operations for cycling turns.
       If Using CircularSinglyLinkedList:
           - Natural cycle with pointer looping back.
       Production Benefit:
           Ideal for cyclic or round-robin structures.

    4. CircularDoublyLinkedList
       Scenario:
           Music player playlist allowing both next and previous with continuous looping.
       If Using Python List:
           - Needs manual handling for cyclic iteration.
       If Using CircularDoublyLinkedList:
           - Supports bi-directional circular iteration naturally.
       Production Benefit:
           Perfect for circular buffers or cyclic browsing.

    5. SkipList
       Scenario:
           A database index supporting fast search, insertion, and deletion.
       If Using Balanced Trees:
           - Complex balancing logic.
       If Using SkipList:
           - Probabilistic balancing with simpler implementation.
       Production Benefit:
           Efficient, scalable sorted data structure with O(log n) operations.

    """
    print(real_world_examples.__doc__)


def list_classes():
    """
    List all available linked list classes in the linked_lists module.
    """
    print(", ".join(__all__[:-1]))


__all__ = [
    "SinglyLinkedList",
    "DoublyLinkedList",
    "CircularSinglyLinkedList",
    "CircularDoublyLinkedList",
    "SkipList",
    "real_world_examples",
    "list_classes",
]
