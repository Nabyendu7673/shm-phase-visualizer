import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Phase Evolution in SHM",
    layout="wide"
)

st.title("Phase Evolution in Simple Harmonic Motion")
st.caption(
    "A phase-based visualization using θ = ωt + φ and y(t) = A sin θ"
)

# -------------------------------------------------
# Sidebar controls
# -------------------------------------------------
st.sidebar.header("Control Parameters")

A = st.sidebar.slider("Amplitude (A)", 0.5, 5.0, 2.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.5, 5.0, 1.0, 0.1)

phi_map = {
    "0": 0,
    "π/2": np.pi / 2,
    "π": np.pi,
    "3π/2": 3 * np.pi / 2
}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

animate = st.sidebar.checkbox("▶ Play / Pause Animation")

t_manual = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.0, 0.01)

# -------------------------------------------------
# Time handling
# -------------------------------------------------
if "t" not in st.session_state:
    st.session_state.t = t_manual

if animate:
    st.session_state.t += 0.03
    time.sleep(0.03)
else:
    st.session_state.t = t_manual

t = st.session_state.t

# -------------------------------------------------
# Core phase physics
# -------------------------------------------------
theta = omega * t + phi
y = A * np.sin(theta)

# -------------------------------------------------
# 🔽 DROPDOWN: Governing Equations
# -------------------------------------------------
with st.expander("📐 Governing Equations (click to expand)", expanded=True):
    st.latex(r"\theta(t) = \omega t + \phi")
    st.latex(r"y(t) = A \sin(\theta)")
    st.latex(r"\frac{d\theta}{dt} = \omega")

# -------------------------------------------------
# 🔽 DROPDOWN: Live Substituted Equations
# -------------------------------------------------
with st.expander("🧮 Live Equation Evaluation", expanded=True):
    st.latex(
        rf"\theta(t) = ({omega}) \times ({t:.2f}) + ({phi_label}) = {theta:.2f}\,\text{{rad}}"
    )
    st.latex(
        rf"y(t) = ({A}) \sin({theta:.2f}) = {y:.2f}"
    )

    st.markdown(
        """
**Note:**  
• Changing **ω** changes the *rate of phase evolution*  
• Changing **φ** changes the *starting phase*  
• Changing **A** changes only the *amplitude*
"""
    )

# -------------------------------------------------
# Data for waveform
# -------------------------------------------------
t_full = np.linspace(0, 10, 1000)
theta_full = omega * t_full + phi
y_full = A * np.sin(theta_full)

# -------------------------------------------------
# Plotting
# -------------------------------------------------
fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(15, 6),
    gridspec_kw={"width_ratios": [1, 2]}
)

# ------------------ Left: Phase circle ------------------
circle = plt.Circle((0, 0), A, fill=False, linestyle="--", alpha=0.6)
ax1.add_artist(circle)

x = A * np.cos(theta)
ax1.arrow(
    0, 0, x, y,
    head_width=0.08, head_length=0.12,
    fc="crimson", ec="crimson", linewidth=2
)

# θ arc
theta_arc = np.linspace(0, theta, 200)
ax1.plot(A * np.cos(theta_arc), A * np.sin(theta_arc),
         color="orange", linewidth=2)

ax1.text(
    0.05, 0.93,
    rf"$\theta = {theta:.2f}\,\mathrm{{rad}}$",
    transform=ax1.transAxes,
    fontsize=12,
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.7)
)

ax1.set_aspect("equal")
ax1.set_xlim(-A - 1, A + 1)
ax1.set_ylim(-A - 1, A + 1)
ax1.set_title("Instantaneous Phase Representation")
ax1.grid(alpha=0.25)

# ------------------ Right: SHM waveform ------------------
ax2.plot(t_full, y_full, color="steelblue", linewidth=2, alpha=0.7)
ax2.plot(t, y, "ro")

ax2.text(
    0.02, 0.92,
    rf"$y(t) = A\sin(\omega t + \phi)$",
    transform=ax2.transAxes,
    fontsize=12,
    bbox=dict(facecolor="white", alpha=0.7)
)

ax2.set_xlim(0, 10)
ax2.set_ylim(-A - 1, A + 1)
ax2.set_title("Simple Harmonic Motion")
ax2.set_xlabel("Time (t)")
ax2.set_ylabel("Displacement y")
ax2.grid(alpha=0.25)

st.pyplot(fig)

# -------------------------------------------------
# 🔽 DROPDOWN: Phase interpretation
# -------------------------------------------------
with st.expander("🧠 Interpretation of Initial Phase φ"):
    if phi == 0:
        txt = "Particle starts from the **mean position**, moving in the **positive direction**."
    elif np.isclose(phi, np.pi / 2):
        txt = "Particle starts from an **extreme position**."
    elif np.isclose(phi, np.pi):
        txt = "Particle starts from the **mean position**, moving in the **negative direction**."
    else:
        txt = "Initial position and direction depend on the chosen phase."

    st.markdown(
        f"""
• Initial phase: **φ = {phi_label}**  
• Phase at t = 0: **θ(0) = φ**  

**Meaning:**  
{txt}
"""
    )
