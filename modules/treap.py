# modules/treap.py
import streamlit as st
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import pandas as pd
from typing import Optional, List, Dict, Any, Set

# ----------------------------
# Treap implementation (keeps your original logic)
# ----------------------------
class TreapNode:
    def __init__(self, key, priority=None):
        self.key = int(key)
        self.priority = float(priority) if priority is not None else round(random.uniform(0, 100), 2)
        self.left: Optional["TreapNode"] = None
        self.right: Optional["TreapNode"] = None

    def __repr__(self):
        return f"{self.key}/{self.priority:.2f}"

class Treap:
    def __init__(self, heap_type="max"):
        assert heap_type in ("max", "min")
        self.root: Optional[TreapNode] = None
        self.heap_type = heap_type

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
    def _insert(self, node: Optional[TreapNode], key: int, priority: float, logs: List[str]) -> TreapNode:
        if node is None:
            node = TreapNode(key, priority)
            logs.append(f"✅ Created node {node.key}/{node.priority:.2f}.")
            return node

        if key == node.key:
            logs.append(f"⚠️ Key {key} already exists ({node.key}/{node.priority:.2f}). Skipped.")
            return node

        if key < node.key:
            logs.append(f"{key}/{priority:.2f} vs {node.key}/{node.priority:.2f}: go left.")
            node.left = self._insert(node.left, key, priority, logs)
            if node.left and node.left.priority > node.priority:
                logs.append(f"Rotate right: left {node.left.priority:.2f} > parent {node.priority:.2f}.")
                node = self.rotate_right(node)
        else:
            logs.append(f"{key}/{priority:.2f} vs {node.key}/{node.priority:.2f}: go right.")
            node.right = self._insert(node.right, key, priority, logs)
            if node.right and node.right.priority > node.priority:
                logs.append(f"Rotate left: right {node.right.priority:.2f} > parent {node.priority:.2f}.")
                node = self.rotate_left(node)
        return node

    def insert(self, key: int, priority: Optional[float] = None) -> List[str]:
        if priority is None or float(priority) == 0.0:
            p = round(random.uniform(0, 100), 2)
        else:
            p = float(priority)
        logs = [f"🟩 INSERT {key}/{p:.2f}"]
        self.root = self._insert(self.root, key, p, logs)
        logs.append("✅ Insertion complete.")
        return logs

    # deletion
    def _delete(self, node: Optional[TreapNode], key: int, logs: List[str]) -> Optional[TreapNode]:
        if node is None:
            logs.append(f"❌ Key {key} not found.")
            return None

        if key < node.key:
            logs.append(f"Search {key} vs {node.key}/{node.priority:.2f}: go left.")
            node.left = self._delete(node.left, key, logs)
        elif key > node.key:
            logs.append(f"Search {key} vs {node.key}/{node.priority:.2f}: go right.")
            node.right = self._delete(node.right, key, logs)
        else:
            logs.append(f"🗑️ Found {node.key}/{node.priority:.2f} → deleting.")
            if node.left is None:
                logs.append("No left child → replace by right.")
                return node.right
            elif node.right is None:
                logs.append("No right child → replace by left.")
                return node.left
            else:
                # rotate towards the child with larger priority
                if node.left.priority < node.right.priority:
                    logs.append(f"Rotate left: right {node.right.priority:.2f} > left {node.left.priority:.2f}.")
                    node = self.rotate_left(node)
                    node.left = self._delete(node.left, key, logs)
                else:
                    logs.append(f"Rotate right: left {node.left.priority:.2f} >= right {node.right.priority:.2f}.")
                    node = self.rotate_right(node)
                    node.right = self._delete(node.right, key, logs)
        return node

    def delete(self, key: int) -> List[str]:
        logs = [f"🟥 DELETE {key}"]
        self.root = self._delete(self.root, key, logs)
        logs.append("✅ Deletion complete.")
        return logs

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
# Visualization helpers
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

def compute_positions(root: Optional[TreapNode], x_spacing=1.6, y_spacing=2.0):
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

def draw_treap(root: Optional[TreapNode], highlight_keys: Optional[Set[int]] = None, title="Treap", fig_width=7, fig_height=6):
    highlight_keys = set(highlight_keys or [])
    positions = compute_positions(root)
    # create a figure
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_facecolor("white")

    if not positions:
        ax.text(0.5, 0.5, "Treap is empty", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    # draw edges (arrows)
    for node, (x, y) in positions.items():
        if node.left and node.left in positions:
            x2, y2 = positions[node.left]
            ax.add_patch(FancyArrowPatch((x, y - 0.45), (x2, y2 + 0.45),
                                         arrowstyle='-|>', mutation_scale=10, lw=1.0, color='gray'))
        if node.right and node.right in positions:
            x2, y2 = positions[node.right]
            ax.add_patch(FancyArrowPatch((x, y - 0.45), (x2, y2 + 0.45),
                                         arrowstyle='-|>', mutation_scale=10, lw=1.0, color='gray'))

    # draw nodes
    node_radius = 0.45
    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]

    for node, (x, y) in positions.items():
        is_high = node.key in highlight_keys
        face = "#FFD54F" if is_high else "#BDE6F2"
        edge = "#FF8A65" if is_high else "black"
        circ = Circle((x, y), node_radius, facecolor=face, edgecolor=edge, lw=1.6, zorder=3)
        ax.add_patch(circ)
        ax.text(x, y + 0.12, f"{node.key}", ha='center', va='center', fontsize=12, fontweight='bold', zorder=4)
        ax.text(x, y - 0.12, f"(p={node.priority:.2f})", ha='center', va='center', fontsize=8, zorder=4)

    ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, pad=10)
    ax.axis('off')
    # adjust limits
    if xs and ys:
        ax.set_xlim(min(xs) - 1.5, max(xs) + 1.5)
        ax.set_ylim(min(ys) - 1.5, max(ys) + 1.5)
    return fig

