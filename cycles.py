import numpy as np

def constructadj(V, adj_matrix):
    adj = [[] for _ in range(V)]  # Initialize adjacency list
    for u in range(V):
        for v in range(V):
            if adj_matrix[u][v]:
                adj[u].append(v)
    return adj

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

def is_induced_cycle(cycle, edge_set):
    n = len(cycle)
    for i in range(n):
        for j in range(i+2, n):
            if i == 0 and j == n - 1:
                continue
            if frozenset({cycle[i], cycle[j]}) in edge_set:
                return False
    return True

def findAllCycles(V, adj_matrix):
    adj = constructadj(V, adj_matrix)
    cycles = set()

    edge_set = set()
    for u in range(V):
        for v in adj[u]:
            edge_set.add(frozenset({u, v}))

    def dfs(start, current, path, visited):
        for neighbor in adj[current]:
            if neighbor == start and len(path) >= 4:
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

# Driver Code
if __name__ == "__main__":
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
    V = len(G13)

    allCycles = findAllCycles(V, G13)
    if allCycles:
        for cycle in allCycles:
            print("Cycle found:", cycle)
    else:
        print("No cycles found.")
