"""
Schumann resonance reference module.

Published fundamental mode frequencies (Hz) from NOAA/GFZ Potsdam ELF
monitoring data and peer-reviewed literature.

References:
  Schumann, W.O. (1952). Z. Naturforsch. 7a, 149-154.
  Williams, E.R. (1992). Science, 256(5062), 1184-1187.
  Nickolaenko, A. & Hayakawa, M. (2002). Resonances in the Earth-Ionosphere Cavity.
  NOAA/GFZ Potsdam ELF monitoring: https://www.gfz-potsdam.de
"""

SCHUMANN_MODES_HZ = [7.83, 14.3, 20.8, 27.3, 33.8]
SCHUMANN_SOURCE = "NOAA/GFZ Potsdam (published reference values)"


def nearest_schumann_mode(f_simulated):
    """
    Returns (nearest_mode_hz, mode_index_1based, deviation_percent).
    """
    diffs = [abs(f_simulated - f) for f in SCHUMANN_MODES_HZ]
    idx = int(diffs.index(min(diffs)))
    nearest = SCHUMANN_MODES_HZ[idx]
    deviation = abs(f_simulated - nearest) / nearest * 100.0
    return nearest, idx + 1, round(deviation, 2)


def schumann_report(f_simulated):
    """
    Returns a list of printable comparison lines.
    """
    nearest, mode_n, deviation = nearest_schumann_mode(f_simulated)
    return [
        f"Simulated resonance   : {f_simulated:.4f} Hz",
        f"Nearest Schumann mode : {nearest:.2f} Hz  (mode {mode_n})",
        f"Deviation             : {deviation:.2f}%",
        f"Reference             : {SCHUMANN_SOURCE}",
    ]