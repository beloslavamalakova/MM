"""
Author: Elitsa Dekova
Date: 8th May 2025
Description: Finding all chordless (induced) cycles of length ≥ 4 in a graph.
Input: Adjacency matrix of an undirected graph.
"""
import numpy as np

# Construct an adjacency list from the given adjacency matrix
def constructadj(V, adj_matrix):
    # Create a list of empty lists for each vertex
    adj = [[] for _ in range(V)]
    for u in range(V):
        for v in range(V):
            # If there's an edge from u to v, add v to u's adjacency list
            if adj_matrix[u][v]:
                adj[u].append(v)
    return adj

# Generate a canonical form of the cycle to remove duplicates (i.e., cyclic permutations)
def canonical(cycle):
    n = len(cycle)
    best = cycle[:]
    # Try all rotations of the cycle and pick the lexicographically smallest
    for i in range(n):
        rotated = cycle[i:] + cycle[:i]
        if rotated < best:
            best = rotated
    # Also try reversed cycle and its rotations
    rev = list(reversed(cycle))
    for i in range(n):
        rotated = rev[i:] + rev[:i]
        if rotated < best:
            best = rotated
    return best

# Check if a cycle is an *induced* cycle (i.e., has no chords)
def is_induced_cycle(cycle, edge_set):
    n = len(cycle)
    # Check for any "chords" (edges not part of the cycle but connect cycle vertices)
    for i in range(n):
        for j in range(i + 2, n):
            # Allow edge between the first and last vertices (since it closes the cycle)
            if i == 0 and j == n - 1:
                continue
            # If an edge exists between non-adjacent cycle vertices, it's not induced
            if frozenset({cycle[i], cycle[j]}) in edge_set:
                return False
    return True

# Main function to find all induced cycles of length ≥ 4
def findAllCycles(V, adj_matrix):
    # Convert matrix to adjacency list for easier traversal
    adj = constructadj(V, adj_matrix)
    cycles = set()  # Use a set to store unique cycles

    # Precompute all edges as frozensets to check for chords later
    edge_set = set()
    for u in range(V):
        for v in adj[u]:
            edge_set.add(frozenset({u, v}))

    # Recursive DFS function to explore cycles
    def dfs(start, current, path, visited):
        for neighbor in adj[current]:
            # If neighbor is the start vertex and the path is long enough, it's a cycle
            if neighbor == start and len(path) >= 4:
                can = canonical(path)
                # Check if cycle is induced before adding
                if is_induced_cycle(can, edge_set):
                    cycles.add(tuple(can))
            # Explore deeper if neighbor hasn't been visited and is "greater" than start
            # This condition avoids duplicate cycles (e.g., A-B-C-A vs C-B-A-C)
            elif neighbor not in visited and neighbor > start:
                visited.add(neighbor)
                dfs(start, neighbor, path + [neighbor], visited)
                visited.remove(neighbor)  # Backtrack

    # Run DFS starting from every vertex
    for v in range(V):
        dfs(v, v, [v], set([v]))
    
    # Convert set of tuples back to list of lists
    return [list(cycle) for cycle in cycles]

# Example usage
if __name__ == "__main__":
    # Vertex labels for reference (optional, not used in computation)
    labels13 = ['A','B','C','D','E','F','G','H','I','J','K','L','M']
    
    # Adjacency matrix for a 13-vertex undirected graph
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

    V = len(G13)  # Number of vertices in the graph

    # Find all induced cycles of length >= 4
    allCycles = findAllCycles(V, G13)

    # Output the results
    if allCycles:
        for cycle in allCycles:
            print("Cycle found:", cycle)
    else:
        print("No cycles found.")
