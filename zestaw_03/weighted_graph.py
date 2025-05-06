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
    
    def visualize_weighted(self, spanning_tree=False, mst=None, total=None, layout="circle"):
        G = nx.Graph()
        G.add_nodes_from(range(self.nodes))

        edge_colors = []
        mst_set = set()
        if spanning_tree and mst:
            mst_set = {(min(u, v), max(u, v)) for u, v, _ in mst}

        for u in range(self.nodes):
            for v in range(u + 1, self.nodes):
                if self.adjacency_matrix.matrix[u][v] == 1:
                    weight = self.weights[u][v]
                    G.add_edge(u, v, weight=weight)
                    if (u, v) in mst_set or (v, u) in mst_set:
                        edge_colors.append('red')
                    else:
                        edge_colors.append('gray')

        if layout == "circle":
            pos = {
                i: (
                    math.cos(2 * math.pi * i / self.nodes),
                    math.sin(2 * math.pi * i / self.nodes)
                )
                for i in range(self.nodes)
            }
        elif layout == "spring":
            pos = nx.spring_layout(G, seed=42)

        fig, ax = plt.subplots(figsize=(10, 10))  # Zwiększony rozmiar

        if layout == "circle":
            circle = plt.Circle((0, 0), 1.05, color='gray', fill=False, linestyle='dashed')
            ax.add_patch(circle)

        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors, ax=ax)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)

        if spanning_tree and total is not None:
            plt.title(f"Minimalne drzewo rozpinające (waga: {total})")
        else:
            plt.title("Graf ważony")

        ax.set_xlim(-1.2, 1.2) if layout == "circle" else None
        ax.set_ylim(-1.2, 1.2) if layout == "circle" else None
        ax.set_aspect('equal')
        plt.tight_layout()
        plt.show()

    
def generate_connected_gnp(n, p):
    while True:
        graph = WeightedGraph(n, p)
        G_nx = nx.Graph()
        G_nx.add_nodes_from(range(n))
        for u in range(n):
            for v in range(u + 1, n):
                if graph.adjacency_matrix.matrix[u][v] == 1:
                    G_nx.add_edge(u, v)
        if nx.is_connected(G_nx):
            return graph


def main():
    graph = generate_connected_gnp(7, 0.5)
    
    original_show = plt.show
    def save_show():
        plt.savefig("weighted_graph.png")
        plt.close()
    plt.show = save_show
    graph.visualize_weighted()


if __name__ == "__main__":
    main()