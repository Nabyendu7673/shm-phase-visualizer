import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="SHM as Phase Projection of UCM",
    layout="wide"
)

st.title("Harmonic Motion as a Phase Projection of Uniform Circular Motion")

# ---------------- Sidebar Controls ----------------
st.sidebar.header("Physical Parameters")

A = st.sidebar.slider("Amplitude / Radius (A)", 0.5, 5.0, 2.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.1, 5.0, 1.0, 0.1)

phi_map = {
    "0": 0.0,
    "π/2": np.pi / 2,
    "π": np.pi,
    "3π/2": 3 * np.pi / 2
}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.01)

# Freeze buttons
freeze_circle = st.sidebar.button("📌 Freeze Phasor Position")
freeze_wave = st.sidebar.button("📌 Freeze Sine Point")
reset = st.sidebar.button("♻ Reset All Freezes")

# ---------------- Session State ----------------
if "circle_points" not in st.session_state:
    st.session_state.circle_points = []

if "wave_points" not in st.session_state:
    st.session_state.wave_points = []

if reset:
    st.session_state.circle_points = []
    st.session_state.wave_points = []

# ---------------- Physics ----------------
theta = omega * t + phi
x = A * np.cos(theta)
y = A * np.sin(theta)

if freeze_circle:
    st.session_state.circle_points.append((x, y))

if freeze_wave:
    st.session_state.wave_points.append((t, y))

# ---------------- Layout ----------------
fig, (ax_circle, ax_wave) = plt.subplots(
    1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1, 2]}
)

# ================= LEFT: CIRCLE =================
circle = plt.Circle((0, 0), A, fill=False, linestyle="--", linewidth=2)
ax_circle.add_artist(circle)

# Current phasor
ax_circle.arrow(
    0, 0, x, y,
    head_width=0.08 * A,
    head_length=0.12 * A,
    length_includes_head=True,
    color="red"
)

# Projection line
ax_circle.plot([x, x], [0, y], linestyle=":", color="blue")

# Frozen phasors
for xf, yf in st.session_state.circle_points:
    ax_circle.plot(xf, yf, "ro", alpha=0.6)

ax_circle.set_aspect("equal")
ax_circle.set_xlim(-A - 0.5, A + 0.5)
ax_circle.set_ylim(-A - 0.5, A + 0.5)
ax_circle.set_title("Uniform Circular Motion (Phasor Representation)")
ax_circle.set_xlabel("x")
ax_circle.set_ylabel("y")
ax_circle.grid(alpha=0.3)

# ================= RIGHT: SINE WAVE =================
t_vals = np.linspace(0, 10, 1000)
y_vals = A * np.sin(omega * t_vals + phi)

ax_wave.plot(t_vals, y_vals, color="black", linewidth=2)
ax_wave.plot(t, y, "ro")

# Frozen sine points
for tf, yf in st.session_state.wave_points:
    ax_wave.plot(tf, yf, "ro", alpha=0.6)

ax_wave.axhline(0, color="gray", linewidth=1)
ax_wave.set_xlim(0, 10)
ax_wave.set_ylim(-A - 0.5, A + 0.5)
ax_wave.set_title("Simple Harmonic Motion (Projection on Diameter)")
ax_wave.set_xlabel("Time (t)")
ax_wave.set_ylabel("Displacement y(t)")
ax_wave.grid(alpha=0.3)

st.pyplot(fig)

# ---------------- Mathematical Description ----------------
with st.expander("📐 Mathematical Description", expanded=True):
    st.latex(r"\textbf{Instantaneous phase of the particle:}")
    st.latex(r"\theta(t) = \omega t + \phi")

    st.latex(r"\textbf{Displacement in simple harmonic motion (projection of uniform circular motion):}")
    st.latex(r"y(t) = A \sin\bigl[\theta(t)\bigr] = A \sin(\omega t + \phi)")

# ---------------- Interpretation ----------------
st.info(
    f"At time t = {t:.2f}, the phase is θ(t) = {theta:.2f} rad. "
    f"The vertical projection of the rotating radius gives y(t) = {y:.2f}."
)
