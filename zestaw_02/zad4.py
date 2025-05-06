from zestaw_01.graph_coder import AdjacencyList
import random



'''
Używając powyższych programów napisać program do tworzenia losowego grafu eulerowskiego i znajdowania na nim cyklu Eulera.

Cykl Eulera - graf spójny, wierzchoki mają parzyste stopnie, ścieżka zawierająca 1 raz każdą krawędź grafu.
Mostem nazywamy taką krawędź, której usunięcie spowoduje utratę spójności.

Algorytm Fleury’ego: niech G będzie grafem eulerowskim. Wtedy następująca konstrukcja jest wykonalna i daje w wyniku cykl Eulera w grafie G.
Zacznij cykl w dowolnym wierzchołku u i przechodź krawędzie w dowolnej kolejności, dbając jedynie
o zachowanie następujących zasad:
1. usuwaj z grafu przechodzone krawędzie i wierzchołki izolowane powstające w wyniku usuwania tych krawędzi
2. w każdym momencie przechodź przez most tylko wtedy, gdy nie masz innej możliwości
'''



#from graphicSequence
def construct_graph(A):
    A = A[:]
    A = sorted(enumerate(A), key=lambda x: x[1], reverse=True)
    n = len(A)

    degrees = [deg for _, deg in A] #stopnie
    nodes = [idx for idx, _ in A] #wierzchołki

    adj_list = {i: [] for i in nodes}

    while degrees and degrees[0] > 0: #dopóki sa jeszcze jakieś "wolne" stopnie
        if degrees[0] >= len(degrees): #jeśli większy stopień niż ogólna ilość stopni to nie będzie jak tego połączyć
            return None

        d = degrees[0]
        node = nodes[0]

        for i in range(1, d + 1): #dodawani krawędzi między sąsiadami i wierzchołkiem
            if degrees[i] == 0:
                return None
            
            #dodane żeby wierzchołek nie mógł mieć krawędzi sam ze sobą
            neighbor = nodes[i]
            if node == neighbor:
                return None

            adj_list[node].append(nodes[i]) #dodaje do listy utworzone krawędzie
            adj_list[nodes[i]].append(node)
            degrees[i] -= 1  # Reduce degree

        degrees[0] = 0 #usuwa wierzchołek, który ma już wszystkie krawędzie utworzone
        nodes.pop(0)
        degrees.pop(0)

        combined = sorted(zip(nodes, degrees), key=lambda x: x[1], reverse=True) #kolejność malejących stopni, bo wierzchołek z największym stopniem musi mieć najwięcej połączeń
        if combined:
            nodes, degrees = zip(*combined)
            nodes, degrees = list(nodes), list(degrees)

    return adj_list if all(d == 0 for d in degrees) else None #zwraca listę sąsiedztwa

def randomize_graph(adj_list, iterations = 10):
    edges = list(set((min(a,b), max(a,b)) for a in adj_list for b in adj_list[a])) #lista krawędzi

    for _ in range(iterations):
        if len(edges) < 2:
            break
        (a,b), (c,d) = random.sample(edges, 2)

        new_edge1 = tuple(sorted((a, d)))
        new_edge2 = tuple(sorted((b, c)))

        if (a == d or b == c) or (new_edge1 in edges) or (new_edge2 in edges): #żeby nie było powtórek albo pętli
            continue

        #usuwanie starych krawędzi
        edges.remove((a,b))
        edges.remove((c,d))
        adj_list[a].remove(b)
        adj_list[b].remove(a)
        adj_list[c].remove(d)
        adj_list[d].remove(c)

        #dodawanie nowych krawędzi
        edges.append((a, d))
        edges.append((b, c))
        adj_list[a].append(d)
        adj_list[d].append(a)
        adj_list[b].append(c)
        adj_list[c].append(b)

    return adj_list

#from commonComponents
def components_R(nr,v,G,comp):
    for u in G[v]:
        if comp[u] == -1: #jeszcze nieodwiedzony
            comp[u] = nr
            components_R(nr,u,G,comp) #DFS żeby wszystkie połączone wierzchołki zaliczyć do tej samej składowej

def components(G):
    nr = 0
    n = len(G)
    comp = [-1]*n #każdy wierzchołek nieodwiedzony (-1)

    for v in range(n):
        if comp[v] == -1: #jeszcze nieodwiedzony
            nr += 1
            comp[v] = nr
            components_R(nr,v,G,comp) #DFS żeby wszystkie połączone wierzchołki zaliczyć do tej samej składowej

    return comp

