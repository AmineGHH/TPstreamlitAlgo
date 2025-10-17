import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math


# ----------------------------
# Helper: draw heap as a tree
# ----------------------------
def draw_heap_tree(heap, is_max=False):
    if not heap:
        st.warning("Heap is empty.")
        return

    values = [-x for x in heap] if is_max else heap
    G = nx.DiGraph()
    for i, val in enumerate(values):
        G.add_node(i, label=str(val))
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(values):
            G.add_edge(i, left)
        if right < len(values):
            G.add_edge(i, right)

    pos = hierarchy_pos(G, 0)
    labels = nx.get_node_attributes(G, "label")
    fig, ax = plt.subplots(figsize=(8, 5))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=800,
            node_color="lightblue", font_size=10, font_weight="bold", arrows=False, ax=ax)
    st.pyplot(fig)


# ----------------------------
# Helper: recursive layout
# ----------------------------
def hierarchy_pos(G, root, width=1., vert_gap=0.3, vert_loc=0, xcenter=0.5):
    pos = {root: (xcenter, vert_loc)}
    children = list(G.successors(root))
    if not children:
        return pos
    dx = width / len(children)
    nextx = xcenter - width / 2 - dx / 2
    for child in children:
        nextx += dx
        pos.update(
            hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                          vert_loc=vert_loc - vert_gap, xcenter=nextx)
        )
    return pos


# ----------------------------
# Helper: heap properties
# ----------------------------
def get_heap_properties(heap):
    return {
        "Number of Nodes": len(heap),
        "Height": math.floor(math.log2(len(heap))) + 1 if heap else 0,
        "Root Value": (-heap[0] if st.session_state.is_max else heap[0]) if heap else "N/A",
    }


# ----------------------------
# Main Streamlit UI
# ----------------------------
def show_heap_page():
    st.title("🧱 Heap Tree Visualizer (Min / Max Heap)")
    st.markdown("Interactively build, visualize, and modify Min or Max Heaps.")

    if "heap" not in st.session_state:
        st.session_state.heap = []
    if "is_max" not in st.session_state:
        st.session_state.is_max = False
    if "logs" not in st.session_state:
        st.session_state.logs = []

    # ---- Heap type ----
    st.subheader("1️⃣ Choose Heap Type")
    heap_type = st.radio("Select type:", ["Min Heap", "Max Heap"], horizontal=True)
    st.session_state.is_max = (heap_type == "Max Heap")

    # ---- Heap creation ----
    st.subheader("2️⃣ Create Heap")
    user_input = st.text_input("Enter space-separated values (e.g. 5 1 9 3):", "")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create / Rebuild Heap"):
            if user_input.strip() == "":
                st.session_state.heap = []
                st.session_state.logs.append("Created empty heap.")
            else:
                try:
                    numbers = list(map(int, user_input.split()))
                    if st.session_state.is_max:
                        st.session_state.heap = [-x for x in numbers]
                        heapq.heapify(st.session_state.heap)
                    else:
                        st.session_state.heap = numbers
                        heapq.heapify(st.session_state.heap)
                    st.session_state.logs.append(
                        f"Created {'Max' if st.session_state.is_max else 'Min'} Heap from values: {numbers}"
                    )
                except ValueError:
                    st.error("Please enter valid integers.")
    with col2:
        if st.button("Reset Tree"):
            st.session_state.heap = []
            st.session_state.logs.append("Heap reset to empty.")
            st.rerun()

    st.divider()

    # ---- Display Section ----
    if st.session_state.heap:
        left, right = st.columns([2, 1])

        with left:
            st.subheader("📊 Heap Visualization")
            draw_heap_tree(st.session_state.heap, st.session_state.is_max)

        with right:
            st.subheader("ℹ️ Heap Properties")
            props = get_heap_properties(st.session_state.heap)
            for k, v in props.items():
                st.write(f"**{k}:** {v}")

            st.markdown("---")

            # --- Insert and Delete controls ---
            insert_val = st.text_input("Enter value to insert:", key="insert_box")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Insert"):
                    if insert_val:
                        try:
                            val = int(insert_val)
                            heapq.heappush(
                                st.session_state.heap,
                                -val if st.session_state.is_max else val
                            )
                            st.session_state.logs.append(f"Inserted {val} into heap.")
                            st.rerun()
                        except ValueError:
                            st.error("Please enter a valid integer.")
                    else:
                        st.warning("Enter a value before inserting.")

            with c2:
                if st.button("Remove Root"):
                    if st.session_state.heap:
                        removed = -heapq.heappop(st.session_state.heap) if st.session_state.is_max else heapq.heappop(st.session_state.heap)
                        st.session_state.logs.append(f"Removed root value {removed}.")
                        st.rerun()
                    else:
                        st.warning("Heap is empty.")

        st.divider()

        # ---- Logs (collapsible) ----
        with st.expander("🧾 Operation Logs (Click to Expand)"):
            if st.session_state.logs:
                for log in reversed(st.session_state.logs[-20:]):
                    st.write(f"- {log}")
            else:
                st.info("No operations yet.")
    else:
        st.info("Heap is empty. Create one to begin!")


# For standalone testing
if __name__ == "__main__":
    show_heap_page()