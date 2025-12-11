import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
import time
import math
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Algorithme de Welsh-Powell",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

class WelshPowell:
    """Implémentation de l'algorithme de Welsh-Powell pour la coloration de graphes"""
    
    def __init__(self, graph: Dict[str, List[str]]):
        self.graph = graph
        self.vertices = list(graph.keys())
        self.operations_count = {
            "comparaisons": 0,
            "affectations": 0,
            "acces_memoire": 0,
            "operations_total": 0,
            "boucles": 0,
            "conditionnelles": 0
        }
        
    def calculate_degrees(self) -> Dict[str, int]:
        """Calcule les degrés avec comptage d'opérations"""
        degrees = {}
        for vertex, neighbors in self.graph.items():
            degrees[vertex] = len(neighbors)
            self.operations_count["affectations"] += 1
            self.operations_count["acces_memoire"] += len(neighbors) + 1
            self.operations_count["boucles"] += 1
        return degrees
    
    def sort_vertices_by_degree(self) -> List[Tuple[str, int]]:
        """Trie les sommets par degré décroissant avec comptage d'opérations"""
        degrees = self.calculate_degrees()
        sorted_vertices = sorted(degrees.items(), key=lambda x: (-x[1], x[0]))
        
        # Opérations de tri: O(n log n) comparaisons
        n = len(degrees)
        self.operations_count["comparaisons"] += n * math.ceil(math.log2(n + 1)) if n > 0 else 0
        self.operations_count["affectations"] += n * math.ceil(math.log2(n + 1)) if n > 0 else 0
        self.operations_count["boucles"] += 1
        
        return sorted_vertices
    
    def welsh_powell_coloring(self, color_names: List[str]) -> Dict:
        """Implémente l'algorithme avec analyse de complexité détaillée"""
        start_time = time.time()
        
        sorted_vertices = self.sort_vertices_by_degree()
        vertices_order = [v[0] for v in sorted_vertices]
        degrees = {v[0]: v[1] for v in sorted_vertices}
        
        n = len(vertices_order)
        colors = {}
        color_usage = defaultdict(list)
        execution_steps = []
        current_color = 0
        iteration_count = 0
        
        # Étape initiale
        execution_steps.append({
            "step": 0,
            "description": "Initialisation - Tri des sommets par degré décroissant",
            "vertices_order": vertices_order.copy(),
            "degrees": degrees.copy(),
            "colors": {},
            "current_color": None,
            "operations": self.operations_count.copy(),
            "iteration": iteration_count
        })
        
        # Boucle principale - Complexité O(n²) dans le pire cas
        while len(colors) < len(vertices_order) and current_color < len(color_names):
            iteration_count += 1
            step_colors = colors.copy()
            assigned_vertices = []
            
            # Pour chaque sommet non coloré - O(n)
            for vertex in vertices_order:
                self.operations_count["boucles"] += 1
                if vertex in colors:
                    self.operations_count["comparaisons"] += 1
                    self.operations_count["conditionnelles"] += 1
                    continue
                
                # Vérifier les conflits - O(n) dans le pire cas
                conflict = False
                for colored_vertex in color_usage[current_color]:
                    self.operations_count["boucles"] += 1
                    self.operations_count["comparaisons"] += 1
                    self.operations_count["acces_memoire"] += 2
                    self.operations_count["conditionnelles"] += 1
                    if vertex in self.graph[colored_vertex] or colored_vertex in self.graph[vertex]:
                        conflict = True
                        self.operations_count["conditionnelles"] += 1
                        break
                
                if not conflict:
                    self.operations_count["conditionnelles"] += 1
                    colors[vertex] = current_color
                    color_usage[current_color].append(vertex)
                    assigned_vertices.append(vertex)
                    step_colors[vertex] = current_color
                    self.operations_count["affectations"] += 3
            
            execution_steps.append({
                "step": current_color + 1,
                "description": f"Attribution de la couleur {color_names[current_color]}",
                "vertices_order": vertices_order.copy(),
                "degrees": degrees.copy(),
                "colors": step_colors.copy(),
                "current_color": current_color,
                "assigned_vertices": assigned_vertices.copy(),
                "color_name": color_names[current_color],
                "operations": self.operations_count.copy(),
                "iteration": iteration_count
            })
            
            current_color += 1
            self.operations_count["affectations"] += 1
        
        execution_time = time.time() - start_time
        
        # Calcul des métriques finales
        self.operations_count["operations_total"] = (
            self.operations_count["comparaisons"] + 
            self.operations_count["affectations"] + 
            self.operations_count["acces_memoire"]
        )
        
        return {
            "final_colors": colors,
            "execution_steps": execution_steps,
            "chromatic_number": len(set(colors.values())),
            "color_names": color_names,
            "execution_time": execution_time,
            "operations_count": self.operations_count
        }

