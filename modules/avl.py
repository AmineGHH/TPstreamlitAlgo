import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import copy

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.logs = []
        self.snapshots = []

    def snapshot(self, root, message):
        self.logs.append(message)
        self.snapshots.append(copy.deepcopy(root))

    def get_height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def node_count(self, node):
        if not node:
            return 0
        return 1 + self.node_count(node.left) + self.node_count(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, root, key):
        if root is None:
            root = Node(key)
            self.snapshot(root, f"Inserted {key}.")
            return root

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            self.snapshot(root, f"Attempted insert {key}, but key already exists — ignored.")
            return root

        self.update_height(root)
        balance = self.get_balance(root)

        # LL
        if balance > 1 and key < root.left.key:
            self.snapshot(root, f"Imbalance at node {root.key} (bf={balance}). LL case -> Right rotation.")
            new_root = self.right_rotate(root)
            self.snapshot(new_root, f"Right rotation at node {root.key} completed.")
            return new_root

        # RR
        if balance < -1 and key > root.right.key:
            self.snapshot(root, f"Imbalance at node {root.key} (bf={balance}). RR case -> Left rotation.")
            new_root = self.left_rotate(root)
            self.snapshot(new_root, f"Left rotation at node {root.key} completed.")
            return new_root

        # LR
        if balance > 1 and key > root.left.key:
            self.snapshot(root, f"Imbalance at node {root.key} (bf={balance}). LR case -> Left rotation on left child, then Right rotation.")
            root.left = self.left_rotate(root.left)
            self.snapshot(root, f"After left-rotate on left child of {root.key}.")
            new_root = self.right_rotate(root)
            self.snapshot(new_root, f"Right rotation at node {root.key} completed (LR).")
            return new_root

        # RL
        if balance < -1 and key < root.right.key:
            self.snapshot(root, f"Imbalance at node {root.key} (bf={balance}). RL case -> Right rotation on right child, then Left rotation.")
            root.right = self.right_rotate(root.right)
            self.snapshot(root, f"After right-rotate on right child of {root.key}.")
            new_root = self.left_rotate(root)
            self.snapshot(new_root, f"Left rotation at node {root.key} completed (RL).")
            return new_root

        self.snapshot(root, f"Inserted {key} — tree balanced at node {root.key} (bf={balance}).")
        return root

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, root, key):
        if not root:
            self.snapshot(root, f"Attempted delete {key}, node not found.")
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                temp = root.right
                self.snapshot(temp, f"Deleted {key}. Node had no left child; replaced with right child.")
                return temp
            elif not root.right:
                temp = root.left
                self.snapshot(temp, f"Deleted {key}. Node had no right child; replaced with left child.")
                return temp
            else:
                temp = self.min_value_node(root.right)
                root.key = temp.key
                root.right = self.delete(root.right, temp.key)
                self.snapshot(root, f"Deleted {key} by replacing with inorder successor {temp.key}.")

        if not root:
            return root

        self.update_height(root)
        balance = self.get_balance(root)

        # LL
        if balance > 1 and self.get_balance(root.left) >= 0:
            self.snapshot(root, f"Imbalance at node {root.key} after deletion (bf={balance}). LL -> Right rotation.")
            new_root = self.right_rotate(root)
            self.snapshot(new_root, f"Right rotation at node {root.key} completed.")
            return new_root

        # LR
        if balance > 1 and self.get_balance(root.left) < 0:
            self.snapshot(root, f"Imbalance at node {root.key} after deletion (bf={balance}). LR -> Left rotation on left child, then Right rotation.")
            root.left = self.left_rotate(root.left)
            self.snapshot(root, f"After left-rotate on left child of {root.key}.")
            new_root = self.right_rotate(root)
            self.snapshot(new_root, f"Right rotation at node {root.key} completed (LR).")
            return new_root

        # RR
        if balance < -1 and self.get_balance(root.right) <= 0:
            self.snapshot(root, f"Imbalance at node {root.key} after deletion (bf={balance}). RR -> Left rotation.")
            new_root = self.left_rotate(root)
            self.snapshot(new_root, f"Left rotation at node {root.key} completed.")
            return new_root

        # RL
        if balance < -1 and self.get_balance(root.right) > 0:
            self.snapshot(root, f"Imbalance at node {root.key} after deletion (bf={balance}). RL -> Right rotation on right child, then Left rotation.")
            root.right = self.right_rotate(root.right)
            self.snapshot(root, f"After right-rotate on right child of {root.key}.")
            new_root = self.left_rotate(root)
            self.snapshot(new_root, f"Left rotation at node {root.key} completed (RL).")
            return new_root

        self.snapshot(root, f"Deletion processed for {key}; node {root.key} balanced (bf={balance}).")
        return root

    def inorder(self, node, res=None):
        if res is None:
            res = []
        if node:
            self.inorder(node.left, res)
            res.append(node.key)
            self.inorder(node.right, res)
        return res

    def preorder(self, node, res=None):
        if res is None:
            res = []
        if node:
            res.append(node.key)
            self.preorder(node.left, res)
            self.preorder(node.right, res)
        return res

    def postorder(self, node, res=None):
        if res is None:
            res = []
        if node:
            self.postorder(node.left, res)
            self.postorder(node.right, res)
            res.append(node.key)
        return res

    def find_unbalanced(self, node, res=None):
        if res is None:
            res = []
        if node:
            bf = self.get_balance(node)
            if abs(bf) > 1:
                res.append((node.key, bf))
            self.find_unbalanced(node.left, res)
            self.find_unbalanced(node.right, res)
        return res

