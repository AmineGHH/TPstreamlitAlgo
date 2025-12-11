import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import time
import re

st.set_page_config(page_title="Johnson Algorithm", page_icon="🗺️", layout="wide")

# --- Utils ---
def clean_node_name(name):
    return str(name).strip()

def create_default_graph():
    return {
        '0': [('1', 4), ('4', 1)],
        '1': [],
        '2': [('1', 7), ('3', -2)],
        '3': [('1', 1)],
        '4': [('3', -5)]
    }

def parse_adjacency_list(text):
    graph = {}
    lines = text.strip().split('\n')
    for line in lines:
        if ':' not in line:
            continue
        src, rest = line.split(':', 1)
        src = clean_node_name(src)
        graph[src] = []
        matches = re.findall(r'\(\s*([^,]+?)\s*,\s*([^\)]+?)\)', rest)
        for tgt, w in matches:
            graph[src].append((clean_node_name(tgt), int(w)))
    return graph

def plot_graph(graph, highlight_node=None):
    G = nx.DiGraph()
    for u, edges in graph.items():
        for v, w in edges:
            G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=42)
    node_colors = ['#FF6B6B' if n==highlight_node else '#4ECDC4' for n in G.nodes()]
    fig, ax = plt.subplots(figsize=(7,5))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, font_weight='bold', ax=ax)
    edge_labels = {(u,v): d['weight'] for u,v,d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='orange', ax=ax)
    return fig

# --- Johnson Algorithm ---
class Johnson:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = list(graph.keys())
        self.steps = []

    def add_step(self, desc, data):
        self.steps.append({'desc': desc, 'data': data.copy()})

    def bellman_ford(self, src):
        dist = {v: float('inf') for v in self.graph}
        dist[src] = 0
        edges = [(u,v,w) for u, lst in self.graph.items() for v,w in lst]
        n = len(self.graph)
        for i in range(n-1):
            for u,v,w in edges:
                if dist[u]+w < dist[v]:
                    dist[v] = dist[u]+w
            self.add_step(f"BF iteration {i+1}", dist)
        # check negative cycle
        for u,v,w in edges:
            if dist[u]+w < dist[v]:
                return None
        return dist

    def dijkstra(self, graph, src):
        import heapq
        dist = {v: float('inf') for v in graph}
        dist[src] = 0
        visited = set()
        heap = [(0, src)]
        while heap:
            d,u = heapq.heappop(heap)
            if u in visited: continue
            visited.add(u)
            for v,w in graph.get(u, []):
                if dist[u]+w < dist[v]:
                    dist[v] = dist[u]+w
                    heapq.heappush(heap, (dist[v], v))
            self.add_step(f"Dijkstra from {src}", dist)
        return dist

    def reweight_edges(self, h):
        new_graph = {}
        for u, lst in self.graph.items():
            new_graph[u] = []
            for v,w in lst:
                new_graph[u].append((v, w + h[u]-h[v]))
        return new_graph

    def run(self):
        # add extra source
        s = 'S'
        graph_s = self.graph.copy()
        graph_s[s] = [(v,0) for v in self.vertices]
        h = self.bellman_ford(s)
        if h is None:
            st.error("Graph contains negative cycle! Cannot run Johnson.")
            return None
        self.add_step("Reweighting edges", h)
        new_graph = self.reweight_edges(h)
        all_pairs = {}
        for v in self.vertices:
            d = self.dijkstra(new_graph, v)
            # convert back original weights
            for u in d:
                if d[u]<float('inf'):
                    d[u] = d[u] - h[v] + h[u]
            all_pairs[v] = d
        return all_pairs

