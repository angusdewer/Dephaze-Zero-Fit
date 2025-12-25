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
# GW MEMORY – DEPHAZE RESIDUE VS. WAVEFORM COLLAPSE
# ============================================================

def run_gw_memory(
    steps=1200,
    burst_amp=1.0,
    burst_width=120,
    asymmetry=0.0,
    noise=0.02,
    Lambda=1.6,
    scale=0.1,
    seed=2025,
):
    rng = np.random.default_rng(int(seed))
    T = int(steps)
    phi3 = _phi3()

    k = np.arange(T)
    center = T // 2
    width = max(1, int(burst_width))

    # --- 1. GW Burst Generation ---
    burst = burst_amp * np.exp(-0.5 * ((k - center) / width) ** 2)
    if asymmetry != 0.0:
        burst *= (1.0 + asymmetry * np.tanh((k - center) / width))
    burst += rng.normal(0.0, noise, size=T)

    # --- 2. Energy-to-Coherence Mapping ---
    E_gw = burst ** 2
    E0 = phi3 * scale
    rho = E_gw / (E0 + 1e-12)

    # --- 3. Dephaze Projection ---
    gain = Lambda * np.tanh(rho - 1.0)
    memory_increment = np.where(gain > 0.0, gain * np.sign(burst), 0.0)
    h_memory = np.cumsum(memory_increment)
    h_memory -= h_memory[0]
    delta_h = float(h_memory[-1])

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    # Waveform Plot
    ax[0].plot(burst, color='black', alpha=0.8, label=r"GW Signal $h(k)$")
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(r"Gravitational Wave Burst: Active $\Phi^3$ Generation")
    ax[0].legend()

    # Coherence Ratio Plot
    ax[1].plot(rho, color='orange', label=r"$\rho = \Omega_p / \Omega_{tr}$")
    ax[1].axhline(1.0, color='red', linestyle="--", label=r"Critical Threshold ($\rho=1$)")
    ax[1].set_ylabel(r"Coherence Ratio $\rho$")
    ax[1].set_title("Dephaze Activation: Manifold Instability")
    ax[1].legend()

    # Memory Offset Plot
    ax[2].plot(h_memory, color='blue', linewidth=2, label=r"Residual Memory $\Delta h$")
    ax[2].set_ylabel("Permanent Offset")
    ax[2].set_xlabel("Sampling Step k")
    ax[2].set_title(r"Spacetime Memory: Permanent $\Phi^{-3}$ Residue")
    ax[2].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE GW MEMORY REPORT\n"
        "------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Final Memory Offset (Delta h): {delta_h:.4f}\n"
        "Observation:\n"
        "- Memory forms only during the supercritical phase (rho > 1).\n"
        "- The permanent offset is a structural fossil, not a dynamical decay.\n"
        "Result: Spacetime geometry updated via bistable relaxation."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_gw_memory()
    fig.savefig("gw_memory_demo.png", dpi=150)
    print(report)