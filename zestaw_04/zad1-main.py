from zad1 import generate_gnp
from zad1 import AdjacencyList

def main():    
    d = AdjacencyList(7)
    d.add_edge(0, 1)
    d.add_edge(0, 2)
    d.add_edge(0, 4)
    d.add_edge(1, 0)
    d.add_edge(1, 2)
    d.add_edge(1, 3)
    d.add_edge(1, 4)
    d.add_edge(1, 6)
    d.add_edge(2, 5)
    d.add_edge(3, 1)
    d.add_edge(3, 6)
    d.add_edge(4, 6) 
    d.add_edge(5, 1)
    d.add_edge(6, 5)

    d.display()
    d.visualize()

    #macierz sąsiedztwa
    am = d.to_adjacency_matrix()
    am.display()

    #macierz incydencji
    im = d.to_incidence_matrix()
    im.display()
        
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
    

if __name__ == "__main__":
    main()