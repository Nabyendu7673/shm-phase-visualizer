import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

st.set_page_config(page_title="SHM as Projection of UCM", layout="wide")
st.title("Harmonic Motion as a Phase Projection of Uniform Circular Motion")

# ---------------- Sidebar ----------------
st.sidebar.header("Physical Parameters")

A = st.sidebar.slider("Amplitude / Radius (A)", 0.5, 5.0, 2.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.1, 5.0, 1.0, 0.1)

phi_map = {"0": 0.0, "π/2": np.pi/2, "π": np.pi, "3π/2": 3*np.pi/2}
phi = phi_map[st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.01)

freeze = st.sidebar.button("📌 Freeze State")
reset = st.sidebar.button("♻ Reset")

# ---------------- State ----------------
if "frozen" not in st.session_state:
    st.session_state.frozen = []

if reset:
    st.session_state.frozen = []

# ---------------- Physics ----------------
theta = omega * t + phi
x = A * np.cos(theta)
y = A * np.sin(theta)

if freeze:
    scale = max(1 - 0.08 * len(st.session_state.frozen), 0.45)
    st.session_state.frozen.append((theta, t, scale))

# ---------------- Figure ----------------
fig, (ax_c, ax_s) = plt.subplots(1, 2, figsize=(14, 6),
                                 gridspec_kw={"width_ratios": [1, 2]})

# ================== CIRCLE ==================
circle = plt.Circle((0, 0), A, fill=False, linestyle="--", linewidth=2)
ax_c.add_artist(circle)

# Axes
ax_c.axhline(0, color="black", linewidth=1)
ax_c.axvline(0, color="black", linewidth=1)

# Frozen phasors (smaller, no labels)
for th, _, sc in st.session_state.frozen:
    xf = A * sc * np.cos(th)
    yf = A * sc * np.sin(th)
    ax_c.arrow(0, 0, xf, yf, color="gray", alpha=0.6,
               head_width=0.04*A, length_includes_head=True)

# Live phasor r(t)
ax_c.arrow(0, 0, x, y, color="#1f77b4",
           head_width=0.08*A, length_includes_head=True)

# Projections
ax_c.plot([x, x], [0, y], linestyle=":", color="gray")
ax_c.plot([0, x], [0, 0], linestyle=":", color="gray")

# θ arc
arc = Arc((0, 0), 0.6*A, 0.6*A, angle=0,
          theta1=0, theta2=np.degrees(theta),
          color="black", linewidth=1.5)
ax_c.add_patch(arc)
ax_c.text(0.35*A*np.cos(theta/2),
          0.35*A*np.sin(theta/2),
          r"$\theta=\omega t$", fontsize=11)

# Labels
ax_c.text(x*0.55, y*0.55, r"$\vec r(t)$", fontsize=12, color="#1f77b4")
ax_c.text(x/2, -0.15, r"$|r(t)|\cos\theta$", ha="center")
ax_c.text(x+0.05, y/2, r"$|r(t)|\sin\theta$", va="center")

ax_c.set_aspect("equal")
ax_c.set_xlim(-A-0.5, A+0.5)
ax_c.set_ylim(-A-0.5, A+0.5)
ax_c.set_xlabel("x")
ax_c.set_ylabel("y")
ax_c.set_title("Uniform Circular Motion (Phasor Representation)")
ax_c.grid(alpha=0.25)

# ================== SINE WAVE ==================
t_vals = np.linspace(0, 10, 1000)
y_vals = A * np.sin(omega*t_vals + phi)
ax_s.plot(t_vals, y_vals, color="black", linewidth=2)

# Frozen points
for th, tf, sc in st.session_state.frozen:
    ax_s.plot(tf, A*sc*np.sin(th), "o", color="gray", alpha=0.6)

# Live point
ax_s.plot(t, y, "ro")

ax_s.set_xlim(0, 10)
ax_s.set_ylim(-A-0.5, A+0.5)
ax_s.set_xlabel("Time (t)")
ax_s.set_ylabel("Displacement y(t)")
ax_s.set_title("Simple Harmonic Motion (Projection on Diameter)")
ax_s.grid(alpha=0.3)

st.pyplot(fig)

# ---------------- Mathematics ----------------
with st.expander("📐 Mathematical Description", expanded=True):
    st.latex(r"\theta(t) = \omega t + \phi")
    st.latex(r"y(t) = A \sin\bigl[\theta(t)\bigr] = A \sin(\omega t + \phi)")
