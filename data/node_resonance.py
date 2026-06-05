import numpy as np
import json
import os

os.makedirs("data", exist_ok=True)

def load_parameters(path="data/parameters.json"):
    with open(path, "r") as f:
        raw = json.load(f)

    fixed = raw.get("I_simulation_fixed_parameters", {})
    derived = raw.get("III_derived_electrical_values", {})

    def parse_range(value):
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str) and " - " in value:
            return float(value.split(" - ")[0])
        return float(value)

    L = float(fixed.get("scaling_constant_k", 1.0)) * 1e-2
    C = parse_range(derived.get("capacitance_f", 1.0))
    R = parse_range(derived.get("ohmic_losses_ohm", 100.0))

    return {
        "L_H": L,
        "C_F": C,
        "R_ohm": R
    }

if __name__ == "__main__":
    params = load_parameters()

    L = params["L_H"]
    C = params["C_F"]
    R = params["R_ohm"]

    omega_0 = 1.0 / np.sqrt(L * C)
    f_res = omega_0 / (2 * np.pi)

    Q = omega_0 * L / R
    BW = f_res / (Q + 1e-12)

    f = np.linspace(f_res * 0.01, f_res * 10, 2000)
    omega = 2 * np.pi * f

    Z = R + 1j * (omega * L - 1.0 / (omega * C))
    H = R / Z

    magnitude = np.abs(H)

    peak = np.max(magnitude)
    mean = np.mean(magnitude)

    k_eff = peak / (mean + 1e-12)

    params_out = {
        "L_H": L,
        "C_F": C,
        "R_ohm": R,
        "omega_0_rad_s": round(omega_0, 6),
        "f_resonance_Hz": round(f_res, 6),
        "Q_factor": round(Q, 6),
        "bandwidth_Hz": round(BW, 6),
        "k_eff": round(k_eff, 6)
    }

    output_path = "data/resonance_params.json"

    with open(output_path, "w") as f_out:
        json.dump(params_out, f_out, indent=2)

    print("")
    print("NODE RESONANCE MODEL (PARAMETRIC)")
    print("")

    print(f"Resonance frequency : {f_res:.4f} Hz")
    print(f"Quality factor Q    : {Q:.4f}")
    print(f"Bandwidth           : {BW:.4f} Hz")
    print(f"k_eff (peak/mean)   : {k_eff:.4f}")

    print("")
    print("Exported -> data/resonance_params.json")
    print("Node Resonance Model: SUCCESSFUL EXECUTION")