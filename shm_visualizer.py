import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Phase-Resolved Harmonic Motion", layout="wide")

st.title("Phase-Resolved Harmonic Motion: Phasor–Time Domain Mapping")

st.markdown(
r"""
**Instantaneous phase**:  
\[
\theta(t) = \omega t + \phi
\]

**Displacement (SHM)**:  
\[
y(t) = A\sin(\theta)
\]
"""
)

# ---------- Sidebar ----------
st.sidebar.header("Control Parameters")

A = st.sidebar.slider("Amplitude / Radius (A)", 0.5, 5.0, 2.0)
omega = st.sidebar.slider("Angular frequency (ω)", 0.5, 5.0, 1.0)

phi_map = {
    "0 (Mean position)": 0,
    "π/2 (Positive extreme)": np.pi/2,
    "π (Mean, opposite direction)": np.pi,
    "3π/2 (Negative extreme)": 3*np.pi/2
}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Current Time (t)", 0.0, 10.0, 0.0)

# ---------- Calculations ----------
theta = omega * t + phi
x = A * np.cos(theta)
y = A * np.sin(theta)

t_wave = np.linspace(0, 10, 600)
y_wave = A * np.sin(omega * t_wave + phi)

# ---------- Layout ----------
fig, (ax_circle, ax_wave) = plt.subplots(
    1, 2, figsize=(14, 6),
    gridspec_kw={"width_ratios": [1, 2]}
)

# ================= LEFT: PHASOR =================
circle = plt.Circle((0, 0), A, fill=False, linestyle='--', linewidth=2)
ax_circle.add_artist(circle)

# Phasor vector
ax_circle.quiver(
    0, 0, x, y,
    angles='xy', scale_units='xy', scale=1,
    color='crimson', linewidth=3
)

# Projections
ax_circle.plot([x, x], [0, y], linestyle=':', color='steelblue', linewidth=2)
ax_circle.plot([0, x], [0, 0], linestyle=':', color='gray', linewidth=1)

ax_circle.scatter(x, y, color='black', zorder=5)

# Axes
ax_circle.axhline(0, color='black', linewidth=1)
ax_circle.axvline(0, color='black', linewidth=1)

# Labels
ax_circle.text(x/2, y/2, r"$\vec{r}(t)$", fontsize=12)
ax_circle.text(0.1*A, 0.1*A, r"$\theta=\omega t+\phi$", fontsize=12)

ax_circle.set_aspect('equal')
ax_circle.set_xlim(-A-0.5, A+0.5)
ax_circle.set_ylim(-A-0.5, A+0.5)
ax_circle.set_title("Rotating Phasor (Uniform Circular Motion)")
ax_circle.set_xticks([])
ax_circle.set_yticks([])
ax_circle.grid(alpha=0.3)

# ================= RIGHT: SINE WAVE =================
ax_wave.plot(t_wave, y_wave, color='navy', linewidth=2)
ax_wave.scatter(t, y, color='crimson', zorder=5)

# Projection transfer line
ax_wave.axhline(y, linestyle=':', color='steelblue', linewidth=2)
ax_wave.axvline(t, linestyle=':', color='gray', linewidth=1)

ax_wave.set_xlim(0, 10)
ax_wave.set_ylim(-A-0.5, A+0.5)
ax_wave.set_xlabel("Time (t)")
ax_wave.set_ylabel("Displacement y(t)")
ax_wave.set_title("Sinusoidal Waveform in Time Domain")
ax_wave.grid(alpha=0.3)

st.pyplot(fig)

# ---------- Live Equation ----------
with st.expander("Live Mathematical State"):
    st.latex(r"\theta(t)=\omega t+\phi")
    st.latex(fr"\theta = {omega:.2f}\times{t:.2f} + {phi:.2f} = {theta:.2f}\ \text{{rad}}")
    st.latex(fr"y(t) = {A:.2f}\sin({theta:.2f}) = {y:.2f}")
