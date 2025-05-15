import heapq
from math import inf
from zestaw_04.zad2 import korsaraju
from zestaw_04.zad3 import bellman_ford, dodaj_wagi, najkrotsz_sciezka
from zestaw_04.zad1 import generate_gnp
from collections import defaultdict

# Można go zastąpić algorytmem z zestawu 3 w przyszłości
def dijkstra(graph, reweighted_weights, start):
    # Pobierz liczbę wierzchołków z obiektu 'graph' (liczba wierzchołków w adjacency_list)
    n = graph.adjacency_list.nodes
    distances = {v: inf for v in range(n)}
    predecessors = {v: None for v in range(n)}
    distances[start] = 0

    # Kolejka priorytetowa (min-heap)
    heap = [(0, start)]  # (dystans, wierzchołek)

    while heap:
        current_dist, u = heapq.heappop(heap)

        # Jeśli już odwiedziliśmy wierzchołek, pomijamy go
        if current_dist > distances[u]:
            continue

        # Sprawdź sąsiadów wierzchołka u
        for v in graph.adjacency_list.list[u]:
            weight = reweighted_weights.get((u, v), inf)
            if distances[v] > distances[u] + weight:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                heapq.heappush(heap, (distances[v], v))

    return distances, predecessors


def reweight_edges(graph, h):
    # Słownik na nowe (przeskalowane) wagi krawędzi
    reweighted_weights = {}

    # Iterujemy po wszystkich wierzchołkach u w grafie
    for u in graph.adjacency_list.list:
        # Iterujemy po wszystkich sąsiadach v wierzchołka u
        for v in graph.adjacency_list.list[u]:
            # Pobieramy oryginalną wagę krawędzi (u, v)
            # Jeśli krawędź nie istnieje, domyślnie waga to +∞
            original_weight = graph.weights.get((u, v), float('inf'))

            # Obliczamy nową wagę zgodnie ze wzorem Johnsona:
            # w'(u,v) = w(u,v) + h(u) - h(v)
            new_weight = original_weight + h[u] - h[v]

            # Zapisujemy przeważoną wagę do słownika
            reweighted_weights[(u, v)] = new_weight

    # Zwracamy słownik z nowymi wagami krawędzi
    return reweighted_weights

def johnson(G, w):
    # Dodanie nowego wierzchołka s do grafu G'
    G_prime = G.copy()  # Tworzymy kopię grafu
    G_prime.add_node()  # Dodajemy nowy wierzchołek (źródło pomocnicze)
    s = G_prime.nodes - 1  # Indeks nowego wierzchołka

    # Dodajemy krawędzie ze sztucznego wierzchołka s do wszystkich pozostałych wierzchołków
    for u in range(G.nodes):
        G_prime.add_edge(s, u, 0)  # Krawędzie o wadze 0

    # Uruchamiamy Bellmana-Forda z wierzchołka s, aby sprawdzić, czy nie ma cykli ujemnych
    if not bellman_ford(G_prime, w, s):
        raise Exception('Error')  # Jeśli są cykle ujemne, przerywamy algorytm
    else:
        h = []
        # Obliczamy funkcję potencjału h(v) dla każdego wierzchołka v
        for v in range(G_prime.nodes):
            h, helper = bellman_ford(G_prime.adjacency_list, G_prime.weights, v)
            # h zawiera dystanse z s do każdego wierzchołka (potencjały)
            # `helper` może zawierać dane do odtworzenia ścieżki – nieużywany tutaj

        # Przekształcamy wagi krawędzi w grafie zgodnie z funkcją h:
        # w'(u,v) = w(u,v) + h(u) - h(v)
        reweighted_weights = reweight_edges(G_prime, h)

        # Inicjalizujemy macierz D na wyniki (najkrótsze ścieżki między każdą parą wierzchołków)
        D = [[None for _ in range(G.nodes)] for _ in range(G.nodes)]

        # Dla każdego wierzchołka uruchamiamy Dijkstrę
        for u in range(G.nodes):
            dist_u, _ = dijkstra(G, reweighted_weights, u)
            for v in range(G.nodes):
                # Odtwarzamy oryginalne odległości z przekształconych wyników:
                # d(u,v) = d'(u,v) - h(u) + h(v)
                D[u][v] = dist_u[v] - h[u] + h[v]

    return D  # Zwracamy macierz najkrótszych ścieżek między wszystkimi parami wierzchołków
if __name__ == '__main__':
    while True:
        graph1 = generate_gnp(8, 0.2)
        components = korsaraju(graph1)
        if len(set(components)) == 1:  # dopóki nie wygenerujemy silnie spójnego digrafu
            break

    # Tworzenie nowego słownika
    component_groups = defaultdict(list)
    for node, component in enumerate(components):
        component_groups[component].append(node)

    print("Silnie spójne składowe:")
    for component, nodes in component_groups.items():
        print(f"Składowa {component}: {nodes}")
    print()
    graph1.visualize()
    G = dodaj_wagi(graph1.adjacency_list)
    G.zmien_wagi_na_ujemne()
    G.visualize()
    for row in johnson(G,G.weights):
        print(row)
