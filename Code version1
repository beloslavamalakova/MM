import networkx as nx
import matplotlib.pyplot as plt

# Create graph
G = nx.Graph()

# Add nodes
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
for node in nodes:
    G.add_node(node)

# Add edges
edges = [
    ["A", "B"],
    ["A", "C"],
    ["A", "D"],
    ["A", "F"],
    ["A", "G"],
    ["A", "I"],
    ["B", "D"],
    ["B", "E"],
    ["B", "I"],
    ["C", "D"],
    ["C", "E"],
    ["C", "G"],
    ["C", "H"],
    ["C", "I"],
    ["D", "I"],
    ["E", "I"],
    ["F", "G"],
    ["F", "I"],
    ["G", "H"],
    ["G", "I"],
    ["H", "I"]
]
for edge in edges:
    G.add_edge(*edge)

# Draw the graph
nx.draw_circular(G, with_labels=True, font_size=20, node_size=1000, node_color="#8ab7ff")
plt.show()

from itertools import combinations

def find_c4_cycles(G):
    c4_cycles = set()
    
    # Check all combinations of 4 nodes
    for four_nodes in combinations(G.nodes, 4):
        subgraph = G.subgraph(four_nodes)
        # To be a C4, it must have exactly 4 edges and be connected
        if len(subgraph.edges) == 4 and nx.is_connected(subgraph):
            # Check if the degree of each node is 2
            if all(degree == 2 for node, degree in subgraph.degree()):
                c4_cycles.add(tuple(subgraph.nodes))
                
    return c4_cycles
    
c4_cycles = find_c4_cycles(G)
print("C4 cycles found:", c4_cycles)

# Finding overlapping vertices in c4_cycles
def find_overlapping_vertices(c4_cycles):
    vertex_count = {}
    
    # Count occurrences of each vertex across all c4_cycles
    for subgraph in c4_cycles:
        for vertex in subgraph:
            if vertex in vertex_count:
                vertex_count[vertex] += 1
            else:
                vertex_count[vertex] = 1
    
    # Overlapping vertices appear in more than one subgraph
    overlapping_vertices = {v for v, count in vertex_count.items() if count > 1}
    
    return overlapping_vertices

# Excluding each overlapping vertex and producing a new graph
def exclude_single_vertex(G, vertex):
    G_new = G.copy()
    G_new.remove_node(vertex)
    return G_new

# Draw the graphs
def draw_graph(G, title):
    pos = nx.spring_layout(G)  # Positioning for visualization
    plt.figure()
    nx.draw_circular(G, with_labels=True, font_size=20, node_size=1000, node_color="#8ab7ff")
    plt.title(title)
    plt.show()
    

# Overlapping vertices
overlapping_vertices = find_overlapping_vertices(c4_cycles)
print("Overlapping vertices:", overlapping_vertices)

excluded_graphs = []

# Exclude and visualize
for vertex in overlapping_vertices:
    G_excluded = exclude_single_vertex(G, vertex)
    draw_graph(G_excluded, f"Graph excluding vertex {vertex}")
    # List of graphs to check
    excluded_graphs.append(G_excluded)

# Creating the complements of the graphs
def complement_graph(G):
    # Create a complement graph
    G_complement = nx.complement(G)
    return G_complement

# Draw graph
def draw_graph(G, title="Graph"):
    plt.figure(figsize=(8, 6))
    nx.draw_circular(G, with_labels=True, font_size=20, node_size=1000, node_color="#8ab7ff")
    plt.title(title)
    plt.show()

# Check for forbidden subgraphs
def contains_forbidden_subgraph(G, forbidden_subgraph):
    for subgraph in nx.algorithms.isomorphism.GraphMatcher(G, forbidden_subgraph).subgraph_isomorphisms_iter():
        return True
    return False

# Define the forbidden structures
def sun():
    G_sun = nx.Graph()
    G_sun.add_edges_from([(1, 2), (1, 4), (2, 3), (2, 4), (2, 5), (3, 5), (4, 5), (4, 6), (5, 6)])
    return G_sun

def net():
    G_net = nx.Graph()
    G_net.add_edges_from([(1, 2), (2, 3), (2, 5), (3, 4), (3, 5), (5, 6)])
    return G_net

for i, G_excluded in enumerate(excluded_graphs):
    print(f"\nProcessing Excluded Graph {i + 1}")
    
    # Create the complement of the graph
    G_complement = complement_graph(G_excluded)
    
    # Draw the original graph and its complement
    draw_graph(G_excluded, f"Excluded Graph {i + 1}")
    draw_graph(G_complement, f"Complement of Excluded Graph {i + 1}")
    
    # Check for forbidden structures in the complement graph
    forbidden_structures = {'Sun': sun(), 'Net': net()}
    
    for name, structure in forbidden_structures.items():
        if contains_forbidden_subgraph(G_complement, structure):
            print(f"The complement graph contains a {name}.")
        else:
            print(f"The complement graph does not contain a {name}.")

# Identify the murderer vertex
def identify_murderer_vertex(G, vertices, forbidden_structures):
    for vertex in vertices:
        G_excluded = exclude_single_vertex(G, vertex)
        G_complement = complement_graph(G_excluded)

        # Check for forbidden structures in the complement graph
        contains_any_forbidden = any(
            contains_forbidden_subgraph(G_complement, structure)
            for structure in forbidden_structures.values()
        )
        
        if not contains_any_forbidden:
            return vertex, G_excluded, G_complement  # Found the murderer vertex

    return None, None, None  # No valid vertex found

# Identify the murderer vertex
murderer_vertex, G_excluded, G_complement = identify_murderer_vertex(G, overlapping_vertices, forbidden_structures)

if murderer_vertex is not None:
    print(f"The murderer vertex is {murderer_vertex}.")
    print(f"The graph without vertex {murderer_vertex} and its complement do not contain any forbidden structures.")

else:
    print("There is no murderer vertex. The removal of no single vertes results in a graph complement with no forbidden structures.")
