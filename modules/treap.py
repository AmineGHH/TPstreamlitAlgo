import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional, List, Dict, Any, Set

# ----------------------------
# Treap implementation
# ----------------------------
class TreapNode:
    def __init__(self, key, priority=None):
        self.key = int(key)
        self.priority = int(priority) if priority is not None else random.randint(0, 100)
        self.left: Optional["TreapNode"] = None
        self.right: Optional["TreapNode"] = None

    def __repr__(self):
        return f"{self.key}/{self.priority}"

class Treap:
    def __init__(self, heap_type="max"):
        assert heap_type in ("max", "min")
        self.root: Optional["TreapNode"] = None
        self.heap_type = heap_type

    def _compare(self, a, b):
        """Return True if 'a' should be above 'b' based on heap type."""
        return a > b if self.heap_type == "max" else a < b

    # rotations
    def rotate_right(self, y: TreapNode) -> TreapNode:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        return x

    def rotate_left(self, x: TreapNode) -> TreapNode:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        return y

    # internal insert with logs
    def _insert(self, node: Optional[TreapNode], key: int, priority: int, logs: List[str]) -> TreapNode:
        if node is None:
            node = TreapNode(key, priority)
            logs.append(f"✅ Created node {node.key}/{node.priority}.")
            return node
        if key == node.key:
            logs.append(f"⚠️ Key {key} already exists ({node.key}/{node.priority}). Skipped.")
            return node
        if key < node.key:
            logs.append(f"{key}/{priority} vs {node.key}/{node.priority}: go left.")
            node.left = self._insert(node.left, key, priority, logs)
            if node.left and self._compare(node.left.priority, node.priority):
                logs.append(f"Rotate right: left {node.left.priority} {'>' if self.heap_type=='max' else '<'} parent {node.priority}.")
                node = self.rotate_right(node)
        else:
            logs.append(f"{key}/{priority} vs {node.key}/{node.priority}: go right.")
            node.right = self._insert(node.right, key, priority, logs)
            if node.right and self._compare(node.right.priority, node.priority):
                logs.append(f"Rotate left: right {node.right.priority} {'>' if self.heap_type=='max' else '<'} parent {node.priority}.")
                node = self.rotate_left(node)
        return node

    def insert(self, key: int, priority: Optional[int] = None) -> List[str]:
        if priority is None or str(priority).strip() == "" or int(priority) == 0:
            p = random.randint(0, 100)
        else:
            p = int(priority)
        logs = [f"🟩 INSERT {key}/{p}"]
        self.root = self._insert(self.root, key, p, logs)
        logs.append("✅ Insertion complete.")
        return logs

    # deletion
    def _delete(self, node: Optional[TreapNode], key: int, logs: List[str]) -> Optional[TreapNode]:
        if node is None:
            logs.append(f"❌ Key {key} not found.")
            return None

        if key < node.key:
            logs.append(f"Search {key} vs {node.key}/{node.priority}: go left.")
            node.left = self._delete(node.left, key, logs)
        elif key > node.key:
            logs.append(f"Search {key} vs {node.key}/{node.priority}: go right.")
            node.right = self._delete(node.right, key, logs)
        else:
            logs.append(f"🗑️ Found {node.key}/{node.priority} → deleting.")
            if node.left is None:
                logs.append("No left child → replace by right.")
                return node.right
            elif node.right is None:
                logs.append("No right child → replace by left.")
                return node.left
            else:
                if self._compare(node.right.priority, node.left.priority):
                    logs.append(f"Rotate left: right {node.right.priority} {'>' if self.heap_type=='max' else '<'} left {node.left.priority}.")
                    node = self.rotate_left(node)
                    node.left = self._delete(node.left, key, logs)
                else:
                    logs.append(f"Rotate right: left {node.left.priority} {'>=' if self.heap_type=='max' else '<='} right {node.right.priority}.")
                    node = self.rotate_right(node)
                    node.right = self._delete(node.right, key, logs)
        return node

    def delete(self, key: int) -> List[str]:
        logs = [f"🟥 DELETE {key}"]
        self.root = self._delete(self.root, key, logs)
        logs.append("✅ Deletion complete.")
        return logs

    # HEAP-LIKE OPERATIONS
    def delete_root(self) -> List[str]:
        """Delete the root node (like heap pop operation) - 'deletion de la racine'"""
        logs = [f"🟥 DELETE ROOT (Heap-like operation)"]
        if self.root is None:
            logs.append("❌ Treap is empty - no root to delete")
            return logs
        
        root_key = self.root.key
        root_priority = self.root.priority
        logs.append(f"🗑️ Deleting root node: {root_key}/{root_priority}")
        self.root = self._delete_root_recursive(self.root, logs)
        logs.append(f"✅ Root deletion complete. Removed key: {root_key}")
        return logs

    def _delete_root_recursive(self, node: TreapNode, logs: List[str]) -> Optional[TreapNode]:
        """Recursively delete root using rotations (like heapify down)"""
        if node.left is None and node.right is None:
            logs.append("Root is now a leaf - removing it")
            return None
        
        # Push root down using rotations (similar to heapify down)
        if node.left is None:
            logs.append(f"Rotate left: no left child, push root down right")
            node = self.rotate_left(node)
            node.left = self._delete_root_recursive(node.left, logs)
        elif node.right is None:
            logs.append(f"Rotate right: no right child, push root down left")
            node = self.rotate_right(node)
            node.right = self._delete_root_recursive(node.right, logs)
        else:
            # Both children exist - rotate towards higher priority child
            if self._compare(node.left.priority, node.right.priority):
                logs.append(f"Rotate right: left priority {node.left.priority} {'>' if self.heap_type=='max' else '<'} right {node.right.priority}")
                node = self.rotate_right(node)
                node.right = self._delete_root_recursive(node.right, logs)
            else:
                logs.append(f"Rotate left: right priority {node.right.priority} {'>' if self.heap_type=='max' else '<'} left {node.left.priority}")
                node = self.rotate_left(node)
                node.left = self._delete_root_recursive(node.left, logs)
        return node

    def get_root(self) -> Optional[Dict[str, int]]:
        """Get root key and priority (like heap peek)"""
        if self.root is None:
            return None
        return {"key": self.root.key, "priority": self.root.priority}

    # OPTIMIZED: BST SORT METHOD - O(n) time, O(h) space
    def bst_sort(self) -> List[tuple]:
        """BST Sort - Iterative in-order traversal returns sorted keys with priorities"""
        result = []
        stack = []
        current = self.root
        
        while current or stack:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process node
            current = stack.pop()
            result.append((current.key, current.priority))
            
            # Move to right subtree
            current = current.right
        
        return result

    # OPTIMIZED: HEAP SORT METHOD - O(n log n) time, O(n) space
    def heap_sort(self) -> List[tuple]:
        """Heap Sort - Extract all nodes by priority using iterative DFS"""
        if self.root is None:
            return []
        
        # Collect all nodes using stack (no recursion limits)
        nodes = []
        stack = [self.root]
        
        while stack:
            node = stack.pop()
            nodes.append((node.key, node.priority))
            
            # Add children to stack (right first, then left for DFS order)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        # Sort by priority
        if self.heap_type == "max":
            nodes.sort(key=lambda x: x[1], reverse=True)  # Sort by priority descending
        else:
            nodes.sort(key=lambda x: x[1])  # Sort by priority ascending
        
        return nodes

    def _copy(self) -> "Treap":
        """Create a copy of the treap for operations like heap_sort"""
        new_treap = Treap(self.heap_type)
        new_treap.root = self._copy_node(self.root)
        return new_treap

    def _copy_node(self, node: Optional[TreapNode]) -> Optional[TreapNode]:
        if node is None:
            return None
        new_node = TreapNode(node.key, node.priority)
        new_node.left = self._copy_node(node.left)
        new_node.right = self._copy_node(node.right)
        return new_node

    # traversals
    def inorder(self, node: Optional[TreapNode], res: Optional[List[int]] = None) -> List[int]:
        if res is None:
            res = []
        if node:
            self.inorder(node.left, res)
            res.append(node.key)
            self.inorder(node.right, res)
        return res

    def preorder(self, node: Optional[TreapNode], res: Optional[List[int]] = None) -> List[int]:
        if res is None:
            res = []
        if node:
            res.append(node.key)
            self.preorder(node.left, res)
            self.preorder(node.right, res)
        return res

    def postorder(self, node: Optional[TreapNode], res: Optional[List[int]] = None) -> List[int]:
        if res is None:
            res = []
        if node:
            self.postorder(node.left, res)
            self.postorder(node.right, res)
            res.append(node.key)
        return res

    def find(self, node: Optional[TreapNode], key: int) -> Optional[TreapNode]:
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self.find(node.left, key)
        return self.find(node.right, key)

