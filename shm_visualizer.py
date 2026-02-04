import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# App Configuration
# ---------------------------
st.set_page_config(page_title="SHM–UCM Phase Visualizer", layout="wide")

st.title("Simple Harmonic Motion as a Projection of Uniform Circular Motion")

st.markdown(
r"""
**Instantaneous phase**
\[
\theta(t) = \omega t + \phi
\]

**Displacement (SHM)**
\[
y(t) = A \sin(\theta)
\]
"""
)

# ---------------------------
# Session State for Freezing
# ---------------------------
if "frozen_states" not in st.session_state:
    st.session_state.frozen_states = []

# ---------------------------
# Controls
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    A = st.slider("Amplitude (A)", 0.5, 2.0, 1.0, 0.1)

with col2:
    omega = st.slider("Angular Frequency (ω rad/s)", 0.5, 5.0, 1.0, 0.1)

with col3:
    theta = st.slider("Phase θ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

freeze = st.button("❄️ Freeze current phase")
clear = st.button("🗑️ Clear all frozen states")

if freeze:
    st.session_state.frozen_states.append(theta)

if clear:
    st.session_state.frozen_states = []

# ---------------------------
# Data
# ---------------------------
t = np.linspace(0, 2*np.pi, 400)
y = A * np.sin(t)

# ---------------------------
# Plot Layout
# ---------------------------
fig, (ax_circle, ax_sine) = plt.subplots(1, 2, figsize=(14, 6))

# ===========================
# 1️⃣ CIRCLE (UCM PHASOR)
# ===========================
circle = plt.Circle((0, 0), A, fill=False, linewidth=2)
ax_circle.add_artist(circle)

# Axes
ax_circle.axhline(0, color='gray', linewidth=0.8)
ax_circle.axvline(0, color='gray', linewidth=0.8)

# Current phasor
x = A * np.cos(theta)
y_ph = A * np.sin(theta)
ax_circle.arrow(0, 0, x, y_ph,
                head_width=0.08, head_length=0.12,
                length_includes_head=True, color="blue", linewidth=2)

ax_circle.plot(x, y_ph, 'ko')

# Frozen phasors
for th in st.session_state.frozen_states:
    xf = A * np.cos(th)
    yf = A * np.sin(th)
    ax_circle.arrow(0, 0, xf, yf,
                    head_width=0.05, head_length=0.08,
                    length_includes_head=True,
                    color="red", alpha=0.5)
    ax_circle.plot(xf, yf, 'ro', alpha=0.6)

ax_circle.set_aspect("equal")
ax_circle.set_xlim(-1.3*A, 1.3*A)
ax_circle.set_ylim(-1.3*A, 1.3*A)
ax_circle.set_title("Rotating Phasor (Uniform Circular Motion)")
ax_circle.set_xlabel("x = A cos θ")
ax_circle.set_ylabel("y = A sin θ")

# ===========================
# 2️⃣ SINE WAVE (SHM)
# ===========================
ax_sine.plot(t, A*np.sin(t), label="Live sine wave", linewidth=2)

# Current point
ax_sine.plot(theta, A*np.sin(theta), 'ko')

# Frozen sine points + verticals
for th in st.session_state.frozen_states:
    ax_sine.plot(th, A*np.sin(th), 'ro')
    ax_sine.axvline(th, color='red', alpha=0.3, linestyle='--')

ax_sine.set_xlim(0, 2*np.pi)
ax_sine.set_ylim(-1.3*A, 1.3*A)
ax_sine.set_xlabel("Phase θ (rad)")
ax_sine.set_ylabel("Displacement y")
ax_sine.set_title("Sinusoidal Waveform (SHM)")
ax_sine.legend()

plt.tight_layout()
st.pyplot(fig)
