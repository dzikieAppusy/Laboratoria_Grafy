import random

def pageRankRandom(graph, d = 0.15, steps = 1000000):
    nodeVisits = {node: 0 for node in graph}
    current = random.choice(list(graph.keys()))

    for _ in range(steps):
        nodeVisits[current] += 1

        if random.random() < d and graph[current]:
            current = random.choice(list(graph.keys()))
        else:
            current = random.choice(list(graph[current]))
    
    totalVisits = sum(nodeVisits.values())
    pageRanks = {node: count / totalVisits for node, count in nodeVisits.items()}

    return pageRanks

def pageRankPowerIteration(graph, d = 0.15, maxIterations = 1000, tol = 1e-6):
    pageRanks = {node: 1 / len(graph) for node in graph}
    newRanks = {node: 0 for node in graph}

    iteration = 0
    converged = False

    while not converged and iteration < maxIterations:
        total = 0

        for i in graph:
            newRanks[i] = 0

            for j in graph:
                for neighbor in graph[j]:
                    if neighbor == i:
                        newRanks[i] += pageRanks[j] / len(graph[j])
                        break

            newRanks[i] = (1 - d) * newRanks[i] + d / len(graph)
            total += newRanks[i]

        newRanks = {node: rank / total for node, rank in newRanks.items()}

        diff = sum(abs(newRanks[node] - pageRanks[node]) for node in graph)
        if diff < tol:
            converged = True

        pageRanks = newRanks
        iteration += 1

    return pageRanks

def printPageRanks(pageRanks, title):
    sortedRanks = sorted(pageRanks.items(), key = lambda x: x[1], reverse = True)
    print(f'{title}')
    for node, rank in sortedRanks:
        print(f'{node} ==> PageRank = {rank:.6f}')

def main():
    graph = {
        'A': {'E', 'F', 'I'},
        'B': {'A', 'C', 'F'},
        'C': {'B', 'D', 'E', 'L'},
        'D': {'C', 'E', 'H', 'I', 'K'},
        'E': {'C', 'G', 'H', 'I'},
        'F': {'B', 'G'},
        'G': {'E', 'F', 'H'},
        'H': {'D', 'G', 'I', 'L'},
        'I': {'D', 'E', 'H', 'J'},
        'J': {'I'},
        'K': {'D', 'I'},
        'L': {'A', 'H'}
    }
    
    pageRanks = pageRankRandom(graph)
    printPageRanks(pageRanks, 'PageRank: random walk with teleportation')

    pageRanks = pageRankPowerIteration(graph)
    printPageRanks(pageRanks, 'PageRank: power iteration')

if __name__ == "__main__":
    main()