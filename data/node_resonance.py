import numpy as np
import json
import os

os.makedirs("data", exist_ok=True)

L = 1.0 
C = 162e-6
R = 100.0 

omega_0 = 1.0 / np.sqrt(L * C)   
f_res   = omega_0 / (2 * np.pi)  
Q       = omega_0 * L / R        
BW      = f_res / Q              

f     = np.linspace(f_res * 0.01, f_res * 10, 2000)
omega = 2 * np.pi * f

Z = R + 1j * (omega * L - 1.0 / (omega * C))
H = R / Z                               

magnitude = np.abs(H)
peak = np.max(magnitude)
mean = np.mean(magnitude)
k_eff = peak / mean

# ── Export ────────────────────────────────────────────────────
params = {
    "L_H":            L,
    "C_F":            C,
    "R_ohm":          R,
    "omega_0_rad_s":  round(omega_0, 6),
    "f_resonance_Hz": round(f_res, 6),
    "Q_factor":       round(Q, 6),
    "bandwidth_Hz":   round(BW, 6),
    "k_eff":          round(k_eff, 6)
}

output_path = "data/resonance_params.json"
with open(output_path, "w") as f_out:
    json.dump(params, f_out, indent=2)

print("\n===================================================")
print(" NODE RESONANCE MODEL")
print("===================================================\n")
print(f" Resonance frequency : {f_res:.4f} Hz")
print(f" Quality factor Q    : {Q:.4f}")
print(f" Bandwidth           : {BW:.4f} Hz")
print(f" k_eff (peak/mean)   : {k_eff:.4f}")
print(f"\n✔ Exported → {output_path}")
print("\n▶ Node Resonance Model: SUCCESSFUL EXECUTION")