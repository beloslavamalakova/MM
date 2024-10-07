### README: Graph Cycle Analysis and Forbidden Subgraph Detection

---

#### **Overview**

Authors: Elitsa Dekova and Yana Jordanova 


Scientific advisor: Beloslava Malakova

This project implements a graph analysis tool that identifies cycles (specifically C4 cycles), overlapping vertices, and detects the presence of forbidden subgraphs such as the "Sun" and "Net" in graph complements. Additionally, it seeks to identify a "murderer" vertex—one which, when removed, results in a complement graph that avoids these forbidden subgraphs.

---

#### **Table of Contents**
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Functions Overview](#functions-overview)
5. [How It Works](#how-it-works)
6. [Visualization](#visualization)
7. [Future Improvements](#future-improvements)

---

### **Features**

- **C4 Cycle Detection**: Identifies 4-node cycles (C4) in the input graph.
- **Overlapping Vertex Detection**: Finds vertices that appear in more than one C4 cycle.
- **Graph Exclusion**: Creates new graphs by removing overlapping vertices and visualizes them.
- **Complement Graph Creation**: Generates complement graphs (edges between non-adjacent nodes).
- **Forbidden Subgraph Detection**: Searches for specific forbidden subgraphs ("Sun" and "Net").
- **Murderer Vertex Identification**: Attempts to identify a vertex whose removal prevents forbidden subgraphs in the complement.

---

### **Installation**

Ensure you have the following dependencies installed:

```bash
pip install networkx matplotlib
```
---

### **Usage**

1. Clone the repository and navigate to the project directory.

    ```bash
    git clone https://github.com/your-username/graph-cycle-analysis.git
    cd graph-cycle-analysis
    ```

2. Run the Python script.

    ```bash
    Code1.py
    ```

3. The program will perform the following:
   - Create and visualize the initial graph.
   - Detect all C4 cycles.
   - Identify overlapping vertices.
   - Visualize graphs with these vertices excluded.
   - Create complement graphs and check for the presence of forbidden subgraphs.
   - If found, the murderer vertex will be displayed.

---

### **Functions Overview**

- `find_c4_cycles(G)`: Detects C4 cycles (4-node cycles with degree 2).
- `find_overlapping_vertices(c4_cycles)`: Identifies vertices appearing in multiple C4 cycles.
- `exclude_single_vertex(G, vertex)`: Removes a specific vertex from the graph.
- `complement_graph(G)`: Generates the complement of a graph.
- `contains_forbidden_subgraph(G, forbidden_subgraph)`: Checks if the complement contains forbidden subgraphs like "Sun" or "Net".
- `identify_murderer_vertex(G, vertices, forbidden_structures)`: Identifies the murderer vertex, if one exists, which makes the complement graph free of forbidden subgraphs.

---

### **How It Works**

1. **Graph Creation**:  
   The program initializes an undirected graph with predefined nodes and edges.

2. **C4 Cycle Detection**:  
   It finds all 4-node cycles (C4) using combinatorial methods. A C4 cycle is a closed loop of 4 nodes where each node has exactly two connections (degree of 2).

3. **Overlapping Vertices**:  
   Overlapping vertices, those that belong to multiple C4 cycles, are identified and analyzed.

4. **Graph Visualization**:  
   The program visualizes the graph with excluded overlapping vertices and shows the resulting graph structures.

5. **Complement Graph**:  
   For each excluded vertex, the complement graph (edges between non-adjacent nodes) is generated.

6. **Forbidden Subgraph Detection**:  
   The complement graphs are checked for the presence of two specific subgraphs:
   - **Sun**: A 6-node, 9-edge structure.
   - **Net**: A 6-node, 6-edge structure.
   
   If no forbidden subgraphs are found, the vertex is identified as the **murderer vertex**.

---

### **Visualization**

Graphs are visualized using `matplotlib`:
- The original graph is drawn in a circular layout.
- For each excluded vertex, the new graph and its complement are visualized.
- Forbidden subgraphs (if present) are reported in the console output.

---

### **Future Improvements**

- **Performance Optimization**: Improve cycle detection for larger graphs.
- **Forbidden Subgraphs**: Extend support for additional subgraph structures.
- **Dynamic Graph Input**: Allow users to input custom graphs instead of hardcoded structures.
- **Enhanced Visualization**: Color-code or highlight key vertices and subgraphs in the visualization.

---

### **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
