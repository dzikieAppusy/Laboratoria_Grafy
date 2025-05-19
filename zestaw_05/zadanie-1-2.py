from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx
import argparse
import random

class Digraph:
    def __init__(self):
        self.adjacency = defaultdict(list)
        self.nodes = dict()
        self.capacity = {}
        self.flow = {}
        self.residual = defaultdict(dict)

    def addNode(self, node, layer):
        self.nodes[node] = layer
        self.adjacency[node]

    def addEdge(self, u, v, presetCapacity=None):
        self.adjacency[u].append(v)
        capacity = random.randint(1, 10)
        self.capacity[(u, v)] = presetCapacity if presetCapacity is not None else capacity
        self.flow[(u, v)] = 0

    def bfs(self):
        ds = {node: float('inf') for node in self.nodes}
        ps = {node: None for node in self.nodes}

        Q = deque(['s']) 
        ds['s'] = 0

        while Q:
            v = Q.popleft()

            for u in self.adjacency[v]:
                if ds[u] == float('inf') and self.residual[v].get(u, 0) > 0:
                    ds[u] = ds[v] + 1
                    ps[u] = v
                    Q.append(u)
                    if u == 't':
                        return ps
                    
        return None

    def fordFulkerson(self):
        for edge in self.flow:
            self.flow[edge] = 0
        
        self.updateResidual()
        maxFlow = 0

        while True:
            ps = self.bfs()
            if ps is None:
                break

            pathFlow = float('inf')
            v = 't'

            path = []
            while v != 's':
                path.append(v)
                u = ps[v]
                pathFlow = min(pathFlow, self.residual[u].get(v, 0))
                v = u
            path.append('s')
            path.reverse()

            v = 't'
            while v != 's':
                u = ps[v]
                if (u, v) in self.flow:
                    self.flow[(u, v)] += pathFlow
                else:
                    self.flow[(v, u)] -= pathFlow
                
                self.residual[u][v] = self.residual[u].get(v, 0) - pathFlow
                self.residual[v][u] = self.residual[v].get(u, 0) + pathFlow
                v = u
            
            maxFlow += pathFlow
        
        return maxFlow

    def updateResidual(self):
        self.residual = defaultdict(dict)

        for (u, v), capacity in self.capacity.items():
            flow = self.flow[(u, v)]
            self.residual[u][v] = capacity - flow
            self.residual[v][u] = flow

            if v not in self.adjacency:
                self.adjacency[v] = []
            if u not in self.adjacency[v]:
                self.adjacency[v].append(u)

    def visualize(self, showFlows = False):
        G = nx.DiGraph()

        for node, layer in self.nodes.items():
            G.add_node(node, layer=layer)

        for u in self.adjacency:
            for v in self.adjacency[u]:
                if (u, v) not in self.capacity:
                    continue
                capacity = self.capacity[(u, v)]
                flow = self.flow.get((u, v), 0)
                label = f'{flow}/{capacity}'
                G.add_edge(u, v, label=label if showFlows else capacity)

        def setupLayout(G, subsetKey):
            layers = defaultdict(list)
            for node in G.nodes():
                layers[subsetKey(node)].append(node)
            for layer in layers:
                layers[layer].sort()
            pos = {}
            layerYGap = 1.5
            nodeXGap = 1.5
            for layer, nodes in layers.items():
                n = len(nodes)
                totalHeight = (n - 1) * nodeXGap
                offset = totalHeight / 2
                layer_offset = 0.3 if (layer % 2 == 0 and (layer != 0 or layer != len(layers))) else 0
                for i, node in enumerate(nodes):
                    pos[node] = (layer * layerYGap, -i * nodeXGap + offset - layer_offset)
            return pos

        pos = setupLayout(G, lambda n: G.nodes[n]['layer'])

        nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue',
                arrowsize=20, font_size=10, font_weight='bold', edgecolors='blue')

        for specialNode in ['s', 't']:
            if specialNode in G.nodes():
                if specialNode == 's':
                    pos['s'] = (pos['s'][0] + 0.0025, pos['s'][1])
                nx.draw_networkx_nodes(G, pos, nodelist=[specialNode], node_size=700,
                                    node_color='none', edgecolors='blue')

        labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=labels, label_pos=0.25, rotate=False,
            font_size=10, bbox=dict(facecolor=(1, 1, 1, 0.8), edgecolor='none'))

        plt.show()

