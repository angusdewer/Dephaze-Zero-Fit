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
# MEME PROPAGATION – DEPHAZE VS. RUNAWAY NARRATIVES
# ============================================================

def run_meme_propagation(
    steps=1500,
    dim=64,            # Dimension of the narrative state space
    exposure=0.06,     # External meme injection strength
    alignment=0.02,    # Internal self-amplification (runaway)
    noise=0.04,        # Stochastic perturbation
    Lambda=1.6,        # Dephaze projection strength
    seed=2025,
):
    """
    INFORMATION DYNAMICS – DEPHAZE SAMPLING PROJECTION
    
    Ontology:
      • State x: Collective narrative vector in R^d.
      • Baseline: Positive feedback (alignment) leads to runaway narrative energy.
      • Dephaze: Identical sampling, but applies Phi^3 geometric projection.
      
    Key Principle: No training, no loss functions, no fitting. 
    The "meaning" or "adoption" emerges as a stable pattern trace (Omega_tr)
    when the system reaches the critical coherence ratio rho approx 1.
    """

    rng = np.random.default_rng(int(seed))
    T = int(steps)
    d = int(dim)

    phi3 = _phi3()
    r_star = np.sqrt(phi3)

    # Meme direction (Target topic vector / Imago axis)
    u = rng.normal(0, 1, size=d)
    u /= np.linalg.norm(u) + 1e-12

    # Initial collective state (Neutral ground state)
    x0 = rng.normal(0, 0.15, size=d)

    # Histories
    xb = np.zeros((T, d))
    xd = np.zeros((T, d))
    xb[0] = x0
    xd[0] = x0

    # Identical noise path for fairness
    eps = rng.normal(0.0, noise, size=(T, d))

    rho_b = np.zeros(T)
    rho_d = np.zeros(T)
    s_b = np.zeros(T) # Adoption observable baseline
    s_d = np.zeros(T) # Adoption observable dephaze

    def _observe(x):
        # Narrative adoption: projection on meme axis mapped to [-1, 1]
        return float(np.tanh(np.dot(x, u)))

    for k in range(1, T):
        # --- 1. BASELINE: Exposure + Self-Amplification ---
        x_raw_b = xb[k - 1] + exposure * u + alignment * xb[k - 1] + eps[k]
        rb = np.linalg.norm(x_raw_b) + 1e-12
        rho_b[k] = (rb * rb) / phi3
        xb[k] = x_raw_b
        s_b[k] = _observe(xb[k])

        # --- 2. DEPHAZE: Structural Projection (Axiom 2.5) ---
        x_raw_d = xd[k - 1] + exposure * u + alignment * xd[k - 1] + eps[k]
        rd = np.linalg.norm(x_raw_d) + 1e-12
        rho = (rd * rd) / phi3
        rho_d[k] = rho

        # Feedback controller toward critical balance rho approx 1
        gain = Lambda * np.tanh(rho - 1.0)
        xd[k] = x_raw_d - gain * (x_raw_d / rd)
        s_d[k] = _observe(xd[k])

    # Narrative Energy Calculation
    Eb = np.linalg.norm(xb, axis=1)
    Ed = np.linalg.norm(xd, axis=1)

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # Energy Plot
    ax[0].plot(Eb, color='gray', alpha=0.6, label="Baseline Energy (Runaway)")
    ax[0].plot(Ed, color='blue', linewidth=2, label="Dephaze Energy (Bounded)")
    ax[0].axhline(r_star, color='black', linestyle="--", label=r"Critical Radius $r^* = \sqrt{\Phi^3}$")
    ax[0].set_ylabel("Narrative Energy ||x||")
    ax[0].set_title("Meme Propagation: Narrative Stability vs. Explosion")
    ax[0].legend()

    # Coherence Ratio Plot
    ax[1].plot(rho_b, color='gray', alpha=0.6, label="Baseline ρ")
    ax[1].plot(rho_d, color='orange', label="Dephaze ρ")
    ax[1].axhline(1.0, color='black', linestyle="--", label="Critical ρ = 1")
    ax[1].set_ylabel("Coherence Ratio ρ")
    ax[1].legend()

    # Adoption/Belief Plot
    ax[2].plot(s_b, color='gray', alpha=0.6, label="Baseline Adoption")
    ax[2].plot(s_d, color='green', label="Dephaze Adoption")
    ax[2].axhline(0.85, color='red', linestyle=":", label="Lock Band")
    ax[2].axhline(-0.85, color='red', linestyle=":")
    ax[2].set_xlabel("Sampling Step k")
    ax[2].set_ylabel("Belief Strength (s)")
    ax[2].set_title("Social Observable: Bistable Narrative Lock")
    ax[2].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE MEME PROPAGATION REPORT\n"
        "------------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Critical Radius (r*): {r_star:.4f}\n"
        "Observation:\n"
        "- Baseline: Self-amplification leads to uncontrolled narrative energy growth.\n"
        "- Dephaze: Structural projection keeps the narrative bounded and critical.\n"
        "Interpretation: Belief 'locks' (s > 0.85) emerge from geometric stability."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_meme_propagation()
    fig.savefig("meme_propagation_demo.png", dpi=150)
    print(report)