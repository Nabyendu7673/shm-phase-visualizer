import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Phase-Resolved Harmonic Motion",
    layout="wide"
)

st.title("Phase-Resolved Harmonic Motion via Rotating Phasor")
st.subheader("Freezing Phasor States and Their Time-Domain Responses")

# ---------------- Theory ----------------
st.latex(r"\theta(t) = \omega t + \phi")
st.latex(r"y(t) = A \sin(\theta)")

st.markdown(
"""
- **θ(t)** → instantaneous phase  
- **φ** → initial phase (phase constant)  
- **ω** → angular frequency  
- **A** → radius of reference circle / amplitude  

Each frozen state represents a **distinct phasor configuration**
mapped into the **time-domain sinusoidal response**.
"""
)

# ---------------- Sidebar Controls ----------------
st.sidebar.header("Control Parameters")

A = st.sidebar.slider("Amplitude / Radius (A)", 0.5, 5.0, 2.0)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.5, 5.0, 1.0)

phi_map = {
    "0  → Mean position": 0.0,
    "π/2 → Positive extreme": np.pi / 2,
    "π  → Mean (opposite direction)": np.pi,
    "3π/2 → Negative extreme": 3 * np.pi / 2
}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.0)

# ---------------- Session State ----------------
if "frozen_states" not in st.session_state:
    st.session_state.frozen_states = []

# ---------------- Calculations ----------------
theta = omega * t + phi
x = A * np.cos(theta)
y = A * np.sin(theta)

t_wave = np.linspace(0, 10, 800)
y_wave = A * np.sin(omega * t_wave + phi)

# ---------------- Freeze Controls ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("❄ Freeze current phasor & sine response"):
        st.session_state.frozen_states.append({
            "A": A,
            "omega": omega,
            "phi": phi,
            "theta": theta,
            "y_wave": y_wave.copy()
        })

with col2:
    if st.button("🗑 Clear all frozen states"):
        st.session_state.frozen_states = []

# ---------------- Plot Layout ----------------
fig, (ax_circle, ax_wave) = plt.subplots(
    1, 2,
    figsize=(15, 6),
    gridspec_kw={"width_ratios": [1, 2]}
)

# =================================================
# LEFT PANEL — EXACT PHASOR DIAGRAM
# =================================================
circle = plt.Circle((0, 0), A, fill=False, linewidth=2)
ax_circle.add_artist(circle)

# Direction arrows on circle
for ang in np.linspace(0, 2*np.pi, 16):
    ax_circle.arrow(
        A*np.cos(ang), A*np.sin(ang),
        -0.15*np.sin(ang), 0.15*np.cos(ang),
        head_width=0.06, length_includes_head=True,
        color='gray', alpha=0.6
    )

# Position vector r(t)
ax_circle.quiver(
    0, 0, x, y,
    angles='xy', scale_units='xy', scale=1,
    color='navy', linewidth=3
)

# Projections
ax_circle.plot([x, x], [0, y], linestyle=':', color='steelblue', linewidth=2)
ax_circle.plot([0, x], [0, 0], linestyle=':', color='gray', linewidth=1)

ax_circle.scatter(x, y, color='black', zorder=5)

# Axes
ax_circle.axhline(0, color='black', linewidth=1)
ax_circle.axvline(0, color='black', linewidth=1)

# Labels
ax_circle.text(x/2, y/2, r"$\vec r(t)$", fontsize=12)
ax_circle.text(0.1*A, 0.1*A, r"$\theta=\omega t+\phi$", fontsize=12)
ax_circle.text(x/2, -0.15*A, r"$A\cos\theta$", ha='center', fontsize=11)
ax_circle.text(x+0.05*A, y/2, r"$A\sin\theta$", va='center', fontsize=11)

ax_circle.set_aspect('equal')
ax_circle.set_xlim(-A-0.5, A+0.5)
ax_circle.set_ylim(-A-0.5, A+0.5)
ax_circle.set_title("Rotating Phasor (Uniform Circular Motion)")
ax_circle.set_xticks([])
ax_circle.set_yticks([])
ax_circle.grid(alpha=0.3)

# =================================================
# RIGHT PANEL — SINE WAVE WITH FREEZING
# =================================================
for i, state in enumerate(st.session_state.frozen_states):
    ax_wave.plot(
        t_wave,
        state["y_wave"],
        linewidth=2,
        alpha=0.5,
        label=f"Frozen {i+1} (φ={state['phi']:.2f})"
    )

# Live sine wave
ax_wave.plot(
    t_wave,
    y_wave,
    color='crimson',
    linewidth=3,
    label="Live wave"
)

# Instantaneous projection
ax_wave.scatter(t, y, color='black', zorder=5)
ax_wave.axhline(y, linestyle=':', color='steelblue', linewidth=2)
ax_wave.axvline(t, linestyle=':', color='gray', linewidth=1)

ax_wave.set_xlim(0, 10)
ax_wave.set_ylim(-A-0.5, A+0.5)
ax_wave.set_xlabel("Time (t)")
ax_wave.set_ylabel("Displacement y(t)")
ax_wave.set_title("Sinusoidal Waveform in Time Domain")
ax_wave.grid(alpha=0.3)
ax_wave.legend()

st.pyplot(fig)

# ---------------- Live State ----------------
with st.expander("Current Phase State"):
    st.latex(fr"\theta = \omega t + \phi = {omega:.2f}\times {t:.2f} + {phi:.2f} = {theta:.2f}")
    st.latex(fr"y(t) = {A:.2f}\sin({theta:.2f}) = {y:.2f}")
