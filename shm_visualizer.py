import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(page_title="UCM → SHM Visualizer", layout="wide")
st.title("Uniform Circular Motion → Simple Harmonic Motion")

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("Parameters")

A = st.sidebar.slider("Amplitude (A)", 0.5, 5.0, 2.0)
omega = st.sidebar.slider("Angular frequency (ω)", 0.5, 5.0, 1.0)
phi = st.sidebar.slider("Phase constant (ϕ)", 0.0, 2*np.pi, 0.0)
t = st.sidebar.slider("Time (t)", 0.0, 10.0, 1.0)

theta = omega * t + phi

# -------------------------------
# Session State for Freezing
# -------------------------------
if "freezers" not in st.session_state:
    st.session_state.freezers = []

if st.sidebar.button("❄️ Freeze Current State"):
    st.session_state.freezers.append({
        "theta": theta,
        "A": A,
        "omega": omega,
        "phi": phi
    })

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2 = st.tabs(["📈 Visualisation", "📐 Equations"])

# ===============================
# TAB 1 — VISUALISATION
# ===============================
with tab1:
    col1, col2 = st.columns(2)

    # ---------- CIRCLE PLOT ----------
    with col1:
        fig1, ax1 = plt.subplots(figsize=(5, 5))
        circle = plt.Circle((0, 0), A, fill=False)
        ax1.add_artist(circle)

        # Current phasor
        x = A * np.cos(theta)
        y = A * np.sin(theta)
        ax1.plot([0, x], [0, y], linewidth=3)
        ax1.scatter(x, y, s=80)

        # Variable labels (current)
        ax1.text(x*1.05, y*1.05, r"$\theta$", fontsize=12)
        ax1.text(A, 0, r"$A$", fontsize=12)

        # Frozen states
        colors = plt.cm.tab10.colors
        for i, fz in enumerate(st.session_state.freezers):
            th = fz["theta"]
            xf = fz["A"] * np.cos(th)
            yf = fz["A"] * np.sin(th)

            ax1.plot([0, xf], [0, yf], color=colors[i % 10], alpha=0.7)
            ax1.scatter(xf, yf, color=colors[i % 10])

            # smaller labels so they don't coincide
            ax1.text(xf*1.03, yf*1.03,
                     rf"$\theta_{i+1}$",
                     fontsize=9,
                     color=colors[i % 10])

        ax1.set_aspect("equal")
        ax1.set_xlim(-A-1, A+1)
        ax1.set_ylim(-A-1, A+1)
        ax1.set_title("Uniform Circular Motion")
        ax1.set_xlabel("x")
        ax1.set_ylabel("y")
        st.pyplot(fig1)

    # ---------- SINE WAVE ----------
    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        t_vals = np.linspace(0, 10, 1000)
        y_vals = A * np.sin(omega * t_vals + phi)

        # Current sine wave
        ax2.plot(t_vals, y_vals, linewidth=2)

        # Frozen sine waves
        for i, fz in enumerate(st.session_state.freezers):
            y_freeze = fz["A"] * np.sin(fz["omega"] * t_vals + fz["phi"])
            ax2.plot(t_vals, y_freeze,
                     color=colors[i % 10],
                     linestyle="--",
                     label=f"Freezer {i+1}")

        ax2.axvline(t, linestyle=":", alpha=0.6)
        ax2.set_title("SHM (Projection of UCM)")
        ax2.set_xlabel("Time (t)")
        ax2.set_ylabel("Displacement y(t)")
        ax2.legend()
        st.pyplot(fig2)

# ===============================
# TAB 2 — EQUATIONS
# ===============================
with tab2:
    st.subheader("Mathematical Description from Frozen States")

    if not st.session_state.freezers:
        st.info("Freeze at least one state to generate equations.")
    else:
        for i, fz in enumerate(st.session_state.freezers):
            st.markdown(f"""
### ❄️ Freezer {i+1}

**Instantaneous phase of the particle**
\[
\theta(t) = \omega t + \phi
\]

**Substituting frozen values**
\[
\theta(t) = {fz['omega']:.2f}t + {fz['phi']:.2f}
\]

**Displacement in simple harmonic motion (projection of UCM)**
\[
y(t) = A \sin\bigl[\theta(t)\bigr]
\]

**Final equation**
\[
y(t) = {fz['A']:.2f}\,\sin\left({fz['omega']:.2f}t + {fz['phi']:.2f}\right)
\]
""")
