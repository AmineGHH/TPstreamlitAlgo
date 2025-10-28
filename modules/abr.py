import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, value): """constructeur"""
        self.value = value
        self.left = None """none cuz mzl m3ndhch children"""
        self.right = None
        self.height = 1

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    else:
        st.warning(f"La valeur {value} existe déjà dans l'arbre.")
    return root

def find_min(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete(root, value):
    """Supprime une valeur de l'arbre."""
    if root is None:
        return root

    if value < root.value:
        root.left = delete(root.left, value)
    elif value > root.value:
        root.right = delete(root.right, value)
    else:
        # Cas : nœud trouvé
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp

        # Cas : deux enfants
        temp = find_min(root.right)
        root.value = temp.value
        root.right = delete(root.right, temp.value)

    return root

def search(root, value):
    if root is None or root.value == value:
        return root
    if value < root.value:
        return search(root.left, value)
    return search(root.right, value)

def get_height(node):
    """Calcule la hauteur de l'arbre."""
    if node is None:
        return 0
    return 1 + max(get_height(node.left), get_height(node.right))

def get_size(node):
    """nombre de nœuds"""
    if node is None:
        return 0
    return 1 + get_size(node.left) + get_size(node.right)

def is_balanced(node):
    """Vérifie si l'arbre est équilibré."""
    if node is None:
        return True
    
    left_height = get_height(node.left)
    right_height = get_height(node.right)
    
    if abs(left_height - right_height) <= 1 and is_balanced(node.left) and is_balanced(node.right):
        return True
    return False

def inorder_traversal(node, result=None):
    """Parcours in-ordre de l'arbre."""
    if result is None:
        result = []
    if node:
        inorder_traversal(node.left, result)
        result.append(node.value)
        inorder_traversal(node.right, result)
    return result

def preorder_traversal(node, result=None):
    """Parcours pré-ordre de l'arbre."""
    if result is None:
        result = []
    if node:
        result.append(node.value)
        preorder_traversal(node.left, result)
        preorder_traversal(node.right, result)
    return result

def postorder_traversal(node, result=None):
    """Parcours post-ordre de l'arbre."""
    if result is None:
        result = []
    if node:
        postorder_traversal(node.left, result)
        postorder_traversal(node.right, result)
        result.append(node.value)
    return result

def build_graph(G, node, pos, x=0, y=0, layer=1):
    """Construit le graphe pour la visualisation."""
    if node is None:
        return
    G.add_node(node.value)
    pos[node.value] = (x, y)
    if node.left:
        G.add_edge(node.value, node.left.value)
        build_graph(G, node.left, pos, x - 1 / layer, y - 1, layer + 1)
    if node.right:
        G.add_edge(node.value, node.right.value)
        build_graph(G, node.right, pos, x + 1 / layer, y - 1, layer + 1)

def visualize_tree(root, title="Arbre Binaire de Recherche", color='lightblue'):
    """Visualise l'arbre avec matplotlib."""
    if root is None:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "L'arbre est vide", ha='center', va='center', fontsize=14)
        ax.axis('off')
        return fig
    
    G = nx.DiGraph()
    pos = {}
    build_graph(G, root, pos, x=0, y=0, layer=1)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color=color, 
            node_size=800, font_weight='bold', arrows=False, ax=ax)
    ax.set_title(title, fontsize=16, pad=20)
    ax.axis('off')
    plt.tight_layout()
    return fig

