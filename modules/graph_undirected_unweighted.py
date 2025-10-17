import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def show_undirected_unweighted_page():
    st.title("🔗 Non-Oriented Non-Weighted Graph")
    st.markdown("Simple undirected graph without weights")
    
    if "graph_undirected_unweighted" not in st.session_state:
        st.session_state.graph_undirected_unweighted = {
            "graph": nx.Graph(),
            "vertices": set(),
            "edges": []
        }
    
    # Simple input
    st.subheader("Graph Input")
    edges_input = st.text_area(
        "Enter edges (format: A B):",
        "A B\nB C\nC A",
        height=100,
        help="Enter one edge per line in format: Vertex1 Vertex2"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Build Graph", use_container_width=True):
            build_undirected_unweighted(edges_input)
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_undirected_unweighted()
    
    # Display results
    G = st.session_state.graph_undirected_unweighted["graph"]
    
    if G.number_of_nodes() > 0:
        # Visualization
        st.subheader("Graph Visualization")
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=800, font_weight='bold', ax=ax)
        ax.set_title("Non-Oriented Non-Weighted Graph")
        ax.axis('off')
        st.pyplot(fig)
        
        # Analysis
        st.subheader("Graph Analysis")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Vertices", G.number_of_nodes())
        with col2:
            st.metric("Edges", G.number_of_edges())
        with col3:
            density = nx.density(G)
            st.metric("Density", f"{density:.3f}")
        with col4:
            if G.number_of_nodes() >= 2:
                connected = "Yes" if nx.is_connected(G) else "No"
                st.metric("Connected", connected)
        
        st.write("**Vertices:**", sorted(G.nodes()))
        st.write("**Edges:**", list(G.edges()))
        
        st.write("**Degree of each vertex:**")
        for node, degree in G.degree():
            st.write(f"  {node}: {degree}")
            
    else:
        st.info("Enter edges above and click 'Build Graph'")

def build_undirected_unweighted(edges_input):
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
            if len(parts) == 2:
                v1, v2 = parts
                edges.append((v1, v2))
                vertices.add(v1)
                vertices.add(v2)
    
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    
    st.session_state.graph_undirected_unweighted = {
        "graph": G,
        "vertices": vertices,
        "edges": edges
    }
    st.success(f"Built graph with {len(vertices)} vertices and {len(edges)} edges!")
    st.rerun()

def reset_undirected_unweighted():
    st.session_state.graph_undirected_unweighted = {
        "graph": nx.Graph(),
        "vertices": set(),
        "edges": []
    }
    st.rerun()