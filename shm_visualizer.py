import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# ---------------- Page Config ----------------
st.set_page_config(page_title="SHM as Projection of UCM", layout="wide")

# ---------------- DARK UI CSS ----------------
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #e6e6e6; }
    .stSidebar { background-color: #161b22; }
    h1, h2, h3, h4 { color: white; }
    label, span, div { color: #e6e6e6 !important; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 12px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Harmonic Motion as a Phase Projection of Uniform Circular Motion")

# ---------------- Sidebar ----------------
st.sidebar.header("Physical Parameters")

A = st.sidebar.slider("Amplitude / Radius (A)", 0.5, 5.0, 2.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.1, 5.0, 1.0, 0.1)

phi_map = {"0": 0.0, "π/2": np.pi/2, "π": np.pi, "3π/2": 3*np.pi/2}
phi = phi_map[st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.01)

freeze = st.sidebar.button("📌 Freeze State")
reset = st.sidebar.button("♻ Reset All")

# ---------------- Session State ----------------
if "frozen" not in st.session_state:
    st.session_state.frozen = []

if reset:
    st.session_state.frozen = []

# ---------------- Physics ----------------
theta = omega * t + phi
x = A * np.cos(theta)
y = A * np.sin(theta)

# ---------------- Solved Values ----------------
st.subheader("🔢 Solved Values")

c1, c2, c3 = st.columns(3)
c1.metric("θ(t) (rad)", f"{theta:.4f}")
c2.metric("x(t)", f"{x:.4f}")
c3.metric("y(t)", f"{y:.4f}")

# ---------------- Freeze ----------------
color_cycle = plt.cm.tab10.colors
if freeze:
    idx = len(st.session_state.frozen)
    scale = max(1 - 0.08 * idx, 0.45)
    color = color_cycle[idx % len(color_cycle)]
    st.session_state.frozen.append((omega, phi, A, t, theta, scale, color))

# ---------------- Figure ----------------
fig, (ax_c, ax_s) = plt.subplots(
    1, 2, figsize=(14, 6),
    gridspec_kw={"width_ratios": [1, 2]}
)

# White graph background
fig.patch.set_facecolor("white")
ax_c.set_facecolor("white")
ax_s.set_facecolor("white")

# ===== FORCE GRAPH TEXT TO BLACK =====
for ax in [ax_c, ax_s]:
    ax.tick_params(colors="black")
    ax.xaxis.label.set_color("black")
    ax.yaxis.label.set_color("black")
    ax.title.set_color("black")

# ================== UCM GRAPH ==================
circle = plt.Circle((0, 0), A, fill=False, linestyle="--", linewidth=2, color="black")
ax_c.add_artist(circle)

ax_c.axhline(0, color="black")
ax_c.axvline(0, color="black")

# Frozen phasors
for ωf, φf, Af, _, θf, sc, col in st.session_state.frozen:
    ax_c.arrow(
        0, 0,
        Af * sc * np.cos(θf),
        Af * sc * np.sin(θf),
        color=col,
        alpha=0.7,
        head_width=0.05 * A,
        length_includes_head=True
    )

# Live phasor
ax_c.arrow(0, 0, x, y, color="red",
           head_width=0.08 * A, length_includes_head=True)

# Projections
ax_c.plot([x, x], [0, y], ":", color="gray")
ax_c.plot([0, x], [0, 0], ":", color="gray")

# Angle arc + text
arc = Arc((0, 0), 0.6*A, 0.6*A,
          theta1=0, theta2=np.degrees(theta),
          linewidth=1.5, color="black")
ax_c.add_patch(arc)

ax_c.text(
    0.35*A*np.cos(theta/2),
    0.35*A*np.sin(theta/2),
    r"$\theta=\omega t + \phi$",
    color="black"
)

ax_c.set_aspect("equal")
ax_c.set_xlim(-A-0.5, A+0.5)
ax_c.set_ylim(-A-0.5, A+0.5)
ax_c.set_xlabel("x")
ax_c.set_ylabel("y")
ax_c.set_title("Uniform Circular Motion (Phasor)")
ax_c.grid(color="gray", alpha=0.3)

# ================== SHM GRAPH ==================
t_vals = np.linspace(0, 10, 1000)

for ωf, φf, Af, _, _, sc, col in st.session_state.frozen:
    ax_s.plot(t_vals, Af*sc*np.sin(ωf*t_vals + φf),
              color=col, linewidth=1.6, alpha=0.8)

ax_s.plot(t_vals, A*np.sin(omega*t_vals + phi),
          color="black", linewidth=2.5)

ax_s.plot(t, y, "ro")

ax_s.set_xlim(0, 10)
ax_s.set_ylim(-A-0.5, A+0.5)
ax_s.set_xlabel("Time (t)")
ax_s.set_ylabel("Displacement y(t)")
ax_s.set_title("Simple Harmonic Motion")
ax_s.grid(color="gray", alpha=0.3)

st.pyplot(fig)

# ---------------- Mathematics ----------------
with st.expander("📐 Mathematical Description", expanded=True):
    st.latex(r"\theta(t) = \omega t + \phi")
    st.latex(rf"\theta(t) = {omega:.2f}({t:.2f}) + {phi:.2f} = {theta:.4f}")
    st.latex(rf"y(t) = {A:.2f}\sin(\omega t + \phi) = {y:.4f}")