def create_default_graph():
    """Crée le graphe par défaut de l'exemple"""
    return {
        'A': ['B', 'D', 'E', 'G'],
        'B': ['A', 'C', 'D', 'H'],
        'C': ['B', 'F', 'H'],
        'D': ['A', 'B', 'E', 'G'],
        'E': ['A', 'D', 'F', 'G'],
        'F': ['C', 'E', 'H'],
        'G': ['A', 'D', 'E', 'H'],
        'H': ['B', 'C', 'F', 'G']
    }

def adjacency_matrix_to_graph(matrix_str: str) -> Dict[str, List[str]]:
    """
    Convertit une matrice d'adjacence en format graphe
    
    Args:
        matrix_str: Chaîne représentant la matrice (CSV ou ligne par ligne)
        
    Returns:
        Dictionnaire représentant le graphe
    """
    # Nettoyer et parser la matrice
    lines = [line.strip() for line in matrix_str.strip().split('\n') if line.strip()]
    
    # Convertir en matrice numérique
    matrix = []
    for line in lines:
        row = []
        # Essayer différents séparateurs
        if ',' in line:
            elements = line.split(',')
        elif ';' in line:
            elements = line.split(';')
        elif '\t' in line:
            elements = line.split('\t')
        else:
            elements = line.split()
        
        for val in elements:
            val = val.strip()
            if val:  # Ignorer les valeurs vides
                try:
                    row.append(int(val))
                except ValueError:
                    st.error(f"Valeur invalide dans la matrice: '{val}'. Utilisez uniquement 0 et 1.")
                    return {}
        
        if row:
            matrix.append(row)
    
    # Vérifier que la matrice est carrée
    n = len(matrix)
    for i, row in enumerate(matrix):
        if len(row) != n:
            st.error(f"La matrice n'est pas carrée. Ligne {i+1} a {len(row)} éléments, attendu {n}")
            return {}
    
    # Vérifier que la matrice contient seulement 0 et 1
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val not in [0, 1]:
                st.error(f"Valeur invalide à la position ({i+1},{j+1}): {val}. Utilisez uniquement 0 et 1.")
                return {}
    
    # Vérifier que la matrice est symétrique (graphe non orienté)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                st.warning(f"Attention: La matrice n'est pas symétrique à la position ({i+1},{j+1}). Le graphe sera traité comme non-orienté.")
    
    # Générer des noms de sommets automatiquement
    vertex_names = []
    for i in range(n):
        if i < 26:
            vertex_names.append(chr(65 + i))  # A, B, C, ...
        else:
            vertex_names.append(f'V{i+1}')
    
    # Construire le graphe
    graph = {}
    for i in range(n):
        vertex = vertex_names[i]
        neighbors = []
        for j in range(n):
            if matrix[i][j] == 1 and i != j:  # Pas de boucle sur soi-même
                neighbors.append(vertex_names[j])
        graph[vertex] = neighbors
    
    return graph

