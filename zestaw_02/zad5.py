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






def main():
    print("Podaj liczbę wierzchołków:")
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
    
if __name__ == "__main__":
    main()