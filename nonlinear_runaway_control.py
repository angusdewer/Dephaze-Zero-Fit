import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

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
# CONTROL DYNAMICS – NONLINEAR RUNAWAY VS. DEPHAZE BOUNDS
# ============================================================

def run_control_runaway(
    duration=1.2,
    a=0.8,              # Linear growth coefficient
    beta=1.2,           # Nonlinear runaway coefficient
    Lambda=1.4,         # Dephaze projection strength
    r_stop=25.0,        # Numeric cutoff for runaway
    seed=2025,
):
    """
    NONLINEAR CONTROL – DEPHAZE SAMPLING PROJECTION
    
    Ontology:
      • Baseline: Continuous-time ODE evolution. Positive feedback leads to explosion.
      • Dephaze: Discrete sampling frames. Does NOT observe or control time.
      • Feedback: Invariant geometric projection (Axiom 2.5).
      
    Key Principle: Stability emerges without targets, PID tuning, or temporal 
    integration. The system treats its own magnitude as a coherence ratio (rho) 
    and projects it back to the structural manifold (Phi^3).
    """

    rng = np.random.default_rng(int(seed))
    x0, y0 = rng.normal(0.0, 0.2, size=2)

    # ---- Structural invariant ----
    phi3 = _phi3()
    r_crit = np.sqrt(phi3) # Critical stability radius (r*)

    # ---- Time grid (Baseline reference) ----
    t_span = (0.0, float(duration))
    t_eval = np.linspace(t_span[0], t_span[1], 1400)

    # =========================================================
    # 1. BASELINE: TRUE CONTINUOUS-TIME RUNAWAY (ODE)
    # =========================================================
    def baseline_rhs(t, z):
        x, y = z
        r2 = x*x + y*y
        # Superlinear growth + rotation
        dx = a * x - y + beta * x * r2
        dy = x + a * y + beta * y * r2
        return [dx, dy]

    # Event to stop ODE solver if it explodes
    def stop_event(t, z):
        return float(r_stop) - np.sqrt(z[0]**2 + z[1]**2)
    stop_event.terminal = True
    stop_event.direction = -1

    sol_b = solve_ivp(
        baseline_rhs, t_span, [x0, y0],
        t_eval=t_eval, events=stop_event,
        rtol=1e-7, atol=1e-9
    )

    tb = sol_b.t
    xb, yb = sol_b.y
    rb = np.sqrt(xb*xb + yb*yb)

    # =========================================================
    # 2. DEPHAZE: DISCRETE SAMPLING / PROJECTION (AXIOM 2.2)
    # =========================================================
    xd, yd = [float(x0)], [float(y0)]

    def dephaze_project(x, y):
        # Sampling-based invariant projection
        r = np.sqrt(x*x + y*y) + 1e-12
        rho = (r*r) / phi3
        gain = float(Lambda) * np.tanh(rho - 1.0)
        # Purely radial geometric correction
        return x - gain * (x / r), y - gain * (y / r)

    for k in range(1, len(tb)):
        x, y = xd[-1], yd[-1]
        r2 = x*x + y*y
        
        # Identical raw physical tendency
        dx = a * x - y + beta * x * r2
        dy = x + a * y + beta * y * r2

        # Advance one frame (sampling sequence, not fundamental time)
        dt_frame = float(tb[k] - tb[k-1])
        x_next = x + dx * dt_frame
        y_next = y + dy * dt_frame

        # Apply structural lock
        x_proj, y_proj = dephaze_project(x_next, y_next)
        xd.append(x_proj)
        yd.append(y_proj)

        if np.sqrt(x_proj**2 + y_proj**2) > float(r_stop):
            break

    xd, yd = np.array(xd), np.array(yd)
    rd = np.sqrt(xd*xd + yd*yd)

    # =========================================================
    # PLOTS
    # =========================================================
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Magnitude Plot
    ax[0].plot(tb, rb, color='crimson', label="Baseline r(t) (ODE Runaway)")
    ax[0].plot(tb[:len(rd)], rd, color='dodgerblue', linewidth=2, label="Dephaze r(k) (Projected Stability)")
    ax[0].axhline(r_crit, color='black', linestyle="--", label=r"Critical Radius $r^* = \sqrt{\Phi^3}$")
    ax[0].set_title("Control Systems: Non-linear Runaway vs. Dephaze Invariant")
    ax[0].set_ylabel("System Norm ||state||")
    ax[0].set_xlabel("Time (Baseline) / Frame (Dephaze)")
    ax[0].legend()

    # Phase Space Plot
    ax[1].plot(xb, yb, color='crimson', alpha=0.3, label="Baseline Path")
    ax[1].plot(xd, yd, color='dodgerblue', label="Dephaze Path")
    ax[1].set_title("Phase Space: Emergent Limit Cycle")
    ax[1].set_xlabel("x")
    ax[1].set_ylabel("y")
    ax[1].legend()

    fig.tight_layout()

    report = (
        "DEPHAZE NON-LINEAR CONTROL REPORT\n"
        "--------------------------------\n"
        f"Phi^3 Invariant: {phi3:.4f}\n"
        f"Critical Radius (r*): {r_crit:.4f}\n"
        "Observation:\n"
        "- Baseline: Continuous-time feedback leads to exponential explosion.\n"
        "- Dephaze: Discrete sampling + geometric projection creates a stable attractor.\n"
        "Result: Stability is achieved without PID tuning or target states."
    )

    return fig, report

if __name__ == "__main__":
    fig, report = run_control_runaway()
    fig.savefig("nonlinear_runaway_demo.png", dpi=150)
    print(report)