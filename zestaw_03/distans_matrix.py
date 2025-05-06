import numpy as np
from zestaw_03.weighted_graph import generate_connected_gnp
from zestaw_03.dijkstra import dijkstra
import matplotlib.pyplot as plt 

def distance_matrix(graph):
    n = graph.nodes
    D = np.zeros((n, n))

    for u in range(n):
        ds, _ = dijkstra(graph, start=u)
        for v in range(n):
            D[u][v] = ds[v]

    for u in range(n):
        for v in range(n):
            D[u][v] = D[v][u] = min(D[u][v], D[v][u])

    return D

def find_graph_center(D):
    sums = np.sum(D, axis=1)
    center = np.argmin(sums)
    return center, sums[center]

def find_minimax_center(D):
    max_distances = np.max(D, axis=1)
    center = np.argmin(max_distances)
    return center, max_distances[center]

def main():
    graph = generate_connected_gnp(8, 0.4)

    D = distance_matrix(graph)

    print("Macierz odległości między wszystkimi parami wierzchołków:")
    print(D)

    center, center_sum = find_graph_center(D)
    minimax, minimax_dist = find_minimax_center(D)

    print(f"\nCentrum grafu (minimum sumy odległości): wierzchołek {center}, suma = {center_sum}")
    print(f"Centrum minimax (minimum maksymalnej odległości): wierzchołek {minimax}, odległość = {minimax_dist}")

    def save_show():
        plt.savefig("graph_visualization.png")
        plt.close()
    plt.show = save_show
    graph.visualize_weighted(layout="spring")

if __name__ == "__main__":
    main()
