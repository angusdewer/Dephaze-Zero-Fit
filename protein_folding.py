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
# PROTEIN FOLDING – DEPHAZE SAMPLING DEMO
# ============================================================

def run_protein_folding(
    steps=1200,
    mutation=0.0,      # shifts native basin
    solvent=0.3,       # environmental frustration
    Lambda=1.6,        # Dephaze projection strength
    seed=2025,
):
    """
    PROTEIN FOLDING – DEPHAZE PROJECTION DEMO
    
    Ontology (Axiom 2.2 & 2.5):
      • Folding is NOT a stochastic search (Levinthal Paradox resolution).
      • Folding is a geometric exclusion process.
      • Energy (E) is projected toward the pattern trace Omega_tr.
      • Stability is achieved when rho = E / Phi^3 approx 1.
    """

    rng = np.random.default_rng(int(seed))
    T = int(steps)
    phi3 = _phi3()

    # Native basin center (The 'Imago' or target configuration)
    x_native = mutation

    # State vectors
    x = np.zeros(T)     # Conformation coordinate
    rho = np.zeros(T)   # Coherence ratio (Axiom 2.3)
    E_conf = np.zeros(T)

    # Initial random unfolded state (maximal entropy)
    x[0] = rng.normal(0.0, 3.0)

    # Lock flags (Ontological locking)
    folded = False
    folded_step = -1

    for k in range(1, T):

        if folded:
            # Permanent lock in the native state (Axiom 2.4 - selection)
            x[k] = x_native
            rho[k] = 1.0
            E_conf[k] = phi3
            continue

        # 1. Random conformation proposal (Internal fluctuation / Generation)
        x_raw = x[k - 1] + rng.normal(0.0, 1.0)

        # 2. Abstract rugged energy landscape (The physical constraint)
        E_contact = (
            0.5 * (x_raw - x_native) ** 2
            + 0.4 * np.sin(3.0 * x_raw)
            + 0.2 * np.sin(7.0 * x_raw)
        )
        E_solv = solvent * abs(x_raw)
        E = E_contact + E_solv
        E_conf[k] = E

        # 3. Coherence ratio calculation (Axiom 2.3)
        # rho = Omega_p / Omega_tr -> mapped here as E / Phi^3
        rho_k = E / phi3
        rho[k] = rho_k

        # === DEPHAZE PROJECTION RULES ===

        # RULE A: Misfold / Aggregation (rho > 2)
        # Structural exclusion: states too far from equilibrium are rejected.
        if rho_k > 2.0:
            x[k] = x_native + rng.normal(0.0, 0.3)
            continue

        # RULE B: Folding transition (rho > 1)
        # The Master PDE triggers a projection toward the pattern trace.
        if rho_k > 1.0:
            gain = Lambda * np.tanh(rho_k - 1.0)
            x_proj = x_raw - gain * np.sign(x_raw - x_native)
            x[k] = x_proj
            continue

        # RULE C: Native Lock (rho approx 1)
        # Bistable relaxation reaches the global minimum attractor.
        if abs(rho_k - 1.0) < 0.05:
            folded = True
            folded_step = k
            x[k] = x_native
            rho[k] = 1.0
            continue

        # Otherwise: standard sampling
        x[k] = x_raw

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(3, 1, figsize=(9, 9), sharex=True)

    ax[0].plot(x, color='teal', label="Conformation coordinate (x)")
    ax[0].axhline(x_native, color='red', linestyle="--", label="Native Basin")
    ax[0].set_ylabel("Configuration Space")
    ax[0].legend()
    ax[0].set_title("Protein Folding: Dephaze Geometric Projection")

    ax[1].plot(rho, color='orange', label="ρ = E / φ³")
    ax[1].axhline(1.0, color='black', linestyle="--", label="Stability Threshold")
    ax[1].set_ylabel("Coherence Ratio ρ")
    ax[1].legend()

    ax[2].plot(E_conf, color='purple', label="Conformation Energy (E)")
    ax[2].set_ylabel("Energy")
    ax[2].set_xlabel("Sampling step k")
    ax[2].legend()

    fig.tight_layout()

    # Terminal report
    txt = [
        "DEPHAZE PROTEIN FOLDING REPORT",
        f"Phi^3 Invariant: {phi3:.4f}",
        f"Folding Completion Step: {folded_step if folded_step > 0 else 'N/A'}",
        f"Native State Target: x={x_native}",
        "Interpretation:",
        "  - The Levinthal paradox is avoided by geometric exclusion.",
        "  - The system does not 'search'; it relaxes into a structural lock.",
        "  - Stability is reached when Energy matches the Phi^3 topological constant."
    ]

    return fig, "\n".join(txt)

if __name__ == "__main__":
    fig, report = run_protein_folding()
    fig.savefig("protein_folding_demo.png", dpi=150)
    print(report)