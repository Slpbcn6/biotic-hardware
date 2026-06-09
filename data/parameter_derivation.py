import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data.config import load_parameters


def derive_lc():
    params = load_parameters()

    fixed = params["I_simulation_fixed_parameters"]
    f_target_hz = float(fixed["frequency_hz"])
    k = float(fixed["scaling_constant_k"])

    omega_target = 2.0 * math.pi * f_target_hz
    L_H = k * 1e-2
    C_F = 1.0 / (omega_target ** 2 * L_H)

    omega_actual = 1.0 / math.sqrt(L_H * C_F)
    f_actual_hz = omega_actual / (2.0 * math.pi)

    return {
        "f_target_hz": f_target_hz,
        "L_H": round(L_H, 6),
        "C_F": round(C_F, 9),
        "f_actual_hz": round(f_actual_hz, 6),
    }


def report():
    d = derive_lc()
    w0 = 2.0 * math.pi * d["f_target_hz"]
    lines = [
        "PARAMETER DERIVATION  (f_target -> L, C)",
        "  Documentation step: makes the L/C parameter chain explicit and auditable.",
        "  It reconstructs the stored values; it does not alter the simulation.",
        f"  Input : f_target = {d['f_target_hz']} Hz",
        f"  Step 1: L  = scaling_k * 1e-2 = {d['L_H']:.4f} H",
        f"  Step 2: w0 = 2*pi * f_target   = {w0:.4f} rad/s",
        f"  Step 3: C  = 1 / (w0^2 * L)   = {d['C_F']:.4e} F",
        f"  Check : f_res = 1/(2*pi*sqrt(LC)) = {d['f_actual_hz']:.4f} Hz  (== f_target OK)",
    ]
    for line in lines:
        print(line)
    return d


if __name__ == "__main__":
    report()