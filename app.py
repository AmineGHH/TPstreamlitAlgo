import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Algorithm Visualizer Dashboard",
    page_icon="🧠",
    layout="wide",
)

st.title("🧩 Algorithm Visualizer Dashboard")
st.write("Welcome! Select a TP to explore different data structures and algorithms.")

# Description text for each TP
tp_descriptions = {
    "TP1": "Covers basic binary search trees (ABR), AVL trees, heaps, and graph fundamentals.",
    "TP2": "Focuses on advanced trees like Treap — combining BST and heap properties.",
    "TP3": "coming soon",
    "TP4": "coming soon",
    "TP5": "coming soon",
    "TP6": "coming soon",
}

cols = st.columns(3)
tp_names = list(tp_descriptions.keys())

# Generate cards
for i, tp_name in enumerate(tp_names):
    with cols[i % 3]:
        st.markdown(f"### {tp_name}")
        st.write(tp_descriptions[tp_name])
        if st.button(f"Open {tp_name}", key=f"btn_{tp_name}"):
            st.switch_page(f"pages/{tp_name}.py")
