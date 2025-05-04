"""
Author: Beloslava Malakova
Date: 4th May 2025
Description: finding Net(S_3) in the complements of interval graphs.
Input: adjacency matrix of a graph that we want to check if it is interval.
"""
import numpy as np
from itertools import combinations

def complement(adj):
    """Return the complement of an undirected adjacency matrix."""
    n = adj.shape[0]
    return np.ones((n, n), dtype=int) - np.eye(n, dtype=int) - adj

def find_nets(adj):
    """
    Detect all Net(S3) structures in the complement graph (adj).
    A Net consists of a triangle (a,b,c) and three leaves (x,y,z) such that:
      - x connected only to a among {a,b,c,x,y,z}
      - y connected only to b among {a,b,c,x,y,z}
      - z connected only to c among {a,b,c,x,y,z}
      - No edges among x,y,z or cross attachments.
    """
    n = adj.shape[0]
    nets = []
    for a, b, c in combinations(range(n), 3):
        # Check triangle in complement
        if not (adj[a, b] and adj[b, c] and adj[c, a]):
            continue
        # potential leaves of triangle vertices
        leaves_a = [x for x in range(n) if x not in (a, b, c)
                    and adj[a, x] == 1
                    and adj[b, x] == 0 and adj[c, x] == 0]
        leaves_b = [y for y in range(n) if y not in (a, b, c)
                    and adj[b, y] == 1
                    and adj[a, y] == 0 and adj[c, y] == 0]
        leaves_c = [z for z in range(n) if z not in (a, b, c)
                    and adj[c, z] == 1
                    and adj[a, z] == 0 and adj[b, z] == 0]
        for x in leaves_a:
            for y in leaves_b:
                if adj[x, y]: continue
                for z in leaves_c:
                    if adj[x, z] or adj[y, z]: continue
                    nets.append(((a, b, c), (x, y, z)))
    return nets

def detect_nets(adj, labels=None):
    comp = complement(adj)
    raw = find_nets(comp)
    results = []
    for (a, b, c), (x, y, z) in raw:
        tri = [labels[i] if labels else i for i in (a, b, c)]
        leaves = [labels[i] if labels else i for i in (x, y, z)]
        results.append({'triangle': tri, 'leaves': leaves})
    return results

# The 13x13 adjacency from the LaTeX matrix
labels13 = ['A','B','C','D','E','F','G','H','I','J','K','L','M']
G13 = np.array([
    [0,0,0,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,1,1,0,0,0,0,0,0],
    [1,0,1,0,1,1,0,0,0,0,0,0,0],
    [1,1,0,1,0,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1,1,1,1,0],
    [0,0,0,0,0,0,0,1,0,0,1,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,1,0],
    [0,0,0,0,0,0,0,1,1,0,0,1,1],
    [0,0,0,0,0,0,0,1,0,1,1,0,1],
    [0,0,0,0,0,0,1,0,0,0,1,1,0],
])
nets13 = detect_nets(G13, labels13)
print(nets13)