# --- Streamlit App ---
def main():
    st.title("🗺️ Johnson Algorithm - All Pairs Shortest Paths")
    st.sidebar.header("Graph Input")

    input_type = st.sidebar.selectbox("Input type", ["Default graph", "Adjacency List"])
    if input_type=="Default graph":
        graph = create_default_graph()
        st.sidebar.write("Default graph loaded.")
    else:
        text = st.sidebar.text_area("Enter adjacency list", 
        "0: (1,4), (4,1)\n1: []\n2: (1,7), (3,-2)\n3: (1,1)\n4: (3,-5)")
        graph = parse_adjacency_list(text)

    st.subheader("Graph visualization")
    st.pyplot(plot_graph(graph))

    if st.button("Run Johnson Algorithm"):
        johnson = Johnson(graph)
        all_pairs = johnson.run()
        if all_pairs:
            st.success("Algorithm finished successfully!")
            st.subheader("Execution Steps")
            for step in johnson.steps:
                st.markdown(f"**{step['desc']}**")
                # convert all entries to strings to avoid PyArrow issues
                df_step = pd.DataFrame(step['data']).astype(str)
                st.dataframe(df_step, use_container_width=True)
            
            st.subheader("All pairs shortest distances")
            df_all = pd.DataFrame(all_pairs).astype(str)
            st.dataframe(df_all, use_container_width=True)

if __name__=="__main__":
    main()
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
import time
import math
import pandas as pd
import re

