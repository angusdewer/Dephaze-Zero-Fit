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
# FINANCIAL DYNAMICS – LEVERAGE BUBBLE VS. DEPHAZE BOUNDS
# ============================================================

def run_financial_bubble(
    steps=1200,
    drift=0.015,         # Natural asset growth
    leverage_gain=0.03,  # Positive feedback strength
    noise=0.02,          # Market shocks
    Lambda=1.6,          # Dephaze projection strength
    seed=2025,
):
    """
    FINANCIAL LEVERAGE BUBBLE – DEPHAZE SAMPLING PROJECTION
    
    Ontology:
      • State [Price, Leverage]: Manifest configuration in economic space.
      • Baseline: Feedback loop leads to systemic instability and bubble burst.
      • Dephaze: Invariant-bounded manifold via structural projection (Axiom 2.5).
      
    Key Principle: Economic 'value' is treated as a projection. Stability is 
    maintained not by external policy, but by the structural limit of the 
    underlying state space (Phi^3). Zero-fit approach: no market tuning needed.
    """

    rng = np.random.default_rng(int(seed))
    T = int(steps)
    phi3 = _phi3()
    r_star = np.sqrt(phi3) # Critical stability radius

    # state = [asset price, leverage ratio]
    xb = np.zeros((T, 2), dtype=float)
    xd = np.zeros((T, 2), dtype=float)

    # Initial neutral state
    xb[0] = np.array([1.0, 0.6], dtype=float)
    xd[0] = xb[0].copy()

    # FAIRNESS: Shared noise path for identical market shocks
    eps_price = rng.normal(0.0, float(noise), size=T)
    eps_lev = rng.normal(0.0, float(noise), size=T)

    rho_b = np.zeros(T, dtype=float)
    rho_d = np.zeros(T, dtype=float)

    def clamp_domain(s):
        # Physical boundary: Price and leverage cannot be negative
        return np.array([max(float(s[0]), 1e-9), max(float(s[1]), 0.0)], dtype=float)

    def baseline_step(s, ex, el):
        x, l = float(s[0]), float(s[1])
        # Price increases with leverage; leverage increases with price growth
        dx = drift * x + leverage_gain * l + ex
        dl = leverage_gain * dx + el
        return np.array([x + dx, l + dl], dtype=float)

    def dephaze_project(s):
        # Sampling projection based on collective energy (Axiom 2.2)
        r = np.linalg.norm(s) + 1e-12
        rho = (r * r) / phi3
        gain = float(Lambda) * np.tanh(rho - 1.0)
        return s - gain * (s / r), rho

    # --- Simulation Loop ---
    for t in range(1, T):
        ex, el = float(eps_price[t]), float(eps_lev[t])

        # 1. BASELINE: Pure feedback-driven growth
        sb = baseline_step(xb[t - 1], ex, el)
        sb = clamp_domain(sb)
        xb[t] = sb
        rho_b[t] = (np.linalg.norm(sb)**2) / phi3

        # 2. DEPHAZE: Same physics + Structural Self-Regulation (Axiom 2.5)
        sd = baseline_step(xd[t - 1], ex, el)
        sd_proj, rho_val = dephaze_project(sd)
        sd_proj = clamp_domain(sd_proj)
        xd[t] = sd_proj
        rho_d[t] = rho_val

    # Metrics for plotting
    norm_b = np.linalg.norm(xb, axis=1)
    norm_d = np.linalg.norm(xd, axis=1)
    stress_b = xb[:, 0] * xb[:, 1] # Systemic stress metric
    stress_d = xd[:, 0] * xd[:, 1]

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(3, 1, figsize=(10, 10))

    # Energy/Bubble Plot (Log Scale for visualization stability)
    ax[0].plot(np.log10(norm_b + 1e-12), color='gray', alpha=0.5, label="Baseline (Runaway Bubble)")
    ax[0].plot(np.log10(norm_d + 1e-12), color='blue', linewidth=2, label="Dephaze (Bounded Economy)")
    ax[0].axhline(np.log10(r_star), color='red', linestyle="--", label=r"Critical Radius $\log_{10}(r^*)$")
    ax[0].set_title("Financial Dynamics: Market Energy Management")
    ax[0].set_ylabel(r"$\log_{10}(||state||)$")
    ax[0].legend()

    # Systemic Stress Plot
    ax[1].plot(stress_b, color='gray', alpha=0.5, label="Baseline Stress")
    ax[1].plot(stress_d, color='purple', label="Dephaze Stress (Self-Regulated)")
    ax[1].set_title("Systemic Financial Stress ($Price \times Leverage$)")
    ax[1].set_ylabel("Stress Level")
    ax[1].legend()

    # Phase Space Plot
    ax[2].plot(xb[:, 0], xb[:, 1], color='gray', alpha=0.3, label="Baseline Path")
    ax[2].plot(xd[:, 0], xd[:, 1], color='green', label="Dephaze Path")
    ax[2].set_xlabel("Asset Price")
    ax[2].set_ylabel("Leverage")
    ax[2].set_title("Financial Phase Space Trajectory")
    ax[2].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE FINANCIAL STABILITY REPORT\n"
        "----------------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Critical Radius (r*): {r_star:.4f}\n"
        "Observation:\n"
        "- Baseline: Positive feedback between price and leverage leads to exponential instability.\n"
        "- Dephaze: Structural projection bounds the market manifold near r*.\n"
        "Result: Systemic stress is managed via internal dynamics, preventing runaway bubbles."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_financial_bubble()
    fig.savefig("financial_bubble_demo.png", dpi=150)
    print(report)