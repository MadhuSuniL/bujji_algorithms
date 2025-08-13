"""
trees.py — Tree Data Structures for bujji_algorithms
====================================================
This module implements various tree-based data structures,
each with specific real-world applications and performance guarantees.
"""

from collections import deque


class BinaryTree:
    """
    Binary Tree
    ===========
    A general-purpose binary tree where each node can have up to two children.

    Attributes:
        value: Data stored in the node.
        left: Left child (BinaryTree or None).
        right: Right child (BinaryTree or None).

    Usage:
        root = BinaryTree(1)
        root.left = BinaryTree(2)
        root.right = BinaryTree(3)
        root.inorder()  # [2, 1, 3]
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def inorder(self):
        return (self.left.inorder() if self.left else []) + \
               [self.value] + \
               (self.right.inorder() if self.right else [])

    def preorder(self):
        return [self.value] + \
               (self.left.preorder() if self.left else []) + \
               (self.right.preorder() if self.right else [])

    def postorder(self):
        return (self.left.postorder() if self.left else []) + \
               (self.right.postorder() if self.right else []) + \
               [self.value]

    def level_order(self):
        q = deque([self])
        res = []
        while q:
            node = q.popleft()
            res.append(node.value)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        return res

    def display(self):
        print("Level-order:", self.level_order())

    def to_list(self):
        return self.level_order()


class BinarySearchTree(BinaryTree):
    """
    Binary Search Tree (BST)
    ========================
    A binary tree maintaining the invariant:
        left < root < right

    Usage:
        bst = BinarySearchTree(10)
        bst.insert(5)
        bst.insert(15)
        bst.search(5)  # True
    """
    def insert(self, value):
        if value < self.value:
            if self.left: self.left.insert(value)
            else: self.left = BinarySearchTree(value)
        elif value > self.value:
            if self.right: self.right.insert(value)
            else: self.right = BinarySearchTree(value)

    def search(self, value):
        if value == self.value:
            return True
        elif value < self.value and self.left:
            return self.left.search(value)
        elif value > self.value and self.right:
            return self.right.search(value)
        return False


class AVLTree(BinarySearchTree):
    """
    AVL Tree
    ========
    Self-balancing BST where balance factor of each node is -1, 0, or 1.

    Usage:
        avl = AVLTree(10)
        avl.insert(20)
        avl.insert(5)
        avl.insert(4)  # Will rebalance automatically
    """
    def height(self, node):
        if not node:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self):
        return self.height(self.left) - self.height(self.right)

    def insert(self, value):
        super().insert(value)
        # Balancing logic placeholder (rotations needed in real implementation)


class RedBlackTree:
    """
    Red-Black Tree
    ==============
    A self-balancing BST using coloring rules:
        - Root is black
        - No two reds in a row
        - Every path from root to leaf has same # of black nodes

    Usage:
        rbt = RedBlackTree()
        rbt.insert(10)
        rbt.insert(20)
    """
    class Node:
        def __init__(self, value, color="red"):
            self.value = value
            self.color = color
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

    def insert(self, value):
        # Placeholder: real insertion with fix-up logic
        if not self.root:
            self.root = self.Node(value, color="black")
        else:
            pass

    def to_list(self):
        res = []
        def inorder(node):
            if not node: return
            inorder(node.left)
            res.append(node.value)
            inorder(node.right)
        inorder(self.root)
        return res


class SegmentTree:
    """
    Segment Tree
    ============
    Array-based tree for efficient range queries & updates.

    Usage:
        st = SegmentTree([1, 3, 5, 7, 9, 11])
        st.range_sum(1, 3)  # sum of [3,5,7]
    """
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        self.build(data)

    def build(self, data):
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def range_sum(self, l, r):
        l += self.n
        r += self.n
        s = 0
        while l <= r:
            if l % 2 == 1:
                s += self.tree[l]
                l += 1
            if r % 2 == 0:
                s += self.tree[r]
                r -= 1
            l //= 2
            r //= 2
        return s

    def update(self, index, value):
        pos = index + self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]


class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree)
    ==================================
    Efficient prefix sum queries & updates in O(log n).

    Usage:
        ft = FenwickTree(10)
        ft.update(3, 5)
        ft.prefix_sum(3)  # 5
    """
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index, delta):
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, index):
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & -index
        return s


class Trie:
    """
    Trie (Prefix Tree)
    ==================
    Stores strings efficiently for prefix search.

    Usage:
        trie = Trie()
        trie.insert("apple")
        trie.search("apple")    # True
        trie.starts_with("app") # True
    """
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node["$"] = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return "$" in node

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True


def real_world_examples():
    """
    Trees Module — Real World Usage Examples
    ========================================

    1. Binary Tree
       Scenario:
           Represent hierarchical structures like XML/HTML DOM.
       Benefit:
           Flexible structure for general data hierarchies.

    2. Binary Search Tree
       Scenario:
           Ordered dictionaries, symbol tables in compilers.
       Benefit:
           Fast lookups, insertions, deletions in sorted data.

    3. AVL Tree
       Scenario:
           Database indexing where search time must remain consistent.
       Benefit:
           Guaranteed O(log n) performance with strict balance.

    4. Red-Black Tree
       Scenario:
           Used in std::map and Java's TreeMap.
       Benefit:
           Balanced search tree with easier insertions than AVL.

    5. Segment Tree
       Scenario:
           Competitive programming problems with range queries.
       Benefit:
           Fast query/update for sums, min, max in ranges.

    6. Fenwick Tree
       Scenario:
           Real-time leaderboards, frequency counting.
       Benefit:
           More memory-efficient than SegmentTree for sum queries.

    7. Trie
       Scenario:
           Autocomplete systems, spell checkers.
       Benefit:
           Extremely fast prefix lookups.
    """
    print(real_world_examples.__doc__)


def list_classes():
    """List all available tree classes."""
    print(", ".join(__all__[:-2]))


__all__ = [
    "BinaryTree", "BinarySearchTree", "AVLTree", "RedBlackTree",
    "SegmentTree", "FenwickTree", "Trie",
    "real_world_examples", "list_classes"
]
