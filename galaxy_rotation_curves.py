import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def get_dephaze_galactic_constant():
    gamma0 = 1.60e-4        
    c_light = 299792.458    
    # JAVÍTÁS: A PDF 15. oldali Eq 62 eredményéhez (1.08e4) 
    # az Upsilonnak 7.5e-4-nek kell lennie (a 7.5e-7 elírás a PDF szövegében).
    Upsilon = 7.5e-4        
    
    C = Upsilon * gamma0 * (c_light**2)
    return C

def run_galaxy_rotation():
    C = get_dephaze_galactic_constant()
    v_flat_limit = np.sqrt(C)

    # NGC 2403 Data (SPARC)
    r_kpc = np.array([2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
    v_obs = np.array([65.0, 95.0, 115.0, 125.0, 130.0, 128.0])
    v_err = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0])
    v_bar = np.array([60.0, 80.0, 85.0, 88.0, 87.0, 85.0])

    # Dephaze Prediction: v^2 = v_bar^2 + C
    v_pred = np.sqrt(v_bar**2 + C)

    plt.figure(figsize=(10, 6))
    plt.errorbar(r_kpc, v_obs, yerr=v_err, fmt='ko', capsize=3, label="Observed (SPARC NGC 2403)")
    plt.plot(r_kpc, v_bar, 'g--', label="Baryonic only (Newtonian)")
    plt.plot(r_kpc, v_pred, 'r-', linewidth=2, label=r"Dephaze Prediction ($v = \sqrt{v_{bar}^2 + C}$)")
    plt.axhline(v_flat_limit, color='blue', linestyle=':', alpha=0.5, label=f"Topological limit ({v_flat_limit:.1f} km/s)")

    plt.xlabel("Radius (kpc)")
    plt.ylabel("Rotation Velocity (km/s)")
    plt.title("Galaxy Rotation Curve: NGC 2403 (Corrected Zero-Fit)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("galaxy_rotation_demo.png", dpi=150)

    residuals = v_obs - v_pred
    rms_error = np.sqrt(np.mean(residuals**2))

    report = (
        "DEPHAZE GALAXY ROTATION REPORT (CORRECTED)\n"
        "------------------------------------------\n"
        f"Corrected Galactic Constant (C): {C:.2e} (km/s)^2\n"
        f"Asymptotic Velocity (sqrt(C)): {v_flat_limit:.2f} km/s\n"
        f"RMS Error for NGC 2403: {rms_error:.2f} km/s\n"
        "Observation:\n"
         
    )
    return report

if __name__ == "__main__":
    print(run_galaxy_rotation())