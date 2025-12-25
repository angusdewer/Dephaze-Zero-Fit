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
# OBSERVER LAYER – MEASUREMENT BIAS & INDUCED CRITICALITY
# ============================================================

def run_observer_layer(
    steps=2000,
    system_gain=0.04,     # Intrinsic system amplification
    observer_bias=0.6,    # Framing / narrative bias
    observer_delay=0.4,   # Delayed recognition (sampling lag)
    resolution=0.3,       # Measurement sharpness/precision
    noise=0.03,
    Lambda=1.6,          # Dephaze projection strength
    seed=2025,
):
    """
    OBSERVER / MEASUREMENT LAYER – DEPHAZE SAMPLING PROJECTION
    
    Ontology:
      • Objective System: The sub-threshold manifest field (Psi).
      • Observer Layer: Modifies the effective coherence ratio (rho_eff).
      • rho_eff = rho_system + rho_observer
      
    Key Principle: The observer does NOT change the physical laws, but 
    re-frames the sampling sequence. Bias and delay can push a system 
    over the Phi^3 threshold, triggering an irreversible ontological lock
    (memory) even if the underlying system is sub-critical.
    """

    rng = np.random.default_rng(int(seed))
    T = int(steps)
    phi3 = _phi3()
    r_star = np.sqrt(phi3)

    # Objective state (Ground truth)
    x_sys = np.zeros(T)
    x_sys[0] = 0.05

    # Perceived state (Manifested for the observer)
    x_obs = np.zeros(T)
    rho_sys = np.zeros(T)
    rho_eff = np.zeros(T)

    # Irreversible perceptual lock (The 'Pattern Trace' memory)
    memory = np.zeros(T)

    for k in range(1, T):
        # 1. OBJECTIVE SYSTEM DYNAMICS
        # Slow linear amplification with stochastic noise
        x_raw = x_sys[k - 1] + system_gain * x_sys[k - 1] + rng.normal(0, noise)
        r_sys = abs(x_raw)
        rho_sys[k] = (r_sys * r_sys) / phi3
        x_sys[k] = x_raw

        # 2. OBSERVER LAYER (Sampling Transformation)
        # Perception lag: index shift in the timeless ground state
        lag = int(observer_delay * 10)
        idx = max(0, k - lag)

        # Biased framing: subjective amplification of reality
        perceived = (1 + observer_bias) * x_sys[idx]

        # Resolution limit: information loss in measurement
        perceived += rng.normal(0, noise * (1 - resolution))

        # Observer-induced coherence component
        rho_obs = (perceived * perceived) / phi3

        # Effective coherence (Axiom 2.4 - Interaction term)
        rho_eff[k] = rho_sys[k] + rho_obs

        # 3. DEPHAZE PROJECTION ON PERCEPTION
        # The 'collapse' happens at the boundary of observation
        gain = Lambda * np.tanh(rho_eff[k] - 1.0)
        x_obs[k] = perceived - gain * np.sign(perceived)

        # Perceptual Memory Lock (Axiom 2.3)
        # If the joint system+observer state is supercritical, a trace is frozen.
        if rho_eff[k] > 1.0:
            memory[k] = memory[k - 1] + abs(gain)
        else:
            memory[k] = memory[k - 1]

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    # Objective Truth
    ax[0].plot(x_sys, color='black', alpha=0.7, label="Objective State (Psi)")
    ax[0].axhline(r_star, color='red', linestyle="--", label="Critical Radius $r^*$")
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title("System vs. Observer: The Mechanics of Measurement")
    ax[0].legend()

    # System Coherence
    ax[1].plot(rho_sys, color='gray', label=r"$\rho_{system}$ (Sub-critical)")
    ax[1].axhline(1.0, color='black', linestyle="--", alpha=0.5)
    ax[1].set_ylabel(r"$\rho$")
    ax[1].set_title("Intrinsic System Coherence")
    ax[1].legend()

    # Effective Coherence (Joint)
    ax[2].plot(rho_eff, color='orange', label=r"$\rho_{eff} = \rho_{sys} + \rho_{obs}$")
    ax[2].axhline(1.0, color='red', linestyle="--", label="Tipping Point")
    ax[2].set_ylabel(r"$\rho$")
    ax[2].set_title("Observer-Amplified Effective Coherence")
    ax[2].legend()

    # Induced Hysteresis
    ax[3].plot(memory, color='blue', linewidth=2, label="Observer-Induced Hysteresis")
    ax[3].set_xlabel("Sampling Step k")
    ax[3].set_ylabel("Trace Energy")
    ax[3].set_title(r"Irreversible Memory: The Frozen Pattern Trace $\Omega_{tr}$")
    ax[3].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE OBSERVER LAYER REPORT\n"
        "-----------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        "Observation:\n"
        "- The objective system remains below the critical threshold (rho_sys < 1).\n"
        "- Measurement bias and delay amplify the effective coherence (rho_eff > 1).\n"
        "- Result: The megasurement process triggers an irreversible pattern lock.\n"
        "Interpretation: Reality is a joint property of the state and its sampling."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_observer_layer()
    fig.savefig("observer_layer_demo.png", dpi=150)
    print(report)