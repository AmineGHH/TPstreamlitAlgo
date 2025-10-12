# modules/avl.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import copy

# ========== AVL core with step logging ==========
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        # logs: list of text messages describing operations
        # snapshots: parallel list of root copies representing the tree state after the message
        self.logs = []
        self.snapshots = []

    # ----------------- utilities -----------------
    def snapshot(self, root, message):
        """Save a deepcopy snapshot of root and the message."""
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

    # ----------------- rotations -----------------
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # rotation
        x.right = y
        y.left = T2

        # update heights
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # rotation
        y.left = x
        x.right = T2

        # update heights
        self.update_height(x)
        self.update_height(y)
        return y

    # ----------------- insert / delete with logging -----------------
    def insert(self, root, key):
        # normal BST insert
        if root is None:
            root = Node(key)
            self.snapshot(root, f"Inserted {key}.")
            return root

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            # duplicate: ignore, but log and snapshot
            self.snapshot(root, f"Attempted insert {key}, but key already exists — ignored.")
            return root

        # update height and balance
        self.update_height(root)
        balance = self.get_balance(root)

        # check imbalances and perform rotations while logging snapshots before/after
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

        # no rotation needed
        self.snapshot(root, f"Inserted {key} — tree balanced at node {root.key} (bf={balance}).")
        return root

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, root, key):
        # usual BST delete
        if not root:
            self.snapshot(root, f"Attempted delete {key}, node not found.")
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # node found
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

        # update height and rebalance
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

    # traversal helpers (for stats)
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

# ========== Visualization helpers ==========
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
    """Return a matplotlib figure for the given tree. highlight_keys is a set."""
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

# ========== Streamlit page ==========
def init_session():
    if "avl_state" not in st.session_state:
        st.session_state.avl_state = {
            "tree": AVLTree(),
            "root": None,
            "step_index": -1,   # -1 means no steps yet
        }

def show_avl_page():
    st.title("🌲 AVL Tree — Interactive Visualizer with Step Replay")
    st.markdown("Create a tree (empty or from values), then insert/delete nodes. "
                "Watch the step-by-step logs and replay the snapshots of what happened.")

    init_session()
    state = st.session_state.avl_state
    tree: AVLTree = state["tree"]

    # --- Left panel: creation + modification + logs navigator ---
    left, right = st.columns([1, 2])

    with left:
        st.subheader("Create / Modify")
        create_mode = st.radio("Start with:", ["Empty tree", "From values (comma/space separated)"])
        values_text = st.text_input("Values (e.g. 10, 5, 20, 15)", key="create_vals")
        if st.button("Create Tree"):
            # reset logs/snapshots and build new tree
            tree.logs = []
            tree.snapshots = []
            state["root"] = None
            if create_mode == "Empty tree" or values_text.strip() == "":
                # empty
                tree.snapshot(state["root"], "Created empty tree.")
            else:
                tokens = values_text.replace(",", " ").split()
                for tok in tokens:
                    try:
                        v = int(tok)
                        state["root"] = tree.insert(state["root"], v)
                    except:
                        tree.snapshot(state["root"], f"Ignored non-int token: {tok}")
                tree.snapshot(state["root"], f"Finished bulk creation from values: {tokens}")
            # move step index to last
            state["step_index"] = len(tree.logs) - 1

        st.markdown("---")
        st.subheader("Modify tree")
        col_a, col_b = st.columns([2, 1])
        with col_a:
            mod_val = st.text_input("Value (single int)", key="mod_val")
        with col_b:
            if st.button("➕ Insert"):
                if mod_val.strip().lstrip("-").isdigit():
                    v = int(mod_val)
                    state["root"] = tree.insert(state["root"], v)
                    state["step_index"] = len(tree.logs) - 1
                else:
                    st.error("Enter a valid integer to insert.")
            if st.button("❌ Delete"):
                if mod_val.strip().lstrip("-").isdigit():
                    v = int(mod_val)
                    state["root"] = tree.delete(state["root"], v)
                    state["step_index"] = len(tree.logs) - 1
                else:
                    st.error("Enter a valid integer to delete.")
        if st.button("🔄 Reset Tree"):
            tree.logs = []
            tree.snapshots = []
            state["root"] = None
            tree.snapshot(state["root"], "Tree reset to empty.")
            state["step_index"] = len(tree.logs) - 1

        st.markdown("---")
        st.subheader("Steps / Replay")
        logs = tree.logs
        if len(logs) == 0:
            st.info("No steps yet. Create/modify the tree to see step logs.")
        else:
            idx = state.get("step_index", len(logs) - 1)
            if idx < 0:
                idx = 0
            # navigation buttons
            nav_cols = st.columns([1, 3, 1])
            if nav_cols[0].button("⬅ Prev"):
                idx = max(0, idx - 1)
            if nav_cols[2].button("Next ➡"):
                idx = min(len(logs) - 1, idx + 1)
            state["step_index"] = idx

            # show step info
            st.markdown(f"**Step {idx+1} / {len(logs)}**")
            st.write(logs[idx])

            # list of recent steps (collapsible)
            with st.expander("All steps (recent first)", expanded=False):
                for i, s in enumerate(reversed(logs)):
                    st.write(f"{len(logs)-i}. {s}")

    # --- Right: visualization + properties ---
    with right:
        st.subheader("Visualization")
        idx = state.get("step_index", -1)
        # choose which root snapshot to draw: if no logs -> current root
        if idx >= 0 and idx < len(tree.snapshots):
            root_to_draw = tree.snapshots[idx]
        else:
            root_to_draw = state.get("root", None)

        # highlight keys that are unbalanced in this snapshot
        highlight = set()
        if root_to_draw:
            # compute unbalanced nodes in snapshot using a temporary tree util
            def collect_unbalanced(n, avl_tmp, out):
                if not n:
                    return
                bf = avl_tmp.get_balance(n)
                if abs(bf) > 1:
                    out.add(n.key)
                collect_unbalanced(n.left, avl_tmp, out)
                collect_unbalanced(n.right, avl_tmp, out)
            collect_unbalanced(root_to_draw, tree, highlight)

        fig = draw_tree_matplotlib(root_to_draw, highlight_keys=highlight)
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("Tree Properties")
        if root_to_draw:
            st.write("**Height:**", tree.get_height(root_to_draw))
            st.write("**Number of nodes:**", tree.node_count(root_to_draw))
            unb = tree.find_unbalanced(root_to_draw)
            if unb:
                st.warning(f"Unbalanced nodes (key, bf): {unb}")
            else:
                st.success("All nodes balanced (|bf| ≤ 1).")
            st.write("**Inorder:**", tree.inorder(root_to_draw))
            st.write("**Preorder:**", tree.preorder(root_to_draw))
        else:
            st.info("Tree is empty.")
