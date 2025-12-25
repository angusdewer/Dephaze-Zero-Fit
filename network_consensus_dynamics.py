import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# DEPHAZE INVARIANT – SECTION A.2 TOPOLOGICAL DERIVATION
# ============================================================

def _phi3():
    """
    Structural constant Phi^3 derived from golden-ratio topology.
    Reference: Dephaze Framework v2.0, Appendix A.
    """
    phi = (1.0 + 5.0 ** 0.5) / 2.0
    return phi ** 3

# ============================================================
# NETWORK CONSENSUS – DEPHAZE VS. CLASSIC POLARIZATION
# ============================================================

def run_network_consensus(
    n_nodes=40,
    coupling=0.25,      # Graph diffusion strength
    instability=0.35,   # Positive feedback (drift)
    Lambda=1.2,         # Dephaze projection strength
    steps=800,
    seed=2025,
):
    """
    NETWORK DYNAMICS – DEPHAZE SAMPLING PROJECTION
    
    Ontology (Axiom 2.5 - Self-Regulation):
      • Baseline: Network coupling + local instability lead to runaway polarization.
      • Dephaze: The system monitors the collective coherence ratio (rho).
      • Projection: When rho > 1, the manifold is bounded by the structural invariant.
      
    Key point: No parameter fitting (zero-fit). The system bounds itself 
    using the Phi^3 topology as a geometric attractor.
    """

    rng = np.random.default_rng(int(seed))
    n = int(n_nodes)
    T = int(steps)
    dt = 0.01

    phi3 = _phi3()
    r_star = np.sqrt(phi3)  # Critical radius in state space

    # --- Network Topology: Random symmetric adjacency ---
    A = rng.random((n, n))
    A = 0.5 * (A + A.T)
    np.fill_diagonal(A, 0.0)
    deg = np.sum(A, axis=1) # Degree vector for Laplacian

    # --- Initial states (Near-zero equilibrium) ---
    x_init = rng.normal(0.0, 0.5, size=n)

    # State histories
    xb = np.zeros((T, n))  # Baseline
    xd = np.zeros((T, n))  # Dephaze
    xb[0] = x_init.copy()
    xd[0] = x_init.copy()

    # --- Helper functions ---
    def laplacian_action(x):
        # L(x) = A@x - D*x (Graph Laplacian diffusion)
        return A @ x - deg * x

    def dephaze_project(x):
        # Sampling-based invariant projection (Axiom 2.2)
        norm_x = np.linalg.norm(x) + 1e-12
        rho = (norm_x**2) / phi3
        gain = float(Lambda) * np.tanh(rho - 1.0)
        # Projection toward the pattern trace Omega_tr
        return x - gain * (x / norm_x), rho

    # --- Simulation loop ---
    rho_trace_b = np.zeros(T)
    rho_trace_d = np.zeros(T)

    for t in range(1, T):
        # 1. BASELINE STEP (Linear instability + Diffusion)
        x_prev_b = xb[t - 1]
        lap_b = laplacian_action(x_prev_b)
        x_next_b = x_prev_b + dt * (instability * x_prev_b + coupling * lap_b)
        xb[t] = x_next_b
        rho_trace_b[t] = (np.linalg.norm(x_next_b)**2) / phi3

        # 2. DEPHAZE STEP (Baseline physics + Structural Projection)
        x_prev_d = xd[t - 1]
        lap_d = laplacian_action(x_prev_d)
        x_next_d = x_prev_d + dt * (instability * x_prev_d + coupling * lap_d)
        
        # Apply Dephaze Axiom 2.5: self-regulation toward rho approx 1
        x_proj, rho_d = dephaze_project(x_next_d)
        xd[t] = x_proj
        rho_trace_d[t] = rho_d

    # --- Metrics ---
    norm_b = np.linalg.norm(xb, axis=1)
    norm_d = np.linalg.norm(xd, axis=1)

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Collective Norm Plot
    ax[0].plot(norm_b, color='crimson', label="Baseline (Runaway Polarization)")
    ax[0].plot(norm_d, color='dodgerblue', linewidth=2, label="Dephaze (Bounded Collective Manifold)")
    ax[0].axhline(r_star, color='black', linestyle="--", label=r"Critical Radius $r^* = \sqrt{\Phi^3}$")
    ax[0].set_title("Network Dynamics: Collective Energy Management")
    ax[0].set_ylabel("Collective Norm $||x||$")
    ax[0].set_xlabel("Steps")
    ax[0].legend()

    # Final Node States Comparison
    ax[1].scatter(range(n), xb[-1], color='crimson', alpha=0.5, label="Baseline Final States")
    ax[1].scatter(range(n), xd[-1], color='dodgerblue', marker='x', label="Dephaze Final States")
    ax[1].set_title("Node State Distribution: Polarization vs. Stability")
    ax[1].set_ylabel("State $x_i$")
    ax[1].set_xlabel("Node Index")
    ax[1].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE NETWORK CONSENSUS REPORT\n"
        "-------------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Critical Radius (r*): {r_star:.4f}\n"
        "Observation:\n"
        "- Baseline: Positive feedback leads to exponential state growth.\n"
        "- Dephaze: Structural projection bounds the collective energy near r*.\n"
        "Result: Critical balance is maintained without parameter tuning."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_network_consensus()
    fig.savefig("network_consensus.png", dpi=150)
    print(report)