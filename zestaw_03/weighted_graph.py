from zestaw_01.graf_generator import Graph
import numpy as np
import random 
import math
import networkx as nx
import matplotlib.pyplot as plt

class WeightedGraph(Graph):
    
    def __init__(self, nodes, p=0.3, min_weight=1, max_weight=10):
        super().__init__(nodes)
        for u in range(nodes):
            for v in range(u + 1, nodes):
                if random.random() < p:
                    self.add_edge(u, v)
        self.weights = self.assign_edge_weights(min_weight, max_weight)
        
    def assign_edge_weights(self, min_weight=1, max_weight=10):
        """Przypisuje losowe wagi do krawędzi grafu."""
        weights = np.zeros((self.nodes, self.nodes), dtype=int)
        
        for u in range(self.nodes):
            for v in range(u + 1, self.nodes):
                if self.adjacency_matrix.matrix[u][v] == 1:
                    weight = random.randint(min_weight, max_weight)
                    weights[u][v] = weight
                    weights[v][u] = weight  

        return weights
    
    def visualize(self):
        G = nx.Graph()
        G.add_nodes_from(range(self.nodes))

        
        for u in range(self.nodes):
            for v in range(u + 1, self.nodes):
                if self.adjacency_matrix.matrix[u][v] == 1:
                    weight = self.weights[u][v]
                    G.add_edge(u, v, weight=weight)

       
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
        
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)

        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        plt.show()
    


def generate_gnp(n, p):
    """Generuje graf losowy w modelu G(n, p)"""
    graph = WeightedGraph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                graph.add_edge(u, v)
    return graph


def main():
    graph =generate_gnp(7,0.5)
    graph.visualize()


if __name__ == "__main__":
    main()