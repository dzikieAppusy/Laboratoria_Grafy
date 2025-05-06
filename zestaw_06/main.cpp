#include <iostream>
#include <vector>
#include <random>
#include <iomanip>
#include <cmath>
#include <algorithm>

// Stale
const double d = 0.15;
const int steps = 1000000;
const int maxIterations = 1000;
const double epsilon = 1e-8;

// PageRank metoda bladzenia przypadkowego
std::vector<double> pagerankRandomWalk(const std::vector<std::vector<int>>& graph) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> distribution(0.0, 1.0);
    std::uniform_int_distribution<> nodeDistribution(0, graph.size() - 1);

    std::vector<int> nodeVisits(graph.size(), 0);

    int current = nodeDistribution(gen);

    for (int i = 0; i < steps; i++) {
        nodeVisits[current]++;

        double r = distribution(gen);
        if (r < d || graph[current].empty()) {
            current = nodeDistribution(gen);
        } else {
            std::uniform_int_distribution<> neighborDistribution(0, graph[current].size() - 1);
            int neighborIndex = neighborDistribution(gen);
            current = graph[current][neighborIndex];
        }
    }

    std::vector<double> ranks(graph.size(), 0.0);
    for (int i = 0; i < graph.size(); i++) {
        ranks[i] = (double) nodeVisits[i] / steps;
    }
    return ranks;
}

// PageRank metoda potegowa
std::vector<double> pagerankPower(const std::vector<std::vector<int>>& graph) {
    std::vector<double> ranks(graph.size(), 1.0 / graph.size());
    std::vector<double> newRanks(graph.size());

    bool converged = false;
    int iter = 0;

    while (!converged && iter < maxIterations) {
        double total = 0.0;

        for (int j = 0; j < graph.size(); ++j) {
            newRanks[j] = 0.0;
            
            for (int i = 0; i < graph.size(); ++i) {
                for (int neighbor : graph[i]) {
                    if (neighbor == j) {
                        newRanks[j] += ranks[i] / graph[i].size();
                        break;
                    }
                }
            }
            
            newRanks[j] = d / graph.size() + (1 - d) * newRanks[j];
            total += newRanks[j];
        }

        for (int j = 0; j < graph.size(); ++j) {
            newRanks[j] /= total;
        }

        double diff = 0.0;
        for (int j = 0; j < graph.size(); ++j) {
            diff += std::abs(newRanks[j] - ranks[j]);
        }

        if (diff < epsilon) {
            converged = true;
        }

        ranks = newRanks;
        iter++;
    }

    std::cout << "Operacja zakonczona po " << iter + 1 << " iteracjach.\n" << std::endl;

    return ranks;
}

// Wypisywanie uzyskanych rang z sortowaniem
void printRanks(const std::vector<double>& ranks) {
    std::vector<std::pair<char, double>> sortedRanks;
    for (int i = 0; i < ranks.size(); ++i) {
        sortedRanks.emplace_back('A' + i, ranks[i]);
    }

    std::sort(sortedRanks.begin(), sortedRanks.end(),
        [](const auto& a, const auto& b) {
            return b.second < a.second;
        });

    std::cout << std::fixed << std::setprecision(6);
    for (const auto& [vertex, rank] : sortedRanks) {
        std::cout << vertex << " ==> PageRank = " << rank << std::endl;
    }
    std::cout << std::endl;
}

int main() {
    // Graf wejściowy w formacie liczbowym jako lista sąsiedztwa
    std::vector<std::vector<int>> graph = {
        {4, 5, 8},
        {0, 2, 5},
        {1, 3, 4, 11},
        {2, 4, 7, 8, 10},
        {2, 6, 7, 8},
        {1, 6},
        {4, 5, 7},
        {3, 6, 8, 11},
        {3, 4, 7, 9},
        {8},
        {3, 8},
        {0, 7}
    };

    std::cout << "PageRank - bladzenie przypadkowe:\n" << std::endl;
    std::vector<double> ranksRandom = pagerankRandomWalk(graph);
    printRanks(ranksRandom);

    std::cout << "PageRank - metoda potegowa:\n" << std::endl;
    std::vector<double> ranksPower = pagerankPower(graph);
    printRanks(ranksPower);

    return 0;
}