import streamlit as st

st.set_page_config(page_title="TP4 — Graph Algorithms", page_icon="📊", layout="wide")

st.title("TP4 — Graph Algorithms")
st.markdown("""
Bienvenue dans le TP4 sur les algorithmes de graphes.

Choisissez un algorithme ci-dessous pour accéder à sa page dédiée.
""")

st.markdown("### Choisissez un algorithme :")

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 Welsh-Powell"):
        # Set query params to simulate navigation to page
        st.query_params = {"page": "TP4welsh_powell_ui"}

with col2:
    if st.button("🗺️ Johnson"):
        st.query_params = {"page": "TP4jhonson_ui"}

# Optional: show message about selected page
params = st.query_params
if "page" in params:
    st.info(f"🔗 Vous avez choisi la page : **{params['page'][0]}**")
    st.markdown("Si vous n’êtes pas redirigé automatiquement, cliquez sur le menu à gauche pour accéder à la page.")
