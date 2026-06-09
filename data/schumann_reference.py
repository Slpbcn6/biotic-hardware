SCHUMANN_MODES_HZ = [7.83, 14.3, 20.8, 27.3, 33.8]
SCHUMANN_SOURCE = "NOAA/GFZ Potsdam (published reference values)"


def nearest_schumann_mode(f_simulated):
    diffs = [abs(f_simulated - f) for f in SCHUMANN_MODES_HZ]
    idx = diffs.index(min(diffs))
    nearest = SCHUMANN_MODES_HZ[idx]
    deviation = abs(f_simulated - nearest) / nearest * 100.0
    return nearest, idx + 1, round(deviation, 2)


def schumann_report(f_simulated):
    nearest, mode_n, deviation = nearest_schumann_mode(f_simulated)
    return [
        f"Simulated resonance   : {f_simulated:.4f} Hz",
        f"Nearest Schumann mode : {nearest:.2f} Hz  (mode {mode_n})",
        f"Deviation             : {deviation:.2f}%",
        f"Reference             : {SCHUMANN_SOURCE}",
    ]