def show_abr_page():
    st.title("🌳 Arbre Binaire de Recherche (ABR)")
    st.markdown("Visualisez et manipulez des arbres binaires de recherche")
    
    # Initialize session state
    if "abr_state" not in st.session_state:
        st.session_state.abr_state = {
            "root": None,
            "history": []
        }
    
    state = st.session_state.abr_state
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🛠️ Opérations")
        
        # Tree creation
        with st.container(border=True):
            st.write("**🌱 Créer l'arbre**")
            values_input = st.text_input(
                "Valeurs initiales (séparées par des espaces):",
                "10 5 15 3 7 12 20",
                help="Exemple: 10 5 15 3 7 12 20"
            )
            
            if st.button("🌳 Construire l'arbre", use_container_width=True):
                try:
                    values = list(map(int, values_input.split()))
                    root = None
                    for v in values:
                        root = insert(root, v)
                    state["root"] = root
                    state["history"].append(f"Arbre créé avec les valeurs: {values}")
                    st.success(f"Arbre créé avec {len(values)} valeurs!")
                    st.rerun()
                except ValueError:
                    st.error("Veuillez entrer uniquement des nombres entiers séparés par des espaces.")
        
        # Tree operations
        with st.container(border=True):
            st.write("**✏️ Modifier l'arbre**")
            operation = st.radio("Opération:", ["Insérer", "Supprimer", "Rechercher"])
            value_input = st.number_input("Valeur:", value=0, step=1)
            
            if st.button("🔧 Exécuter", use_container_width=True):
                if state["root"] is None and operation != "Insérer":
                    st.warning("L'arbre est vide! Veuillez d'abord créer un arbre.")
                else:
                    if operation == "Insérer":
                        state["root"] = insert(state["root"], value_input)
                        state["history"].append(f"Valeur {value_input} insérée")
                        st.success(f"Valeur {value_input} insérée avec succès!")
                    
                    elif operation == "Supprimer":
                        if search(state["root"], value_input) is None:
                            st.warning(f"La valeur {value_input} n'existe pas dans l'arbre.")
                        else:
                            state["root"] = delete(state["root"], value_input)
                            state["history"].append(f"Valeur {value_input} supprimée")
                            st.success(f"Valeur {value_input} supprimée avec succès!")
                    
                    elif operation == "Rechercher":
                        node = search(state["root"], value_input)
                        if node:
                            st.success(f"✅ La valeur {value_input} existe dans l'arbre.")
                        else:
                            st.warning(f"❌ La valeur {value_input} n'existe pas dans l'arbre.")
                    st.rerun()
        
        # Reset button
        if st.button("🔄 Réinitialiser", use_container_width=True):
            state["root"] = None
            state["history"] = []
            st.rerun()
        
        # Operation history
        if state["history"]:
            st.subheader("📖 Historique")
            with st.container(border=True):
                for i, action in enumerate(reversed(state["history"][-10:])):
                    st.write(f"• {action}")
    
    with col2:
        st.subheader("📊 Visualisation")
        
        root = state["root"]
        
        if root:
            # Visualization
            fig = visualize_tree(root, "Arbre Binaire de Recherche", 'lightblue')
            st.pyplot(fig)
            
            # Tree information
            st.subheader("ℹ️ Informations sur l'arbre")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Hauteur", get_height(root))
            with col_info2:
                st.metric("Taille", get_size(root))
            with col_info3:
                balanced = "✅ Oui" if is_balanced(root) else "❌ Non"
                st.metric("Équilibré", balanced)
            
            # Traversals
            st.subheader("🔄 Parcours")
            trav_col1, trav_col2, trav_col3 = st.columns(3)
            with trav_col1:
                st.write("**In-ordre**")
                st.code(str(inorder_traversal(root)))
            with trav_col2:
                st.write("**Pré-ordre**")
                st.code(str(preorder_traversal(root)))
            with trav_col3:
                st.write("**Post-ordre**")
                st.code(str(postorder_traversal(root)))
            
        else:
            st.info("🌱 L'arbre est vide. Créez un arbre pour commencer!")
            st.markdown("""
            **Comment utiliser:**
            1. Entrez des valeurs initiales séparées par des espaces
            2. Cliquez sur 'Construire l'arbre'
            3. Utilisez les opérations pour modifier l'arbre
            4. Visualisez les résultats en temps réel
            """)

if __name__ == "__main__":
    show_abr_page()
