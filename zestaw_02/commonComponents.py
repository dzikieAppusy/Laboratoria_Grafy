from graphicSequence import construct_graph
from zestaw_01.graph_coder import AdjacencyList

# Rekurencyjna funkcja DFS do oznaczania wierzchołków należących do tej samej spójnej składowej
# nr – numer bieżącej składowej
# v – aktualnie odwiedzany wierzchołek
# G – graf w postaci listy sąsiedztwa
# comp – lista przypisująca wierzchołkom numer składowej (-1 oznacza nieodwiedzony)
def components_R(nr, v, G, comp):
    for u in G[v]:  # Przechodzimy przez sąsiadów v
        if comp[u] == -1:  # Jeśli wierzchołek nie został jeszcze odwiedzony
            comp[u] = nr  # Przypisujemy mu numer bieżącej składowej
            components_R(nr, u, G, comp)  # Rekurencyjnie odwiedzamy sąsiadów

# G – graf jako lista sąsiedztwa (np. G[0] = [1,2] oznacza, że wierzchołek 0 ma krawędzie do 1 i 2)
def components(G):
    nr = 0  # Numerowanie składowych spójnych, zaczynamy od 0 i zwiększamy przy każdej nowej
    n = len(G)  # Liczba wierzchołków
    comp = [-1] * n  # Tworzymy listę oznaczającą do której składowej należy dany wierzchołek

    for v in range(n):  # Iterujemy po wszystkich wierzchołkach
        if comp[v] == -1:  # Jeśli wierzchołek nie został jeszcze przypisany do składowej
            nr += 1  # Zaczynamy nową składową
            comp[v] = nr
            components_R(nr, v, G, comp)  # Uruchamiamy DFS dla tej składowej

    return comp  # Zwracamy listę przypisań wierzchołków do składowych

# Funkcja grupuje wierzchołki według ich przypisanej składowej
# comp – lista zawierająca numer składowej dla każdego wierzchołka
def group_components(comp):
    listComp = {}  # Słownik: klucz to numer składowej, wartość to lista wierzchołków
    for i, u in enumerate(comp):  # Iterujemy po liście przypisań
        if u not in listComp:
            listComp[u] = []  # Tworzymy nową listę jeśli to pierwszy wierzchołek w tej składowej
        listComp[u].append(i)  # Dodajemy wierzchołek do odpowiedniej składowej
    return listComp  # Zwracamy słownik grup wierzchołków

#Tests
if __name__ == '__main__':
    A = [1, 3, 2, 3, 2, 4, 1]
    adj_list_A = construct_graph(A)
    AdjList = AdjacencyList(len(A))
    AdjList.list = adj_list_A
    AdjList.visualize()
    g = components(adj_list_A)
    print("Wspólne składowe: {}".format(group_components(g)))
