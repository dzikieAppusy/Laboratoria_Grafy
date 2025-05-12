from zad1 import generate_gnp
from zad1 import AdjacencyList

#silnie spojny graf skierowany - miedzy kazda para wierzcholkow istnieje sciezka
#algorytm Kosaraju do znajdowania silnie wspolnych skladoych (2 przeszukiwania wglab)
#I DFS O(n + k)

def korsaraju(G):
    d = [] #czasy odwiedzin, czyli jak z danego wierzcholka nie damy rady dojsc dalej (brak lub juz odwiedzone weirzchoki) i zaczynamy sie cofac
    f = [] #czasy przetworzenia
    
    for i in range(G.nodes): #wszystkie wirzcholki oznaczamy jako nieodwiedzone
        d.append(-1)
        f.append(-1)
        
    t = 0
    
    for v in range(G.nodes): #dla kazdego wierzcholka przechodzimy przeszukiwaniem w glab 
        if d[v] == -1: #tylko jesli wierzcholek nie zostal jeszcze odwiedzony "w innym cyklu"
            t = dfs_visit(v, G, d, f, t)
            
    #majac uzupełnione d i f sprawdzamy ile jest skladowych
    G2 = AdjacencyList(G.nodes) #transpozycja
    for v in range(G.nodes):
        for u in G.adjacency_list.list[v]:
            G2.add_edge(u, v)
            
    nr = 0
    comp = [] #zbior silnie spojnych skladowych
    for v in range(G2.nodes):
        comp.append(-1)
        
    nodes_sorted = sorted(range(G.nodes), key=lambda x: f[x], reverse=True) #sortowanie wierzcholkow po czasie zakonczenia f
    for v in nodes_sorted:
        if comp[v] == -1: #jesli wierzcholek nie ma ustalonej skladowej
            nr = nr + 1
            comp[v] = nr
            components_r(nr, v, G2, comp)
        
    return comp

def dfs_visit(v, G, d, f, t): #przechodzi przez daną składową, w d są czasy wejścia do wierzchołka, w f czasy wyjścia
    t = t + 1
    d[v] = t
    for u in G.adjacency_list.get_neighbors(v): #jeśli u jest sasiadem v
        if d[u] == -1: #jak nie bylo jeszcze odwiedzone
            t = dfs_visit(u, G, d, f, t)
            
    t = t + 1
    f[v] = t
    return t

def components_r(nr, v, G2, comp):
    for u in G2.get_neighbors(v): #jeśli u jest sąsiadem v
        if comp[u] == -1: #jesli u nie ma skladowej
            comp[u] = nr
            components_r(nr, u, G2, comp) #przeszukujemy wglab tak zeby zebrac wszystkie wierzcholki nalezace do 1 spojnej skladowej

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