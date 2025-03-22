
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx #libka do rysowania grafów
import math

class AdjacencyMatrix:
    def __init__(self, nodes):
        self.nodes = nodes
        self.matrix = np.zeros((nodes, nodes), dtype=int)
    
    def add_edge(self, u, v):
        self.matrix[u][v] = 1
        self.matrix[v][u] = 1  
    
    def display(self):
        print("Macierz sąsiedztwa:")
        print(self.matrix)
    
    def visualize(self):
        G = nx.Graph()
        G.add_nodes_from(range(self.nodes))  
        for u in range(self.nodes):
            for v in range(u + 1, self.nodes):
                if self.matrix[u][v] == 1:
                    G.add_edge(u, v)
        pos = {i: (math.cos(2 * math.pi * i / self.nodes), math.sin(2 * math.pi * i / self.nodes)) for i in range(self.nodes)}
        
        fig, ax = plt.subplots(figsize=(6,6))
        circle = plt.Circle((0, 0), 1.05, color='gray', fill=False, linestyle='dashed')
        ax.add_patch(circle)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        plt.show()

    def to_adjacency_list(self):
        adjacency_list = AdjacencyList(self.nodes)
        for u in range(self.nodes):
            for v in range(self.nodes):
                if self.matrix[u][v] == 1:
                    adjacency_list.list[u].append(v)
                    adjacency_list.list[u].sort()
        return adjacency_list
    
    def to_incidence_matrix(self):
        edges = []
        for u in range(self.nodes):
            for v in range(u + 1, self.nodes):
                if self.matrix[u][v] == 1:
                    edges.append((u, v))
        edge_count = len(edges)
        Imatrix = IncidenceMatrix(self.nodes, edge_count)
        for i, (u, v) in enumerate(edges):
            Imatrix.add_edge(i, u, v)
        return Imatrix


class IncidenceMatrix:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.matrix = np.zeros((nodes, edges), dtype=int)
    
    def add_edge(self, edge_index, u, v): 
        self.matrix[u][edge_index] = 1
        self.matrix[v][edge_index] = 1 
    
    def display(self):
        print("Macierz incydencji:")
        print(self.matrix)
    
    def visualize(self):
        adjacency_matrix = self.to_adjacency_matrix()
        adjacency_matrix.visualize()

    def to_adjacency_matrix(self):
        Amatrix = AdjacencyMatrix(self.nodes)
        for edge_index in range(self.edges):
            nodes = [i for i in range(self.nodes) if self.matrix[i][edge_index] == 1]
            if len(nodes) == 2:
                u, v = nodes
                Amatrix.add_edge(u,v) 
        return Amatrix
    
    def to_adjacency_list(self):
        adjacency_list = AdjacencyList(self.nodes)
        for edge_index in range(self.edges):
            nodes = [i for i in range(self.nodes) if self.matrix[i][edge_index] == 1]
            if len(nodes) == 2:
                u, v = nodes
                adjacency_list.add_edge(u,v)
        return adjacency_list


class AdjacencyList:
    def __init__(self, nodes):
        self.nodes = nodes
        self.list = {i: [] for i in range(nodes)}
    
    def add_edge(self, u, v):
        self.list[u].append(v)
        self.list[v].append(u)  
        self.list[u].sort()
        self.list[v].sort()
    
    def display(self):
        print("Lista sąsiedztwa:")
        for key, value in self.list.items():
            print(f"{key}: {value}")
    
    def visualize(self):
        G = nx.Graph()
        G.add_nodes_from(range(self.nodes)) 
        for node, neighbors in self.list.items():
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
        for node, neighbors in self.list.items():
            for neighbor in neighbors:
                Amatrix.matrix[node][neighbor] = 1  
        return Amatrix 
        
    def to_incidence_matrix(self):
        edges = []
        seen_edges = set()
        
        for node, neighbors in self.list.items():
            for neighbor in neighbors:
                if (neighbor, node) not in seen_edges:  
                    edges.append((node, neighbor))
                    seen_edges.add((node, neighbor))
        
        edge_count = len(edges)
        Imatrix = IncidenceMatrix(self.nodes, edge_count)

        for i, (u, v) in enumerate(edges):
            Imatrix.add_edge(i,u,v) 

        return Imatrix