def plot_graph_interactive(graph, colors, color_names, title="Graphe coloré"):
    """Crée une visualisation interactive du graphe avec Plotly"""
    G = nx.Graph()
    
    # Ajouter les sommets et arêtes
    for vertex, neighbors in graph.items():
        G.add_node(vertex)
        for neighbor in neighbors:
            if neighbor not in G.nodes():
                G.add_node(neighbor)
            if not G.has_edge(vertex, neighbor):
                G.add_edge(vertex, neighbor)
    
    # Disposition du graphe - utilisation d'une disposition circulaire
    pos = nx.circular_layout(G)
    
    # Couleurs pour les sommets
    color_palette = ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2', '#7209B7', '#F72585', '#3A86FF']
    
    # Préparer les données pour Plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    
    # Couleurs des nœuds
    node_color_indices = [colors.get(node, -1) for node in G.nodes()]
    node_colors = []
    for idx in node_color_indices:
        if idx == -1:
            node_colors.append('#CCCCCC')  # Gris pour non coloré
        else:
            node_colors.append(color_palette[idx % len(color_palette)])
    
    node_text = [f"{node}<br>Degré: {len(graph.get(node, []))}<br>Couleur: {color_names[colors.get(node, -1)] if colors.get(node, -1) != -1 else 'Non coloré'}" 
                 for node in G.nodes()]
    
    # Créer la figure
    fig = go.Figure()
    
    # Ajouter les arêtes
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines',
        showlegend=False
    ))
    
    # Ajouter les sommets
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=list(G.nodes()),
        textposition="middle center",
        marker=dict(
            size=40,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        textfont=dict(color='white', size=14, family="Arial Black"),
        hovertemplate='<b>%{text}</b><br>%{hovertext}<extra></extra>',
        hovertext=node_text
    ))
    
    # Mise en forme
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=20, color='#2C3E50')
        ),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=20, r=20, t=50),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
        width=500,
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def display_adjacency_matrix(matrix: List[List[int]], vertex_names: List[str]):
    """Affiche une matrice d'adjacence stylisée"""
    df = pd.DataFrame(matrix, index=vertex_names, columns=vertex_names)
    
    # Style la DataFrame
    styled_df = df.style.applymap(
        lambda x: 'background-color: #4ECDC4' if x == 1 else 'background-color: white'
    ).format(lambda x: '1' if x == 1 else '0')
    
    st.dataframe(styled_df, use_container_width=True)

def display_color_table(step_data, color_names):
    """Affiche le tableau de coloration pour une étape donnée"""
    vertices_order = step_data["vertices_order"]
    degrees = step_data["degrees"]
    colors = step_data["colors"]
    current_color = step_data.get("current_color")
    
    # Créer un tableau stylisé avec Streamlit
    st.markdown(f"**Étape {step_data['step']}:** {step_data['description']}")
    
    # En-tête du tableau
    cols = st.columns(len(vertices_order) + 1)
    with cols[0]:
        st.markdown("**Sommet**")
    for i, vertex in enumerate(vertices_order):
        with cols[i + 1]:
            st.markdown(f"**{vertex}**")
    
    # Ligne des degrés
    cols = st.columns(len(vertices_order) + 1)
    with cols[0]:
        st.markdown("**Degré**")
    for i, vertex in enumerate(vertices_order):
        with cols[i + 1]:
            st.markdown(f"{degrees[vertex]}")
    
    # Lignes pour chaque couleur - seulement les couleurs utilisées jusqu'à présent
    max_color_used = max([colors.get(v, -1) for v in vertices_order]) + 1 if colors else 0
    
    for color_idx in range(min(max_color_used + 1, len(color_names))):
        cols = st.columns(len(vertices_order) + 1)
        with cols[0]:
            color_display_name = color_names[color_idx] if color_idx < len(color_names) else f"Couleur {color_idx+1}"
            st.markdown(f"**{color_display_name}**")
        
        for i, vertex in enumerate(vertices_order):
            with cols[i + 1]:
                if vertex in colors:
                    if colors[vertex] == color_idx:
                        if current_color == color_idx:
                            st.success("✓")  # Vert pour couleur actuelle assignée
                        else:
                            st.info("✓")     # Bleu pour couleur précédente assignée
                    else:
                        st.error("✗")        # Rouge pour conflit
                else:
                    if current_color == color_idx:
                        st.warning("•")      # Orange pour en cours d'évaluation
                    else:
                        st.write(" ")        # Vide pour non évalué

