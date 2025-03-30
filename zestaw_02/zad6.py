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





#based on https://www.geeksforgeeks.org/hamiltonian-cycle/
def has_hamiltonian_cycle(adj_list):
    n = len(adj_list)
    visited = [False] * n
    path = []

    for start_node in range(n): #próbujemy każdy wierzchołek
        if dfs(start_node, start_node, 1, visited, path, adj_list, n):
            print("Cykl Hamiltona:", path + [start_node])
            return True

    print("Cykl Hamiltona nie znaleziony.")
    return False

def dfs(node, start, count, visited, path, adj_list, n):
        visited[node] = True
        path.append(node) #początkowy wierzchołek dodany do cyklu

        if count == n: #jeśli długość listy jest równa ilości wierzchołków to nie ma już więcej wierzchołków do odwiedzenia
            if start in adj_list[node]: #ostatni odwiedzony wierzchołek musi być połączony z pierwszym
                return True
            else:
                visited[node] = False #cofamy się o 1 krok do góry
                path.pop()
                return False

        for neighbor in adj_list[node]: #wśró tych, które nie zostały jeszcze odwiedzone podczas danego sprawdzania szukamy cyklu
            if not visited[neighbor]:
                if dfs(neighbor, start, count + 1, visited, path, adj_list, n):
                    return True

        visited[node] = False
        path.pop()
        return False
    
    

def main():
    print("Podaj liczbę wierzchołków (warunek: n >= 3):")
    n = int(input())
    while n < 3:
        print("Liczba wierzchołków musi być większa lub równa 3 żeby występowanie cyklu Hamiltona było możliwe.")
        n = int(input())
    
    print("Podaj stopień wierzchołków:")
    k = int(input())    
    while k >= n:
            print("Stopień wierzchołków musi być niższy niż ich ilość.")
            k = int(input())
    while (n * k) % 2 != 0:
            print("Stopień wierzchołków musi być parzysty jeśli ich ilość jest nieparzysta.")
            k = int(input())
        
            
    A = [k] * n
    adj_list = construct_graph(A)
    if adj_list is None:
        print("Nie można skonstruować grafu.")
        return
    
    adj_list = randomize_graph(adj_list, iterations=100)
    
    # wygenerowany graf
    AdjList = AdjacencyList(len(A))
    AdjList.list = adj_list
    AdjList.display()
    AdjList.visualize()
    
    print("ADJ")
    print(adj_list)
    print("ADJ")    
    #na podstawie grafu k-regularnego sprawdzamy czy występuje cykl Hamiltona
    #graf musi być spójny
    comp = components(adj_list)
    if len(set(comp)) != 1:
        print("Graf nie jest spójny, nie można znaleźć cyklu Hamiltona.")
        return
    
    has_hamiltonian_cycle(adj_list)
    
    print("\n\n\nDla agrafu k-nieregularnego")
    
    adj_list = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1, 3],
        3: [0, 2]
    }
    adj_list = {
        0: [2, 3],
        1: [2],
        2: [0, 1, 3],
        3: [0, 2]
    }
    # adj_list = randomize_graph(adj_list, iterations=10)
    
    # wygenerowany graf
    AdjList = AdjacencyList(len(A))
    AdjList.list = adj_list
    AdjList.display()
    AdjList.visualize()
    
    #na podstawie grafu k-regularnego sprawdzamy czy występuje cykl Hamiltona
    #graf musi być spójny
    comp = components(adj_list)
    if len(set(comp)) != 1:
        print("Graf nie jest spójny, nie można znaleźć cyklu Hamiltona.")
        return
    
    has_hamiltonian_cycle(adj_list)
    
if __name__ == "__main__":
    main()