import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Any, Dict
from collections import defaultdict
import graphviz # Import for graph visualization

# Define a large number for infinity in shortest path calculations
INF = float('inf')

# ====================================================================
# A. CORE LOGIC FUNCTIONS (Johnson's and Welsh-Powell)
# ====================================================================

# --- Johnson's Algorithm Components ---

def _find_min_distance_vertex(dist: List[float], visited: List[bool]) -> int:
    """Helper for Dijkstra's: Finds the unvisited vertex with minimum distance."""
    min_dist = INF
    min_vertex = -1
    for vertex in range(len(dist)):
        if not visited[vertex] and dist[vertex] < min_dist:
            min_dist = dist[vertex]
            min_vertex = vertex
    return min_vertex

def bellman_ford_potentials(edges: List[Tuple[int, int, float]], num_vertices: int) -> Optional[List[float]]:
    """Runs Bellman-Ford on an augmented graph to compute potentials h(v) and check for negative cycles."""
    total_nodes = num_vertices + 1
    h = [INF] * total_nodes
    h[num_vertices] = 0.0
    augmented_edges = list(edges)
    
    # Add zero-weight edges from virtual source s (index num_vertices) to all other nodes
    for i in range(num_vertices):
        augmented_edges.append((num_vertices, i, 0.0))

    # Relaxation Loop: Runs |V| times
    for i in range(num_vertices):
        relaxed = False
        for u, v, weight in augmented_edges:
            if h[u] != INF and h[u] + weight < h[v]:
                h[v] = h[u] + weight
                relaxed = True
        if not relaxed:
            # If no relaxation occurred in a full pass, we can stop early
            break

    # Negative Cycle Check (one final pass)
    for u, v, weight in augmented_edges:
        if h[u] != INF and h[u] + weight < h[v]:
            return None # Negative cycle detected

    return h[:num_vertices]

def dijkstra_shortest_path(altered_graph: List[List[float]], source: int) -> List[float]:
    """Runs Dijkstra's algorithm on the non-negative reweighted graph (w' >= 0)."""
    num_vertices = len(altered_graph)
    d_prime = [INF] * num_vertices
    visited = [False] * num_vertices
    d_prime[source] = 0.0

    for _ in range(num_vertices):
        cur_vertex = _find_min_distance_vertex(d_prime, visited)
        if cur_vertex == -1:
            break
        visited[cur_vertex] = True

        for neighbor in range(num_vertices):
            weight_prime = altered_graph[cur_vertex][neighbor]
            if (weight_prime != 0.0 and 
                weight_prime != INF and
                not visited[neighbor] and
                d_prime[cur_vertex] != INF and
                d_prime[cur_vertex] + weight_prime < d_prime[neighbor]):
                
                d_prime[neighbor] = d_prime[cur_vertex] + weight_prime
    return d_prime

