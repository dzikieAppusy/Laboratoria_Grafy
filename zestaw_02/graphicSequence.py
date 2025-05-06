from zestaw_01.graph_coder import AdjacencyList
import random

# Funkcja pomocnicza: sprawdza, czy wszystkie elementy listy A są równe zero
def check_zero_elements(A):
    return all(a == 0 for a in A)

# Zadanie 1
# Funkcja sprawdzająca, czy dana sekwencja liczb jest ciągiem graficznym (algorytm Havel-Hakimi)
def graphic_sequence(A):
    A = A[:]  # Tworzymy kopię listy, żeby nie modyfikować oryginału
    A.sort(reverse=True)  # Sortujemy malejąco

    # Dopóki lista nie jest pusta i największy element > 0
    while A and A[0] > 0:
        if check_zero_elements(A):
            return True  # Wszystkie stopnie są 0, czyli to ciąg graficzny

        if A[0] >= len(A):
            return False  # Nie można połączyć tylu wierzchołków - błąd

        d = A[0]  # Największy stopień
        A = A[1:]  # Usuwamy ten element

        if len(A) < d:
            return False  # Nie ma wystarczającej liczby wierzchołków do połączenia

        # Odejmuje 1 od kolejnych d elementów (symulując połączenia)
        for i in range(d):
            A[i] -= 1
            if A[i] < 0:
                return False  # Stopień nie może być ujemny

        A.sort(reverse=True)  # Sortujemy ponownie

    return True  # Jeśli pętla się skończy, to ciąg jest graficzny

# Funkcja tworzy graf (listę sąsiedztwa) z danej sekwencji stopni (jeśli jest graficzna)
def construct_graph(A):
    A = A[:]  # Tworzymy kopię
    # Sortujemy pary (indeks, stopień) malejąco po stopniu
    A = sorted(enumerate(A), key=lambda x: x[1], reverse=True)
    n = len(A)

    # Rozdzielamy indeksy i stopnie
    degrees = [deg for _, deg in A]
    nodes = [idx for idx, _ in A]

    # Tworzymy pustą listę sąsiedztwa
    adj_list = {i: [] for i in nodes}

    # Dopóki są jeszcze stopnie do przypisania
    while degrees and degrees[0] > 0:
        if degrees[0] >= len(degrees):
            return None  # Nie można połączyć tylu wierzchołków

        d = degrees[0]  # Największy stopień
        node = nodes[0]  # Wierzchołek o największym stopniu

        # Łączymy ten wierzchołek z kolejnymi d wierzchołkami
        for i in range(1, d + 1):
            if degrees[i] == 0:
                return None  # Nie można już użyć wierzchołka bez stopnia

            # Dodajemy krawędź do obu list sąsiedztwa (graf nieskierowany)
            adj_list[node].append(nodes[i])
            adj_list[nodes[i]].append(node)
            degrees[i] -= 1  # Zmniejszamy stopień

        degrees[0] = 0  # Aktualny wierzchołek już został przetworzony
        nodes.pop(0)    # Usuwamy go z listy
        degrees.pop(0)

        # Sortujemy pozostałe wierzchołki po aktualnych stopniach malejąco
        combined = sorted(zip(nodes, degrees), key=lambda x: x[1], reverse=True)
        if combined:
            nodes, degrees = zip(*combined)
            nodes, degrees = list(nodes), list(degrees)

    # Zwracamy listę sąsiedztwa, jeśli wszystkie stopnie zostały wykorzystane
    return adj_list if all(d == 0 for d in degrees) else None

# Zadanie 2
# Funkcja losowo modyfikuje graf (bez zmiany stopni wierzchołków) poprzez przetasowywanie krawędzi

def randomize_graph(adj_list, iterations=10):
    # Tworzymy listę unikalnych krawędzi w formacie (mniejszy_wierzchołek, większy_wierzchołek)
    edges = list(set((min(a, b), max(a, b)) for a in adj_list for b in adj_list[a]))

    # Wykonujemy podaną liczbę iteracji przetasowywania
    for _ in range(iterations):
        if len(edges) < 2:
            break  # Potrzebujemy przynajmniej dwóch krawędzi do zamiany

        # Losowo wybieramy dwie różne krawędzie
        (a, b), (c, d) = random.sample(edges, 2)

        # Sprawdzamy warunki bezpieczeństwa przed zamianą
        # Unikamy tworzenia pętli (np. a==d), i sprawdzamy czy nowe krawędzie już nie istnieją
        if a == d or b == c or (a, d) in edges or (b, c) in edges or (d, a) in edges or (c, b) in edges:
            continue  # Jeśli nowe krawędzie byłyby niepoprawne, pomijamy iterację

        # Usuwamy stare krawędzie z listy i listy sąsiedztwa
        edges.remove((a, b))
        edges.remove((c, d))
        adj_list[a].remove(b)
        adj_list[b].remove(a)
        adj_list[c].remove(d)
        adj_list[d].remove(c)

        # Dodajemy nowe krawędzie do listy i listy sąsiedztwa
        edges.append((a, d))
        edges.append((b, c))
        adj_list[a].append(d)
        adj_list[d].append(a)
        adj_list[b].append(c)
        adj_list[c].append(b)

    # Zwracamy zmodyfikowaną listę sąsiedztwa
    return adj_list

if __name__ == '__main__':
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

    # Testy randomizacji grafu
    AdjList.list=randomize_graph(AdjList.list)
    AdjList.visualize()
