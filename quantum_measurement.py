import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ============================================================
# Dephaze invariant
# ============================================================

def _phi3():
    phi = (1.0 + 5.0 ** 0.5) / 2.0
    return phi ** 3


# ============================================================
# QUANTUM DECOHERENCE – DEPHAZE SAMPLING (SINGLE-SHOT)
# ============================================================

def run_quantum_decoherence(
    steps=800,
    meas_strength=0.4,   # measurement coupling (sampling, NOT time)
    noise=0.05,          # backaction noise
    Lambda=1.6,          # Dephaze strength
    seed=2025,
):
    """
    QUANTUM DECOHERENCE – DEPHAZE SAMPLING DEMO

    Ontology:
      • Measurement ≠ time evolution
      • Collapse = geometric exclusion in state space
      • Collapse happens ONCE per run (single-shot)
      • After collapse, branch switching is forbidden

    NO Schrödinger equation
    NO Lindblad dynamics
    NO environment size
    NO time variable

    ONLY:
      sampling
      coherence ratio
      φ³-based threshold
      bistable ontological locking
    """

    rng = np.random.default_rng(int(seed))
    T = int(steps)

    phi3 = _phi3()

    # Critical coherence threshold
    C0 = 1.0 / np.sqrt(phi3)

    # Collapse lock threshold
    z_lock = 0.9

    collapsed = False
    collapsed_sign = 0.0

    # Bloch trajectory
    s = np.zeros((T, 3))

    # Initial maximal superposition
    s[0] = np.array([1.0, 0.0, 0.0])

    # Identical noise path (fairness)
    eps = rng.normal(0.0, noise, size=(T, 3))

    for k in range(1, T):
        sx, sy, sz = s[k - 1]

        # Permanent exclusion after collapse
        if collapsed:
            s[k] = np.array([0.0, 0.0, collapsed_sign])
            continue

        # Raw sampled disturbance (sampling, not time)
        sx_raw = sx + eps[k, 0]
        sy_raw = sy + eps[k, 1]
        sz_raw = sz + meas_strength * eps[k, 2]

        # Coherence measure (plane only)
        C = np.sqrt(sx_raw**2 + sy_raw**2)

        # Dephaze coherence ratio
        rho = (C / (C0 + 1e-12)) ** 2

        # Geometric Dephaze gain
        gain = Lambda * np.tanh(rho - 1.0)

        # Suppress coherence plane
        sx_new = sx_raw * (1.0 - gain)
        sy_new = sy_raw * (1.0 - gain)

        # Bistable projection
        sz_new = sz_raw + gain * np.sign(sz_raw + 1e-9)

        # Keep inside Bloch ball
        r = np.sqrt(sx_new**2 + sy_new**2 + sz_new**2)
        if r > 1.0:
            sx_new /= r
            sy_new /= r
            sz_new /= r

        # Single-shot collapse + permanent lock
        if abs(sz_new) > z_lock:
            collapsed = True
            collapsed_sign = float(np.sign(sz_new))
            s[k] = np.array([0.0, 0.0, collapsed_sign])
            continue

        s[k] = [sx_new, sy_new, sz_new]

    # Diagnostics
    C_trace = np.sqrt(s[:, 0]**2 + s[:, 1]**2)
    Z_trace = s[:, 2]
    collapse_fraction = float(np.mean(np.abs(Z_trace) > 0.9))
    collapse_step = int(np.argmax(np.abs(Z_trace) > 0.9)) if np.any(np.abs(Z_trace) > 0.9) else -1

    # ===============================
    # PLOTS
    # ===============================
    fig, ax = plt.subplots(2, 1, figsize=(9, 6))

    ax[0].plot(C_trace, label="Coherence C = √(sx² + sy²)")
    ax[0].axhline(C0, linestyle="--", linewidth=1, label="critical C₀ = 1/√φ³")
    ax[0].set_ylabel("Coherence")
    ax[0].set_xlabel("Sampling step k")
    ax[0].legend()
    ax[0].set_title("Quantum coherence collapse (Dephaze sampling)")

    ax[1].plot(Z_trace, label="Measurement axis ⟨σ_z⟩")
    ax[1].axhline(z_lock, linestyle="--", linewidth=1, label="lock threshold")
    ax[1].axhline(-z_lock, linestyle="--", linewidth=1)
    ax[1].set_ylabel("sz")
    ax[1].set_xlabel("Sampling step k")
    ax[1].legend()
    ax[1].set_title("Bistable measurement outcome (ontological lock)")

    fig.tight_layout()

    # Text report
    txt = []
    txt.append("QUANTUM DECOHERENCE – Dephaze (sampling-only, single-shot)")
    txt.append(f"steps={T}, meas_strength={meas_strength}, noise={noise}, Lambda={Lambda}, seed={seed}")
    txt.append(f"phi^3 = {phi3:.3f}")
    txt.append(f"critical coherence C0 = {C0:.3f}")
    txt.append(f"lock threshold z_lock = {z_lock:.2f}")
    txt.append(f"collapse fraction |sz|>0.9 : {collapse_fraction:.2f}")
    txt.append(f"collapse step (first lock) : {collapse_step}")
    txt.append("")
    txt.append("Interpretation:")
    txt.append("  Measurement is not time evolution.")
    txt.append("  Collapse is a geometric exclusion in state space.")
    txt.append("  Collapse happens once per run; no branch switching.")
    txt.append("  No Schrödinger equation. No Lindblad. No environment.")

    return fig, "\n".join(txt)


# ============================================================
# ENTRY POINT – FUTTATHATÓ SCRIPT
# ============================================================

if __name__ == "__main__":
    fig, txt = run_quantum_decoherence()
    fig.savefig("quantum_measurement.png", dpi=150)
    print(txt)
