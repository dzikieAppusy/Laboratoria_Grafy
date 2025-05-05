from graph_coder import AdjacencyMatrix, IncidenceMatrix, AdjacencyList
from graf_generator import *
import os
import numpy as np
import matplotlib.pyplot as plt
#podając wejście dla macierzy podajemy po prostu po kolei : wiersz + znak nowej linii. 
# Dla listy sąsiedztwa nie podajemy indeksu wierzchołka, np:
# Dla grafu :
# 0: 2, 4, 5
# 1: 4, 5
# 2: 0, 3, 4
# 3: 2
# 4: 0, 1, 2, 5
# 5: 0, 1, 4
#Wejscie będzie:
# 2 4 5 
# 4 5 
# 0 3 4 
# 2 
# 0 1 2 5 
# 0 1 4

def save_matrix_to_file(matrix, filename):
    np.savetxt(filename, matrix, fmt='%d')

def save_adj_list_to_file(adj_list_obj, filename):
    with open(filename, 'w') as f:
        for node, neighbors in adj_list_obj.list.items():
            line = f"{node}: {' '.join(map(str, neighbors))}\n"
            f.write(line)

def generate_10_graphs():
    os.makedirs("output", exist_ok=True)
    os.chdir("output")

    # 5 grafów G(n, p) - z wizualizacją kołową
    for i in range(1, 6):
        graph = generate_gnp(8, 0.4)
        prefix = f"gnp_{i}"

        save_matrix_to_file(graph.adjacency_matrix.matrix, f"adj_matrix_{prefix}.txt")
        save_adj_list_to_file(graph.adjacency_list, f"adj_list_{prefix}.txt")
        save_matrix_to_file(graph.incidence_matrix.matrix, f"inc_matrix_{prefix}.txt")

        plt.figure()
        graph.adjacency_matrix.visualize(circle=True)
        plt.savefig(f"{prefix}.png")
        plt.close()

    # 5 grafów G(n, l) - z wizualizacją siatkową
    for i in range(1, 6):
        graph = generate_gnl(8, 10)
        prefix = f"gnl_{i}"

        save_matrix_to_file(graph.adjacency_matrix.matrix, f"adj_matrix_{prefix}.txt")
        save_adj_list_to_file(graph.adjacency_list, f"adj_list_{prefix}.txt")
        save_matrix_to_file(graph.incidence_matrix.matrix, f"inc_matrix_{prefix}.txt")

        plt.figure()
        graph.adjacency_matrix.visualize(circle=False)
        plt.savefig(f"{prefix}.png")
        plt.close()

if __name__ == "__main__":
    generate_10_graphs()
