import streamlit as st
from modules.avl import show_avl_page
from modules.heap import show_heap_page
from modules.abr import show_abr_page
from modules.graph_undirected_unweighted import show_undirected_unweighted_page
from modules.graph_undirected_weighted import show_undirected_weighted_page
from modules.graph_directed_unweighted import show_directed_unweighted_page
from modules.graph_directed_weighted import show_directed_weighted_page

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Data Structure Visualizer", layout="wide")

# Custom CSS for dashboard styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid;
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
    }
    
    .tree-card {
        border-left-color: #4CAF50;
    }
    
    .graph-card {
        border-left-color: #2196F3;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .step-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #e9ecef;
        margin: 0.5rem;
    }
    
    .feature-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .nav-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        margin: 0.5rem 0;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Get query parameters using the new API
query_params = st.query_params
page_from_url = query_params.get("page", ["🏠 Dashboard Home"])[0]

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = page_from_url

# Update page based on URL or session
current_page = st.session_state.current_page

# Sidebar navigation
st.sidebar.markdown("## 🚀 Navigation Panel")

# Use radio buttons in sidebar for reliable navigation
sidebar_page = st.sidebar.radio(
    "**Select Tool:**",
    [
        "🏠 Dashboard Home", 
        "🌳 Binary Search Tree",
        "🌲 AVL Tree", 
        "🧱 Heap", 
        "🔗 Non-Oriented Non-Weighted Graph",
        "🔗 Non-Oriented Weighted Graph", 
        "➡️ Oriented Non-Weighted Graph",
        "➡️ Oriented Weighted Graph"
    ],
    index=[
        "🏠 Dashboard Home", 
        "🌳 Binary Search Tree",
        "🌲 AVL Tree", 
        "🧱 Heap", 
        "🔗 Non-Oriented Non-Weighted Graph",
        "🔗 Non-Oriented Weighted Graph", 
        "➡️ Oriented Non-Weighted Graph",
        "➡️ Oriented Weighted Graph"
    ].index(current_page) if current_page in [
        "🏠 Dashboard Home", 
        "🌳 Binary Search Tree",
        "🌲 AVL Tree", 
        "🧱 Heap", 
        "🔗 Non-Oriented Non-Weighted Graph",
        "🔗 Non-Oriented Weighted Graph", 
        "➡️ Oriented Non-Weighted Graph",
        "➡️ Oriented Weighted Graph"
    ] else 0
)

# Update current page if sidebar selection changes
if sidebar_page != current_page:
    st.session_state.current_page = sidebar_page
    st.query_params["page"] = sidebar_page
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use buttons on the main page or select from this list!")

# Navigation function
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.query_params["page"] = page_name
    st.rerun()

