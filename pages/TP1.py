import streamlit as st
from modules import abr, avl, heap, graph_directed_unweighted, graph_directed_weighted, graph_undirected_unweighted, graph_undirected_weighted

st.set_page_config(page_title="TP1 - Trees and Graphs", page_icon="🌳", layout="wide")

st.title("🌳 TP1: Trees and Graphs")
st.markdown("Explore and visualize fundamental data structures below.")

# List of visual modules
options = {
    "Binary Search Tree (ABR)": abr.show_abr_page,
    "AVL Tree": avl.show_avl_page,
    "Heap Tree": heap.show_heap_page,
    "Directed Unweighted Graph": graph_directed_unweighted.show_directed_unweighted_page,
    "Directed Weighted Graph": graph_directed_weighted.show_directed_weighted_page,
    "Undirected Unweighted Graph": graph_undirected_unweighted.show_undirected_unweighted_page,
    "Undirected Weighted Graph": graph_undirected_weighted.show_undirected_weighted_page
}

choice = st.selectbox("Choose a visualization:", list(options.keys()))

st.divider()
options[choice]()  # run the selected module