class FlowNetwork:
    def __init__(self, N, setupTest = False):
        self.N = N
        self.graph = Digraph()
        if setupTest:
            self.generateTestDiagram()
        else:
            self.generateNodes()
            self.generateEdges()
    
    def generateNodes(self):
        nodeCount = 0
        self.graph.addNode('s', 0)

        for layer in range(1, self.N + 1):
            NN = random.randint(2, self.N)
            for _ in range(NN):
                self.graph.addNode(chr(ord('a') + nodeCount), layer)
                nodeCount += 1

        self.graph.addNode('t', self.N + 1)

    def generateEdges(self):
        # edges between s, t and their neighbor layers
        sNodes = [node for node, layer in self.graph.nodes.items() if layer == 1]
        for node in sNodes:
            self.graph.addEdge('s', node)

        tNodes = [node for node, layer in self.graph.nodes.items() if layer == self.N]
        for node in tNodes:
            self.graph.addEdge(node, 't')

        # base edges in layers 1..N
        for i in range(1, self.N):
            currNodes = [node for node, layer in self.graph.nodes.items() if layer == i]
            nextNodes = [node for node, layer in self.graph.nodes.items() if layer == i + 1]
            
            for node in currNodes:
                emptyNodes = [n for n in nextNodes if not self.checkAdjacency(n)]
                
                if emptyNodes:
                    self.graph.addEdge(node, random.choice(emptyNodes))
                else:
                    self.graph.addEdge(node, random.choice(nextNodes))

            for node in nextNodes:
                if not self.checkAdjacency(node):
                    self.graph.addEdge(random.choice(currNodes), node)

        # additional 2N edges in layers 1..N
        edgesAdded = 0
        nodes = [node for node, layer in self.graph.nodes.items() if layer not in {0, self.N + 1}]
        while edgesAdded < 2 * self.N:
            u = random.choice(nodes)
            v = random.choice(nodes)

            if u != v and not (v in self.graph.adjacency[u] or u in self.graph.adjacency[v]):
                self.graph.addEdge(u, v)
                edgesAdded += 1

    def generateTestDiagram(self):
        # setup nodes
        nodeCount = 0
        self.graph.addNode('s', 0)
        for layer in range(1, 4):
            for _ in range(3):
                self.graph.addNode(chr(ord('a') + nodeCount), layer)
                nodeCount += 1
        self.graph.addNode('t', 4)

        # setup edges
        self.graph.addEdge('s', 'a', 10)
        self.graph.addEdge('s', 'b', 3)
        self.graph.addEdge('s', 'c', 6)

        self.graph.addEdge('a', 'd', 8)
        self.graph.addEdge('a', 'e', 6)
        self.graph.addEdge('a', 'b', 8)
        self.graph.addEdge('b', 'e', 2)
        self.graph.addEdge('b', 'f', 10)
        self.graph.addEdge('c', 'd', 9)
        self.graph.addEdge('c', 'f', 1)

        self.graph.addEdge('d', 'h', 5)
        self.graph.addEdge('e', 'i', 7)
        self.graph.addEdge('f', 'g', 9)
        self.graph.addEdge('e', 'd', 1)

        self.graph.addEdge('g', 't', 7)
        self.graph.addEdge('h', 't', 5)
        self.graph.addEdge('i', 't', 7)
        self.graph.addEdge('h', 'g', 1)
        self.graph.addEdge('h', 'f', 8)

    def checkAdjacency(self, v):
        return any(v in self.graph.adjacency[u] for u in self.graph.adjacency)

    def getMaxFlow(self):
        maxFlow = self.graph.fordFulkerson()
        print('Flow network: Ford-Fulkerson')
        print(f'maxFlow: {maxFlow}')

    def visualize(self, showFlows = False):
        self.graph.visualize(showFlows)

def main(N, calcFlow, setupTest):
    flowNetwork = FlowNetwork(N, setupTest)
    if calcFlow:
        flowNetwork.getMaxFlow()
    flowNetwork.visualize(calcFlow)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generowanie sieci przeplywowej')
    parser.add_argument('--N', type=int, default=2, help='Liczba warstw w sieci')
    parser.add_argument('--calcFlow', type=bool, default=False, help='Czy obliczyć maksymalny przeplyw')
    parser.add_argument('--setupTest', type=bool, default=False, help='Czy wygenerowac testowy graf')

    args = parser.parse_args()

    main(max(2, min(4, args.N)), args.calcFlow, args.setupTest)