def JohnsonAlgorithm(graph: List[List[float]]) -> Optional[Tuple[List[List[float]], List[float], List[List[float]], List[List[float]]]]:
    """
    Runs Johnson's algorithm and returns final distances, potentials (h), 
    the reweighted graph, and the intermediate Dijkstra's results (d').
    """
    num_vertices = len(graph)
    edges = []
    # 1. Extract edges for Bellman-Ford
    for i in range(num_vertices):
        for j in range(num_vertices):
            weight = graph[i][j]
            # Assume 0.0 in the input matrix means no edge, unless i==j (loop)
            if weight != 0.0 or i == j: 
                # Skip zero-weight edges (if not self-loop) and infinity values for clean edges list
                if weight != 0.0 and weight != INF:
                    edges.append((i, j, weight))

    # 2. Compute potentials h(v) via Bellman-Ford on augmented graph
    h = bellman_ford_potentials(edges, num_vertices)
    if h is None:
        return None # Negative cycle detected

    # 3. Reweight the Graph w'(u, v) = w(u, v) + h(u) - h(v)
    altered_graph = [[0.0 for _ in range(num_vertices)] for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            original_weight = graph[i][j]
            if original_weight != 0.0 and original_weight != INF:
                # Calculate new non-negative weight
                altered_graph[i][j] = original_weight + h[i] - h[j]
            elif original_weight == INF:
                altered_graph[i][j] = INF

    # 4. Run Dijkstra's from every source node on the reweighted graph
    final_distance_matrix = [[INF for _ in range(num_vertices)] for _ in range(num_vertices)]
    d_prime_matrix = [[INF for _ in range(num_vertices)] for _ in range(num_vertices)]

    for source in range(num_vertices):
        d_prime = dijkstra_shortest_path(altered_graph, source) 
        d_prime_matrix[source] = d_prime
        
        # 5. Calculate Final Paths D(u, v) = d'(u, v) - h(u) + h(v)
        for dest in range(num_vertices):
            if d_prime[dest] != INF:
                final_distance = d_prime[dest] - h[source] + h[dest]
                final_distance_matrix[source][dest] = final_distance
    
    # Updated return structure to include d_prime_matrix
    return final_distance_matrix, h, altered_graph, d_prime_matrix


# --- Welsh-Powell Algorithm Component (Unchanged) ---

def WelshPowellAlgorithm(adj_list: Dict[Any, List[Any]]) -> Tuple[Dict[Any, int], int, List[Tuple[Any, int]]]:
    """
    Implements the Welsh-Powell algorithm for graph coloring.
    Returns: (coloring map, total colors, sorted_vertices_with_degree)
    """
    if not adj_list:
        return ({}, 0, [])
    
    vertices = list(adj_list.keys())
    degrees = {v: len(adj_list[v]) for v in vertices}
    
    # Sort vertices in descending order of degree
    sorted_vertices = sorted(vertices, key=lambda v: degrees[v], reverse=True)
    sorted_vertices_with_degree = [(v, degrees[v]) for v in sorted_vertices]

    coloring: Dict[Any, int] = {}
    current_color = 1
    
    while len(coloring) < len(vertices):
        
        for u in sorted_vertices:
            if u not in coloring:
                can_be_colored = True
                
                for v in adj_list.get(u, []):
                    if v in coloring and coloring[v] == current_color:
                        can_be_colored = False
                        break
                
                if can_be_colored:
                    coloring[u] = current_color

        if len(coloring) < len(vertices) and current_color == max(coloring.values(), default=0):
            pass
            
        current_color += 1

    return coloring, current_color - 1, sorted_vertices_with_degree


# ====================================================================
# B. INPUT PARSERS, CONVERTERS, AND VISUALIZATION (Unchanged)
# ====================================================================

# --- Graph Visualization ---
def draw_graph(data: Any, labels: List[str], is_directed: bool, is_weighted: bool, coloring: Optional[Dict[Any, int]] = None):
    """Draws the graph using graphviz based on matrix or adjacency list."""
    
    # Use Digraph for directed, Graph for undirected
    dot = graphviz.Digraph('G', comment='Graph', graph_attr={'rankdir': 'LR'}) if is_directed else graphviz.Graph('G', comment='Graph', graph_attr={'rankdir': 'LR'})
    
    # Define a simple color palette
    color_palette = ['#FF6666', '#66B2FF', '#66FF66', '#FFCC66', '#CC66FF', '#66FFFF', '#FF66B2', '#B266FF']
    
    # 1. Add Nodes (with coloring if provided)
    for i, label in enumerate(labels):
        node_attrs = {'shape': 'circle'}
        if coloring and label in coloring:
            color_index = (coloring[label] - 1) % len(color_palette)
            node_attrs['style'] = 'filled'
            node_attrs['fillcolor'] = color_palette[color_index]
            
        dot.node(label, **node_attrs)
    
    # 2. Add Edges (from Adjacency Matrix/List)
    if isinstance(data, list) and all(isinstance(row, list) for row in data): # Adjacency Matrix
        N = len(data)
        for i in range(N):
            for j in range(N):
                weight = data[i][j]
                if weight != 0.0 and weight != INF:
                    u = labels[i]
                    v = labels[j]
                    
                    edge_label = f"{weight:.1f}" if is_weighted else ""
                    
                    if is_directed:
                        dot.edge(u, v, label=edge_label)
                    elif i < j: # Undirected: add only one way
                        dot.edge(u, v, label=edge_label, dir='none')

    elif isinstance(data, dict): # Adjacency List
        for u_str, neighbors in data.items():
            for v_str in neighbors:
                if u_str != v_str: # Avoid self loops for visualization clarity
                    if is_directed:
                        dot.edge(u_str, v_str, label="")
                    elif u_str < v_str: # Undirected: ensure one edge per pair
                        dot.edge(u_str, v_str, label="", dir='none')

    st.graphviz_chart(dot)


# --- Input Parsers (Unchanged) ---

def parse_matrix_input(matrix_str: str) -> Optional[List[List[float]]]:
    """Parses a string of comma/space-separated rows into a float matrix."""
    rows = matrix_str.strip().split('\n')
    matrix = []
    
    try:
        first_row_values = [float(x) for x in rows[0].replace(',', ' ').split() if x]
        N = len(first_row_values)
        matrix.append(first_row_values)

        for i in range(1, len(rows)):
            if not rows[i].strip(): continue
            values = [float(x) for x in rows[i].replace(',', ' ').split() if x]
            if len(values) != N:
                st.error(f"Row {i+1} has {len(values)} columns, expected {N}.")
                return None
            matrix.append(values)

        if len(matrix) != N:
            st.error(f"Input must be an N x N matrix. Found {len(matrix)} rows and {N} columns.")
            return None
        return matrix
    except ValueError:
        st.error("Invalid input format. Please ensure all entries are numbers.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during parsing: {e}")
        return None


def parse_adj_list_input(list_str: str) -> Dict[str, List[str]]:
    """Parses a string input like 'A: B C\nB: A C' into an adjacency dictionary."""
    adj_list: Dict[str, List[str]] = {}
    lines = list_str.strip().split('\n')
    
    for line in lines:
        if ':' not in line: continue
        try:
            vertex, neighbors_str = line.split(':', 1)
            vertex = vertex.strip()
            neighbors = [n.strip() for n in neighbors_str.replace(',', ' ').split() if n.strip()]
            adj_list[vertex] = neighbors
        except Exception:
            st.error(f"Invalid format in line: {line}. Use format 'Vertex: Neighbor1 Neighbor2'")
            return {}
            
    return adj_list

def parse_incidence_matrix_to_adj_matrix(matrix_str: str, is_directed: bool) -> Optional[List[List[float]]]:
    """Parses an Incidence Matrix string (V rows, E columns) and converts it to an Adjacency Matrix (V x V)."""
    rows = matrix_str.strip().split('\n')
    
    try:
        if not rows or not rows[0].strip():
            st.error("Incidence Matrix cannot be empty.")
            return None
            
        incident_matrix = []
        for row in rows:
            if not row.strip(): continue
            values = [float(x) for x in row.replace(',', ' ').split() if x]
            incident_matrix.append(values)

        V = len(incident_matrix)
        if V == 0: return None
        E = len(incident_matrix[0])
        
        # Initialize Adjacency Matrix
        adj_matrix = [[0.0 for _ in range(V)] for _ in range(V)]

        for e in range(E): # Iterate over each edge (column)
            head_v = -1
            tail_v = -1
            weight = 0.0

            if is_directed:
                # Directed/Weighted: Convention -w at tail, +w at head
                for v in range(V):
                    val = incident_matrix[v][e]
                    if val < 0:
                        tail_v = v
                        weight = abs(val) # Weight is magnitude of negative entry
                    elif val > 0:
                        head_v = v
                
                if tail_v != -1 and head_v != -1 and tail_v != head_v:
                    adj_matrix[tail_v][head_v] = weight
            
            else:
                # Undirected/Unweighted (for coloring): Convention 1 at incident vertices
                incident_vertices = []
                for v in range(V):
                    if incident_matrix[v][e] != 0:
                        incident_vertices.append(v)

                if len(incident_vertices) == 2:
                    v1, v2 = incident_vertices
                    # Set weight to 1 for unweighted coloring
                    adj_matrix[v1][v2] = 1.0
                    adj_matrix[v2][v1] = 1.0

        return adj_matrix

    except ValueError:
        st.error("Invalid input format. Please ensure all incidence matrix entries are numbers.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during incidence matrix parsing: {e}")
        return None


def adj_matrix_to_adj_list(matrix: List[List[float]], labels: List[str]) -> Dict[str, List[str]]:
    """Converts an Adjacency Matrix to an Adjacency List (for Welsh-Powell)."""
    adj_list = defaultdict(list)
    N = len(matrix)
    
    for i in range(N):
        for j in range(N):
            # Assumes 0 means no edge, non-zero means edge (for unweighted coloring)
            if matrix[i][j] != 0:
                u = labels[i]
                v = labels[j]
                
                # For coloring, we assume undirected: ensure undirected connectivity
                if v not in adj_list[u]:
                    adj_list[u].append(v)
                if u not in adj_list[v]:
                    adj_list[v].append(u) 
    return dict(adj_list)


# ====================================================================
# C. STREAMLIT UI IMPLEMENTATION (Updated for Johnson's details)
# ====================================================================

def render_johnson_page():
    st.title("🛣️ Johnson's Algorithm: All-Pairs Shortest Paths")
    st.markdown("""
        Johnson's algorithm finds the shortest path between all pairs of vertices in a weighted, directed graph. 
        It is efficient for sparse graphs and can handle negative edge weights, provided there are no negative cycles.
    """)
    st.markdown("") 

    st.subheader("1. Weighted Directed Graph Input")
    
    input_type = st.radio(
        "Choose Input Format:",
        ("Adjacency Matrix", "Incidence Matrix"),
        key='johnson_input_type'
    )
    
    graph_matrix = None
    input_key = 'johnson_input'
    
    if input_type == "Adjacency Matrix":
        # Default example with negative weights
        default_matrix = "0, -5, 2, 3\n0, 0, 4, 0\n0, 0, 0, 1\n0, 0, 0, 0"
        matrix_input = st.text_area(
            "Enter Weighted Adjacency Matrix (N x N, 0 means no edge, or use 'inf'):", 
            default_matrix, 
            height=150,
            key=input_key
        )
        # Replace 'inf' with INF for parsing
        matrix_input = matrix_input.replace('inf', str(INF))
        graph_matrix = parse_matrix_input(matrix_input)
    
    elif input_type == "Incidence Matrix":
        st.info("Incidence Matrix for Directed Weighted Graph: Enter $-w$ for the tail and $+w$ for the head of an edge with weight $w$.")
        default_incidence = "-5, 2, 3, 0\n5, -4, 0, 0\n0, 4, -1, 0\n0, 0, 1, 0"
        matrix_input = st.text_area(
            "Enter Incidence Matrix (V rows, E columns):", 
            default_incidence, 
            height=150,
            key=input_key
        )
        graph_matrix = parse_incidence_matrix_to_adj_matrix(matrix_input, is_directed=True)
    
    if graph_matrix is not None and st.button("Apply Johnson's Algorithm"):
        
        num_vertices = len(graph_matrix)
        vertex_labels = [f"V{i}" for i in range(num_vertices)]
        
        st.subheader("2. Graph Visualization")
        st.caption("Directed Weighted Graph Input:")
        draw_graph(graph_matrix, vertex_labels, is_directed=True, is_weighted=True)
        
        with st.spinner("Running Bellman-Ford and repeated Dijkstra's..."):
            results = JohnsonAlgorithm(graph_matrix)

        st.subheader("3. Results and Analysis")
        
        if results is None:
            st.error("❌ Negative Cycle Detected!")
            st.markdown(
                "The algorithm stopped because the **Bellman-Ford step** detected a cycle where the sum of edge weights is negative. "
                "The shortest path is undefined in the presence of a negative cycle."
            )
            return
        
        final_distance_matrix, h, altered_graph, d_prime_matrix = results

        # Format the final matrix for display
        final_data = [[f"{val:.2f}" if val != INF else "Inf" for val in row] for row in final_distance_matrix]
        df_final = pd.DataFrame(final_data, index=vertex_labels, columns=vertex_labels)

        st.markdown("---")
        st.success("✅ Algorithm Completed successfully (No Negative Cycles)")

        st.subheader("Final All-Pairs Shortest Path Matrix D(u, v)")
        st.caption("The true shortest path distance from the row vertex (Source, u) to the column vertex (Destination, v).")
        st.dataframe(df_final)

        st.subheader("Detailed Steps of Johnson's Algorithm")
        st.markdown(
            """
            Johnson's algorithm relies on reweighting the graph using potential values ($h(v)$) calculated by Bellman-Ford, 
            so that Dijkstra's algorithm can be safely applied.
            """
        )

        with st.expander("Step 1: Potentials (h) and Reweighted Graph (w')"):
            
            st.markdown(f"**Potential Values (h):** $h(v)$ are the shortest path distances from the virtual source $s$ to all vertices $v$ via Bellman-Ford.")
            h_data = {v: f"{h[i]:.2f}" for i, v in enumerate(vertex_labels)}
            st.json(h_data)

            st.markdown(r"""
            **Reweighting Formula:** The new, non-negative weight $w'(u, v)$ for every edge is calculated as:
            $$w'(u, v) = w(u, v) + h(u) - h(v)$$
            """)
            st.markdown("**Reweighted Adjacency Matrix (w'):** All weights are non-negative, allowing Dijkstra's to run correctly.")
            altered_data = [[f"{val:.2f}" if val != 0.0 and val != INF else "0.00" if val != INF else "Inf" for val in row] for row in altered_graph]
            df_altered = pd.DataFrame(altered_data, index=vertex_labels, columns=vertex_labels)
            st.dataframe(df_altered)
            
            st.caption("Note: $w'(u, v)$ is guaranteed to be non-negative.")


        with st.expander("Step 2: Repeated Dijkstra's Results (d')"):
            
            st.markdown(r"""
            **Dijkstra's Results (d'):** Dijkstra's algorithm is run from every source $u$ on the non-negative reweighted graph $G'$, yielding the shortest path distance $d'(u, v)$.
            """)
            
            # Format the d_prime_matrix for display
            d_prime_data = [[f"{val:.2f}" if val != INF else "Inf" for val in row] for row in d_prime_matrix]
            df_d_prime = pd.DataFrame(d_prime_data, index=vertex_labels, columns=vertex_labels)
            st.dataframe(df_d_prime)

        with st.expander("Step 3: Recovering the Final Distance D(u, v)"):
            
            st.markdown(r"""
            **Final Distance Recovery Formula:** The true shortest path distance $D(u, v)$ is recovered from the temporary Dijkstra's result $d'(u, v)$ using the potential values:
            $$D(u, v) = d'(u, v) - h(u) + h(v)$$
            """)
            
            # Show an example calculation for the first source vertex
            st.markdown(f"**Example: Calculation for Source {vertex_labels[0]} ($u={vertex_labels[0]}$)**")
            
            source_u_index = 0
            h_u = h[source_u_index]
            
            recovery_details = []
            for dest_v_index in range(num_vertices):
                h_v = h[dest_v_index]
                d_prime_uv = d_prime_matrix[source_u_index][dest_v_index]
                final_D_uv = final_distance_matrix[source_u_index][dest_v_index]
                
                if d_prime_uv != INF:
                    calculation = f"{final_D_uv:.2f} = {d_prime_uv:.2f} (d') - {h_u:.2f} (h(u)) + {h_v:.2f} (h(v))"
                else:
                    calculation = "Inf"
                
                recovery_details.append([vertex_labels[dest_v_index], calculation])

            df_recovery = pd.DataFrame(recovery_details, columns=['Destination (v)', 'D(u, v) Calculation'])
            st.dataframe(df_recovery.set_index('Destination (v)'))


def render_welsh_powell_page():
    st.title("🎨 Welsh-Powell Algorithm: Graph Coloring")
    st.markdown("""
        The Welsh-Powell algorithm is a **greedy sequential coloring algorithm** used to find an upper bound 
        for the chromatic number ($\chi(G)$) of an **undirected, unweighted** graph.
    """)
    st.markdown("[Image of Graph Coloring Example]")

    st.subheader("1. Undirected Graph Input")
    
    input_type = st.radio(
        "Choose Input Format:",
        ("Adjacency List", "Adjacency Matrix", "Incidence Matrix"),
        key='welsh_powell_input_type'
    )
    
    adj_list = None
    
    if input_type == "Adjacency List":
        default_adj_list = "A: B C D\nB: A C E\nC: A B D E\nD: A C\nE: B C"
        input_data = st.text_area(
            "Enter Adjacency List (e.g., 'A: B C D'):", 
            default_adj_list, 
            height=150
        )
        adj_list = parse_adj_list_input(input_data)
        
    else: # Matrix inputs (convert to Adj List)
        matrix = None
        if input_type == "Adjacency Matrix":
            default_matrix = "0 1 1 1 0\n1 0 1 0 1\n1 1 0 1 1\n1 0 1 0 0\n0 1 1 0 0"
            input_data = st.text_area(
                "Enter Adjacency Matrix (N x N, 1=edge, 0=no edge):", 
                default_matrix, 
                height=150
            )
            matrix = parse_matrix_input(input_data)
        
        elif input_type == "Incidence Matrix":
            st.info("Incidence Matrix for Undirected Unweighted Graph: Use 1 for incident vertices, 0 otherwise.")
            default_incidence = "1 1 1 0 0\n1 0 0 1 1\n0 1 1 0 1\n0 0 1 0 0\n0 1 0 1 1"
            input_data = st.text_area(
                "Enter Incidence Matrix (V rows, E columns):", 
                default_incidence, 
                height=150
            )
            matrix = parse_incidence_matrix_to_adj_matrix(input_data, is_directed=False)

        if matrix is not None:
            # Generate labels V0, V1, ... for matrix input
            labels = [f"V{i}" for i in range(len(matrix))]
            adj_list = adj_matrix_to_adj_list(matrix, labels)

    
    if adj_list is not None and st.button("Apply Welsh-Powell Algorithm"):
        
        st.subheader("2. Initial Graph Visualization")
        all_vertices = sorted(list(adj_list.keys()))
        draw_graph(adj_list, all_vertices, is_directed=False, is_weighted=False)
        
        with st.spinner("Sorting vertices and assigning colors..."):
            coloring, total_colors, sorted_with_degree = WelshPowellAlgorithm(adj_list)

        st.subheader("3. Results and Analysis")
        st.success(f"✅ Coloring Completed. Total Colors Used: {total_colors}")
        
        st.subheader("Color Visualization")
        st.caption("Nodes are colored according to the final assignment.")
        draw_graph(adj_list, all_vertices, is_directed=False, is_weighted=False, coloring=coloring)


        st.subheader("Approach and Detailed Steps (Greedy Sequential)")
        st.markdown(
            """
            The Welsh-Powell algorithm is a **Greedy Algorithm** that follows three steps:
            1.  **Degree Calculation:** Calculate the degree of every vertex.
            2.  **Sorting:** Sort the vertices in **descending order** of their degrees. This is the heuristic used.
            3.  **Sequential Coloring:** Iterate through the sorted list, assigning the *lowest available* color to each vertex, ensuring no adjacent vertices share the same color.
            """
        )

        st.subheader("Vertex Ordering and Degree")
        df_degree = pd.DataFrame(sorted_with_degree, columns=['Vertex', 'Degree'])
        st.dataframe(df_degree.set_index('Vertex'))

        st.subheader("Color Assignment")
        
        # Group vertices by color for display
        colors_map = defaultdict(list)
        for vertex, color in coloring.items():
            colors_map[color].append(vertex)
            
        color_details = []
        for color, vertices_list in sorted(colors_map.items()):
            color_details.append([color, ', '.join(vertices_list)])
        
        df_coloring = pd.DataFrame(color_details, columns=['Color ID', 'Vertices'])
        st.dataframe(df_coloring.set_index('Color ID'))


def main():
    st.sidebar.title("Graph Algorithm Selector")
    algorithm_choice = st.sidebar.radio(
        "Choose Algorithm Page:",
        ("Welsh-Powell (Coloring)", "Johnson's (Shortest Paths)")
    )
    
    if algorithm_choice == "Welsh-Powell (Coloring)":
        render_welsh_powell_page()
    elif algorithm_choice == "Johnson's (Shortest Paths)":
        render_johnson_page()

if __name__ == "__main__":
    main()