# ----------------------------
# Visualization helpers - MINIMALISTIC SPLIT RECTANGLES
# ----------------------------
def compute_inorder_x(root: Optional[TreapNode]):
    x_index = {"i": 0}
    pos_x = {}
    def inorder(node):
        if not node:
            return
        inorder(node.left)
        pos_x[node] = x_index["i"]
        x_index["i"] += 1
        inorder(node.right)
    inorder(root)
    return pos_x

def compute_positions(root: Optional[TreapNode], x_spacing=2.5, y_spacing=3.0):
    positions = {}
    if root is None:
        return positions
    x_indices = compute_inorder_x(root)
    def dfs(node, depth=0):
        if not node:
            return
        x = x_indices[node] * x_spacing
        y = -depth * y_spacing
        positions[node] = (x, y)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)
    dfs(root, 0)
    if positions:
        xs = [x for x, y in positions.values()]
        mid = (min(xs) + max(xs)) / 2
        for n in list(positions.keys()):
            x, y = positions[n]
            positions[n] = (x - mid, y)
    return positions

def draw_treap(root: Optional[TreapNode], highlight_keys: Optional[Set[int]] = None, 
               title="Treap", fig_width=12, fig_height=8, heap_type="max"):
    highlight_keys = set(highlight_keys or [])
    positions = compute_positions(root, x_spacing=3.0, y_spacing=3.5)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Clean background
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    if not positions:
        ax.text(0.5, 0.5, "Treap is empty", ha="center", va="center", fontsize=16, color="#666666")
        ax.axis("off")
        return fig

    # Draw connections
    for node, (x, y) in positions.items():
        if node.left and node.left in positions:
            x2, y2 = positions[node.left]
            ax.plot([x, x2], [y-0.8, y2+0.8], '#95a5a6', lw=2, alpha=0.6)
        if node.right and node.right in positions:
            x2, y2 = positions[node.right]
            ax.plot([x, x2], [y-0.8, y2+0.8], '#95a5a6', lw=2, alpha=0.6)

    # Highlight root with special color
    root_node = root
    root_pos = positions.get(root_node, None)

    # Draw split rectangle nodes
    node_width, node_height = 2.0, 1.2
    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]

    for node, (x, y) in positions.items():
        is_high = node.key in highlight_keys
        is_root = node == root_node
        
        # Colors - special color for root
        key_color = "#FF6B6B"  # Red for key
        priority_color = "#4ECDC4"  # Teal for priority
        
        if is_root:
            border_color = "#9B59B6"  # Purple for root
            border_width = 4
        else:
            border_color = "#FFD93D" if is_high else "#2C3E50"
            border_width = 3 if is_high else 1
        
        # Draw main rectangle
        rect = plt.Rectangle((x - node_width/2, y - node_height/2), node_width, node_height,
                           facecolor='white', edgecolor=border_color, 
                           lw=border_width, zorder=3)
        ax.add_patch(rect)
        
        # Draw key half (left)
        key_rect = plt.Rectangle((x - node_width/2, y - node_height/2), 
                                node_width/2, node_height,
                                facecolor=key_color, edgecolor=border_color, 
                                lw=1, zorder=4, alpha=0.9)
        ax.add_patch(key_rect)
        
        # Draw priority half (right)
        priority_rect = plt.Rectangle((x, y - node_height/2), 
                                     node_width/2, node_height,
                                     facecolor=priority_color, edgecolor=border_color, 
                                     lw=1, zorder=4, alpha=0.9)
        ax.add_patch(priority_rect)
        
        # Key text (left half) - large and centered
        ax.text(x - node_width/4, y, f"{node.key}", ha='center', va='center', 
                fontsize=14, fontweight='bold', zorder=5, color='white')
        
        # Priority text (right half) - large and centered
        ax.text(x + node_width/4, y, f"{node.priority}", ha='center', va='center', 
                fontsize=14, fontweight='bold', zorder=5, color='white')

        # Add root indicator
        if is_root:
            ax.text(x, y + node_height/2 + 0.3, "ROOT", ha='center', va='bottom',
                   fontsize=10, fontweight='bold', color='#9B59B6')

    # Clean styling
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=18, pad=20, fontweight='bold', color='#2C3E50')
    ax.axis('off')
    
    if xs and ys:
        ax.set_xlim(min(xs) - 2.5, max(xs) + 2.5)
        ax.set_ylim(min(ys) - 2.0, max(ys) + 1.5)
    
    return fig

