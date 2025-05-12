from zad1 import generate_gnp
from zad2 import korsaraju
from collections import defaultdict
from zad1 import AdjacencyList
import random
import matplotlib.pyplot as plt
import networkx as nx #libka do rysowania grafów
import math

class DigraphWithWeights:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adjacency_list = AdjacencyList(nodes)
        self.weights = {} #poszerzenie klasy AdjacencyList o wagi krawedzi

    def add_edge(self, u, v, weight):
        self.adjacency_list.add_edge(u, v)
        self.weights[(u, v)] = weight

    def display(self):
        print("=== Lista sąsiedztwa ===\n")
        self.adjacency_list.display()
        print("=== Wagi krawędzi ===\n")
        for edge, weight in self.weights.items():
            print(f"Krawędź {edge}: waga {weight}")

    def visualize(self):
        G = nx.DiGraph()
        G.add_nodes_from(range(self.nodes))
        for (u, v), weight in self.weights.items():
            G.add_edge(u, v, weight=weight)
            
        pos = {
            i: (
                math.cos(2 * math.pi * i / self.nodes),
                math.sin(2 * math.pi * i / self.nodes)
            )
            for i in range(self.nodes)
        }
        
        fig, ax = plt.subplots(figsize=(6, 6))
        circle = plt.Circle((0, 0), 1.05, color='gray', fill=False, linestyle='dashed')
        ax.add_patch(circle)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax)
        
        edge_labels = {(u, v): f"{weight}" for (u, v), weight in self.weights.items()} #dodanie wag krawedzi
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_color='red')

        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        plt.show()
        
    def zmien_wagi_na_ujemne(self):
        #wylosowane 3 krawędzie o wadze <= 2 staną się ujemne
        negative_edges = random.sample(
            [edge for edge, weight in self.weights.items() if weight <= 2], 
            min(3, len([edge for edge, weight in self.weights.items() if weight <= 2]))
        )
        for edge in negative_edges:
            self.weights[edge] = -abs(self.weights[edge]) #zmiana na ujemne dla wylosowanych krawedzi
            
        
        
def dodaj_wagi(adj_list, min_weight= 1, max_weight = 10):
    wg = DigraphWithWeights(adj_list.nodes)
    
    for u in range(adj_list.nodes):
        for v in adj_list.list[u]:
            weight = random.randint(min_weight, max_weight) #dodanie wad z zakresu
            wg.add_edge(u, v, weight)
    
    return wg

def bellman_ford(G, w, s): #algorytm dziala przy ujemnych wagach i wykrywa ujemny cykl, G - graf, w - wagi, s - wierzcholek startowy
    n = G.nodes
    
    d = [float('inf')] * n
    helper = [None] * n #zapamietywanie wierzcholkow w najkrotszej sciezce
    d[s] = 0 #wierzchołek startowy, odleglosc 0
    
    for i in range(n - 1):
        for (u, v) in w:
            relax(d, u, v, w, helper) #dla kazdego wierzcholka szukamy najkrotszej sciezki
    
    for (u, v) in w:
        if d[v] > d[u] + w[(u, v)]:
            return None #pojawił się cykl ujemny
    
    return d, helper

def relax(d, u, v, w, helper):
    if d[u] + w[(u, v)] < d[v]: #jesli aktualnie sprawdzana krawedz ma mniejsza wage to ja wybieramy
        d[v] = d[u] + w[(u, v)]
        helper[v] = u

def najkrotsz_sciezka(helper, node): #node - wierzcholek koncowy sciezki
    path = []
    current = node
    
    while current is not None: #dopoki nie dotarlismy do pierwszego wierzcholka to dodajemy wierzcholki do sciezki
        path.append(current)
        current = helper[current]
    
    path.reverse()
    return path

def main():    
    while True:
        graph1 = generate_gnp(8, 0.2)    
        components = korsaraju(graph1)
        if len(set(components)) == 1:  #dopoki nie wygenerujemy silnie spojnego digrafu - wtedy mamy sciezki do kazdego wierzcholka
            break
    
    component_groups = defaultdict(list)
    for node, component in enumerate(components):
        component_groups[component].append(node) #slownik z liczba weirzcholkow w poszczegolnej skladowej (musi byc 1)

    print("Silnie spójne składowe:")
    for component, nodes in component_groups.items():
        print(f"Składowa {component}: {nodes}")
    graph1.visualize()
        
    #przypisanie losowych wag, sum a wag w danym cyklu nie może byc ujemna
    graph_with_weights = dodaj_wagi(graph1.adjacency_list)
    graph_with_weights.zmien_wagi_na_ujemne()
    graph_with_weights.visualize()
    
    print("\n\n\n")
    for start_node in range(graph_with_weights.nodes): #do kazdego wierzcholka w grafie poszukiwane sa najkrotsze sciezki
        print(f"\nRozpoczynając od wierzchołka {start_node}:")
        d, helper = bellman_ford(graph_with_weights.adjacency_list, graph_with_weights.weights, start_node)
        print("Odległości od wierzchołka:")
        print(d)
        
        for node in range(graph_with_weights.nodes): #wypisanie najkrotszych sciezek dla danego wierzcholka
            if d[node] == float('inf'):
                print(f"Nie ma ścieżki od {start_node} do {node}")
            else:
                print(f"Najkrótsza ścieżka od {start_node} do {node}: ", najkrotsz_sciezka(helper, node))
        
if __name__ == "__main__":
    main()