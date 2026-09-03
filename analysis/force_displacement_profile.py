import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def generate_reference_curve(displacement: np.ndarray) -> np.ndarray:
    """Models nominal press force (kN) as a function of ram displacement (mm)."""
    # Phase 1: Entry / alignment (low resistance)
    # Phase 2: Interference seating (linear rise)
    # Phase 3: Bottoming out / final seat contact (exponential hardening)
    force = np.zeros_like(displacement)
    p1 = displacement <= 10.0
    p2 = (displacement > 10.0) & (displacement <= 22.0)
    p3 = displacement > 22.0

    force[p1] = 0.25 * (displacement[p1] / 10.0)
    force[p2] = 0.25 + 4.5 * ((displacement[p2] - 10.0) / 12.0)
    force[p3] = 4.75 + 3.0 * ((displacement[p3] - 22.0) / 3.0)**2
    return force

def run_simulation(num_samples: int = 150):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    displacement = np.linspace(0, 25, num_samples)
    nominal_force = generate_reference_curve(displacement)

    # Define industrial tolerance boundaries (±12% tolerance band)
    upper_limit = nominal_force * 1.15 + 0.3
    lower_limit = np.maximum(nominal_force * 0.85 - 0.2, 0.0)

    # Synthetic press runs
    np.random.seed(42)
    normal_run = nominal_force + np.random.normal(0, 0.08, size=num_samples)
    fault_underfit = nominal_force * 0.72 + np.random.normal(0, 0.05, size=num_samples)
    fault_misaligned = nominal_force.copy()
    fault_misaligned[displacement > 14] *= 1.45

    # Export sample dataset
    df = pd.DataFrame({
        "Displacement_mm": displacement,
        "Nominal_Force_kN": nominal_force,
        "Upper_Limit_kN": upper_limit,
        "Lower_Limit_kN": lower_limit,
        "Run_Pass_kN": normal_run,
        "Run_Fault_Underfit_kN": fault_underfit,
        "Run_Fault_Misaligned_kN": fault_misaligned
    })
    csv_path = output_dir / "valve_press_telemetry.csv"
    df.to_csv(csv_path, index=False)
    print(f"Logged dataset saved to: {csv_path}")

    # Plotting
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(displacement, nominal_force, label="Nominal Target Curve", color="black", linestyle="--", linewidth=1.5)
    plt.fill_between(displacement, lower_limit, upper_limit, color="gray", alpha=0.2, label="Acceptable QA Tolerance Band")
    
    plt.plot(displacement, normal_run, label="Cycle #1041 (Pass - Nominal Fit)", color="#2ca02c", linewidth=2)
    plt.plot(displacement, fault_underfit, label="Cycle #1042 (Fail - Loose Fit / Under-force)", color="#1f77b4", linestyle=":", linewidth=2)
    plt.plot(displacement, fault_misaligned, label="Cycle #1043 (Fail - Bore Jam / High Force)", color="#d62728", linewidth=2)

    plt.axvline(22.0, color='orange', linestyle='--', alpha=0.7, label='Final Seating Contact Threshold')
    plt.title("Valve Press Seating: Force vs. Displacement Monitoring", fontsize=13, fontweight="bold")
    plt.xlabel("Stroke Displacement (mm)", fontsize=11)
    plt.ylabel("Pressing Force (kN)", fontsize=11)
    plt.xlim(0, 25)
    plt.ylim(0, 10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", framealpha=0.9)
    plt.tight_layout()

    fig_path = output_dir / "force_displacement_profile.png"
    plt.savefig(fig_path)
    plt.close()
    print(f"Quality curve diagram generated: {fig_path}")

if __name__ == "__main__":
    run_simulation()