def group_components(comp):
    listComp = {}
    for i, u in enumerate(comp): #grupuje wierzchołki do kolejnych składowych
        if u not in listComp:
            listComp[u] = []
        listComp[u].append(i)
    return listComp





def losowe_stopnie_wierzcholkow(n):
    stopnie = [random.randint(1, (n - 1) // 2) * 2 for _ in range(n)] #zbior parzystych stopni od 2 do n-1, dla n wierzchołków
    #suma stopni powinna równać się podwojonej liczbie krawędzi (2 wierzchołki łączy 1 krawędź), więc musi być parzysta
    
    return stopnie

def sprawdz_most(adj_list, u, v):
    #sprawdzamy do ilu krawędzi można dojść
    visited = set()
    stack = [u]
    count_before = 0
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            count_before += 1
            stack.extend(adj_list[node]) #dodajemy wszystkich sąsiadów i ich będziemy sprawdzać dalej
    
    adj_list[u].remove(v)
    adj_list[v].remove(u)
    
    # sprawdzamy do ilu krawędzi można dojść po usunięciu krawędzi u-v
    visited = set()
    stack = [u]
    count_after = 0
    while stack: #przeszukiwanie wgłąb 
        node = stack.pop()
        if node not in visited: #
            visited.add(node)
            count_after += 1
            stack.extend(adj_list[node])
    
    adj_list[u].append(v)
    adj_list[v].append(u)
    
    return count_before != count_after #jeśli są różne wyniki to krawędź u-v jest mostem

#na podstawie https://www.geeksforgeeks.org/fleurys-algorithm-for-printing-eulerian-path/
def fleury_algorithm(adj_list):
    start_node = next(iter(adj_list))
    path = []
    stack = [start_node] #dodajemy 1 wierzchołek
    
    while stack:
        u = stack[-1]
        if adj_list[u]: #jeśli wierzchołek ma jakichś sąsiadów, szukamy krawędzi, która nie jest mostem i tą krawędź usuwamy z grafu = dodajemy do cyklu Eulera
            for v in adj_list[u]:
                if not sprawdz_most(adj_list, u, v): #jak nie jest mostem to możemy usunąć badaną krawędź i sprawdzać dalej
                    break
            else:
                v = adj_list[u][0] #bierzemy pierwszego sąsiada wierzchołka
            
            adj_list[u].remove(v)
            adj_list[v].remove(u)
            stack.append(v) #teraz szukamy od v
        else:
            path.append(stack.pop()) #jak już nie ma sąsiadów to trafia do ścieżki Eulera (dodawane są od końcowego do początkowego)
    
    return path[::-1] #na wierzchu stosu jest ostatni dodany wierzchołek, więc odwracamy kolejność

def randomize_graph_euler(adj_list):
    adj_list = randomize_graph(adj_list, iterations=10)
    comp = components(adj_list) #chcemy żeby była 1 spójna składowa, bo tylko wtedy wszystkie wierzchołki są połączone
    while len(set(comp)) != 1 and all(len(n) % 2 != 0 for n in adj_list.values()): #jeśli nie jest spójny to nie można znaleźć cyklu Eulera, graf spójny -> 1 spójna składowa,, trzeba sprawdzić czy wierzchołki mają parzsyty stopień (1 krawędź wchodzi, a druga wychodzi)
        adj_list = randomize_graph(adj_list, iterations=10)
        comp = components(adj_list)
    return adj_list

def main():
    print("Podaj liczbę wierzchołków (warunek: n >= 3):")
    n = int(input())
    while n < 3:
            print("Liczba wierzchołków musi być większa lub równa 3.")
            n = int(input())
    
    
    A = losowe_stopnie_wierzcholkow(n)
    adj_list = construct_graph(A)
    if adj_list is None:
        print("Nie można skonstruować grafu.")
        return
    
    # wygenerowany graf
    AdjList = AdjacencyList(len(A))
    AdjList.list = adj_list
    AdjList.display()
    AdjList.visualize()
    
    adj_list = randomize_graph_euler(adj_list)
    
    #graf po randomizacji
    AdjList = AdjacencyList(len(A))
    AdjList.list = adj_list
    AdjList.display()
    AdjList.visualize()
    
    #graf powinien być spójny (każda para wierzchołków połączona 1 ścieżką) + ma parzyste stopnie wierzchołków
    wynik = fleury_algorithm(adj_list)
    print("Cykl Eulera:")
    print(wynik)

if __name__ == "__main__":
    main()