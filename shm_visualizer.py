import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# ================= Page Setup & Professional CSS =================
st.set_page_config(page_title="SHM Lab", layout="wide")

st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    /* Freeze Button (Green) */
    div[data-testid="column"]:nth-child(1) .stButton>button {
        background-color: #238636;
        color: white;
        border: 1px solid rgba(240,246,252,0.1);
    }
    
    /* Reset Button (Red) */
    div[data-testid="column"]:nth-child(2) .stButton>button {
        background-color: #da3633;
        color: white;
        border: 1px solid rgba(240,246,252,0.1);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Harmonic Motion: Phase Projection Lab")

# ================= Sidebar Controls =================
st.sidebar.header("🕹️ Simulation Controls")
A = st.sidebar.slider("Amplitude (A)", 0.5, 5.0, 2.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.1, 5.0, 1.0, 0.1)

phi_map = {"0": 0.0, "π/2": np.pi/2, "π": np.pi, "3π/2": 3*np.pi/2}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.01)

st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
freeze = col1.button("📌 Freeze")
reset = col2.button("♻ Reset")

# ================= Session State Management =================
if "frozen" not in st.session_state:
    st.session_state.frozen = []

if reset:
    st.session_state.frozen = []
    st.rerun()

# ================= Physics Calculations =================
theta = omega * t + phi
x_pos = A * np.cos(theta)
y_pos = A * np.sin(theta)
color_cycle = plt.cm.tab10.colors

if freeze:
    idx = len(st.session_state.frozen)
    color = color_cycle[idx % len(color_cycle)]
    st.session_state.frozen.append((omega, phi, A, theta, color))

# ================= Visualization =================
plt.style.use('dark_background')
fig, (ax_c, ax_s) = plt.subplots(1, 2, figsize=(15, 7), gridspec_kw={"width_ratios": [1, 1.7]})
fig.patch.set_facecolor('#0d1117')

# --- 1. Circular Motion Plot (Phasor) ---
ax_c.set_facecolor('#0d1117')
circle = plt.Circle((0, 0), A, fill=False, linestyle="--", color="#30363d", linewidth=1.5)
ax_c.add_artist(circle)
ax_c.axhline(0, color="#8b949e", linewidth=0.8)
ax_c.axvline(0, color="#8b949e", linewidth=0.8)

# Draw Frozen Phasors
for ωf, φf, Af, θf, col in st.session_state.frozen:
    ax_c.arrow(0, 0, Af * np.cos(θf), Af * np.sin(θf), color=col, head_width=0.1, alpha=0.3)

# Draw Live Phasor (r vector)
ax_c.arrow(0, 0, x_pos, y_pos, color="#58a6ff", linewidth=2.5, head_width=0.15, length_includes_head=True, zorder=5)

# Projections & Labels (Matching your reference image)
ax_c.arrow(0, 0, x_pos, 0, color="#3fb950", linewidth=2, head_width=0.12, length_includes_head=True) # Cos comp
ax_c.plot([x_pos, x_pos], [0, y_pos], color="#a5d6ff", linestyle=":", alpha=0.6) # Sine vertical line

# Text Annotations
ax_c.text(x_pos/2, y_pos/2 + 0.3, r"$\vec{r}(t)$", color="#58a6ff", fontsize=14, fontweight='bold')
ax_c.text(x_pos/2, -0.5, r"$|\vec{r}(t)|\cos\omega t$", color="#3fb950", fontsize=10, ha='center')
ax_c.text(x_pos + 0.2, y_pos/2, r"$|\vec{r}(t)|\sin\omega t$", color="#a5d6ff", fontsize=10, rotation=90, va='center')

# Angle Arc
arc = Arc((0, 0), 0.8, 0.8, theta1=0, theta2=np.degrees(theta), color="#f0f6fc", linewidth=1.2)
ax_c.add_patch(arc)
ax_c.text(0.6*np.cos(theta/2), 0.6*np.sin(theta/2), r"$\theta$", color="#f0f6fc", fontsize=12)

ax_c.set_xlim(-5.5, 5.5); ax_c.set_ylim(-5.5, 5.5)
ax_c.set_aspect("equal")
ax_c.set_title("Uniform Circular Motion", color="#8b949e", pad=15)

# --- 2. SHM Wave Plot ---
ax_s.set_facecolor('#0d1117')
t_vals = np.linspace(0, 10, 1000)

# Toggle Logic: Show solid wave ONLY if nothing is frozen
if not st.session_state.frozen:
    y_live_wave = A * np.sin(omega * t_vals + phi)
    ax_s.plot(t_vals, y_live_wave, color="white", linewidth=2, alpha=0.5, label="Live Path")
else:
    # Show only frozen dashed lines
    for ωf, φf, Af, θf, col in st.session_state.frozen:
        y_frozen = Af * np.sin(ωf * t_vals + φf)
        ax_s.plot(t_vals, y_frozen, color=col, linestyle="--", linewidth=1.5, alpha=0.8)

# Live point tracking
ax_s.plot(t, y_pos, marker="o", color="#f85149", markersize=10, zorder=10)
ax_s.axhline(y_pos, xmin=0, xmax=t/10, color="#f85149", linestyle=":", alpha=0.4)

ax_s.set_xlim(0, 10); ax_s.set_ylim(-5.5, 5.5)
ax_s.set_title("Simple Harmonic Motion Projection", color="#8b949e", pad=15)
ax_s.grid(color='#30363d', linestyle='--', linewidth=0.5)

st.pyplot(fig)

# ================= Technical Details =================


st.markdown("### 📐 Mathematical Relationship")
st.latex(r"y(t) = A \sin(\omega t + \phi)")

st.info(f"Currently tracking: Amplitude = {A} | Frequency = {omega} rad/s")

if st.session_state.frozen:
    st.success(f"Number of frozen states: {len(st.session_state.frozen)}")
