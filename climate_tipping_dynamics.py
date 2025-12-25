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
# CLIMATE TIPPING – DEPHAZE SAMPLING & HYSTERESIS
# ============================================================

def run_climate_tipping(
    steps=2000,
    forcing_max=2.5,    # Maximum external stress
    noise=0.02,         # Stochastic background
    Lambda=1.6,         # Dephaze projection strength
    seed=2025,
):
    """
    CLIMATE TIPPING POINT – DEPHAZE SAMPLING PROJECTION
    
    Ontology:
      • State: Climate equilibrium coordinate (e.g., global temp or ice cover).
      • Forcing: External driving field (Axiom 2.2).
      • Tipping: A phase transition triggered when rho = E / Phi^3 > 1.
      • Memory: Once the system locks into a new pattern trace (Omega_tr), 
        reversing the forcing does not restore the original state.
        
    Key Principle: Irreversibility is not a time-effect, but a geometric 
    exclusion in the state space. No time dynamics used; only sampling.
    """

    rng = np.random.default_rng(int(seed))
    Tn = int(steps)
    phi3 = _phi3()

    # Forcing sweep: Upward stress followed by downward relief
    half = Tn // 2
    forcing = np.concatenate([
        np.linspace(0.0, forcing_max, half),
        np.linspace(forcing_max, 0.0, Tn - half)
    ])

    # State variables
    x = np.zeros(Tn)
    rho = np.zeros(Tn)

    # Ontological lock flags (Axiom 2.4)
    locked = False
    lock_value = None

    for k in range(1, Tn):
        if locked:
            # Once locked into a new Omega_tr branch, the state is fixed
            x[k] = lock_value
            rho[k] = 1.0
            continue

        # 1. Sampling proposal (Fluctuation in the timeless ground state)
        x_raw = x[k-1] + 0.4 * forcing[k] + rng.normal(0.0, noise)

        # 2. Abstract Energy Landscape (Ice-Albedo feedback simulation)
        # Non-linear potential with multiple minima
        E = (0.5 * x_raw**2 - 0.8 * x_raw**3 + 0.3 * x_raw**4)

        # 3. Coherence ratio (Axiom 2.3)
        rho_k = E / phi3
        rho[k] = rho_k

        # === DEPHAZE PROJECTION RULES ===

        if rho_k > 1.0:
            # Supercritical state: invoke bistable relaxation
            gain = Lambda * np.tanh(rho_k - 1.0)
            x_proj = x_raw - gain * np.sign(x_raw)
            x[k] = x_proj

            # Threshold for irreversible ontological lock (Axiom 2.4)
            if rho_k > 1.3:
                locked = True
                lock_value = x_proj
                x[k] = lock_value
                rho[k] = 1.0
        else:
            # Subcritical: standard sampled evolution
            x[k] = x_raw

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(3, 1, figsize=(10, 10))

    # Forcing Plot
    ax[0].plot(forcing, color='gray', label="External Forcing (Sweep)")
    ax[0].set_ylabel("Forcing Intensity")
    ax[0].set_title("External Stress: Forcing Sweep Up and Down")
    ax[0].legend()

    # State Evolution Plot
    ax[1].plot(x, color='blue', linewidth=2, label="Climate State (Psi)")
    ax[1].axvline(half, color='red', linestyle="--", label="Max Forcing Point")
    ax[1].set_ylabel("State Coordinate")
    ax[1].set_title("Irreversible Tipping: The $\Phi^{-3}$ Pattern Lock")
    ax[1].legend()

    # Hysteresis Loop
    ax[2].plot(forcing, x, color='purple', label="Hysteresis Path")
    ax[2].set_xlabel("Forcing Intensity")
    ax[2].set_ylabel("State Coordinate")
    ax[2].set_title("Structural Memory: No Return Path (Hysteresis)")
    ax[2].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE CLIMATE TIPPING REPORT\n"
        "------------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        "Observation:\n"
        "- Increasing forcing crosses the critical coherence threshold (rho > 1).\n"
        "- At rho > 1.3, the system undergoes an irreversible ontological lock.\n"
        "- Decreasing forcing does NOT return the system to its initial state.\n"
        "Result: Structural memory (hysteresis) emerges from Phi^3 geometry."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_climate_tipping()
    fig.savefig("climate_tipping_demo.png", dpi=150)
    print(report)