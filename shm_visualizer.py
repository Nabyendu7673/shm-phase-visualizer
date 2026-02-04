import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# ================= Page Setup =================
st.set_page_config(page_title="SHM Projection", layout="wide")
st.title("Harmonic Motion: UCM Projection")

# ================= Sidebar =================
st.sidebar.header("Physical Parameters")
A = st.sidebar.slider("Amplitude (A)", 0.5, 5.0, 2.0, 0.1)
omega = st.sidebar.slider("Angular Frequency (ω)", 0.1, 5.0, 1.0, 0.1)

phi_map = {"0": 0.0, "π/2": np.pi/2, "π": np.pi, "3π/2": 3*np.pi/2}
phi_label = st.sidebar.selectbox("Initial Phase (φ)", list(phi_map.keys()))
phi = phi_map[phi_label]

t = st.sidebar.slider("Time (t)", 0.0, 10.0, 0.01)

col1, col2 = st.sidebar.columns(2)
freeze = col1.button("📌 Freeze State")
reset = col2.button("♻ Reset All")

# ================= Session State =================
if "frozen" not in st.session_state:
    st.session_state.frozen = []

if reset:
    st.session_state.frozen = []
    st.rerun()

# ================= Physics Math =================
theta = omega * t + phi
x = A * np.cos(theta)
y = A * np.sin(theta)

color_cycle = plt.cm.tab10.colors

if freeze:
    idx = len(st.session_state.frozen)
    color = color_cycle[idx % len(color_cycle)]
    # Store parameters: (omega, phase, amplitude, current_theta, color)
    st.session_state.frozen.append((omega, phi, A, theta, color))

# ================= Plotting =================
fig, (ax_c, ax_s) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1, 2]})

# --- Left: Circular Motion (Phasor) ---
circle = plt.Circle((0, 0), A, fill=False, linestyle="--", color="gray", alpha=0.5)
ax_c.add_artist(circle)
ax_c.axhline(0, color="black", linewidth=0.8)
ax_c.axvline(0, color="black", linewidth=0.8)

# Draw Frozen Phasors
for ωf, φf, Af, θf, col in st.session_state.frozen:
    xf = Af * np.cos(θf)
    yf = Af * np.sin(θf)
    ax_c.arrow(0, 0, xf, yf, color=col, head_width=0.1, length_includes_head=True, alpha=0.6)

# Draw Live Phasor (Red)
ax_c.arrow(0, 0, x, y, color="red", head_width=0.15, length_includes_head=True, zorder=5)

# Visual Projections (Dotted lines)
ax_c.plot([x, x], [0, y], linestyle=":", color="red", alpha=0.3) # y-projection
ax_c.plot([0, x], [y, y], linestyle=":", color="red", alpha=0.3) # x-projection

ax_c.set_xlim(-5.5, 5.5)
ax_c.set_ylim(-5.5, 5.5)
ax_c.set_aspect("equal")
ax_c.set_xlabel("X (Cos Projection)")
ax_c.set_ylabel("Y (Sin Projection)")
ax_c.set_title("Uniform Circular Motion")

# --- Right: SHM Wave ---
t_vals = np.linspace(0, 10, 1000)

# Logic for Wave drawing
if not st.session_state.frozen:
    # No frozen states? Show the "Live Preview" wave
    y_live_wave = A * np.sin(omega * t_vals + phi)
    ax_s.plot(t_vals, y_live_wave, color="black", linewidth=2, label="Live Preview")
else:
    # Once frozen, show ONLY the frozen history
    for ωf, φf, Af, θf, col in st.session_state.frozen:
        y_frozen = Af * np.sin(ωf * t_vals + φf)
        ax_s.plot(t_vals, y_frozen, color=col, linestyle="--", linewidth=1.5)

# Horizontal connector (Connects circle's Y to Wave's Y)
# We use a connection line from the circle plot to the wave plot
# In Streamlit/Matplotlib, we can simulate this with a marker at (0, y)
ax_s.plot([0, t], [y, y], linestyle=":", color="red", alpha=0.5)
ax_s.plot(t, y, marker="o", color="red", markersize=8, zorder=10)

ax_s.set_xlim(0, 10)
ax_s.set_ylim(-5.5, 5.5)
ax_s.set_xlabel("Time (t)")
ax_s.set_ylabel("Displacement y(t)")
ax_s.set_title("SHM as Projection of UCM")
ax_s.grid(True, alpha=0.3)

st.pyplot(fig)

# ================= Math & Explanation =================


with st.expander("📐 Mathematical Relationship", expanded=True):
    st.write("The vertical position $y(t)$ of a point moving in a circle is equivalent to Simple Harmonic Motion:")
    st.latex(rf"y(t) = A \sin(\omega t + \phi)")
    st.write(f"**Current Parameters:** $A={A}$, $\omega={omega}$, $\phi={phi_label}$")
    
    if st.session_state.frozen:
        st.info(f"You have {len(st.session_state.frozen)} frozen state(s) displayed.")

st.markdown("""
**Instructions:**
1. Adjust the **Amplitude** and **Frequency** to see the live red dot change.
2. Click **Freeze State** to save the current wave path. 
3. The solid black line will disappear on the first freeze, leaving only your saved paths!
""")
