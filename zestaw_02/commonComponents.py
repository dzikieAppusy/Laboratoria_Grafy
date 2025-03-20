from graphicSequence import construct_graph
from zestaw_01.graph_coder import AdjacencyList

# algorytm z wykładu
def components_R(nr,v,G,comp):
    for u in G[v]:
        if comp[u] == -1:
            comp[u] = nr
            components_R(nr,u,G,comp)

# Jako parametr G jest podawany graf w postaci listy sąsiedztwa
def components(G):
    nr = 0
    n = len(G)
    comp = [-1]*n

    for v in range(n):
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            components_R(nr,v,G,comp)

    return comp

# Funkcja dzieląca na grupy dla lepszego obrazowania wspólnych składowych
def group_components(comp):
    listComp = {}
    for i, u in enumerate(comp):
        if u not in listComp:
            listComp[u] = []
        listComp[u].append(i)
    return listComp

#Tests
A = [1, 3, 2, 3, 2, 4, 1]
adj_list_A = construct_graph(A)
g = components(adj_list_A)

print("Wspólne składowe: {}".format(group_components(g)))
