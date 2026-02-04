import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Phase-Resolved Harmonic Motion", layout="wide")

st.title("Phase-Resolved Harmonic Motion via Rotating Phasor Representation")

st.markdown(
r"""
This visualization represents **Simple Harmonic Motion (SHM)** as the **projection of uniform circular motion (UCM)**.

- **Instantaneous phase**: $\theta(t) = \omega t + \phi$
- **Displacement**: $y(t) = A \sin(\theta)$
"""
)

# ---------- Sidebar Controls ----------
st.sidebar.header("Physical Parameters")

A = st.sidebar.slider("Radius / Amplitude (A)", 0.5, 5.0, 2.0)
omega = st.sidebar.slider("Angular frequency (ω)", 0.5, 5.0, 1.0)

phi_map = {
    "0 (Mean position)": 0,
    "π/2 (Upper extreme)": np.pi/2,
    "π (Mean, opposite direction)": np.pi,
    "3π/2 (Lower extreme)": 3*np.pi/2
}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.0)

# ---------- Calculations ----------
theta = omega * t + phi

x = A * np.cos(theta)
y = A * np.sin(theta)

# ---------- Plot ----------
fig, ax = plt.subplots(figsize=(6, 6))

# Reference circle
circle = plt.Circle((0, 0), A, fill=False, linestyle='--', linewidth=2)
ax.add_artist(circle)

# Position vector r(t)
ax.quiver(
    0, 0, x, y,
    angles='xy', scale_units='xy', scale=1,
    color='navy', linewidth=3
)

# Horizontal projection: |r| cosθ
ax.plot([0, x], [0, 0], color='gray', linestyle=':', linewidth=2)
ax.plot([x, x], [0, y], color='gray', linestyle=':', linewidth=2)

# Projection markers
ax.scatter(x, y, color='black', zorder=5)

# Axes
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Labels
ax.text(x/2, y/2, r"$\vec{r}(t)$", fontsize=12)
ax.text(x/2, -0.15*A, r"$A\cos\theta$", fontsize=11, ha='center')
ax.text(x+0.05*A, y/2, r"$A\sin\theta$", fontsize=11, va='center')

# Theta annotation
ax.text(0.1*A, 0.1*A, r"$\theta = \omega t + \phi$", fontsize=12)

# Formatting
ax.set_aspect('equal')
ax.set_xlim(-A-0.5, A+0.5)
ax.set_ylim(-A-0.5, A+0.5)
ax.set_title("Rotating Phasor and Orthogonal Projections")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(alpha=0.3)

st.pyplot(fig)

# ---------- Dynamic Equation Display ----------
with st.expander("Current Mathematical State"):
    st.latex(r"\theta(t) = \omega t + \phi")
    st.latex(fr"\theta = {omega:.2f}\times {t:.2f} + {phi:.2f} = {theta:.2f}\ \text{{rad}}")
    st.latex(fr"y(t) = {A:.2f}\sin({theta:.2f}) = {y:.2f}")
