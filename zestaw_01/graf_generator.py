import random
from .graph_coder import AdjacencyMatrix
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adjacency_matrix = AdjacencyMatrix(nodes)
        self.adjacency_list = self.adjacency_matrix.to_adjacency_list()
        self.incidence_matrix = self.adjacency_matrix.to_incidence_matrix()

    def add_edge(self, u, v):
        self.adjacency_matrix.add_edge(u, v)
        self.adjacency_list.add_edge(u, v)
        self.incidence_matrix = self.adjacency_matrix.to_incidence_matrix()

    def display(self):
        print("=== Macierz sąsiedztwa ===\n")
        self.adjacency_matrix.display()
        print("=== Lista sąsiedztwa ===\n")
        self.adjacency_list.display()
        print("=== Macierz incydencji ===\n")
        self.incidence_matrix.display()

    def visualize(self, circle=True):
        self.adjacency_matrix.visualize(circle)

def generate_gnp(n, p):
    """Generuje graf losowy w modelu G(n, p)"""
    graph = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                graph.add_edge(u, v)
    return graph


def generate_gnl(n, l):
    """Generuje graf losowy w modelu G(n, l)"""
    if l > (n * (n - 1)) // 2:
        raise ValueError("Za dużo krawędzi dla podanej liczby wierzchołków")

    graph = Graph(n)
    edges = set()

    while len(edges) < l:
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            graph.add_edge(u, v)

    return graph
