from zestaw_01.graph_coder import AdjacencyList
import random

#from graphicSequence
def construct_graph(A):
    A = A[:]
    A = sorted(enumerate(A), key=lambda x: x[1], reverse=True)
    n = len(A)

    degrees = [deg for _, deg in A]
    nodes = [idx for idx, _ in A]

    adj_list = {i: [] for i in nodes}

    while degrees and degrees[0] > 0:
        if degrees[0] >= len(degrees):
            return None

        d = degrees[0]
        node = nodes[0]

        for i in range(1, d + 1):
            if degrees[i] == 0:
                return None
            
            #dodane żeby wierzchołek nie mógł mieć krawędzi sam ze sobą
            neighbor = nodes[i]
            if node == neighbor:
                return None

            adj_list[node].append(nodes[i])
            adj_list[nodes[i]].append(node)
            degrees[i] -= 1  # Reduce degree

        degrees[0] = 0
        nodes.pop(0)
        degrees.pop(0)

        combined = sorted(zip(nodes, degrees), key=lambda x: x[1], reverse=True)
        if combined:
            nodes, degrees = zip(*combined)
            nodes, degrees = list(nodes), list(degrees)

    return adj_list if all(d == 0 for d in degrees) else None

def randomize_graph(adj_list, iterations = 10):
    edges = list(set((min(a,b), max(a,b)) for a in adj_list for b in adj_list[a]))

    for _ in range(iterations):
        if len(edges) < 2:
            break
        (a,b), (c,d) = random.sample(edges, 2)

        new_edge1 = tuple(sorted((a, d)))
        new_edge2 = tuple(sorted((b, c)))

        if (a == d or b == c) or (new_edge1 in edges) or (new_edge2 in edges):
            continue

        # Usuwanie starych krawędzi
        edges.remove((a,b))
        edges.remove((c,d))
        adj_list[a].remove(b)
        adj_list[b].remove(a)
        adj_list[c].remove(d)
        adj_list[d].remove(c)

        # dodawanie nowych krawędzi
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
        if comp[u] == -1:
            comp[u] = nr
            components_R(nr,u,G,comp)

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

def group_components(comp):
    listComp = {}
    for i, u in enumerate(comp):
        if u not in listComp:
            listComp[u] = []
        listComp[u].append(i)
    return listComp





def losowe_stopnie_wierzcholkow(n):
    stopnie = [random.randint(1, (n - 1) // 2) * 2 for _ in range(n)] #zbior parzsytych stopni mniejszy od n
    
    if sum(stopnie) % 2 != 0: #suma stopni powinna równać się podwojonej liczbie krawędzi
        idx = random.randint(0, n - 1)
        stopnie[idx] += 2
    
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
            stack.extend(adj_list[node])
    
    adj_list[u].remove(v)
    adj_list[v].remove(u)
    
    # sprawdzamy do ilu krawędzi można dojść po usunięciu krawędzi u-v
    visited = set()
    stack = [u]
    count_after = 0
    while stack:
        node = stack.pop()
        if node not in visited:
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
    stack = [start_node]
    
    while stack:
        u = stack[-1]
        if adj_list[u]: #szukamy krawędzi, która nie jest mostem i tą krawędź usuwamy z grafu = dodajemy do cyklu Eulera
            for v in adj_list[u]:
                if not sprawdz_most(adj_list, u, v):
                    break
            else:
                v = adj_list[u][0]
            
            adj_list[u].remove(v)
            adj_list[v].remove(u)
            stack.append(v)
        else:
            path.append(stack.pop())
    
    return path[::-1] #na wierzchu stosu jest ostatni dodany wierzchołek, więc odwracamy kolejność

def randomize_graph_euler(adj_list):
    adj_list = randomize_graph(adj_list, iterations=10)
    comp = components(adj_list)
    while len(set(comp)) != 1: #jeśli nie jest spójny to nie można znaleźć cyklu Eulera, graf spójny = 1 spójna składowa
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