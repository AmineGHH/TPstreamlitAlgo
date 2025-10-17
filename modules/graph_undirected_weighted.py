import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def show_undirected_weighted_page():
    st.title("🔗 Non-Oriented Weighted Graph")
    st.markdown("Undirected graph with edge weights")
    
    if "graph_undirected_weighted" not in st.session_state:
        st.session_state.graph_undirected_weighted = {
            "graph": nx.Graph(),
            "vertices": set(),
            "edges": []
        }
    
    # Simple input
    st.subheader("Graph Input")
    edges_input = st.text_area(
        "Enter edges (format: A B 2.5):",
        "A B 2.5\nB C 1.0\nC A 3.2",
        height=100,
        help="Enter one edge per line in format: Vertex1 Vertex2 Weight"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Build Graph", use_container_width=True):
            build_undirected_weighted(edges_input)
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_undirected_weighted()
    
    # Display results
    G = st.session_state.graph_undirected_weighted["graph"]
    
    if G.number_of_nodes() > 0:
        # Visualization
        st.subheader("Graph Visualization")
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightgreen', 
                node_size=800, font_weight='bold', ax=ax)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                   font_color='red', font_weight='bold', ax=ax)
        
        ax.set_title("Non-Oriented Weighted Graph")
        ax.axis('off')
        st.pyplot(fig)
        
        # Analysis
        st.subheader("Graph Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Vertices", G.number_of_nodes())
        with col2:
            st.metric("Edges", G.number_of_edges())
        with col3:
            density = nx.density(G)
            st.metric("Density", f"{density:.3f}")
        
        st.write("**Vertices:**", sorted(G.nodes()))
        
        st.write("**Edges with weights:**")
        for u, v, data in G.edges(data=True):
            st.write(f"  {u} — {v}: {data['weight']}")
        
        st.write("**Degree (unweighted):**")
        for node, degree in G.degree():
            st.write(f"  {node}: {degree}")
        
        st.write("**Weighted Degree:**")
        for node, degree in G.degree(weight='weight'):
            st.write(f"  {node}: {degree:.1f}")
            
    else:
        st.info("Enter edges above and click 'Build Graph'")

def build_undirected_weighted(edges_input):
    G = nx.Graph()
    edges = []
    vertices = set()
    
    if edges_input.strip():
        lines = edges_input.strip().split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 3:
                try:
                    v1, v2, weight_str = parts
                    weight = float(weight_str)
                    edges.append((v1, v2, weight))
                    vertices.add(v1)
                    vertices.add(v2)
                except ValueError:
                    st.error(f"Line {line_num}: Invalid weight '{weight_str}'")
    
    G.add_nodes_from(vertices)
    for v1, v2, weight in edges:
        G.add_edge(v1, v2, weight=weight)
    
    st.session_state.graph_undirected_weighted = {
        "graph": G,
        "vertices": vertices,
        "edges": edges
    }
    st.success(f"Built graph with {len(vertices)} vertices and {len(edges)} edges!")
    st.rerun()

def reset_undirected_weighted():
    st.session_state.graph_undirected_weighted = {
        "graph": nx.Graph(),
        "vertices": set(),
        "edges": []
    }
    st.rerun()