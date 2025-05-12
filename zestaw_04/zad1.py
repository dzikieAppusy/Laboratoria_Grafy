#updated from zestaw_01/grapg_coder.py
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx #libka do rysowania grafów
import math
import random

class AdjacencyList:
    def __init__(self, nodes):
        self.nodes = nodes
        self.list = {i: [] for i in range(nodes)}
    
    def add_edge(self, u, v):
        self.list[u].append(v) 
        self.list[u].sort()
    
    def display(self):
        print("Lista sąsiedztwa:")
        for key, value in self.list.items():
            print(f"{key}: {value}")
    
    def get_neighbors(self, v):
        return self.list.get(v, [])
    
    def visualize(self):
        G = nx.DiGraph()
        G.add_nodes_from(range(self.nodes)) #dodanie wierzcholkow
        for node, neighbors in self.list.items(): #dodanie krawedzi do sasiadow
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        pos = {
            i: (
                math.cos(2 * math.pi * i / self.nodes),
                math.sin(2 * math.pi * i / self.nodes)
            )
            for i in range(self.nodes)
        }
        
        fig, ax = plt.subplots(figsize=(6, 6))
        circle = plt.Circle((0, 0), 1.05, color='gray', fill=False, linestyle='dashed')
        ax.add_patch(circle)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        plt.show()
    
    def to_adjacency_matrix(self):
        Amatrix = AdjacencyMatrix(self.nodes)
        for node in range(self.nodes):
            for neighbor in self.list[node]:
                if 0 <= neighbor < self.nodes:
                    Amatrix.matrix[node][neighbor] = 1
                else:
                    print(f"Blad: {node} -> {neighbor}")
        return Amatrix
    
    def to_incidence_matrix(self):
        edges = []
        
        for node, neighbors in self.list.items():
            for neighbor in neighbors:
                edges.append((node, neighbor))
        
        edge_count = len(edges)
        Imatrix = IncidenceMatrix(self.nodes, edge_count)

        for i, (u, v) in enumerate(edges):
            Imatrix.matrix[u][i] = -1
            Imatrix.matrix[v][i] = 1 

        return Imatrix

class AdjacencyMatrix:
    def __init__(self, nodes):
        self.nodes = nodes
        self.matrix = np.zeros((nodes, nodes), dtype=int)
    
    def add_edge(self, u, v):
        self.matrix[u][v] = 1 #krawedz skierowana
    
    def display(self):
        print("Macierz sasiedztwa:")
        print(self.matrix)
    
    def visualize(self):
        G = nx.DiGraph()
        for u in range(self.nodes):
            for v in range(u + 1, self.nodes):
                if self.matrix[u][v] == 1: #jak istnieje krawedz od do
                    G.add_edge(u, v)
        pos = {i: (math.cos(2 * math.pi * i / self.nodes), math.sin(2 * math.pi * i / self.nodes)) for i in range(self.nodes)} #polozenie na okregu
        
        #rysowanie
        fig, ax = plt.subplots(figsize=(6,6))
        circle = plt.Circle((0, 0), 1.05, color='gray', fill=False, linestyle='dashed')
        ax.add_patch(circle)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        plt.show()


#czytamy kolumnami od lewej do prawej, w kazdej kolumnie jest -1 oraz 1 ktore wskazuja ktory wierzchołek jest poczatkowym, a ktory koncowym danej krawedzi (wiersze - krawedzie, kolumny - wierzcholki)
class IncidenceMatrix:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.matrix = np.zeros((nodes, edges), dtype=int)
    
    def add_edge(self, edge_index, u, v): 
        self.matrix[u][edge_index] = -1 #wierzcholek poczatkowy
        self.matrix[v][edge_index] = 1 #wierzcholek koncowy
    
    def display(self):
        print("Macierz incydencji:")
        print(self.matrix)





class Digraph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adjacency_list = AdjacencyList(nodes)

    def add_edge(self, u, v):
        self.adjacency_list.add_edge(u, v) #krawedz skierowana od u do v

    def display(self):
        print("=== Macierz sąsiedztwa ===\n")
        adjacency_matrix = self.adjacency_list.to_adjacency_matrix()
        adjacency_matrix.display()
        print("=== Lista sąsiedztwa ===\n")
        self.adjacency_list.display()
        print("=== Macierz incydencji ===\n")
        incidence_matrix = self.adjacency_list.to_incidence_matrix()
        incidence_matrix.display()

    def visualize(self):
        self.adjacency_list.visualize()

def generate_gnp(n, p):
    graph = Digraph(n)
    for u in range(n): #dla kazdego wierzcholka
        for v in range(n): #wszystkie mozliwe polaczenia krawedzi
            if u == v:
                continue #nie ma petli, sam do siebie wierzcholek sie nie polaczy krawedzia
            if random.random() < p: #dodanie krawedzi z prawdopodobienstwem p
                graph.add_edge(u, v)
                # print( u, "->", v)
    return graph