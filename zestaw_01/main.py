from graph_coder import AdjacencyMatrix, IncidenceMatrix, AdjacencyList

#podając wejście dla macierzy podajemy po prostu po kolei : wiersz + znak nowej linii. 
# Dla listy sąsiedztwa nie podajemy indeksu wierzchołka, np:
# Dla grafu :
# 0: 2, 4, 5
# 1: 4, 5
# 2: 0, 3, 4
# 3: 2
# 4: 0, 1, 2, 5
# 5: 0, 1, 4
#Wejscie będzie:
# 2 4 5 
# 4 5 
# 0 3 4 
# 2 
# 0 1 2 5 
# 0 1 4

def main():
    print("Wybierz format wejściowy:")
    print("1 - Macierz sąsiedztwa")
    print("2 - Macierz incydencji")
    print("3 - Lista sąsiedztwa")
    choice = int(input("Wybór: "))
    
    if choice == 1:
        nodes = int(input("Podaj liczbę wierzchołków: "))
        adjacency_matrix = AdjacencyMatrix(nodes)
        print("Podaj macierz sąsiedztwa wiersz po wierszu:")
        for i in range(nodes):
            adjacency_matrix.matrix[i] = list(map(int, input().split()))
        adjacency_matrix.display()
        adjacency_matrix.to_adjacency_list().display()
        adjacency_matrix.to_incidence_matrix().display()
        adjacency_matrix.visualize()
    
    elif choice == 2:
        nodes = int(input("Podaj liczbę wierzchołków: "))
        edges = int(input("Podaj liczbę krawędzi: "))
        incidence_matrix = IncidenceMatrix(nodes, edges)
        print("Podaj macierz incydencji wiersz po wierszu:")
        for i in range(nodes):
            incidence_matrix.matrix[i] = list(map(int, input().split()))
        incidence_matrix.display()
        incidence_matrix.to_adjacency_list().display()
        incidence_matrix.to_adjacency_matrix().display()
        incidence_matrix.visualize()
    
    elif choice == 3:
        nodes = int(input("Podaj liczbę wierzchołków: "))
        adjacency_list = AdjacencyList(nodes)
        print("Podaj listę sąsiedztwa")
        for i in range(nodes):
            adjacency_list.list[i] = list(map(int, input().split()))
        adjacency_list.display()
        adjacency_list.to_adjacency_matrix().display()
        adjacency_list.to_incidence_matrix().display()
        adjacency_list.visualize()
    else:
        print("Niepoprawny wybór.")

if __name__ == "__main__":
    main()