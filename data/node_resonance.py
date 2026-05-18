import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# FIXED PARAMETERS FROM APPENDIX B [DOI: 10.17605/OSF.IO/N3PB7]
# =============================================================================
L_INDUCTANCE = 1.0              # Fixed node inductance (Henries)
C_CAPACITANCE = 162e-6          # Capacitance (162 uF converted to Farads)
R_RESISTANCE = 100.0            # Lower-bound ohmic resistance (Ohms)
V_INPUT = 1.0                   # Input excitation voltage (Volts)

# Frequency sweep range (ELF band centered around Schumann Resonance)
frequencies = np.linspace(1.0, 30.0, 1000)
omega = 2 * np.pi * frequencies

# =============================================================================
# RLC SERIES CIRCUIT IMPEDANCE AND RESPONSE CALCULATIONS
# =============================================================================
X_L = omega * L_INDUCTANCE
X_C = 1.0 / (omega * C_CAPACITANCE)

Z_complex = R_RESISTANCE + 1j * (X_L - X_C)
Z_magnitude = np.abs(Z_complex)
I_magnitude = V_INPUT / Z_magnitude

V_output = I_magnitude * X_C
phase_angle = np.angle(Z_complex, deg=True)

f_resonance = 1.0 / (2 * np.pi * np.sqrt(L_INDUCTANCE * C_CAPACITANCE))

# =============================================================================
# MATHEMATICAL COHERENCE PLOT GENERATION
# =============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot 1: Output Voltage (Resonance Curve)
ax1.plot(frequencies, V_output, 'b-', linewidth=2, label='Output Voltage ($V_{out}$)')
ax1.axvline(f_resonance, color='r', linestyle='--', alpha=0.7, 
            label=f'Theoretical Tuning: {f_resonance:.2f} Hz (Schumann)')
ax1.set_ylabel('Voltage Amplitude ($V$)', fontsize=11)
ax1.set_title('Biotic Node RLC Frequency Response Curve [DOI: N3PB7]', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='upper right')

# Plot 2: Impedance Phase Angle
ax2.plot(frequencies, phase_angle, 'g-', linewidth=2, label='Phase Angle')
ax2.axvline(f_resonance, color='r', linestyle='--', alpha=0.7)
ax2.axhline(0, color='k', linestyle='-', alpha=0.3)
ax2.set_xlabel('Excitation Frequency (Hz)', fontsize=11)
ax2.set_ylabel('Phase (Degrees °)', fontsize=11)
ax2.set_xlim(1.0, 30.0)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='lower right')

plt.tight_layout()
plt.savefig('node_frequency_response.png', dpi=300)
plt.show()
