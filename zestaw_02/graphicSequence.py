from zestaw_01.graph_coder import AdjacencyList

def check_zero_elements(A):
    return all(a == 0 for a in A)

# Funkcja sprawdzająca czy dana sekwencja liczb jest ciągiem graficznym
def graphic_sequence(A):
    A = A[:]
    A.sort(reverse=True)

    while A and A[0] > 0:
        if check_zero_elements(A):
            return True
        if A[0] >= len(A):
            return False

        d = A[0]
        A = A[1:]

        if len(A) < d:
            return False

        for i in range(d):
            A[i] -= 1
            if A[i] < 0:
                return False

        A.sort(reverse=True)

    return True

# Funkcja służąca do stworzenia grafu z podanej sekwencji licz naturalnych
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


# Test cases
A = [1, 3, 2, 3, 2, 4, 1]
B = [1, 2, 4]

print(graphic_sequence(A))
print(graphic_sequence(B))

adj_list_A = construct_graph(A)
print(adj_list_A)

AdjList = AdjacencyList(len(A))
AdjList.list = adj_list_A
AdjList.display()
AdjList.visualize()