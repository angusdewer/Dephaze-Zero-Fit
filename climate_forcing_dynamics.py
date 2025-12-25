import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# DEPHAZE INVARIANT – UNIVERSAL STRUCTURAL CONSTANT
# ============================================================

def _phi3():
    """
    Structural constant Phi^3 derived from golden-ratio topology.
    Reference: Dephaze Framework v2.0, Appendix A.
    """
    phi = (1.0 + 5.0 ** 0.5) / 2.0
    return phi ** 3

# ============================================================
# CLIMATE FORCING RUNAWAY – DEPHAZE VS. POSITIVE FEEDBACK
# ============================================================

def run_climate_forcing(
    steps=2000,
    forcing_drift=0.003, # Continuous input increase
    feedback=0.04,      # Strength of T -> F coupling
    inertia=0.01,       # Physical system resistance
    noise=0.02,         # Stochastic background
    Lambda=1.6,         # Dephaze projection strength
    seed=2025,
):
    """
    CLIMATE FORCING RUNAWAY – DEPHAZE SAMPLING PROJECTION
    
    Ontology:
      • State [T, F]: Temperature (T) and Carbon Forcing (F).
      • Baseline: Positive feedback (T-F coupling) creates runaway warming.
      • Dephaze: Identical raw samples, but Phi^3 geometric projection bounds the manifold.
      
    Key Principle (Axiom 2.5): Sustainability emerges when the system treats 
    its state magnitude as a coherence ratio (rho) and relaxes toward 
    the critical manifold (Phi^3). No time-based policy or optimization.
    """

    rng = np.random.default_rng(int(seed))
    Tn = int(steps)

    phi3 = _phi3()
    r_star = np.sqrt(phi3) # Critical radius for stability

    # State vectors: [Temperature, Forcing]
    xb = np.zeros((Tn, 2)) # Baseline
    xd = np.zeros((Tn, 2)) # Dephaze

    # Initial state (Ground state)
    xb[0] = np.array([0.1, 0.1])
    xd[0] = np.array([0.1, 0.1])

    # FAIRNESS: Identical noise path for shared shocks
    eps = rng.normal(0.0, noise, size=(Tn, 2))

    for k in range(1, Tn):

        # --- 1. BASELINE: Positive Feedback Loop ---
        Tb, Fb = xb[k - 1]
        Tb_raw = Tb + 0.05 * Fb + eps[k, 0]
        Fb_raw = Fb + forcing_drift + feedback * Tb + eps[k, 1]

        # Apply mild inertia and soft physical saturation
        Tb_raw *= (1.0 - inertia)
        Fb_raw *= (1.0 - inertia)
        xb[k] = np.array([np.tanh(Tb_raw) * 6.0, np.tanh(Fb_raw) * 6.0])

        # --- 2. DEPHAZE: Structural Self-Regulation (Axiom 2.2) ---
        Td, Fd = xd[k - 1]
        # Identical raw physics
        Td_raw = Td + 0.05 * Fd + eps[k, 0]
        Fd_raw = Fd + forcing_drift + feedback * Td + eps[k, 1]
        Td_raw *= (1.0 - inertia)
        Fd_raw *= (1.0 - inertia)

        x_raw = np.array([Td_raw, Fd_raw])
        
        # Monitor coherence ratio rho (Axiom 2.3)
        r = np.linalg.norm(x_raw) + 1e-12
        rho = (r * r) / phi3
        
        # Project toward pattern trace Omega_tr
        gain = Lambda * np.tanh(rho - 1.0)
        xd[k] = x_raw - gain * (x_raw / r)

    # Calculate boundedness
    Eb = np.linalg.norm(xb, axis=1)
    Ed = np.linalg.norm(xd, axis=1)
    bounded_b = float(np.mean(Eb < r_star))
    bounded_d = float(np.mean(Ed < r_star))

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(3, 1, figsize=(10, 10))

    # Temperature Evolution
    ax[0].plot(xb[:, 0], color='crimson', alpha=0.5, label="Baseline (Runaway Warming)")
    ax[0].plot(xd[:, 0], color='blue', linewidth=2, label="Dephaze (Bounded State)")
    ax[0].set_ylabel("Temperature (T)")
    ax[0].set_title("Climate Stability: Runaway Feedback vs. $\Phi^3$ Projection")
    ax[0].legend()

    # Forcing / Carbon load
    ax[1].plot(xb[:, 1], color='crimson', alpha=0.5, label="Baseline Load")
    ax[1].plot(xd[:, 1], color='green', label="Dephaze Load")
    ax[1].set_ylabel("Carbon Forcing (F)")
    ax[1].legend()

    # Phase Space
    ax[2].plot(xb[:, 0], xb[:, 1], color='crimson', alpha=0.3, label="Baseline Trajectory")
    ax[2].plot(xd[:, 0], xd[:, 1], color='blue', label="Dephaze Trajectory")
    ax[2].axhline(r_star, color='black', linestyle=":", alpha=0.5, label=r"Critical $r^*$")
    ax[2].set_xlabel("Temperature")
    ax[2].set_ylabel("Forcing")
    ax[2].set_title("Phase Space: Emergent Attractor (No Time)")
    ax[2].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE CLIMATE RUNAWAY REPORT\n"
        "------------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Critical Radius (r*): {r_star:.4f}\n"
        f"Boundedness (Dephaze): {bounded_d:.2f}\n"
        "Observation:\n"
        "- Baseline: Self-amplifying loops lead to max saturation (runaway).\n"
        "- Dephaze: Structural projection maintains a critical balance.\n"
        "Result: System stability is a geometric property of state space."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_climate_forcing()
    fig.savefig("climate_forcing_demo.png", dpi=150)
    print(report)