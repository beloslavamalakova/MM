import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from networkx.algorithms.approximation import clique
from networkx.algorithms.coloring import greedy_color

def find_c4_cycles(G):
    print("Finding C4 cycles...")
    c4_cycles = set()
    for four_nodes in combinations(G.nodes, 4):
        subgraph = G.subgraph(four_nodes)
        if len(subgraph.edges) == 4 and nx.is_connected(subgraph):
            if all(degree == 2 for node, degree in subgraph.degree()):
                c4_cycles.add(tuple(sorted(subgraph.nodes)))
    print(f"Found {len(c4_cycles)} C4 cycles: {c4_cycles}")
    return c4_cycles

def find_common_vertices(c4_cycles):
    print("Finding common vertices in C4 cycles...")
    vertex_count = {}
    for subgraph in c4_cycles:
        for vertex in subgraph:
            vertex_count[vertex] = vertex_count.get(vertex, 0) + 1
    max_count = max(vertex_count.values(), default=0)
    common_vertices = {v for v, count in vertex_count.items() if count == max_count}
    print(f"Common vertices: {common_vertices}")
    return common_vertices, vertex_count

def cluster_c4_cycles(G, c4_cycles):
    print("Clustering C4 cycles...")
    clusters = []
    remaining_c4s = list(c4_cycles)
    while remaining_c4s:
        common_vertices, vertex_count = find_common_vertices(remaining_c4s)
        cluster = set()
        if common_vertices:
            cluster = common_vertices
        else:
            max_vertex = max(vertex_count, key=vertex_count.get)
            cluster.add(max_vertex)
        clusters.append(cluster)
        remaining_c4s = [c4 for c4 in remaining_c4s if not cluster.intersection(c4)]
    print(f"Clusters found: {clusters}")
    return clusters

def draw_graph(G, title="Graph"):
    plt.figure(figsize=(8, 6))
    nx.draw_circular(G, with_labels=True, font_size=20, node_size=1000, node_color="#8ab7ff")
    plt.title(title)
    plt.show()

def create_sun_pattern():
    sun = nx.Graph()
    sun.add_edges_from([
        ("a", "b"), ("a", "d"), ("b", "c"), ("b", "d"), ("b", "e"),
        ("c", "e"), ("d", "e"), ("d", "f"), ("e", "f")
    ])
    return sun

def create_net_pattern():
    net = nx.Graph()
    net.add_edges_from([
        ("a", "b"), ("b", "c"), ("b", "e"), ("c", "d"), ("c", "e"), ("e", "f")
    ])
    return net

def check_forbidden_structure(G_complement, forbidden_patterns):
    print("Checking for forbidden structures in the complement graph...")
    for name, pattern in forbidden_patterns.items():
        print(f"\nSearching for {name} pattern...")
        matcher = nx.algorithms.isomorphism.GraphMatcher(G_complement, pattern)
        for mapping in matcher.subgraph_isomorphisms_iter():
            print(f"{name} pattern found with mapping: {mapping}")
            return True
    return False

def check_murderer_combinations(G, clusters, forbidden_patterns):
    """
    Instead of removing one vertex per cluster, we now remove the entire set of vertices
    that appear in any cluster.
    """
    print("Checking murderer combinations by removing vertices from clusters...")
    # Combine all clusters (each a set of vertices) into a single set:
    selected_vertices = set.union(*clusters) if clusters else set()
    print(f"Selected vertices for removal: {selected_vertices}")
   
    G_excluded = G.copy()
    G_excluded.remove_nodes_from(selected_vertices)
    G_complement = nx.complement(G_excluded)
   
    draw_graph(G_complement, "Complement of Graph after Removal")
   
    if check_forbidden_structure(G_complement, forbidden_patterns):
        print("Forbidden pattern detected in the complement graph. Another forbidden structure exists, and the problem cannot be solved.")
    else:
        print("The complement graph does not contain any forbidden patterns. Valid murderer combination found:", selected_vertices)
   
    return G_complement

def is_perfect_graph(G):
    """
    Checks if the graph is perfect.
    A graph is perfect if its chromatic number is equal to its largest clique size.
    """
    chromatic_number = greedy_color(G, strategy="largest_first")  # Use greedy coloring
    max_clique_size = len(clique.max_clique(G))  # Find the largest clique

    chromatic_value = max(chromatic_number.values()) + 1  # Chromatic number
    print(f"Chromatic Number: {chromatic_value}")
    print(f"Largest Clique Size: {max_clique_size}")

    if chromatic_value == max_clique_size:
        print("The graph is perfect.")
        return True
    else:
        print("The graph is NOT perfect.")
        return False


def main():
    print("Creating graph...")
    G = nx.Graph()
    edges = [
        ["1", "2"],
        ["1", "4"],
        ["1", "5"],
        ["1", "7"],
        ["2", "3"],
        ["3", "4"],
        ["2", "4"],
        ["3", "1"],
        ["4", "5"],
        ["6", "7"],
        ["5", "6"],
        ["4", "8"],
        ["11", "8"],
        ["15", "9"],
        ["15", "11"],
        ["15", "12"],
        ["15", "14"],
        ["9", "10"],
        ["15", "10"],
        ["10", "11"],
        ["12", "11"],
        ["12", "13"],
        ["13", "14"]
    ]



    G.add_edges_from(edges)
   
    c4_cycles = find_c4_cycles(G)
    clusters = cluster_c4_cycles(G, c4_cycles)
   
    forbidden_patterns = {
        'Sun': create_sun_pattern(),
        'Net': create_net_pattern()
    }
   
    # Get the complement of the modified graph (after removing problematic vertices)
    G_complement = check_murderer_combinations(G, clusters, forbidden_patterns)

    # Check if the original graph is perfect
    print("\nChecking if the graph is perfect...")
    is_perfect_graph(G)

    # Check if the modified complement graph is perfect
    print("\nChecking if the complement of the modified graph is perfect...")
    is_perfect_graph(G_complement)


if __name__ == "__main__":
    main()
