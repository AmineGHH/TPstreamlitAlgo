import streamlit as st

st.set_page_config(
    page_title="Advanced Algorithms & Data Structures",
    page_icon="🧠",
    layout="wide",
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
/* General body */
body {
    background-color: #f8fafc;
    color: #1f2937;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Hero section */
.hero {
    text-align: center;
    padding: 50px 20px 30px 20px;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #4f46e5, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero p {
    font-size: 1.2rem;
    color: #374151;
}

/* Section titles */
.section-title {
    font-size: 2rem;
    font-weight: 700;
    margin: 40px 0 20px 0;
    color: #1f2937;
}

/* TP Cards */
.card {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 22px;
    border: 1px solid #e5e7eb;
    min-height: 210px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.card h3 {
    color: #1f2937;
    font-weight: 600;
    margin-bottom: 10px;
}

.card p {
    color: #4b5563;
    font-size: 15px;
    line-height: 1.6;
}

/* Buttons */

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #4f46e5); /* Indigo gradient */
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 10px 0;
    width: 100%;
    font-size: 15px;
    transition: filter 0.2s ease;
}

.stButton > button:hover {
    filter: brightness(1.15);
}


.stButton > button:hover {
    filter: brightness(1.1);
}

/* Group members */
.members {
    font-size: 18px;
    line-height: 2;
}

.members span {
    font-weight: 600;
    color: #4f46e5;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 50px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero">
    <h1>Advanced Algorithms & Data Structures</h1>
    <p>Interactive exploration of advanced algorithms and data structures</p>
</div>
""", unsafe_allow_html=True)

# =========================
# TP DATA
# =========================
tp_descriptions = {
    "TP1 — Fundamental Structures": "Binary Search Trees (ABR), AVL Trees, Heaps, and graph fundamentals.",
    "TP2 — Treap": "Hybrid tree combining Binary Search Tree and Heap properties.",
    "TP3 — Complexity Analysis": "Algorithm analysis, benchmarking, and performance evaluation.",
    "TP4 — Johnson Algorithm": "Shortest path computation in weighted graphs.",
    "TP4 — Welsh–Powell Algorithm": "Graph coloring using the Welsh–Powell heuristic.",
}

tp_pages = {
    "TP1 — Fundamental Structures": "pages/TP1.py",
    "TP2 — Treap": "pages/TP2.py",
    "TP3 — Complexity Analysis": "pages/TP3.py",
    "TP4 — Johnson Algorithm": "pages/TP4johnson_ui.py",
    "TP4 — Welsh–Powell Algorithm": "pages/TP4welsh_powell_ui.py",
}

# =========================
# TP SECTION
# =========================
st.markdown('<div class="section-title">Travaux Pratiques</div>', unsafe_allow_html=True)

cols = st.columns(3)
for i, tp in enumerate(tp_descriptions):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="card">
                <h3>{tp}</h3>
                <p>{tp_descriptions[tp]}</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Open TP", key=f"btn_{tp}"):
            st.switch_page(tp_pages[tp])

# =========================
# GROUP MEMBERS
# =========================
st.markdown('<div class="section-title">Les membres du groupe 5</div>', unsafe_allow_html=True)

st.markdown("""
<div class="members">
<span>Ghorab Mohammed Amine</span><br>
<span>Boumaza Aya</span><br>
<span>Djellil Lilia</span><br>
<span>Douid Rania</span><br>
<span>Hamadash Lamia</span><br>
<span>Ghaoui Bouthaina</span>
</div>
""", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
Department of Computer Science — Advanced Algorithms & Data Structures
</div>
""", unsafe_allow_html=True)
