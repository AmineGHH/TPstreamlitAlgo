import streamlit as st

st.set_page_config(
    page_title="Advanced Algorithms & Data Structures",
    page_icon="🧠",
    layout="wide",
)

# =========================
# THEME CSS
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
}

/* Hero */
.hero {
    text-align: center;
    padding: 50px 20px 30px 20px;
}

.hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #2dd4bf);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 1.2rem;
    color: #cbd5f5;
}

/* Section title */
.section-title {
    font-size: 1.9rem;
    font-weight: 600;
    margin: 40px 0 20px 0;
    color: #e0f2fe;
}

/* Cards */
.card {
    background: #020617;
    border-radius: 16px;
    padding: 22px;
    border-left: 6px solid #38bdf8;
    box-shadow: 0 0 0 rgba(56,189,248,0);
    transition: all 0.3s ease;
    min-height: 220px;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 30px rgba(56,189,248,0.25);
}

.card h3 {
    color: #e0f2fe;
}

.card p {
    color: #94a3b8;
    font-size: 15px;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #2dd4bf);
    color: #020617;
    font-weight: 600;
    border-radius: 12px;
    border: none;
    padding: 10px 16px;
    width: 100%;
}

.stButton > button:hover {
    filter: brightness(1.1);
}

/* Members */
.member-card {
    background: #020617;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    border: 1px solid #1e293b;
    color: #e5e7eb;
    transition: 0.2s;
}

.member-card:hover {
    border-color: #2dd4bf;
    box-shadow: 0 0 20px rgba(45,212,191,0.25);
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 50px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
    <h1>Advanced Algorithms & Data Structures</h1>
    <p>Visual exploration of complex algorithms and graph-based methods</p>
</div>
""", unsafe_allow_html=True)

# =========================
# TP DATA
# =========================
tp_descriptions = {
    "TP1 — Fundamental Structures":
        "Binary Search Trees (ABR), AVL Trees, Heaps, and graph fundamentals.",
    "TP2 — Treap":
        "Hybrid tree structure combining Binary Search Tree and Heap properties.",
    "TP3 — Complexity Analysis":
        "Advanced algorithm analysis, benchmarking, and performance evaluation.",
    "TP4 — Johnson Algorithm":
        "Shortest path computation in weighted graphs.",
    "TP4 — Welsh–Powell Algorithm":
        "Graph coloring using the Welsh–Powell heuristic.",
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
            """,
            unsafe_allow_html=True
        )
        if st.button("Open TP", key=f"btn_{tp}"):
            st.switch_page(tp_pages[tp])

# =========================
# GROUP MEMBERS
# =========================
st.markdown('<div class="section-title">Les membres du groupe 5</div>', unsafe_allow_html=True)

members = [
    "Ghorab Mohammed Amine",
    "Boumaza Aya",
    "Djellil Lilia",
    "Douid Rania",
    "Hamadash Lamia",
    "Ghaoui Bouthaina",
]

cols = st.columns(3)
for i, m in enumerate(members):
    with cols[i % 3]:
        st.markdown(
            f'<div class="member-card">{m}</div>',
            unsafe_allow_html=True
        )

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    Department of Computer Science — Advanced Algorithms & Data Structures
</div>
""", unsafe_allow_html=True)
