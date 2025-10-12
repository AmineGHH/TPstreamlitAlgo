import streamlit as st
from modules.avl import AVLTree
from utils.visualizer import draw_graphviz_avl_bytes, draw_matplotlib_tree_fig

def run():
    st.header("AVL Tree — visualizer & editor")

    # initialize session state
    if "avl_tree" not in st.session_state:
        st.session_state.avl_tree = AVLTree()
        st.session_state.avl_root = None

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Edit")
        action = st.selectbox("Action", ["Insert", "Delete", "Bulk insert", "Reset"])
        value_input = st.text_input("Value (single int) or list (space/comma separated)", "")
        if st.button("Apply"):
            if action == "Reset":
                st.session_state.avl_root = None
            elif action == "Insert":
                try:
                    v = int(value_input.strip())
                    st.session_state.avl_root = st.session_state.avl_tree.insert(st.session_state.avl_root, v)
                except:
                    st.error("Enter a single integer for Insert.")
            elif action == "Delete":
                try:
                    v = int(value_input.strip())
                    st.session_state.avl_root = st.session_state.avl_tree.delete(st.session_state.avl_root, v)
                except:
                    st.error("Enter a single integer for Delete.")
            elif action == "Bulk insert":
                # parse "1 2 3" or "1,2,3"
                text = value_input.replace(",", " ").strip()
                if text == "":
                    st.error("Provide values for bulk insert.")
                else:
                    nums = []
                    for tok in text.split():
                        try:
                            nums.append(int(tok))
                        except:
                            st.warning(f"Ignored non-int token: {tok}")
                    for n in nums:
                        st.session_state.avl_root = st.session_state.avl_tree.insert(st.session_state.avl_root, n)

    with col2:
        st.subheader("Visualization")
        root = st.session_state.avl_root
        if root is None:
            st.info("Tree is empty. Insert nodes to see visualization.")
        else:
            # try graphviz first
            png = draw_graphviz_avl_bytes(root, st.session_state.avl_tree)
            if png:
                st.image(png, use_column_width=True)
            else:
                fig = draw_matplotlib_tree_fig(root, st.session_state.avl_tree)
                st.pyplot(fig)

       # properties and traversals
    st.subheader("Properties")
    root = st.session_state.avl_root
    t = st.session_state.avl_tree
    if root:
        st.write("Height:", t.get_height(root))
        st.write("Number of nodes:", t.node_count(root))
        unbal = t.find_unbalanced_nodes(root)
        if unbal:
            st.warning("Unbalanced nodes (key, bf): " + str(unbal))
        else:
            st.success("All nodes balanced (|bf| ≤ 1).")

        st.subheader("Traversals")

        inorder = t.inorder(root)
        preorder = t.preorder(root)
        postorder = t.postorder(root)

        st.write("**Inorder:**", f"[{', '.join(map(str, inorder))}]")
        st.write("**Preorder:**", f"[{', '.join(map(str, preorder))}]")
        st.write("**Postorder:**", f"[{', '.join(map(str, postorder))}]")
    else:
        st.info("Tree is empty.")
