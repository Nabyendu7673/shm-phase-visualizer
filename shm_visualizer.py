import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SHM as Phase Projection of UCM", layout="wide")
st.title("Harmonic Motion as a Phase Projection of Uniform Circular Motion")

# ---------------- Sidebar ----------------
st.sidebar.header("Physical Parameters")

A = st.sidebar.slider("Amplitude / Radius (A)", 0.5, 5.0, 2.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.1, 5.0, 1.0, 0.1)

phi_map = {"0": 0.0, "π/2": np.pi/2, "π": np.pi, "3π/2": 3*np.pi/2}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.01)

freeze = st.sidebar.button("📌 Freeze Phasor & SHM State")
reset = st.sidebar.button("♻ Reset")

# ---------------- Session State ----------------
if "frozen_states" not in st.session_state:
    st.session_state.frozen_states = []

if reset:
    st.session_state.frozen_states = []

# ---------------- Physics ----------------
theta = omega * t + phi
x = A * np.cos(theta)
y = A * np.sin(theta)

if freeze:
    scale = 1.0 - 0.08 * len(st.session_state.frozen_states)
    scale = max(scale, 0.4)  # prevent vanishing
    st.session_state.frozen_states.append((theta, t, scale))

# ---------------- Figure ----------------
fig, (ax_c, ax_s) = plt.subplots(1, 2, figsize=(14, 6),
                                 gridspec_kw={"width_ratios": [1, 2]})

# ===== Circle =====
circle = plt.Circle((0, 0), A, fill=False, linestyle="--", linewidth=2)
ax_c.add_artist(circle)

# Frozen phasors
for th_f, _, sc in st.session_state.frozen_states:
    xf = A * sc * np.cos(th_f)
    yf = A * sc * np.sin(th_f)

    ax_c.arrow(0, 0, xf, yf,
               head_width=0.04*A,
               length_includes_head=True,
               color="gray", alpha=0.6)

    ax_c.plot([xf, xf], [0, yf], linestyle=":", color="gray", alpha=0.6)

# Current phasor
ax_c.arrow(0, 0, x, y,
           head_width=0.08*A,
           length_includes_head=True,
           color="red")

ax_c.plot([x, x], [0, y], linestyle=":", color="blue")

ax_c.set_aspect("equal")
ax_c.set_xlim(-A-0.5, A+0.5)
ax_c.set_ylim(-A-0.5, A+0.5)
ax_c.set_title("Uniform Circular Motion (Phasor Representation)")
ax_c.set_xlabel("x")
ax_c.set_ylabel("y")
ax_c.grid(alpha=0.3)

# ===== Sine Wave =====
t_vals = np.linspace(0, 10, 1000)
y_vals = A * np.sin(omega*t_vals + phi)
ax_s.plot(t_vals, y_vals, color="black", linewidth=2)

# Frozen SHM points
for th_f, tf, sc in st.session_state.frozen_states:
    yf = A * sc * np.sin(th_f)
    ax_s.plot(tf, yf, "o", color="gray", alpha=0.6)

# Current point
ax_s.plot(t, y, "ro")

ax_s.set_xlim(0, 10)
ax_s.set_ylim(-A-0.5, A+0.5)
ax_s.set_title("Simple Harmonic Motion (Projection of UCM)")
ax_s.set_xlabel("Time (t)")
ax_s.set_ylabel("Displacement y(t)")
ax_s.grid(alpha=0.3)

st.pyplot(fig)

# ---------------- Mathematics ----------------
with st.expander("📐 Mathematical Description", expanded=True):
    st.latex(r"\theta(t) = \omega t + \phi")
    st.latex(r"y(t) = A \sin\bigl[\theta(t)\bigr] = A \sin(\omega t + \phi)")