# --- Dashboard Home Page ---
if current_page == "🏠 Dashboard Home":
    # Hero Section
    st.markdown('<div class="main-header">Data Structure Visualizer</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.3rem; color: #666; margin-bottom: 3rem;">Interactive Dashboard for Data Structures & Algorithms</div>', unsafe_allow_html=True)
    
    # Stats Overview
    st.subheader("📈 Dashboard Overview")
    
    stats_cols = st.columns(4)
    
    with stats_cols[0]:
        st.markdown("""
        <div class="stats-card">
            <h3>🌳</h3>
            <h4>3 Tree Tools</h4>
            <p>BST, AVL, Heap</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[1]:
        st.markdown("""
        <div class="stats-card">
            <h3>🔗</h3>
            <h4>4 Graph Tools</h4>
            <p>Weighted & Directed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[2]:
        st.markdown("""
        <div class="stats-card">
            <h3>⚡</h3>
            <h4>Real-time</h4>
            <p>Live Visualization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[3]:
        st.markdown("""
        <div class="stats-card">
            <h3>🎯</h3>
            <h4>Easy to Use</h4>
            <p>Simple Interface</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tools Dashboard with WORKING BUTTONS
    st.subheader("🛠️ Quick Access Tools")
    
    # Tree Tools Section
    st.markdown("### 🌳 Tree Structures")
    
    tree_cols = st.columns(3)
    
    with tree_cols[0]:
        st.markdown("""
        <div class="dashboard-card tree-card">
            <h3>🌳 Binary Search Tree</h3>
            <p><strong>Features:</strong></p>
            <ul>
            <li>Insert/Delete operations</li>
            <li>Multiple traversals</li>
            <li>Balance checking</li>
            <li>Real-time updates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Open BST Tool", key="bst_btn", use_container_width=True):
            navigate_to("🌳 Binary Search Tree")
    
    with tree_cols[1]:
        st.markdown("""
        <div class="dashboard-card tree-card">
            <h3>🌲 AVL Tree</h3>
            <p><strong>Features:</strong></p>
            <ul>
            <li>Self-balancing trees</li>
            <li>Automatic rotations</li>
            <li>Step-by-step history</li>
            <li>Balance factors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Open AVL Tool", key="avl_btn", use_container_width=True):
            navigate_to("🌲 AVL Tree")
    
    with tree_cols[2]:
        st.markdown("""
        <div class="dashboard-card tree-card">
            <h3>🧱 Heap Structure</h3>
            <p><strong>Features:</strong></p>
            <ul>
            <li>Min/Max heap support</li>
            <li>Priority operations</li>
            <li>Tree visualization</li>
            <li>Array representation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Open Heap Tool", key="heap_btn", use_container_width=True):
            navigate_to("🧱 Heap")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graph Tools Section
    st.markdown("### 🔗 Graph Structures")
    
    graph_cols = st.columns(2)
    
    with graph_cols[0]:
        st.markdown("""
        <div class="dashboard-card graph-card">
            <h3>🔗 Non-Oriented Graphs</h3>
            <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <h4>⚖️ Weighted Version</h4>
                <p>• Edge weight support<br>• Weighted degrees<br>• Comprehensive metrics</p>
            </div>
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <h4>🎯 Non-Weighted Version</h4>
                <p>• Simple connections<br>• Basic analysis<br>• Connectivity checks</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Open Weighted", key="nw_btn", use_container_width=True):
                navigate_to("🔗 Non-Oriented Weighted Graph")
        with col2:
            if st.button("Open Non-Weighted", key="nw2_btn", use_container_width=True):
                navigate_to("🔗 Non-Oriented Non-Weighted Graph")
    
    with graph_cols[1]:
        st.markdown("""
        <div class="dashboard-card graph-card">
            <h3>➡️ Oriented Graphs</h3>
            <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <h4>⚖️ Weighted Version</h4>
                <p>• Directed edges with weights<br>• In/Out degree analysis<br>• Flow analysis</p>
            </div>
            <div style="background: #fce4ec; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <h4>🎯 Non-Weighted Version</h4>
                <p>• Directed connections<br>• Connectivity analysis<br>• Component detection</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Open Weighted", key="dw_btn", use_container_width=True):
                navigate_to("➡️ Oriented Weighted Graph")
        with col4:
            if st.button("Open Non-Weighted", key="dnw_btn", use_container_width=True):
                navigate_to("➡️ Oriented Non-Weighted Graph")
    
    st.markdown("---")
    
    # Quick Navigation Buttons
    st.subheader("⚡ Quick Navigation")
    
    quick_cols = st.columns(4)
    
    with quick_cols[0]:
        if st.button("🌳 BST", use_container_width=True):
            navigate_to("🌳 Binary Search Tree")
    with quick_cols[1]:
        if st.button("🌲 AVL", use_container_width=True):
            navigate_to("🌲 AVL Tree")
    with quick_cols[2]:
        if st.button("🧱 Heap", use_container_width=True):
            navigate_to("🧱 Heap")
    with quick_cols[3]:
        if st.button("🔗 Graphs", use_container_width=True):
            navigate_to("🔗 Non-Oriented Non-Weighted Graph")
    
    st.markdown("---")
    
    # Features Section
    st.subheader("⭐ Key Features")
    
    feature_cols = st.columns(2)
    
    with feature_cols[0]:
        st.markdown("""
        <div class="feature-item">
            <h4>🎨 Professional Visualization</h4>
            <p>Clean, interactive visualizations with professional styling</p>
        </div>
        
        <div class="feature-item">
            <h4>⚡ Real-time Interaction</h4>
            <p>Instant updates as you modify data structures</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_cols[1]:
        st.markdown("""
        <div class="feature-item">
            <h4>📊 Comprehensive Analysis</h4>
            <p>Detailed metrics and structural analysis</p>
        </div>
        
        <div class="feature-item">
            <h4>🎯 User-Friendly</h4>
            <p>Simple interface with working navigation</p>
        </div>
        """, unsafe_allow_html=True)

# --- Other Pages ---
elif current_page == "🌳 Binary Search Tree":
    show_abr_page()

elif current_page == "🌲 AVL Tree":
    show_avl_page()

elif current_page == "🧱 Heap":
    show_heap_page()

elif current_page == "🔗 Non-Oriented Non-Weighted Graph":
    show_undirected_unweighted_page()

elif current_page == "🔗 Non-Oriented Weighted Graph":
    show_undirected_weighted_page()

elif current_page == "➡️ Oriented Non-Weighted Graph":
    show_directed_unweighted_page()

elif current_page == "➡️ Oriented Weighted Graph":
    show_directed_weighted_page()