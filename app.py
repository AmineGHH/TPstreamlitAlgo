import streamlit as st
from modules import avl  # you can import others later

st.set_page_config(page_title="Tree & Graph Visualizer", layout="wide")

# --- Main Menu ---
st.sidebar.title("📘 Menu")
page = st.sidebar.radio(
    "Choose what to visualize:",
    ["🏠 Home", "🌲 AVL Tree", "🌳 Binary Tree", "🔗 Graph"]
)

# --- Routing ---
if page == "🏠 Home":
    st.title("Welcome to the Tree & Graph Visualizer 🌿")
    st.markdown("""
        This app lets you visualize and interact with different data structures:
        - 🌲 AVL Trees  
        - 🌳 Binary Trees  
        - 🔗 Directed/Undirected Graphs  

        Select a structure from the sidebar to get started!
    """)

elif page == "🌲 AVL Tree":
    avl.show_avl_page()

elif page == "🌳 Binary Tree":
    st.info("Binary Tree section — coming soon!")

elif page == "🔗 Graph":
    st.info("Graph section — coming soon!")
