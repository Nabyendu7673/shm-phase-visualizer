import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Phase Freezing in Harmonic Motion",
    layout="wide"
)

st.title("Phase Freezing of Harmonic Motion")
st.subheader("Multiple Phasor States Visualized on a Single Sine Wave")

# ---------------- Theory ----------------
st.latex(r"\theta(t) = \omega t + \phi")
st.latex(r"y(t) = A\sin(\theta)")

st.markdown(
"""
This tool allows **freezing** the sine-wave response corresponding to different
phasor (phase) configurations and visualizing them together.
"""
)

# ---------------- Sidebar ----------------
st.sidebar.header("Control Parameters")

A = st.sidebar.slider("Amplitude (A)", 0.5, 5.0, 2.0)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.5, 5.0, 1.0)

phi_map = {
    "0": 0.0,
    "π/2": np.pi / 2,
    "π": np.pi,
    "3π/2": 3 * np.pi / 2
}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Current Time (t)", 0.0, 10.0, 0.0)

# ---------------- Session State ----------------
if "frozen_waves" not in st.session_state:
    st.session_state.frozen_waves = []

# ---------------- Calculations ----------------
theta = omega * t + phi

t_wave = np.linspace(0, 10, 800)
y_wave = A * np.sin(omega * t_wave + phi)

# ---------------- Buttons ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("❄ Freeze current phasor response"):
        st.session_state.frozen_waves.append({
            "A": A,
            "omega": omega,
            "phi": phi,
            "y": y_wave.copy()
        })

with col2:
    if st.button("🗑 Clear all frozen waves"):
        st.session_state.frozen_waves = []

# ---------------- Plot ----------------
fig, ax = plt.subplots(figsize=(12, 6))

# Plot frozen waves
for i, wave in enumerate(st.session_state.frozen_waves):
    ax.plot(
        t_wave,
        wave["y"],
        alpha=0.5,
        linewidth=2,
        label=f"Frozen {i+1}: φ={wave['phi']:.2f}"
    )

# Plot current live wave
ax.plot(
    t_wave,
    y_wave,
    color="crimson",
    linewidth=3,
    label="Live wave"
)

# Mark current point
y_now = A * np.sin(theta)
ax.scatter(t, y_now, color="black", zorder=5)

ax.set_xlabel("Time (t)")
ax.set_ylabel("Displacement y(t)")
ax.set_title("Superposition of Frozen Phase Responses")
ax.grid(alpha=0.3)
ax.legend()

st.pyplot(fig)

# ---------------- Live State ----------------
with st.expander("Current Phase State"):
    st.latex(fr"\theta = \omega t + \phi = {omega:.2f}\times {t:.2f} + {phi:.2f}")
    st.latex(fr"y(t) = {A:.2f}\sin({theta:.2f}) = {y_now:.2f}")
