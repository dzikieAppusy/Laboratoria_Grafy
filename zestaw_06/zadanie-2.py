import numpy as np
import matplotlib.pyplot as plt
import random

def calculateDistance(cycle):
    total = 0

    for i in range(len(cycle) - 1):
        total += np.linalg.norm(cycle[i + 1] - cycle[i])

    return total

def calculateDeltaDistance(cycle, i, j):
    a, b = cycle[i - 1], cycle[i]
    c, d = cycle[j], cycle[(j + 1) % len(cycle)]

    beforeSwap = np.linalg.norm(a - b) + np.linalg.norm(c - d)
    afterSwap = np.linalg.norm(a - c) + np.linalg.norm(b - d)

    return afterSwap - beforeSwap

def swapEdges(cycle):
    while True:
        i, j = sorted(random.sample(range(1, len(cycle) - 1), 2))

        if abs(i - j) > 1:
            break

    newCycle = np.vstack([
        cycle[:i],
        cycle[i:j + 1][::-1],
        cycle[j + 1:]
    ])

    return newCycle, i, j

def simulatedAnnealing(cycle, maxIterations=100000, T0=10):
    T = T0

    for i in range(1, maxIterations + 1):
        newCycle, ab, cd = swapEdges(cycle)

        delta = calculateDeltaDistance(cycle, ab, cd)

        if delta < 0 or random.random() < np.exp(-delta / T):
            cycle = newCycle

        T = T0 / (1 + np.log(1 + i))
    
    return cycle

def main():
    data = np.loadtxt('xqf131.dat')
    cycle = np.vstack([data, data[0]])

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 5))

    ax1.plot(cycle[:, 0], cycle[:, 1], 'r-', marker = 'o')
    ax1.set_title(rf'$\bf{{Cykl\ poczatkowy}}$ o długości: {calculateDistance(cycle):.3f}')
    ax1.set_xlabel(r'$\bf{{x}}$')
    ax1.set_ylabel(r'$\bf{{y}}$')

    bestCycle = cycle
    bestDistance = calculateDistance(cycle)

    for _ in range(5):
        newCycle = simulatedAnnealing(bestCycle)
        distance = calculateDistance(newCycle)

        if distance < bestDistance:
            bestCycle = newCycle
            bestDistance = distance

    ax2.plot(bestCycle[:, 0], bestCycle[:, 1], 'r-', marker = 'o')
    ax2.set_title(rf'$\bf{{Cykl\ wyjsciowy}}$ o długości: {bestDistance:.3f}')
    ax2.set_xlabel(r'$\bf{{x}}$')
    ax2.set_ylabel(r'$\bf{{y}}$')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()