"""
graphs.py — Graph Data Structures
==================================

This module implements various graph representations and types:
- Adjacency List Graph
- Adjacency Matrix Graph
- Directed Graph
- Undirected Graph
- Weighted Graph

Each class includes useful and optional methods, along with display helpers.
"""

class AdjacencyListGraph:
    """
    Graph representation using an adjacency list.

    Example:
    --------
    >>> g = AdjacencyListGraph()
    >>> g.add_vertex("A")
    >>> g.add_edge("A", "B")
    >>> g.display()
    A -> ['B']
    """
    def __init__(self):
        self.graph = {}

    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, v1, v2):
        self.add_vertex(v1)
        self.add_vertex(v2)
        if v2 not in self.graph[v1]:
            self.graph[v1].append(v2)

    def remove_edge(self, v1, v2):
        if v1 in self.graph and v2 in self.graph[v1]:
            self.graph[v1].remove(v2)

    def remove_vertex(self, v):
        if v in self.graph:
            del self.graph[v]
        for vertices in self.graph.values():
            if v in vertices:
                vertices.remove(v)

    def get_neighbors(self, v):
        return self.graph.get(v, [])

    def to_dict(self):
        return dict(self.graph)

    def display(self):
        for v, neighbors in self.graph.items():
            print(f"{v} -> {neighbors}")


class AdjacencyMatrixGraph:
    """
    Graph representation using an adjacency matrix.

    Example:
    --------
    >>> g = AdjacencyMatrixGraph()
    >>> g.add_vertex("A")
    >>> g.add_vertex("B")
    >>> g.add_edge(0, 1)
    >>> g.display()
    0 1
    0 [0, 1]
    1 [0, 0]
    """
    def __init__(self):
        self.vertices = []
        self.matrix = []

    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.append(v)
            size = len(self.vertices)
            for row in self.matrix:
                row.append(0)
            self.matrix.append([0] * size)

    def add_edge(self, idx1, idx2):
        if 0 <= idx1 < len(self.vertices) and 0 <= idx2 < len(self.vertices):
            self.matrix[idx1][idx2] = 1

    def remove_edge(self, idx1, idx2):
        if 0 <= idx1 < len(self.vertices) and 0 <= idx2 < len(self.vertices):
            self.matrix[idx1][idx2] = 0

    def has_edge(self, idx1, idx2):
        return self.matrix[idx1][idx2] == 1

    def to_matrix(self):
        return [row[:] for row in self.matrix]

    def display(self):
        print("   " + " ".join(map(str, range(len(self.vertices)))))
        for i, row in enumerate(self.matrix):
            print(f"{i}: {row}")


class DirectedGraph(AdjacencyListGraph):
    """
    Directed graph implementation using adjacency list.

    Example:
    --------
    >>> dg = DirectedGraph()
    >>> dg.add_edge("A", "B")
    >>> dg.display()
    A -> ['B']
    """
    pass  # Inherits from AdjacencyListGraph (directed by default)


class UndirectedGraph(AdjacencyListGraph):
    """
    Undirected graph implementation using adjacency list.

    Example:
    --------
    >>> ug = UndirectedGraph()
    >>> ug.add_edge("A", "B")
    >>> ug.display()
    A -> ['B']
    B -> ['A']
    """
    def add_edge(self, v1, v2):
        self.add_vertex(v1)
        self.add_vertex(v2)
        if v2 not in self.graph[v1]:
            self.graph[v1].append(v2)
        if v1 not in self.graph[v2]:
            self.graph[v2].append(v1)


class WeightedGraph:
    """
    Weighted graph implementation using adjacency list.

    Example:
    --------
    >>> wg = WeightedGraph()
    >>> wg.add_edge("A", "B", 5)
    >>> wg.display()
    A -> [('B', 5)]
    """
    def __init__(self):
        self.graph = {}

    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, v1, v2, weight):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.graph[v1].append((v2, weight))

    def get_weight(self, v1, v2):
        for neighbor, w in self.graph.get(v1, []):
            if neighbor == v2:
                return w
        return None

    def display(self):
        for v, neighbors in self.graph.items():
            print(f"{v} -> {neighbors}")

    def to_dict(self):
        return dict(self.graph)


def real_world_examples():
    """
    Graphs Module — Real World Usage Examples
    ==========================================

    1. Adjacency List Graph
       - Scenario: Representing a sparse social network.
       - Pros: Low memory for sparse graphs.
       - Cons: Slower edge existence checks.

    2. Adjacency Matrix Graph
       - Scenario: Representing airline connections between cities.
       - Pros: Instant edge lookup.
       - Cons: High memory for sparse networks.

    3. Directed Graph
       - Scenario: Webpage link mapping (A links to B).
       - Pros: Models one-way relationships.
       - Cons: Can't directly represent bidirectional edges.

    4. Undirected Graph
       - Scenario: Facebook friend connections.
       - Pros: Simple for symmetric relations.
       - Cons: Can't represent one-way links.

    5. Weighted Graph
       - Scenario: Road network with distances.
       - Pros: Models costs for routing.
       - Cons: More storage for weights.
    """
    print(real_world_examples.__doc__)


def list_classes():
    """List all available graph classes in the graphs module."""
    print(", ".join(__all__[:-2]))


__all__ = [
    "AdjacencyListGraph", "AdjacencyMatrixGraph", "DirectedGraph",
    "UndirectedGraph", "WeightedGraph", "real_world_examples", "list_classes"
]