def build_graph(G, node, pos, x=0, y=0, layer=1):
    if node is None:
        return
    G.add_node(node.key)
    pos[node.key] = (x, y)
    if node.left:
        G.add_edge(node.key, node.left.key)
        build_graph(G, node.left, pos, x - 1 / layer, y - 1, layer + 1)
    if node.right:
        G.add_edge(node.key, node.right.key)
        build_graph(G, node.right, pos, x + 1 / layer, y - 1, layer + 1)

def draw_tree_matplotlib(root, highlight_keys=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    if root is None:
        ax.text(0.5, 0.5, "Empty tree", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    G = nx.DiGraph()
    pos = {}
    build_graph(G, root, pos, x=0, y=0, layer=1)
    node_colors = []
    highlight_keys = set(highlight_keys or [])
    for n in G.nodes:
        node_colors.append("#9FE2BF" if n not in highlight_keys else "#FF8A65")

    nx.draw(G, pos=pos, with_labels=True, node_size=1000,
            node_color=node_colors, font_weight="bold", arrows=False, ax=ax)
    ax.set_axis_off()
    fig.tight_layout()
    return fig

def init_session():
    if "avl_state" not in st.session_state:
        st.session_state.avl_state = {
            "tree": AVLTree(),
            "root": None,
            "step_index": -1,
        }

def show_avl_page():
    st.title("🌲 AVL Tree Visualizer")
    st.markdown("Create and manipulate self-balancing AVL trees with real-time visualization!")

    init_session()
    state = st.session_state.avl_state
    tree = state["tree"]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🛠️ Tree Operations")
        
        with st.container(border=True):
            st.write("**🌱 Create Tree**")
            create_mode = st.radio("Start with:", ["Empty tree", "From values"], key="avl_create")
            values_text = st.text_input("Values (e.g., 10, 5, 20, 15)", key="avl_vals")
            if st.button("🌳 Build Tree", use_container_width=True):
                tree.logs = []
                tree.snapshots = []
                state["root"] = None
                if create_mode == "Empty tree" or not values_text.strip():
                    tree.snapshot(state["root"], "Created empty tree.")
                else:
                    tokens = values_text.replace(",", " ").split()
                    for tok in tokens:
                        try:
                            v = int(tok)
                            state["root"] = tree.insert(state["root"], v)
                        except:
                            tree.snapshot(state["root"], f"Ignored non-int token: {tok}")
                    tree.snapshot(state["root"], f"Built tree from: {tokens}")
                state["step_index"] = len(tree.logs) - 1
                st.rerun()

        with st.container(border=True):
            st.write("**✏️ Modify Tree**")
            node_value = st.number_input("Node value", value=0, key="avl_node_val")
            op_col1, op_col2 = st.columns(2)
            with op_col1:
                if st.button("➕ Insert", use_container_width=True):
                    state["root"] = tree.insert(state["root"], node_value)
                    state["step_index"] = len(tree.logs) - 1
                    st.rerun()
            with op_col2:
                if st.button("🗑️ Delete", use_container_width=True):
                    state["root"] = tree.delete(state["root"], node_value)
                    state["step_index"] = len(tree.logs) - 1
                    st.rerun()

        if st.button("🔄 Reset Tree", use_container_width=True):
            tree.logs = []
            tree.snapshots = []
            state["root"] = None
            tree.snapshot(state["root"], "Tree reset to empty.")
            state["step_index"] = len(tree.logs) - 1
            st.rerun()

        st.subheader("📖 Operation History")
        logs = tree.logs
        if logs:
            idx = state.get("step_index", len(logs) - 1)
            if idx < 0: idx = 0
            
            nav_cols = st.columns([1, 2, 1])
            with nav_cols[0]:
                if st.button("⬅ Previous", use_container_width=True):
                    idx = max(0, idx - 1)
            with nav_cols[2]:
                if st.button("Next ➡", use_container_width=True):
                    idx = min(len(logs) - 1, idx + 1)
            state["step_index"] = idx
            
            st.info(f"**Step {idx+1}/{len(logs)}**: {logs[idx]}")
            
            with st.expander("View All Steps"):
                for i, step in enumerate(reversed(logs)):
                    st.write(f"• {step}")
        else:
            st.info("No operations yet. Build a tree to see step history.")

    with col2:
        st.subheader("📊 Tree Visualization")
        
        idx = state.get("step_index", -1)
        if idx >= 0 and idx < len(tree.snapshots):
            current_root = tree.snapshots[idx]
        else:
            current_root = state.get("root", None)

        if current_root:
            highlight = set()
            def find_unbalanced(node, avl_tree, result):
                if not node: return
                bf = avl_tree.get_balance(node)
                if abs(bf) > 1:
                    result.add(node.key)
                find_unbalanced(node.left, avl_tree, result)
                find_unbalanced(node.right, avl_tree, result)
            find_unbalanced(current_root, tree, highlight)
            
            fig = draw_tree_matplotlib(current_root, highlight)
            st.pyplot(fig)
            
            st.subheader("📈 Tree Properties")
            prop_col1, prop_col2, prop_col3 = st.columns(3)
            with prop_col1:
                st.metric("Height", tree.get_height(current_root))
            with prop_col2:
                st.metric("Node Count", tree.node_count(current_root))
            with prop_col3:
                balance_status = "✅ Balanced" if not highlight else "⚠️ Unbalanced"
                st.metric("Balance Status", balance_status)
            
            st.subheader("🔄 Tree Traversals")
            trav_col1, trav_col2, trav_col3 = st.columns(3)
            with trav_col1:
                st.write("**Inorder**")
                st.code(str(tree.inorder(current_root)))
            with trav_col2:
                st.write("**Preorder**")
                st.code(str(tree.preorder(current_root)))
            with trav_col3:
                st.write("**Postorder**")
                st.code(str(tree.postorder(current_root)))
        else:
            st.info("🌱 Tree is empty. Create a tree to see visualization.")