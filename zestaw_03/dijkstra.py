from .weighted_graph import generate_connected_gnp
import matplotlib.pyplot as plt 

def init(graph, start):
    n = graph.nodes
    ds = [float('inf')] * n  # ds[v] = długość najkrótszej ścieżki z s do v
    ps = [None] * n          # ps[v] = poprzednik v na najkrótszej ścieżce
    ds[start] = 0
    return ds, ps

def relax(u, v, weights, ds, ps):
    if ds[v] > ds[u] + weights[u][v]:
        ds[v] = ds[u] + weights[u][v]
        ps[v] = u

def dijkstra(graph, start=0):
    ds, ps = init(graph, start)
    n = graph.nodes
    visited = set()  # S <- /0

    while len(visited) < n:  # while S != zbiór wszystkich wierzchołków
        # u <- wierzchołek o najmniejszym ds[u] spośród niegotowych
        u = min((i for i in range(n) if i not in visited), key=lambda x: ds[x])
        visited.add(u)  # S <- S ∪ {u}

        # for każdy sąsiad v nie w S:
        for v in range(n):
            if graph.adjacency_matrix.matrix[u][v] == 1 and v not in visited:
                relax(u, v, graph.weights, ds, ps)

    return ds, ps

# Odtworzenie ścieżki z tablicy poprzedników
def reconstruct_path(ps, target):
    path = []
    while target is not None:
        path.append(target)
        target = ps[target]
    path.reverse()
    return path

# Główna funkcja testująca algorytm
def main():
    graph = generate_connected_gnp(12, 0.4)
    start = 0
    ds, ps = dijkstra(graph, start)

    print(f"START : s = {start}")  # numeracja od 1
    for v in range(graph.nodes):
        path = reconstruct_path(ps, v)
        path_str = " - ".join(str(p) for p in path)  # numeracja od 1
        print(f"d ({v}) = {ds[v]} ==> [{path_str}]")
    def save_show():
        plt.savefig("graph_visualization.png")
        plt.close()
    plt.show = save_show
    graph.visualize_weighted(layout="spring")

if __name__ == "__main__":
    main()