def display_priorities(vertices_order, degrees, colors, current_step):
    """Affiche les priorités des sommets à colorer"""
    st.subheader("🎯 Priorités des sommets")
    
    # Calculer la priorité pour chaque sommet non coloré
    priorities = []
    for vertex in vertices_order:
        if vertex not in colors:
            # Priorité = degré - nombre de voisins déjà colorés
            colored_neighbors = 0
            for neighbor in st.session_state.graph[vertex]:
                if neighbor in colors:
                    colored_neighbors += 1
            priority = degrees[vertex] - colored_neighbors
            priorities.append((vertex, degrees[vertex], priority))
    
    # Trier par priorité décroissante
    priorities.sort(key=lambda x: (-x[2], -x[1], x[0]))
    
    # Afficher le tableau des priorités
    if priorities:
        st.markdown("**Ordre de priorité pour la prochaine couleur:**")
        data = []
        for i, (vertex, degree, priority) in enumerate(priorities):
            data.append({
                "Rang": i+1,
                "Sommet": vertex,
                "Degré": degree,
                "Voisins colorés": degree - priority,
                "Priorité": priority
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Tous les sommets sont déjà colorés.")

def main():
    st.title("🎨 Algorithme de Welsh-Powell - Coloration de Graphes")
    st.markdown("""
    Cette application implémente l'algorithme de Welsh-Powell pour la coloration de graphes.
    L'algorithme permet de colorier les sommets d'un graphe de telle sorte qu'aucun sommet adjacent n'ait la même couleur.
    """)
    
    # Sidebar pour la configuration
    st.sidebar.header("Configuration du Graphe")
    
    # Choix du mode
    mode = st.sidebar.selectbox(
        "Mode d'entrée",
        ["Graphe par défaut", "Matrice d'adjacence"]
    )
    
    graph = {}
    
    if mode == "Graphe par défaut":
        graph = create_default_graph()
        st.sidebar.success("✅ Graphe d'exemple chargé (8 sommets)")
        
        # Afficher le graphe par défaut
        st.sidebar.subheader("Structure du graphe")
        for vertex, neighbors in graph.items():
            st.sidebar.write(f"**{vertex}**: {', '.join(neighbors)}")
    
    else:  # Matrice d'adjacence
        st.sidebar.subheader("Entrée par Matrice d'Adjacence")
        
        # Instructions
        st.sidebar.markdown("""
        **Format de la matrice :**
        - Entrez une matrice carrée de **0** et **1**
        - **0** : pas d'arête entre les sommets
        - **1** : arête entre les sommets
        - La matrice doit être symétrique (graphe non orienté)
        """)
        
        # Option 1: Matrice prédéfinie
        example_matrix = """0 1 0 1 0
1 0 1 0 1
0 1 0 1 0
1 0 1 0 1
0 1 0 1 0"""
        
        # Option 2: Entrée manuelle
        matrix_input = st.sidebar.text_area(
            "Matrice d'adjacence",
            value=example_matrix,
            height=150,
            help="Entrez une matrice carrée. Les sommets seront nommés automatiquement (A, B, C, ...)."
        )
        
        if matrix_input.strip():
            graph = adjacency_matrix_to_graph(matrix_input)
            
            if graph:
                st.sidebar.success(f"✅ Matrice chargée ({len(graph)} sommets)")
                
                # Afficher la matrice
                st.sidebar.subheader("Matrice d'adjacence")
                lines = [line.strip() for line in matrix_input.strip().split('\n') if line.strip()]
                matrix = []
                for line in lines:
                    row = []
                    # Essayer différents séparateurs
                    if ',' in line:
                        elements = line.split(',')
                    elif ';' in line:
                        elements = line.split(';')
                    elif '\t' in line:
                        elements = line.split('\t')
                    else:
                        elements = line.split()
                    
                    for val in elements:
                        val = val.strip()
                        if val:
                            try:
                                row.append(int(val))
                            except:
                                row.append(0)
                    if row:
                        matrix.append(row)
                
                if matrix and graph:
                    display_adjacency_matrix(matrix, list(graph.keys()))
    
    # Configuration des couleurs
    st.sidebar.header("Configuration des Couleurs")
    default_colors = ["Rouge", "Bleu", "Jaune", "Vert", "Orange", "Violet", "Rose", "Marron"]
    color_names = []
    
    for i, default_color in enumerate(default_colors):
        color_name = st.sidebar.text_input(
            f"Couleur {i+1}",
            value=default_color,
            key=f"color_{i}"
        )
        if color_name:
            color_names.append(color_name)
    
    # Vérifier que le graphe n'est pas vide
    if not graph:
        st.warning("⚠️ Veuillez définir un graphe dans la sidebar")
        return
    
    # Initialisation de l'algorithme
    if st.sidebar.button("🚀 Lancer l'algorithme", type="primary", use_container_width=True):
        with st.spinner("Exécution de l'algorithme de Welsh-Powell..."):
            wp = WelshPowell(graph)
            result = wp.welsh_powell_coloring(color_names)
            
            # Stocker le résultat dans la session
            st.session_state.result = result
            st.session_state.graph = graph
            st.session_state.current_step = 0
            st.session_state.color_names = color_names
        
        st.success("✅ Algorithme terminé !")
        st.rerun()
    
    # Affichage des résultats
    if hasattr(st.session_state, 'result'):
        result = st.session_state.result
        graph = st.session_state.graph
        color_names = st.session_state.color_names
        
        st.markdown("---")
        
        # Navigation entre les étapes
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("◀ Étape précédente", use_container_width=True):
                st.session_state.current_step = max(0, st.session_state.current_step - 1)
                st.rerun()
        with col2:
            current_step = st.session_state.current_step
            total_steps = len(result['execution_steps'])
            st.markdown(f"<h3 style='text-align: center; color: #2C3E50;'>Étape {current_step + 1}/{total_steps}</h3>", 
                       unsafe_allow_html=True)
        with col3:
            if st.button("Étape suivante ▶", use_container_width=True):
                st.session_state.current_step = min(len(result['execution_steps']) - 1, 
                                                  st.session_state.current_step + 1)
                st.rerun()
        
        # Barre de progression
        progress = (st.session_state.current_step + 1) / len(result['execution_steps'])
        st.progress(progress)
        
        # Affichage de l'étape courante
        current_step_data = result['execution_steps'][st.session_state.current_step]
        
        # Layout en deux colonnes - Tableau à gauche, Graphique à droite
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("📊 Tableau de Coloration")
            display_color_table(current_step_data, color_names)
            
            # Informations sur l'étape
            if st.session_state.current_step > 0:
                assigned = current_step_data.get('assigned_vertices', [])
                if assigned:
                    st.success(f"**Sommets colorés à cette étape:** {', '.join(assigned)}")
                else:
                    st.info("Aucun sommet coloré à cette étape (tous en conflit)")
        
        with col_right:
            st.subheader("🎨 Graphique du graphe")
            
            # Créer la visualisation pour l'étape courante
            fig = plot_graph_interactive(
                graph, 
                current_step_data['colors'], 
                color_names,
                title=f"Étape {st.session_state.current_step + 1} - {current_step_data['description']}"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Section des priorités en bas
        st.markdown("---")
        if st.session_state.current_step < len(result['execution_steps']) - 1:
            # Afficher les priorités seulement si ce n'est pas la dernière étape
            display_priorities(
                current_step_data["vertices_order"],
                current_step_data["degrees"],
                current_step_data["colors"],
                st.session_state.current_step
            )
        
        # Dernière étape seulement
        if st.session_state.current_step == len(result['execution_steps']) - 1:
            st.balloons()
            st.success("🎉 **Coloration terminée avec succès !**")
            
            # Statistiques de base
            st.subheader("📈 Statistiques de Base")
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            
            with col_stats1:
                st.metric("Sommets totaux", len(graph))
                st.metric("Temps d'exécution", f"{result['execution_time']:.6f} s")
            
            with col_stats2:
                st.metric("Couleurs utilisées", result['chromatic_number'])
                degrees = [len(neighbors) for neighbors in graph.values()]
                st.metric("Degré moyen", f"{np.mean(degrees):.2f}")
            
            with col_stats3:
                m = sum(len(neighbors) for neighbors in graph.values()) // 2
                st.metric("Arêtes totales", m)
                st.metric("Degré maximum", max(degrees))
            
            with col_stats4:
                n = len(graph)
                if n > 1:
                    density = (2*m)/(n*(n-1))
                    st.metric("Densité", f"{density:.3f}")
                efficiency = result['chromatic_number'] / max(degrees) if max(degrees) > 0 else 0
                st.metric("Efficacité (χ/Δ)", f"{efficiency:.2f}")
        
        # Bouton pour recommencer
        if st.button("🔄 Recommencer l'algorithme", use_container_width=True):
            for key in ['result', 'graph', 'current_step', 'color_names']:
                if hasattr(st.session_state, key):
                    delattr(st.session_state, key)
            st.rerun()
    
    else:
        # Affichage initial sans résultats
        st.info("👈 **Configurez le graphe dans la sidebar et cliquez sur 'Lancer l'algorithme' pour commencer**")

if __name__ == "__main__":
    main()