# Configuration de la page
st.set_page_config(
    page_title="Algorithme de Johnson",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def clean_node_name(name):
    """Nettoie un nom de sommet: enlève espaces, caractères invisibles, garde seulement alphanum + _-"""
    s = str(name).strip()
    return ''.join(c for c in s if c.isalnum() or c in '_-')

class JohnsonAlgorithm:
    """Implémentation de l'algorithme de Johnson pour les plus courts chemins entre toutes les paires"""
    
    def __init__(self, graph: Dict):
        # ✅ Nettoyer le graphe d'entrée: assurer que toutes les clés et cibles sont propres
        cleaned_graph = {}
        for k, v in graph.items():
            clean_k = clean_node_name(k)
            cleaned_graph[clean_k] = []
            for target, weight in v:
                clean_target = clean_node_name(target)
                cleaned_graph[clean_k].append((clean_target, weight))
        
        self.original_graph = cleaned_graph.copy()
        self.vertices = list(self.original_graph.keys())
        self.operations_count = {
            "comparaisons": 0,
            "affectations": 0,
            "acces_memoire": 0,
            "operations_total": 0,
            "boucles": 0,
            "conditionnelles": 0,
            "additions": 0,
        }
        self.execution_steps = []
        self.step_counter = 0
        
    def add_source_vertex(self) -> Dict:
        """Ajoute un sommet source nommé 'S' connecté à tous les autres sommets avec un poids de 0"""
        new_graph = self.original_graph.copy()
        source = 'S'
        new_graph[source] = []
        
        for vertex in self.vertices:
            new_graph[source].append((vertex, 0))
            self.operations_count["affectations"] += 2
            self.operations_count["acces_memoire"] += 1
            self.operations_count["boucles"] += 1
            
        self.source_vertex = source
        return new_graph
    
    def bellman_ford(self, graph: Dict, source: str) -> Tuple[Dict, bool, list]:
        """Exécute Bellman-Ford depuis le sommet source avec visualisation détaillée"""
        start_time = time.time()
        
        distances = {v: float('inf') for v in graph.keys()}
        distances[source] = 0
        self.operations_count["affectations"] += len(graph) + 1
        self.operations_count["boucles"] += 1
        
        all_edge_steps = []
        n = len(graph)
        graph_with_source = graph
        
        for i in range(n - 1):
            self.operations_count["boucles"] += 1
            updated = False
            
            for u in graph:
                if u not in distances:
                    continue
                for v, weight in graph[u]:
                    if v not in distances:
                        continue
                    
                    self.operations_count["boucles"] += 1
                    self.operations_count["acces_memoire"] += 3
                    self.operations_count["comparaisons"] += 1
                    
                    condition = f"d[{u}] + w({u},{v}) < d[{v}] → {distances[u]} + {weight} < {distances[v]}"
                    old_dist = distances[v]
                    new_dist = distances[u] + weight if distances[u] != float('inf') else float('inf')
                    relaxed = False
                    
                    if distances[u] != float('inf') and new_dist < distances[v]:
                        distances[v] = new_dist
                        updated = True
                        relaxed = True
                        self.operations_count["affectations"] += 1
                        self.operations_count["additions"] += 1
                        self.operations_count["conditionnelles"] += 1
                    
                    all_edge_steps.append({
                        "iteration": i + 1,
                        "edge": (u, v),
                        "weight": weight,
                        "old_distance": old_dist,
                        "new_distance": new_dist,
                        "relaxed": relaxed,
                        "condition": condition,
                        "distances": distances.copy()
                    })
            
            if not updated:
                break
        
        has_negative_cycle = False
        for u in graph:
            for v, weight in graph[u]:
                self.operations_count["boucles"] += 1
                self.operations_count["acces_memoire"] += 3
                self.operations_count["comparaisons"] += 1
                
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    has_negative_cycle = True
                    self.operations_count["conditionnelles"] += 1
                    break
            if has_negative_cycle:
                break
        
        execution_time = time.time() - start_time
        
        return distances, has_negative_cycle, all_edge_steps
    
    def reweight_edges(self, graph: Dict, h: Dict) -> Tuple[Dict, list]:
        """Répondre les poids des arêtes en utilisant les distances de Bellman-Ford"""
        reweighted_graph = {}
        reweighting_steps = []
        
        for u in graph:
            reweighted_graph[u] = []
            for v, weight in graph[u]:
                new_weight = weight + h[u] - h[v]
                reweighted_graph[u].append((v, new_weight))
                
                formula = f"w'({u},{v}) = w({u},{v}) + h[{u}] - h[{v}] → {weight} + {h[u]} - {h[v]} = {new_weight}"
                reweighting_steps.append({
                    "edge": (u, v),
                    "original_weight": weight,
                    "h_u": h[u],
                    "h_v": h[v],
                    "new_weight": new_weight,
                    "formula": formula
                })
                
                self.operations_count["affectations"] += 1
                self.operations_count["additions"] += 2
                self.operations_count["acces_memoire"] += 3
                self.operations_count["boucles"] += 1
        
        return reweighted_graph, reweighting_steps
    
    def dijkstra(self, graph: Dict, source) -> Dict:
        """Exécute Dijkstra pour trouver les plus courts chemins depuis le sommet source"""
        start_time = time.time()
        distances = {v: float('inf') for v in graph.keys()}
        distances[source] = 0
        visited = set()
        self.operations_count["affectations"] += len(graph) + 2
        self.operations_count["boucles"] += 1
        
        while len(visited) < len(graph):
            self.operations_count["boucles"] += 1
            min_dist = float('inf')
            current = None
            for v in graph:
                if v not in visited and distances[v] < min_dist:
                    min_dist = distances[v]
                    current = v
                    self.operations_count["comparaisons"] += 1
                    self.operations_count["conditionnelles"] += 1
            if current is None:
                break
            visited.add(current)
            self.operations_count["affectations"] += 1
            
            for neighbor, weight in graph[current]:
                self.operations_count["boucles"] += 1
                self.operations_count["acces_memoire"] += 3
                self.operations_count["comparaisons"] += 1
                if neighbor not in visited and distances[current] != float('inf'):
                    new_dist = distances[current] + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        self.operations_count["affectations"] += 1
                        self.operations_count["additions"] += 1
                        self.operations_count["conditionnelles"] += 1
        execution_time = time.time() - start_time
        return distances
    
    def johnson_all_pairs_shortest_paths(self) -> Dict:
        """Implémente l'algorithme de Johnson avec analyse détaillée"""
        start_time = time.time()
        self.execution_steps = []
        self.step_counter = 0
        
        self._add_step("Graphe original", {"graph": self.original_graph})
        
        graph_with_source = self.add_source_vertex()
        self._add_step("Ajout du sommet source 'S'", 
                      {"graph": graph_with_source, "source": self.source_vertex})
        
        h_distances, has_negative_cycle, all_edge_steps = self.bellman_ford(graph_with_source, self.source_vertex)
        if has_negative_cycle:
            self._add_step("Détection de cycle négatif", 
                          {"has_negative_cycle": True, "distances": h_distances})
            return {
                "error": "Le graphe contient un cycle négatif. L'algorithme de Johnson ne peut pas être appliqué.",
                "execution_steps": self.execution_steps,
                "operations_count": self.operations_count
            }
        
        self._add_step("Détails de Bellman-Ford", {
            "all_edge_steps": all_edge_steps,
            "final_distances": h_distances,
            "source": self.source_vertex,
            "graph_with_source": graph_with_source
        })
        
        reweighted_graph, reweighting_steps = self.reweight_edges(self.original_graph, h_distances)
        self._add_step("Détails du répondrement", {
            "reweighting_steps": reweighting_steps,
            "h_distances": h_distances,
            "reweighted_graph": reweighted_graph
        })
        
        all_pairs_distances = {}
        for source in self.vertices:
            dijkstra_distances = self.dijkstra(reweighted_graph, source)
            original_distances = {}
            for target in dijkstra_distances:
                if dijkstra_distances[target] != float('inf'):
                    original_distances[target] = dijkstra_distances[target] - h_distances[source] + h_distances[target]
                else:
                    original_distances[target] = float('inf')
            all_pairs_distances[source] = original_distances
            self._add_step(f"Dijkstra depuis le sommet {source}", 
                          {"source": source, "distances": original_distances})
        
        execution_time = time.time() - start_time
        self.operations_count["operations_total"] = (
            self.operations_count["comparaisons"] + 
            self.operations_count["affectations"] + 
            self.operations_count["acces_memoire"] +
            self.operations_count["additions"]
        )
        
        return {
            "all_pairs_distances": all_pairs_distances,
            "execution_steps": self.execution_steps,
            "execution_time": execution_time,
            "operations_count": self.operations_count,
            "h_distances": h_distances
        }

    def _add_step(self, description: str, data: Dict):
        self.step_counter += 1
        step_data = {
            "step": self.step_counter,
            "description": description,
            "data": data,
            "operations": self.operations_count.copy(),
            "timestamp": time.time()
        }
        self.execution_steps.append(step_data)

def create_default_graph():
    # ✅ Default graph: nodes 0 to 4 only (NO 5)
    return {
        '0': [('1', 4), ('4', 1)],
        '1': [],
        '2': [('1', 7), ('3', -2)],
        '3': [('1', 1)],
        '4': [('3', -5)]
    }

def adjacency_list_to_graph(adj_list_str: str) -> Dict:
    """Parser robuste — nettoie tous les noms de sommets"""
    graph = {}
    lines = [line.strip() for line in adj_list_str.strip().split('\n') if line.strip()]
    
    for line in lines:
        if ':' not in line:
            continue
        try:
            source_part, edges_part = line.split(':', 1)
            source = clean_node_name(source_part)
            graph[source] = []
            
            edges_part = edges_part.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
            
            # Find (target, weight) patterns
            matches = re.findall(r'\(\s*([^,]+?)\s*,\s*([^,\)]+?)\s*\)', edges_part)
            for target_str, weight_str in matches:
                target = clean_node_name(target_str)
                weight = int(weight_str.strip())
                graph[source].append((target, weight))
            
            # Fallback: simple space/comma split
            if not graph[source] and edges_part.strip() not in ('', '[]', '()', '{}'):
                parts = re.split(r'[,\s]+', edges_part.replace('(', '').replace(')', ''))
                clean_parts = [p.strip() for p in parts if p.strip()]
                if len(clean_parts) % 2 == 0:
                    for i in range(0, len(clean_parts), 2):
                        try:
                            target = clean_node_name(clean_parts[i])
                            weight = int(clean_parts[i+1])
                            graph[source].append((target, weight))
                        except:
                            pass
        except Exception as e:
            st.warning(f"⚠️ Ligne ignorée: {line}")
    
    return graph

def plot_graph_interactive(graph, title="", highlight_source=None, show_weights=True, node_labels=None):
    G = nx.DiGraph()
    for source, edges in graph.items():
        G.add_node(source)
        for target, weight in edges:
            G.add_node(target)
            G.add_edge(source, target, weight=weight)
    
    nodes = list(G.nodes())
    if 'S' in nodes:
        nodes.remove('S')
        nodes.append('S')
    pos = nx.circular_layout(G.subgraph(nodes))
    
    node_colors = []
    for node in G.nodes():
        if highlight_source is not None and node == highlight_source:
            node_colors.append('#FF6B6B')
        else:
            node_colors.append('#4ECDC4')
    
    fig, ax = plt.subplots(figsize=(8, 6))
    if title:
        ax.set_title(title, fontsize=16, fontweight='bold', color='#2C3E50')
    ax.set_facecolor('white')
    ax.axis('off')
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, edgecolors='white', linewidths=2, ax=ax)
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='#888', arrows=True, arrowsize=20, arrowstyle='->', connectionstyle='arc3,rad=0.0', ax=ax)
    
    labels_to_use = node_labels if node_labels else {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels_to_use, font_size=12, font_weight='bold', font_color='black', ax=ax)
    
    if show_weights:
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='orange', font_size=10, ax=ax)
    
    plt.tight_layout()
    return fig