# ----------------------------
# Utilities
# ----------------------------
def collect_nodes(root: Optional[TreapNode]) -> List[Dict[str, Any]]:
    rows = []
    def dfs(node):
        if not node:
            return
        left_key = node.left.key if node.left else None
        right_key = node.right.key if node.right else None
        rows.append({"key": node.key, "priority": node.priority, "left": left_key, "right": right_key})
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    rows_sorted = sorted(rows, key=lambda r: r["key"])
    return rows_sorted

# ----------------------------
# Streamlit UI
# ----------------------------
def main():
    st.set_page_config(page_title="Treap Visualizer", layout="wide", page_icon="🌳")
    
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 300;
    }
    .sort-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4ECDC4;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🌳 Treap Visualizer</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if "treap_obj" not in st.session_state:
        st.session_state.treap_obj = Treap("max")
        st.session_state.treap_logs = ["Treap initialized as max-heap."]
        st.session_state.treap_highlight = set()

    treap = st.session_state.treap_obj

    # Main layout
    left, right = st.columns([1, 1.4])

    with left:
        st.subheader("⚙️ Configuration")
        
        # Heap type
        heap_type = st.radio("Heap Type", ["max", "min"], horizontal=True, key="heap_type")
        if st.session_state.treap_obj.heap_type != heap_type:
            st.session_state.treap_obj = Treap(heap_type)
            st.session_state.treap_logs = [f"Treap initialized as {heap_type}-heap."]
            st.session_state.treap_highlight = set()

        st.markdown("---")
        st.subheader("🔧 Operations")
        
        # Single operation
        col1, col2 = st.columns(2)
        with col1:
            key = st.number_input("Key", value=0, step=1)
        with col2:
            priority = st.text_input("Priority", placeholder="Random if empty")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Insert", use_container_width=True, type="primary"):
                try:
                    p = None if not priority.strip() else int(priority)
                    logs = treap.insert(key, p)
                    st.session_state.treap_logs.extend(logs)
                    st.session_state.treap_highlight = {key}
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        with col2:
            if st.button("Delete", use_container_width=True):
                logs = treap.delete(key)
                st.session_state.treap_logs.extend(logs)
                st.session_state.treap_highlight = set()
                st.rerun()
        with col3:
            if st.button("Delete Root", use_container_width=True, type="secondary"):
                logs = treap.delete_root()
                st.session_state.treap_logs.extend(logs)
                st.session_state.treap_highlight = set()
                st.rerun()

        # Bulk operations
        with st.expander("Bulk Operations"):
            bulk_keys = st.text_input("Keys (space or comma separated)", "10 5 15 3 7")
            bulk_priority = st.text_input("Priority for all", placeholder="Random if empty")
            if st.button("Insert All"):
                keys = [int(k) for k in bulk_keys.replace(',', ' ').split() if k.strip()]
                for k in keys:
                    p = None if not bulk_priority.strip() else int(bulk_priority)
                    treap.insert(k, p)
                st.session_state.treap_highlight = set(keys)
                st.rerun()

        # Search
        with st.expander("Search"):
            search_key = st.number_input("Search key", value=0, step=1)
            if st.button("Find"):
                found = treap.find(treap.root, search_key)
                if found:
                    st.success(f"Found: {found.key} (Priority: {found.priority})")
                    st.session_state.treap_highlight = {search_key}
                else:
                    st.warning("Not found")
                    st.session_state.treap_highlight = set()

        # Sorting Section - CLEARLY SEPARATED
        st.markdown("---")
        st.subheader("📊 Sorting Methods")
        
        # BST Sort Section
        with st.container():
            st.markdown('<div class="sort-section">', unsafe_allow_html=True)
            st.markdown("**🌳 BST Sort (Tri par BST)**")
            st.markdown("*In-order traversal - sorted by keys*")
            
            if st.button("Show BST Sort", key="bst_sort"):
                bst_sorted = treap.bst_sort()
                if bst_sorted:
                    st.success(f"BST Sorted (by keys):")
                    st.write(bst_sorted)
                else:
                    st.warning("Treap is empty")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Heap Sort Section  
        with st.container():
            st.markdown('<div class="sort-section">', unsafe_allow_html=True)
            st.markdown("**⚡ Heap Sort (Tri par Tas)**")
            st.markdown("*Extract root repeatedly - sorted by priority*")
            
            if st.button("Show Heap Sort", key="heap_sort"):
                heap_sorted = treap.heap_sort()
                if heap_sorted:
                    st.success(f"Heap Sorted (by priority):")
                    st.write(heap_sorted)
                else:
                    st.warning("Treap is empty")
            st.markdown('</div>', unsafe_allow_html=True)

        # Root Info
        st.markdown("---")
        st.subheader("🎯 Root Information")
        if st.button("Get Root"):
            root = treap.get_root()
            if root:
                st.success(f"**Root Node:** Key={root['key']}, Priority={root['priority']}")
                st.session_state.treap_highlight = {root['key']}
            else:
                st.warning("Treap is empty")

    with right:
        st.subheader("🖼️ Visualization")
        
        # Visualization
        fig = draw_treap(treap.root, 
                        highlight_keys=st.session_state.treap_highlight,
                        heap_type=heap_type)
        st.pyplot(fig)

        st.info("🔴 Key | 🔵 Priority | 🟡 Highlighted | 🟣 Root Node")

        # Node table
        st.markdown("---")
        st.subheader("📋 Node Details")
        nodes = collect_nodes(treap.root)
        if nodes:
            df = pd.DataFrame(nodes)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No nodes in the treap")

        # Controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Highlight", use_container_width=True):
                st.session_state.treap_highlight = set()
                st.rerun()
        with col2:
            if st.button("Reset Treap", use_container_width=True):
                st.session_state.treap_obj = Treap(heap_type)
                st.session_state.treap_logs = [f"Treap reset ({heap_type}-heap)"]
                st.session_state.treap_highlight = set()
                st.rerun()

    # Logs at bottom
    st.markdown("---")
    with st.expander("Recent Logs"):
        for log in st.session_state.treap_logs[-20:]:
            st.text(log)

if __name__ == "__main__":
    main()