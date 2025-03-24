
from zestaw_03.weighted_graph import generate_gnp


def minimum_spanning_tree(G):
    visited = [False] * G.nodes
    mst_edges = []
    total_weight = 0

    visited[0] = True
    for _ in range(G.nodes - 1):
        min_weight = float('inf')
        u_min, v_min = -1, -1
        for u in range(G.nodes):
            if visited[u]:
                for v in range(G.nodes):
                    if not visited[v] and G.adjacency_matrix.matrix[u][v] == 1:
                        if G.weights[u][v] < min_weight:
                            min_weight = G.weights[u][v]
                            u_min, v_min = u, v
        if u_min != -1 and v_min != -1:
            mst_edges.append((u_min, v_min, G.weights[u_min][v_min]))
            total_weight += G.weights[u_min][v_min]
            visited[v_min] = True

    return mst_edges, total_weight

def main():
    graph = generate_gnp(7, 0.5)

    mst, total = minimum_spanning_tree(graph)
    print("Minimum Spanning Tree:")
    for u, v, w in mst:
        print(f"{u} -- {v}  (waga: {w})")
    print("\nCałkowita waga MST: {total}")
    graph.visualize_weighted(spanning_tree = True, mst = mst, total = total)


if __name__ == "__main__":
    main()