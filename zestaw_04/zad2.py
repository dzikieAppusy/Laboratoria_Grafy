from zad1 import generate_gnp
from zad1 import AdjacencyList

def korsaraju(G):
    d = []
    f = []
    
    for i in range(G.nodes):
        d.append(-1)
        f.append(-1)
        
    t = 0
    
    for v in range(G.nodes):
        if d[v] == -1:
            t = dfs_visit(v, G, d, f, t)
            
    #mając uzupełnione d i f sprawdzamy ile jest składowych
    G2 = AdjacencyList(G.nodes) #transpozycja
    for v in range(G.nodes):
        for u in G.adjacency_list.list[v]:
            G2.add_edge(u, v)
            
    nr = 0
    comp = []
    for v in range(G2.nodes):
        comp.append(-1)
        
    nodes_sorted = sorted(range(G.nodes), key=lambda x: f[x], reverse=True)
    for v in nodes_sorted:
        if comp[v] == -1:
            nr = nr + 1
            comp[v] = nr
            components_r(nr, v, G2, comp)
        
    return comp

def dfs_visit(v, G, d, f, t): #przechodzi przez daną składową, w d są czasy wejścia do wierzchołka, w f czasy wyjścia
    t = t + 1
    d[v] = t
    for u in G.adjacency_list.get_neighbors(v): #jeśli u jest sąsiadem v
        if d[u] == -1:
            t = dfs_visit(u, G, d, f, t)
            
    t = t + 1
    f[v] = t
    return t

def components_r(nr, v, G2, comp):
    for u in G2.get_neighbors(v): #jeśli u jest sąsiadem v
        if comp[u] == -1:
            comp[u] = nr
            components_r(nr, u, G2, comp)

def main():
    print("Podaj liczbę wierzchołków:")
    n = int(input())
    print("Podaj prawdopodobieństwo, że pomiędzy dwoma wierzchołkami istnieje krawędź (warunek: 0 <= p <= 1):")
    p = float(input())
    while p < 0 or p > 1:
        print("Prawdopodobieństwo musi mieć wartość od o do 1.")
        p = float(input())
        
    graph1 = generate_gnp(n, p)
    print("\n--- Digraf G(n, p) ---")
    graph1.display()
    graph1.visualize()
    
    #tylko 1 silnie spójna składowa = graf jest silnie spójny, między każdą parą wierzchołków istnieje ścieżka
    components = korsaraju(graph1)
    
    from collections import defaultdict
    component_groups = defaultdict(list)
    for node, component in enumerate(components):
        component_groups[component].append(node)

    print("Silnie spójne składowe:")
    for component, nodes in component_groups.items():
        print(f"Składowa {component}: {nodes}")
    
if __name__ == "__main__":
    main()