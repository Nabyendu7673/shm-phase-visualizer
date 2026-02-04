import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.header("Control Parameters")

A = st.sidebar.slider("Amplitude (A)", 0.5, 2.0, 1.0, 0.1)
omega = st.sidebar.slider("Angular Frequency ω (rad/s)", 0.5, 5.0, 1.0, 0.1)
phi = st.sidebar.slider("Initial Phase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

theta = st.sidebar.slider(
    "Instantaneous Phase θ (rad)",
    0.0, 2*np.pi, 0.0, 0.01
)

freeze = st.sidebar.button("❄️ Freeze Current State")
clear = st.sidebar.button("🗑️ Clear All Frozen States")

# ---------------------------
# State storage
# ---------------------------
if "frozen_theta" not in st.session_state:
    st.session_state.frozen_theta = []

if freeze:
    st.session_state.frozen_theta.append(theta)

if clear:
    st.session_state.frozen_theta = []

# ---------------------------
# Phase definition
# ---------------------------
theta_eff = theta + phi

# ---------------------------
# Layout
# ---------------------------
st.title("Simple Harmonic Motion as Projection of Uniform Circular Motion")

st.markdown(
r"""
### Mathematical Description

**Instantaneous Phase**
\[
\theta(t) = \omega t + \phi
\]

**Displacement of SHM (Projection of UCM)**
\[
y(t) = A \sin\theta
\]
"""
)

col1, col2 = st.columns(2)

# ===========================
# Circular Motion Plot
# ===========================
with col1:
    fig1, ax1 = plt.subplots(figsize=(5,5))

    # Circle
    t = np.linspace(0, 2*np.pi, 400)
    ax1.plot(A*np.cos(t), A*np.sin(t), color="gray")

    # Axes
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.axvline(0, color="black", linewidth=0.8)

    # Current phasor
    x = A * np.cos(theta_eff)
    y = A * np.sin(theta_eff)

    ax1.arrow(
        0, 0, x, y,
        head_width=0.08,
        length_includes_head=True,
        color="blue"
    )

    # Projection
    ax1.plot([x, x], [0, y], linestyle="dashed", color="gray")

    # Frozen phasors
    for th in st.session_state.frozen_theta:
        th_eff = th + phi
        xf = A*np.cos(th_eff)
        yf = A*np.sin(th_eff)
        ax1.arrow(0, 0, xf, yf, color="red", alpha=0.5, head_width=0.05)

    ax1.set_aspect("equal")
    ax1.set_xlim(-A-0.3, A+0.3)
    ax1.set_ylim(-A-0.3, A+0.3)
    ax1.set_title("Uniform Circular Motion (Phasor Representation)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    st.pyplot(fig1)

# ===========================
# Sine Wave Plot
# ===========================
with col2:
    fig2, ax2 = plt.subplots(figsize=(6,4))

    theta_range = np.linspace(0, 2*np.pi, 400)
    y_wave = A * np.sin(theta_range)

    ax2.plot(theta_range, y_wave, label=r"$y = A\sin\theta$")

    # Current point
    ax2.plot(theta_eff % (2*np.pi), A*np.sin(theta_eff), "ko")

    # Frozen points
    for th in st.session_state.frozen_theta:
        th_eff = th + phi
        ax2.plot(
            th_eff % (2*np.pi),
            A*np.sin(th_eff),
            "ro",
            alpha=0.6
        )

    ax2.set_xlim(0, 2*np.pi)
    ax2.set_ylim(-A-0.2, A+0.2)
    ax2.set_xlabel("Phase θ (rad)")
    ax2.set_ylabel("Displacement y")
    ax2.set_title("Sinusoidal Waveform (SHM)")
    ax2.grid(True)

    st.pyplot(fig2)
