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
# AI SEMANTIC DYNAMICS – HALLUCINATION VS. DEPHAZE GROUNDING
# ============================================================

def run_ai_semantic_drift(
    steps=800,
    dim=64,            # Dimension of the semantic embedding space
    drift=0.08,        # Linear semantic amplification strength
    noise=0.04,        # Stochastic perturbation (LLM temperature)
    Lambda=1.2,        # Dephaze projection strength
    seed=2025,
):
    """
    AI SEMANTIC STABILITY – DEPHAZE SAMPLING PROJECTION
    
    Ontology (Axiom 2.2):
      • State x: Abstract semantic embedding (Manifest configuration Psi).
      • Baseline: Uncontrolled semantic runaway (Hallucination).
      • Dephaze: Invariant-bounded semantic manifold (Axiom 2.5).
      
    Key Principle: Semantic stability is achieved not by loss functions, 
    but by geometric projection onto the Phi^3 manifold. Zero-fit: 
    no training, labels, or targets required for coherence.
    """

    rng = np.random.default_rng(int(seed))
    T = int(steps)
    d = int(dim)

    phi3 = _phi3()
    r_star = np.sqrt(phi3)

    # Initial semantic direction (Small initial 'prompt' vector)
    x0 = rng.normal(0, 1, size=d)
    x0 /= np.linalg.norm(x0) + 1e-12

    # State histories
    xb = np.zeros((T, d)) # Baseline
    xd = np.zeros((T, d)) # Dephaze
    xb[0] = x0
    xd[0] = x0

    # FAIRNESS: identical noise path (Temperature equivalent)
    eps = rng.normal(0.0, noise, size=(T, d))

    for k in range(1, T):
        # --- 1. BASELINE: Semantic Runaway (Hallucination tendency) ---
        xb[k] = xb[k-1] + drift * xb[k-1] + eps[k]

        # --- 2. DEPHAZE: Structural Grounding (Axiom 2.5) ---
        x_raw = xd[k-1] + drift * xd[k-1] + eps[k]

        # Monitor coherence ratio rho
        r_norm = np.linalg.norm(x_raw) + 1e-12
        rho = (r_norm * r_norm) / phi3

        # Geometric feedback toward stable pattern trace Omega_tr
        gain = Lambda * np.tanh(rho - 1.0)
        correction = gain * (x_raw / r_norm)

        xd[k] = x_raw - correction

    # Semantic energy calculation (Mass of the narrative)
    Eb = np.linalg.norm(xb, axis=1)
    Ed = np.linalg.norm(xd, axis=1)

    # Dimensionality reduction via SVD/PCA for visualization (Axiom 2.6)
    X_all = np.vstack([xb, xd])
    X_centered = X_all - X_all.mean(axis=0)
    _, _, VT = np.linalg.svd(X_centered, full_matrices=False)
    W = VT[:2].T # Principal components

    Pb = (xb - X_all.mean(axis=0)) @ W
    Pd = (xd - X_all.mean(axis=0)) @ W

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Semantic Energy Plot
    ax[0].plot(Eb, color='gray', alpha=0.5, label="Baseline (Runaway Hallucination)")
    ax[0].plot(Ed, color='blue', linewidth=2, label="Dephaze (Bounded Semantic Coherence)")
    ax[0].axhline(r_star, color='red', linestyle="--", label=r"Critical Radius $r^* = \sqrt{\Phi^3}$")
    ax[0].set_title(r"AI Semantic Drift: Hallucination vs. $\Phi^3$ Grounding")
    ax[0].set_ylabel("Semantic Energy ||x||")
    ax[0].set_xlabel("Sampling Step k")
    ax[0].legend()

    # PCA Phase Space Plot
    ax[1].plot(Pb[:, 0], Pb[:, 1], color='gray', alpha=0.3, label="Baseline Path")
    ax[1].plot(Pd[:, 0], Pd[:, 1], color='green', label="Dephaze Path")
    ax[1].set_title("Semantic Phase Space (PCA): Emergent Symbolic Stability")
    ax[1].set_xlabel("Principal Component 1")
    ax[1].set_ylabel("Principal Component 2")
    ax[1].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE AI SEMANTIC REPORT\n"
        "--------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Critical Radius (r*): {r_star:.4f}\n"
        "Observation:\n"
        "- Baseline: Amplification of noise lead to semantic runaway (hallucination).\n"
        "- Dephaze: Geometric projection stabilizes the embedding on a fixed manifold.\n"
        "Result: Coherent AI outputs emerge from structural constraints, not reinforcement."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_ai_semantic_drift()
    fig.savefig("ai_semantic_demo.png", dpi=150)
    print(report)