# ----------------------------
# Utilities to make node table and traversal
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
    # sort by key for table clarity
    rows_sorted = sorted(rows, key=lambda r: r["key"])
    return rows_sorted

# ----------------------------
# Streamlit UI entrypoint
# ----------------------------
def main():
    st.set_page_config(page_title="Treap Visualizer", layout="wide")
    st.title("🌳 Treap Visualizer (TP2)")

    # initialize session state
    if "treap_obj" not in st.session_state:
        st.session_state.treap_obj = Treap("max")
    if "treap_logs" not in st.session_state:
        st.session_state.treap_logs = ["Treap initialized."]
    if "treap_highlight" not in st.session_state:
        st.session_state.treap_highlight = set()

    treap: Treap = st.session_state.treap_obj

    # layout: operations / visualization
    left, right = st.columns([1.0, 1.6])

    with left:
        st.subheader("⚙️ Operations")
        # single insert
        with st.expander("Insert single key", expanded=True):
            colk, colp = st.columns([1, 1])
            with colk:
                ins_key = st.number_input("Key (int)", value=0, step=1, key="treap_ins_key")
            with colp:
                ins_priority = st.text_input("Priority (leave blank for random)", value="", key="treap_ins_pr")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Insert", use_container_width=True):
                    try:
                        p = None if ins_priority.strip() == "" else float(ins_priority)
                        logs = treap.insert(int(ins_key), p)
                        st.session_state.treap_logs.extend(logs)
                        st.session_state.treap_highlight = {int(ins_key)}
                    except Exception as e:
                        st.error(f"Insert error: {e}")
            with col2:
                if st.button("🗑️ Delete", use_container_width=True):
                    logs = treap.delete(int(ins_key))
                    st.session_state.treap_logs.extend(logs)
                    st.session_state.treap_highlight = set()

        # bulk insert
        with st.expander("Insert bulk (comma or space separated)", expanded=False):
            bulk_input = st.text_area("Enter keys (e.g. 10 5 20 or 10,5,20):", "10 5 15 3 7")
            bulk_priority = st.text_input("Optional priority for all (blank = random):", value="", key="treap_bulk_pr")
            if st.button("➕ Insert Bulk", use_container_width=True):
                tokens = []
                raw = bulk_input.replace(",", " ").split()
                for t in raw:
                    try:
                        tokens.append(int(t))
                    except:
                        st.warning(f"Ignored token: {t}")
                for k in tokens:
                    p = None if bulk_priority.strip() == "" else float(bulk_priority)
                    logs = treap.insert(int(k), p)
                    st.session_state.treap_logs.extend(logs)
                st.session_state.treap_highlight = set(tokens)

        # search
        with st.expander("Search", expanded=False):
            s_key = st.number_input("Search key", value=0, step=1, key="treap_search_key")
            if st.button("🔍 Search", use_container_width=True):
                found = treap.find(treap.root, int(s_key))
                if found:
                    st.session_state.treap_logs.append(f"🔎 Found {found.key}/{found.priority:.2f}")
                    st.session_state.treap_highlight = {int(s_key)}
                    st.success(f"Found: {found.key} (priority {found.priority:.2f})")
                else:
                    st.session_state.treap_logs.append(f"🔎 {s_key} not found")
                    st.session_state.treap_highlight = set()
                    st.warning(f"{s_key} not found.")

        # reset
        if st.button("🔁 Reset Treap", use_container_width=True):
            st.session_state.treap_obj = Treap("max")
            st.session_state.treap_logs = ["Treap reset."]
            st.session_state.treap_highlight = set()

        st.markdown("---")
        # traversals
        st.subheader("🔄 Traversals")
        inord = treap.inorder(treap.root)
        preord = treap.preorder(treap.root)
        postord = treap.postorder(treap.root)
        st.write("**In-order:**", inord)
        st.write("**Pre-order:**", preord)
        st.write("**Post-order:**", postord)

        st.markdown("---")
        # logs (show recent)
        st.subheader("📜 Logs (recent)")
        logs_to_show = st.session_state.treap_logs[-30:]
        for ln in logs_to_show:
            st.write(ln)

    # visualization and table on the right
    with right:
        st.subheader("🖼️ Treap Structure")
        fig = draw_treap(treap.root, highlight_keys=st.session_state.treap_highlight, title="Treap (key / priority)")
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("📊 Nodes Table")
        rows = collect_nodes(treap.root)
        if rows:
            df = pd.DataFrame(rows)
            df = df[["key", "priority", "left", "right"]]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No nodes yet — insert some keys to populate the table.")

    # footer controls: clear highlight
    st.markdown("---")
    colc1, colc2 = st.columns([1, 3])
    with colc1:
        if st.button("Clear Highlight"):
            st.session_state.treap_highlight = set()
    with colc2:
        st.caption("Tip: use bulk insert to quickly create a treap. Priorities are random unless specified.")

# Allow running module directly for debugging
if __name__ == "__main__":
    main()