def display_step_details(step_data, graph, color_names=None):
    description = step_data["description"]
    data = step_data["data"]
    
    st.markdown(f"### 📌 Étape {step_data['step']}: {description}")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        if "graph" in data:
            st.subheader("🔢 Matrice d'adjacence")
            vertices = sorted([v for v in data["graph"].keys() if v != 'S']) + (['S'] if 'S' in data["graph"] else [])
            matrix = []
            for i in vertices:
                row = []
                for j in vertices:
                    found = False
                    for neighbor, weight in data["graph"].get(i, []):
                        if neighbor == j:
                            row.append(weight)
                            found = True
                            break
                    if not found:
                        row.append(0)
                matrix.append(row)
            
            df = pd.DataFrame(matrix, index=vertices, columns=vertices)
            styled_df = df.style.applymap(
                lambda x: f'background-color: #4ECDC4; color: black' if x != 0 else 'background-color: white'
            ).format(lambda x: str(x) if x != 0 else '')
            st.dataframe(styled_df, use_container_width=True)
            
            ops = step_data["operations"]
            st.subheader("⚙️ Opérations effectuées")
            col_ops1, col_ops2, col_ops3 = st.columns(3)
            with col_ops1:
                st.metric("Comparaisons", ops["comparaisons"])
                st.metric("Affectations", ops["affectations"])
            with col_ops2:
                st.metric("Accès mémoire", ops["acces_memoire"])
                st.metric("Additions", ops["additions"])
            with col_ops3:
                st.metric("Boucles", ops["boucles"])
                st.metric("Conditionnelles", ops["conditionnelles"])

        elif "all_edge_steps" in data:
            st.subheader("📊 Détails de Bellman-Ford")
            st.markdown("### Examen de toutes les arêtes par itération")
            
            all_edge_steps = data["all_edge_steps"]
            final_distances = data["final_distances"]
            source = data["source"]
            graph_with_source = data["graph_with_source"]
            
            steps_by_iteration = defaultdict(list)
            for step in all_edge_steps:
                steps_by_iteration[step["iteration"]].append(step)
            
            for iteration in sorted(steps_by_iteration.keys()):
                with st.expander(f"🔄 Itération {iteration}", expanded=False):
                    st.markdown(f"**Arêtes examinées dans l'itération {iteration}:**")
                    for step in steps_by_iteration[iteration]:
                        edge_str = f"{step['edge'][0]} → {step['edge'][1]} (poids {step['weight']})"
                        status = "✅ Relâchée" if step["relaxed"] else "❌ Non relâchée"
                        dist_change = f"{step['old_distance']} → {step['new_distance']}" if step["relaxed"] else "Pas de changement"
                        st.markdown(f"- **{edge_str}** | {status} | {dist_change}")
                        st.markdown(f"  - Condition: `{step['condition']}`")
                    
                    st.markdown(f"**Distances après l'itération {iteration}:**")
                    vertices = sorted([v for v in final_distances.keys() if v != 'S']) + (['S'] if 'S' in final_distances else [])
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Sommets**")
                        for v in vertices:
                            st.write(f"**{v}**")
                    with col2:
                        st.markdown("**Distances**")
                        for v in vertices:
                            dist = step["distances"].get(v, float('inf'))
                            if dist == float('inf'):
                                st.write("∞")
                            else:
                                st.write(dist)
            
            st.subheader("📏 Distances finales h(v)")
            vertices = sorted([v for v in final_distances.keys() if v != 'S']) + (['S'] if 'S' in final_distances else [])
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Sommets**")
                for v in vertices:
                    st.write(f"**{v}**")
            with col2:
                st.markdown("**Distances h(v)**")
                for v in vertices:
                    dist = final_distances[v]
                    if dist == float('inf'):
                        st.write("∞")
                    else:
                        st.write(dist)
            
            st.subheader("📋 Tableau des distances par itération")
            iterations = max(step["iteration"] for step in all_edge_steps) if all_edge_steps else 0
            vertices = sorted([v for v in final_distances.keys() if v != 'S']) + (['S'] if 'S' in final_distances else [])
            
            df_data = []
            for i in range(iterations + 1):
                row = {"Itération": i}
                for v in vertices:
                    if i == 0:
                        dist = float('inf') if v != source else 0
                    else:
                        dist = float('inf')
                        for step in all_edge_steps:
                            if step["iteration"] <= i:
                                dist = step["distances"].get(v, float('inf'))
                    row[v] = "∞" if dist == float('inf') else str(dist)
                df_data.append(row)
            
            df = pd.DataFrame(df_data)
            styled_df = df.style.applymap(
                lambda x: 'background-color: #4ECDC4; color: black' if x != '∞' else 'background-color: white'
            )
            st.dataframe(styled_df, use_container_width=True)
            
            ops = step_data["operations"]
            st.subheader("⚙️ Opérations effectuées")
            col_ops1, col_ops2, col_ops3 = st.columns(3)
            with col_ops1:
                st.metric("Comparaisons", ops["comparaisons"])
                st.metric("Affectations", ops["affectations"])
            with col_ops2:
                st.metric("Accès mémoire", ops["acces_memoire"])
                st.metric("Additions", ops["additions"])
            with col_ops3:
                st.metric("Boucles", ops["boucles"])
                st.metric("Conditionnelles", ops["conditionnelles"])

        elif "reweighting_steps" in data:
            st.subheader("📊 Détails du répondrement des arêtes")
            st.markdown("### Formule de répondrement: `w'(u,v) = w(u,v) + h[u] - h[v]`")
            
            reweighting_steps = data["reweighting_steps"]
            h_distances = data["h_distances"]
            reweighted_graph = data["reweighted_graph"]
            
            st.markdown("#### Tableau des répondrements")
            df_data = []
            for step in reweighting_steps:
                df_data.append({
                    "Arête": f"{step['edge'][0]} → {step['edge'][1]}",
                    "Poids original": step['original_weight'],
                    "h[u]": step['h_u'],
                    "h[v]": step['h_v'],
                    "Nouveau poids": step['new_weight'],
                    "Formule": step['formula']
                })
            
            df = pd.DataFrame(df_data)
            styled_df = df.style.applymap(
                lambda x: 'background-color: #4ECDC4; color: black' if isinstance(x, (int, float)) or (isinstance(x, str) and x.isdigit()) else 'background-color: white'
            )
            st.dataframe(styled_df, use_container_width=True)
            
            ops = step_data["operations"]
            st.subheader("⚙️ Opérations effectuées")
            col_ops1, col_ops2, col_ops3 = st.columns(3)
            with col_ops1:
                st.metric("Comparaisons", ops["comparaisons"])
                st.metric("Affectations", ops["affectations"])
            with col_ops2:
                st.metric("Accès mémoire", ops["acces_memoire"])
                st.metric("Additions", ops["additions"])
            with col_ops3:
                st.metric("Boucles", ops["boucles"])
                st.metric("Conditionnelles", ops["conditionnelles"])

        elif "h_distances" in data:
            st.subheader("📏 Distances de Bellman-Ford (h(v))")
            h_distances = data["h_distances"]
            vertices = sorted([v for v in h_distances.keys() if v != 'S']) + (['S'] if 'S' in h_distances else [])
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Sommets**")
                for v in vertices:
                    st.write(f"**{v}**")
            with col2:
                st.markdown("**Distances h(v)**")
                for v in vertices:
                    dist = h_distances[v]
                    if dist == float('inf'):
                        st.write("∞")
                    else:
                        st.write(dist)
            
            ops = step_data["operations"]
            st.subheader("⚙️ Opérations effectuées")
            col_ops1, col_ops2, col_ops3 = st.columns(3)
            with col_ops1:
                st.metric("Comparaisons", ops["comparaisons"])
                st.metric("Affectations", ops["affectations"])
            with col_ops2:
                st.metric("Accès mémoire", ops["acces_memoire"])
                st.metric("Additions", ops["additions"])
            with col_ops3:
                st.metric("Boucles", ops["boucles"])
                st.metric("Conditionnelles", ops["conditionnelles"])

        elif "distances" in data and "source" in data:
            st.subheader(f"🏁 Résultats de Dijkstra depuis le sommet {data['source']}")
            distances = data["distances"]
            vertices = sorted(distances.keys())
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Sommets cibles**")
                for v in vertices:
                    st.write(f"**{v}**")
            with col2:
                st.markdown("**Distances**")
                for v in vertices:
                    dist = distances[v]
                    if dist == float('inf'):
                        st.write("∞")
                    else:
                        st.write(dist)
            
            ops = step_data["operations"]
            st.subheader("⚙️ Opérations effectuées")
            col_ops1, col_ops2, col_ops3 = st.columns(3)
            with col_ops1:
                st.metric("Comparaisons", ops["comparaisons"])
                st.metric("Affectations", ops["affectations"])
            with col_ops2:
                st.metric("Accès mémoire", ops["acces_memoire"])
                st.metric("Additions", ops["additions"])
            with col_ops3:
                st.metric("Boucles", ops["boucles"])
                st.metric("Conditionnelles", ops["conditionnelles"])

    with col_right:
        if "graph" in data:
            st.subheader("🎨 Visualisation du graphe")
            fig = plot_graph_interactive(data["graph"], title="", highlight_source=data.get("source"))
            st.pyplot(fig)
        
        elif "all_edge_steps" in data:
            if data["all_edge_steps"]:
                last_step = data["all_edge_steps"][-1]
                current_distances = last_step["distances"]
                node_labels = {}
                for node in data["graph_with_source"].keys():
                    dist = current_distances[node]
                    if dist == float('inf'):
                        node_labels[node] = f"{node}\n∞"
                    else:
                        node_labels[node] = f"{node}\n{dist}"
                
                st.subheader("🎨 Graphe final de Bellman-Ford")
                fig = plot_graph_interactive(
                    data["graph_with_source"], 
                    title="Graphe avec source S",
                    highlight_source=data["source"],
                    node_labels=node_labels
                )
                st.pyplot(fig)
            else:
                st.subheader("🎨 Graphe initial")
                fig = plot_graph_interactive(
                    data["graph_with_source"], 
                    title="Graphe avec source S",
                    highlight_source=data["source"]
                )
                st.pyplot(fig)
        
        elif "reweighting_steps" in data:
            st.subheader("🎨 Visualisation du graphe répondu")
            fig = plot_graph_interactive(data["reweighted_graph"], title="Graphe répondu")
            st.pyplot(fig)
        
        elif "distances" in data and "source" in data:
            st.subheader("🎨 Visualisation du graphe")
            fig = plot_graph_interactive(graph, title="", highlight_source=data["source"])
            st.pyplot(fig)

