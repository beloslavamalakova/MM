import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, product
from networkx.algorithms.coloring import greedy_color
import sys
sys.setrecursionlimit(2000)  # Increase recursion limit to allow deep DFS calls

# Constructs adjacency list from list of edges for undirected graph
def constructadj(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

# Returns the canonical form of a cycle, meaning the lexicographically smallest
# rotation of the cycle, either in original or reversed order
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

# Checks if a cycle is an induced cycle (i.e., a cycle with no chords)
def is_induced_cycle(cycle, edge_set):
    n = len(cycle)
    for i in range(n):
        for j in range(i+2, n):
            if i == 0 and j == n - 1:
                continue  # skip adjacent ends
            if frozenset({cycle[i], cycle[j]}) in edge_set:
                return False
    return True

# Finds all chordless (induced) cycles of length >= 4 in the graph
def find_induced_cycles_ge4(G):
    print("Finding chordless cycles of length ≥ 4...")
    adj = {n: list(G.neighbors(n)) for n in G.nodes}  # adjacency list
    edge_set = {frozenset({u, v}) for u, v in G.edges}  # all edges as frozensets
    cycles = set()

    # Recursive DFS to explore all cycles
    def dfs(start, current, path, visited):
        for neighbor in adj[current]:
            if neighbor == start and len(path) >= 4:
                can = canonical(path)
                if is_induced_cycle(can, edge_set):
                    if tuple(can) not in cycles:
                        print(f"Chordless cycle found: {can}")
                    cycles.add(tuple(can))
            elif neighbor not in visited and neighbor > start:
                visited.add(neighbor)
                dfs(start, neighbor, path + [neighbor], visited)
                visited.remove(neighbor)

    for v in G.nodes:
        dfs(v, v, [v], set([v]))

    print(f"\nTotal chordless cycles of length ≥ 4: {len(cycles)}\n")
    return [list(c) for c in cycles]

# Counts how many cycles each vertex appears in and finds the most common ones
def find_common_vertices(cycles):
    print("Finding common vertices in cycles...")
    vertex_count = {}
    for cycle in cycles:
        for vertex in cycle:
            vertex_count[vertex] = vertex_count.get(vertex, 0) + 1
    max_count = max(vertex_count.values(), default=0)
    common_vertices = {v for v, count in vertex_count.items() if count == max_count}
    print(f"Common vertices: {common_vertices}")
    return common_vertices, vertex_count

# Clusters chordless cycles by grouping them based on shared vertices
from collections import defaultdict

def cluster_c4_cycles(G, cycles):
    print("Clustering chordless cycles (custom greedy logic)...")
    clusters = []
    remaining_cycles = list(cycles)

    while remaining_cycles:
        # Count how many cycles each vertex is in
        vertex_to_cycles = defaultdict(list)
        for i, cycle in enumerate(remaining_cycles):
            for v in cycle:
                vertex_to_cycles[v].append(i)

        if not vertex_to_cycles:
            break

        # Find max participation
        max_count = max(len(cycle_indices) for cycle_indices in vertex_to_cycles.values())
        candidates = [v for v, cycle_indices in vertex_to_cycles.items() if len(cycle_indices) == max_count]

        # Check for exact same cycle participation
        participation_groups = defaultdict(list)
        for v in candidates:
            participation_signature = tuple(sorted(vertex_to_cycles[v]))
            participation_groups[participation_signature].append(v)

        # Take the first group (lexicographically) with the same participation
        chosen_group = sorted(participation_groups.items(), key=lambda x: sorted(x[1]))[0][1]
        cluster = set(chosen_group) if len(chosen_group) > 1 else {chosen_group[0]}
        clusters.append(cluster)

        # Remove all cycles involving any vertex in the cluster
        remaining_cycles = [cycle for cycle in remaining_cycles if not cluster.intersection(cycle)]

    print(f"Clusters found: {clusters}")
    return clusters


# Helper function to visualize a graph
def draw_graph(G, title="Graph"):
    plt.figure(figsize=(8, 6))
    nx.draw_circular(G, with_labels=True, font_size=20, node_size=1000, node_color="#8ab7ff")
    plt.title(title)
    plt.show()

# Define the forbidden 'sun' pattern graph
def create_sun_pattern():
    sun = nx.Graph()
    sun.add_edges_from([
        ("a", "b"), ("a", "d"), ("b", "c"), ("b", "d"), ("b", "e"),
        ("c", "e"), ("d", "e"), ("d", "f"), ("e", "f")
    ])
    return sun

# Define the forbidden 'net' pattern graph
def create_net_pattern():
    net = nx.Graph()
    net.add_edges_from([
        ("a", "b"), ("b", "c"), ("b", "e"), ("c", "d"), ("c", "e"), ("e", "f")
    ])
    return net

# Finds all induced odd-length cycles (odd holes) of length ≥ 5
def odd_holes_search(G):
    print("Finding odd holes (chordless cycles of odd length ≥ 5)...")
    adj = {n: list(G.neighbors(n)) for n in G.nodes}
    edge_set = {frozenset({u, v}) for u, v in G.edges}
    cycles = set()

    def dfs(start, current, path, visited):
        for neighbor in adj[current]:
            if neighbor == start and len(path) >= 5 and len(path) % 2 == 1:
                can = canonical(path)
                if is_induced_cycle(can, edge_set):
                    cycles.add(tuple(can))
            elif neighbor not in visited and neighbor > path[0] and len(path) < 15:
                visited.add(neighbor)
                dfs(start, neighbor, path + [neighbor], visited)
                visited.remove(neighbor)

    print(f"Found {len(cycles)} odd holes (chordless cycles of odd length ≥ 5).")
    return [list(c) for c in cycles]

# Checks if a graph contains forbidden substructures or odd holes
def check_forbidden_structure(G_complement, forbidden_patterns):
    print("Checking for forbidden structures in the complement graph...")

    for name, pattern in forbidden_patterns.items():
        print(f"\nSearching for {name} pattern...")
        matcher = nx.algorithms.isomorphism.GraphMatcher(G_complement, pattern)
        for mapping in matcher.subgraph_isomorphisms_iter():
            print(f"{name} pattern found with mapping: {mapping}")
            return True

    print("\nSearching for odd holes...")
    odd_holes = odd_holes_search(G_complement)
    if odd_holes:
        print(f"Odd holes found: {odd_holes}")
        return True

    print("No forbidden structures found.")
    return False

# Tries all combinations of selecting one vertex per cluster,
# removes them, checks if resulting complement graph is "clean"
def check_murderer_combinations(G, clusters, forbidden_patterns):
    print("Trying all combinations of one vertex per cluster...")

    all_choices = list(product(*[sorted(cluster) for cluster in clusters]))
    print(f"Total combinations to check: {len(all_choices)}")

    valid_combinations = []

    for idx, choice in enumerate(all_choices, 1):
        selected_vertices = set(choice)
        print(f"\nChecking combination {idx}: {selected_vertices}")

        G_excluded = G.copy()
        G_excluded.remove_nodes_from(selected_vertices)
        G_complement = nx.complement(G_excluded)
        
        if check_forbidden_structure(G_complement, forbidden_patterns):
            print(f"Combination {selected_vertices} leads to forbidden structure.")
        else:
            print(f"Valid murderer combination found: {selected_vertices}")
            draw_graph(G_complement, f"Valid Complement for {selected_vertices}")
            valid_combinations.append((selected_vertices, G_complement))

        print(f"Largest Clique Size in the Complement Graph: {max_clique_size_complement}")
        print(f"Largest Clique Vertices: {max_clique}")

    if not valid_combinations:
        print("\nNo valid combinations found.")
    else:
        print(f"\nTotal valid combinations: {len(valid_combinations)}")

    return valid_combinations

# Checks if a graph is perfect (i.e., chromatic number == clique number)
def is_perfect_graph(G):
    chromatic_number = greedy_color(G, strategy="largest_first")
    max_clique = max(nx.find_cliques(G), key=len)
    chromatic_value = max(chromatic_number.values()) + 1

    print(f"Chromatic Number: {chromatic_value}")
    print(f"Largest Clique Size: {len(max_clique)}")

    if chromatic_value == len(max_clique):
        print("The graph is perfect.")
        return True
    else:
        print("The graph is NOT perfect.")
        return False

# Main function tying everything together
def main():
    print("Creating graph...")
    G = nx.Graph()
    edges = [
        ("A", "B"), ("A", "C"), ("A", "D"), ("A", "F"), ("A", "G"), ("A", "I"),
        ("B", "E"), ("B", "I"), ("B", "D"),
        ("C", "E"), ("C", "D"), ("C", "G"), ("C", "H"), ("C", "I"),
        ("D", "I"),
        ("E", "I"),
        ("F", "G"), ("F", "I"),
        ("G", "H"), ("G", "I"),
        ("H", "I")
    ]
    G.add_edges_from(edges)

    print("\n--- Step 1: Finding chordless cycles ---")
    cycles = find_induced_cycles_ge4(G)

    print("\n--- Step 2: Clustering cycles ---")
    clusters = cluster_c4_cycles(G, cycles)

    print("\n--- Step 3: Defining forbidden patterns ---")
    forbidden_patterns = {
        'Sun': create_sun_pattern(),
        'Net': create_net_pattern()
    }

    print("\n--- Step 4: Trying combinations of vertex removals ---")
    valid_combinations = check_murderer_combinations(G, clusters, forbidden_patterns)

    print("\n--- Step 5: Checking perfection of the original graph ---")
    is_perfect_graph(G)

    print("\n--- Step 6: Checking perfection of each valid complement graph ---")
    for vertex_set, G_complement in valid_combinations:
        print(f"\nRemoved vertices: {vertex_set}")
        is_perfect_graph(G_complement)

if __name__ == "__main__":
    main()
