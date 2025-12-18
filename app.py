import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Algorithm Visualizer Dashboard",
    page_icon="🧠",
    layout="wide",
)

st.title("🧩 Algorithm Visualizer Dashboard")
st.write("Welcome! Select a TP to explore different data structures and algorithms.")

# Updated TP descriptions
tp_descriptions = {
    "TP1": "Covers basic binary search trees (ABR), AVL trees, heaps, and graph fundamentals.",
    "TP2": "Focuses on advanced trees like Treap — combining BST and heap properties.",
    "TP3": "Advanced algorithm analysis with complexity measurement and performance testing.",
    "TP4 – Johnson Algorithm": "Shortest paths in weighted graphs using Johnson’s algorithm.",
    "TP4 – Welsh-Powell Algorithm": "Graph coloring using the Welsh–Powell heuristic.",
}

# Mapping TP names to actual page files
tp_pages = {
    "TP1": "pages/TP1.py",
    "TP2": "pages/TP2.py",
    "TP3": "pages/TP3.py",
    "TP4 – Johnson Algorithm": "pages/TP4johnson_ui.py",
    "TP4 – Welsh-Powell Algorithm": "pages/TP4welsh_powell_ui.py",
}

cols = st.columns(3)
tp_names = list(tp_descriptions.keys())

# Generate cards
for i, tp_name in enumerate(tp_names):
    with cols[i % 3]:
        st.markdown(f"### {tp_name}")
        st.write(tp_descriptions[tp_name])
        if st.button(f"Open {tp_name}", key=f"btn_{tp_name}"):
            st.switch_page(tp_pages[tp_name])