def main():
    st.title("🗺️ Algorithme de Johnson - Plus Courts Chemins entre Toutes les Paires")
    st.markdown("""
    Cette application implémente l'algorithme de Johnson pour trouver les plus courts chemins entre toutes les paires de sommets dans un graphe pondéré.
    L'algorithme fonctionne même avec des poids négatifs (mais pas de cycles négatifs).
    """)
    
    st.sidebar.header("Configuration du Graphe")
    mode = st.sidebar.selectbox("Mode d'entrée", ["Graphe par défaut", "Liste d'adjacence"])
    graph = {}
    
    if mode == "Graphe par défaut":
        graph = create_default_graph()
        st.sidebar.success("✅ Graphe d'exemple chargé (5 sommets)")
        st.sidebar.subheader("Structure du graphe")
        for vertex, edges in graph.items():
            edge_str = ", ".join([f"({target}, {weight})" for target, weight in edges])
            st.sidebar.write(f"**{vertex}**: {edge_str}")
    else:
        st.sidebar.subheader("Entrée par Liste d'Adjacence")
        st.sidebar.markdown("""
        **Format libre** — exemples valides :
        - `0: (1,4), (4,1)`
        - `A: (B,5)`
        - `5: (3,0)`
        - Mélange de lettres, chiffres, formats
        """)
        example_graph = """0: [(1, 4), (4, 1)]
1: []
2: [(1, 7), (3, -2)]
3: [(1, 1)]
4: [(3, -5)]"""
        graph_input = st.sidebar.text_area("Liste d'adjacence", value=example_graph, height=200)
        if graph_input.strip():
            graph = adjacency_list_to_graph(graph_input)
            if graph:
                st.sidebar.success(f"✅ Graphe chargé ({len(graph)} sommets)")
                st.sidebar.subheader("Graphe entré")
                for vertex, edges in graph.items():
                    edge_str = ", ".join([f"({target}, {weight})" for target, weight in edges])
                    st.sidebar.write(f"**{vertex}**: {edge_str}")
    
    if not graph:
        st.warning("⚠️ Veuillez définir un graphe dans la sidebar")
        return
    
    if st.sidebar.button("🚀 Lancer l'algorithme", type="primary", use_container_width=True):
        with st.spinner("Exécution de l'algorithme de Johnson..."):
            jp = JohnsonAlgorithm(graph)
            result = jp.johnson_all_pairs_shortest_paths()
            st.session_state.result = result
            st.session_state.graph = graph
            st.session_state.current_step = 0
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("✅ Algorithme terminé !")
            st.rerun()
    
    if hasattr(st.session_state, 'result'):
        result = st.session_state.result
        graph = st.session_state.graph
        if "error" in result:
            st.error(result["error"])
            return
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("◀ Étape précédente", use_container_width=True):
                st.session_state.current_step = max(0, st.session_state.current_step - 1)
                st.rerun()
        with col2:
            current_step = st.session_state.current_step
            total_steps = len(result['execution_steps'])
            st.markdown(f"<h3 style='text-align: center; color: #2C3E50;'>Étape {current_step + 1}/{total_steps}</h3>", unsafe_allow_html=True)
        with col3:
            if st.button("Étape suivante ▶", use_container_width=True):
                st.session_state.current_step = min(len(result['execution_steps']) - 1, st.session_state.current_step + 1)
                st.rerun()
        
        progress = (st.session_state.current_step + 1) / len(result['execution_steps'])
        st.progress(progress)
        
        current_step_data = result['execution_steps'][st.session_state.current_step]
        display_step_details(current_step_data, graph)
        
        if st.session_state.current_step == len(result['execution_steps']) - 1:
            st.balloons()
            st.success("🎉 **Algorithme de Johnson terminé avec succès !**")
            
            st.subheader("📊 Distances entre toutes les paires")
            all_pairs_distances = result['all_pairs_distances']
            vertices = sorted(all_pairs_distances.keys())
            distance_matrix = []
            for source in vertices:
                row = []
                for target in vertices:
                    dist = all_pairs_distances[source].get(target, float('inf'))
                    if dist == float('inf'):
                        row.append("∞")
                    else:
                        row.append(str(dist))
                distance_matrix.append(row)
            
            df = pd.DataFrame(distance_matrix, index=vertices, columns=vertices)
            styled_df = df.style.applymap(
                lambda x: 'background-color: #4ECDC4; color: black' if x != '∞' else 'background-color: white'
            )
            st.dataframe(styled_df, use_container_width=True)
            
            st.subheader("📈 Statistiques de Base")
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            with col_stats1:
                st.metric("Sommets totaux", len(graph))
                st.metric("Temps d'exécution", f"{result['execution_time']:.6f} s")
            with col_stats2:
                st.metric("Arêtes totales", sum(len(edges) for edges in graph.values()))
                st.metric("Poids minimum", min(weight for edges in graph.values() for _, weight in edges))
            with col_stats3:
                st.metric("Poids maximum", max(weight for edges in graph.values() for _, weight in edges))
                st.metric("Nombre d'étapes", len(result['execution_steps']))
            with col_stats4:
                st.metric("Opérations totales", result['operations_count']['operations_total'])
                st.metric("Comparaisons", result['operations_count']['comparaisons'])
        
        if st.button("🔄 Recommencer l'algorithme", use_container_width=True):
            for key in ['result', 'graph', 'current_step']:
                if hasattr(st.session_state, key):
                    delattr(st.session_state, key)
            st.rerun()
    
    else:
        st.info("👈 **Configurez le graphe dans la sidebar et cliquez sur 'Lancer l'algorithme' pour commencer**")

if __name__ == "__main__":
    main()
