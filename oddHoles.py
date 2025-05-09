"""
Author: Elitsa Dekova
Date: 9th May 2025
Description: Finding all odd chordless (induced) cycles of length ≥ 5 in the complement of a graph.
Input: Adjacency matrix of an undirected graph.
"""
import numpy as np
import sys
sys.setrecursionlimit(1000)

# Construct adjacency list from adjacency matrix
def constructadj(V, adj_matrix):
    adj = [[] for _ in range(V)]
    for u in range(V):
        for v in range(V):
            if adj_matrix[u][v]:
                adj[u].append(v)
    return adj

# Canonical form of cycle (for deduplication)
def canonical(cycle):
    n = len(cycle)
    best = cycle[:]
    for i in range(n):
        rotated = cycle[i:] + cycle[:i]
        if rotated < best:
            best = rotated
    rev = list(reversed(cycle))
    for i in range(n):
        rotated = rev[i:] + rev[:i]
        if rotated < best:
            best = rotated
    return best

# Check if a cycle is induced (i.e., no chords)
def is_induced_cycle(cycle, edge_set):
    n = len(cycle)
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if frozenset({cycle[i], cycle[j]}) in edge_set:
                return False
    return True

# Find all induced cycles of length ≥ 5 with odd length
def findAllCycles(V, adj_matrix):
    adj = constructadj(V, adj_matrix)
    cycles = set()
    edge_set = set()
    for u in range(V):
        for v in adj[u]:
            edge_set.add(frozenset({u, v}))

    def dfs(start, current, path, visited):
        for neighbor in adj[current]:
            if neighbor == start and len(path) >= 5 and len(path)%2==1:
                can = canonical(path)
                if is_induced_cycle(can, edge_set):
                    cycles.add(tuple(can))
            elif neighbor not in visited and neighbor > start:
                visited.add(neighbor)
                dfs(start, neighbor, path + [neighbor], visited)
                visited.remove(neighbor)

    for v in range(V):
        dfs(v, v, [v], set([v]))
    
    return [list(cycle) for cycle in cycles]

# Invert adjacency matrix to get complement (excluding diagonal)
def complement_matrix(adj_matrix):
    V = len(adj_matrix)
    comp = np.ones((V, V), dtype=int) - adj_matrix
    np.fill_diagonal(comp, 0)
    return comp

# Driver code
if __name__ == "__main__":
    labels8 = ['A','B','C','D','E','F','G','H']
    G8 = np.array([
    [0, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 1, 0]
    ])

    V = len(G8)

    # Get complement graph
    G8_comp = complement_matrix(G8)

    # Find all induced cycles in the complement graph
    allCycles = findAllCycles(V, G8_comp)

    if allCycles:
        for cycle in allCycles:
            print("Cycle found:", cycle)
    else:
        print("No cycles found.")
        
