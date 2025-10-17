import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def show_directed_unweighted_page():
    st.title("➡️ Oriented Non-Weighted Graph")
    st.markdown("Directed graph without weights")
    
    if "graph_directed_unweighted" not in st.session_state:
        st.session_state.graph_directed_unweighted = {
            "graph": nx.DiGraph(),
            "vertices": set(),
            "edges": []
        }
    
    # Simple input
    st.subheader("Graph Input")
    edges_input = st.text_area(
        "Enter edges (format: A B):",
        "A B\nB C\nC A",
        height=100,
        help="Enter one edge per line in format: Source Target"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Build Graph", use_container_width=True):
            build_directed_unweighted(edges_input)
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_directed_unweighted()
    
    # Display results
    G = st.session_state.graph_directed_unweighted["graph"]
    
    if G.number_of_nodes() > 0:
        # Visualization
        st.subheader("Graph Visualization")
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightcoral', 
                node_size=800, font_weight='bold', arrows=True,
                arrowsize=20, arrowstyle='->', ax=ax)
        ax.set_title("Oriented Non-Weighted Graph")
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
        st.write("**Directed Edges:**", list(G.edges()))
        
        col_deg1, col_deg2 = st.columns(2)
        with col_deg1:
            st.write("**In-Degree:**")
            for node, degree in G.in_degree():
                st.write(f"  {node}: {degree}")
        
        with col_deg2:
            st.write("**Out-Degree:**")
            for node, degree in G.out_degree():
                st.write(f"  {node}: {degree}")
                
    else:
        st.info("Enter edges above and click 'Build Graph'")

def build_directed_unweighted(edges_input):
    G = nx.DiGraph()
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
                source, target = parts
                edges.append((source, target))
                vertices.add(source)
                vertices.add(target)
    
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    
    st.session_state.graph_directed_unweighted = {
        "graph": G,
        "vertices": vertices,
        "edges": edges
    }
    st.success(f"Built graph with {len(vertices)} vertices and {len(edges)} edges!")
    st.rerun()

def reset_directed_unweighted():
    st.session_state.graph_directed_unweighted = {
        "graph": nx.DiGraph(),
        "vertices": set(),
        "edges": []
    }
    st.rerun()