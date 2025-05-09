"""
Author: Elitsa Dekova
Date: 9th May 2025
Description: Finding Sun(3) patterns in the complements of interval graphs.
Input: Adjacency matrix of a graph to check if it contains a Sun(3) in its complement.
"""

import numpy as np
from itertools import combinations

def complement(adj):
    """Return the complement of an undirected adjacency matrix."""
    n = adj.shape[0]
    return np.ones((n, n), dtype=int) - np.eye(n, dtype=int) - adj

def find_suns(adj):
    """
    Detect all Sun(3) structures in the complement graph (adj).
    A Sun consists of:
      - triangle core (a, b, c)
      - three rays (d, e, f), each connected to two adjacent triangle vertices:
        - d connects to a and b
        - e connects to a and c
        - f connects to b and c
      - no edges among d, e, f
    """
    n = adj.shape[0]
    suns = []
    for a, b, c in combinations(range(n), 3):
        if not (adj[a, b] and adj[b, c] and adj[c, a]):
            continue  # triangle check
        triangle = {a, b, c}
        for d, e, f in combinations(set(range(n)) - triangle, 3):
            if (
                adj[d, a] and adj[d, b] and not adj[d, c] and
                adj[e, a] and adj[e, c] and not adj[e, b] and
                adj[f, b] and adj[f, c] and not adj[f, a] and
                not (adj[d, e] or adj[d, f] or adj[e, f])
            ):
                suns.append(((a, b, c), (d, e, f)))
    return suns

def detect_suns(adj, labels=None):
    comp = complement(adj)
    raw = find_suns(comp)
    results = []
    for (a, b, c), (d, e, f) in raw:
        tri = [labels[i] if labels else i for i in (a, b, c)]
        rays = [labels[i] if labels else i for i in (d, e, f)]
        results.append({'triangle': tri, 'rays': rays})
    return results

# Example usage
labels8 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
G8 = np.array([
    [0,0,0,0,0,1,0,0],  # A
    [0,0,0,0,1,0,0,0],  # B
    [0,0,0,1,0,0,0,0],  # C
    [0,0,1,0,1,1,0,0],  # D
    [0,1,0,1,0,1,1,1],  # E
    [1,0,0,1,1,0,1,0],  # F
    [0,0,0,0,1,1,0,1],  # G
    [0,0,0,0,1,0,1,0],  # H
])

suns8 = detect_suns(G8, labels8)
print(suns8)
