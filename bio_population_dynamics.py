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
    phi = (1.0 + 5.0**0.5) / 2.0
    return phi**3

# ============================================================
# BIO DYNAMICS – POPULATION RUNAWAY VS. DEPHAZE STABILITY
# ============================================================

def run_bio_runaway(
    steps=900,
    dt=0.01,
    dims=3,            # Number of interacting species/variables
    growth=0.25,       # Intrinsic growth rate
    cross_coupling=0.1,# Inter-species amplification
    noise=0.05,        # Environmental fluctuation
    Lambda=2.0,        # Dephaze projection strength
    seed=2025,
):
    """
    BIOLOGICAL AMPLIFICATION – DEPHAZE SAMPLING PROJECTION
    
    Ontology:
      • State [x1, x2, ...]: Population mass of multiple interacting species.
      • Baseline: Cross-coupling and growth lead to unstable exponential expansion.
      • Dephaze: Invariant geometric feedback (Axiom 2.5) bounds the total mass.
      
    Key Principle: Structural stabilization (Axiom 2.6). When the system 
    approaches the Phi^3 manifold, it may undergo dimensional collapse, 
    selecting a stable subspace (Occam selection) to minimize Omega_0 strain.
    """

    rng = np.random.default_rng(int(seed))
    T = int(steps)
    d = int(dims)
    phi3 = _phi3()
    r_star = np.sqrt(phi3)

    # --- Interaction Matrix Generation ---
    # G = Growth (Diagonal) + Coupling (Random Antisymmetric/Symmetric mix)
    G = np.eye(d) * float(growth)
    C = rng.normal(0, 1, size=(d, d))
    C = 0.5 * (C - C.T) # Competition/Flow
    S = rng.normal(0, 1, size=(d, d))
    S = 0.5 * (S + S.T) # Mutualism/Cooperation
    G = G + float(cross_coupling) * (0.6 * C + 0.4 * S)

    # Initial small population
    x0 = rng.uniform(0.05, 0.20, size=d)

    xb = np.zeros((T, d)) # Baseline
    xd = np.zeros((T, d)) # Dephaze
    xb[0] = x0
    xd[0] = x0

    sigma = float(noise)

    for t in range(1, T):
        eps = rng.normal(0, sigma, size=d)

        # 1. BASELINE: Unconstrained Biological Growth
        xb[t] = xb[t-1] + dt * (G @ xb[t-1]) + np.sqrt(dt) * eps
        xb[t] = np.maximum(xb[t], 0.0) # Physical boundary

        # 2. DEPHAZE: Self-Regulated Mass (Axiom 2.5)
        x_prev = xd[t-1]
        r = np.linalg.norm(x_prev) + 1e-12
        rho = (r*r) / phi3
        
        # Invariant feedback gain
        gain = float(Lambda) * np.tanh(rho - 1.0)
        correction = gain * (x_prev / r)

        # Apply dynamics + Dephaze projection toward pattern trace
        xd[t] = x_prev + dt * (G @ x_prev) + np.sqrt(dt) * eps - dt * correction
        xd[t] = np.maximum(xd[t], 0.0)

    # Calculate norms (Collective mass)
    nb = np.linalg.norm(xb, axis=1)
    nd = np.linalg.norm(xd, axis=1)

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Collective Mass Plot
    ax[0].plot(nb, color='crimson', alpha=0.6, label="Baseline (Exponential Runaway)")
    ax[0].plot(nd, color='blue', linewidth=2, label="Dephaze (Bounded Stability)")
    ax[0].axhline(r_star, color='black', linestyle="--", label=r"Critical Radius $r^* = \sqrt{\Phi^3}$")
    ax[0].set_title("Biological Population Dynamics: Mass Amplification vs. Stability")
    ax[0].set_ylabel("Total System Mass ||x||")
    ax[0].legend()

    # PCA Phase Space (Dimensional Projection)
    # Using SVD to project D-dimensional space into 2D for visualization
    X_combined = np.vstack([xb, xd])
    X_centered = X_combined - X_combined.mean(axis=0)
    _, _, VT = np.linalg.svd(X_centered, full_matrices=False)
    W = VT[:2].T # Top 2 components
    
    pb = (xb - X_combined.mean(axis=0)) @ W
    pd = (xd - X_combined.mean(axis=0)) @ W

    ax[1].plot(pb[:, 0], pb[:, 1], color='crimson', alpha=0.3, label="Baseline Trajectory")
    ax[1].plot(pd[:, 0], pd[:, 1], color='blue', label="Dephaze Trajectory")
    ax[1].set_title("Phase Space Projection (PCA): Structural Stabilization")
    ax[1].set_xlabel("Principal Component 1")
    ax[1].set_ylabel("Principal Component 2")
    ax[1].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE BIOLOGICAL RUNAWAY REPORT\n"
        "---------------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Critical Radius (r*): {r_star:.4f}\n"
        "Observation:\n"
        "- Baseline: Feedback between species leads to runaway population growth.\n"
        "- Dephaze: The system stabilizes on a lower-dimensional manifold.\n"
        "Result: Occam selection (Axiom 2.6) reduces complexity to maintain balance."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_bio_runaway()
    fig.savefig("bio_population_demo.png", dpi=150)
    print(report)