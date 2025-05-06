from zestaw_03.weighted_graph import generate_connected_gnp
from zestaw_03.dijkstra import dijkstra, reconstruct_path
from zestaw_03.distans_matrix import distance_matrix, find_graph_center, find_minimax_center
from zestaw_03.prim import minimum_spanning_tree
import matplotlib.pyplot as plt

def main():
    # Tworzenie grafu
    graph = generate_connected_gnp(12, 0.4)
    start = 0

    # Zadanie 2: Algorytm Dijkstry
    print(f"ZADANIE 2: Najkrótsze ścieżki od wierzchołka {start}")
    ds, ps = dijkstra(graph, start)
    for v in range(graph.nodes):
        path = reconstruct_path(ps, v)
        path_str = " - ".join(str(p) for p in path)
        print(f"d({start}, {v}) = {ds[v]} ==> [{path_str}]")

    # Zadanie 3: Macierz odległości
    print("\nZADANIE 3: Macierz odległości między wszystkimi parami wierzchołków:")
    D = distance_matrix(graph)
    print(D)

    # Zadanie 4: Centrum grafu i centrum minimax
    center, center_sum = find_graph_center(D)
    minimax, minimax_dist = find_minimax_center(D)

    print(f"\nZADANIE 4: Centrum grafu: wierzchołek {center}, suma odległości = {center_sum}")
    print(f"Centrum minimax: wierzchołek {minimax}, maksymalna odległość = {minimax_dist}")

    # Wizualizacja pełnego grafu
    graph.visualize_weighted(layout="spring")
    plt.savefig("graph_full.png")
    plt.close()

    # Zadanie 5: Minimum Spanning Tree
    print("\nZADANIE 5: Drzewo rozpinające o minimalnej wadze (MST):")
    mst_edges, total_weight = minimum_spanning_tree(graph)
    for u, v, w in mst_edges:
        print(f"{u} -- {v}  (waga: {w})")
    print(f"Całkowita waga MST: {total_weight}")

    # Wizualizacja grafu z MST
    graph.visualize_weighted(layout="spring", spanning_tree=True, mst=mst_edges, total=total_weight)
    plt.savefig("graph_mst.png")
    plt.close()

if __name__ == "__main__":
    main()
