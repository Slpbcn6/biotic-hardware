import numpy as np
import matplotlib.pyplot as plt

L_INDUCTANCE = 1.0              
C_CAPACITANCE = 162e-6          
R_RESISTANCE = 100.0            
V_INPUT = 1.0                   

frequencies = np.linspace(1.0, 30.0, 1000)
omega = 2 * np.pi * frequencies

X_L = omega * L_INDUCTANCE
X_C = 1.0 / (omega * C_CAPACITANCE)

Z_complex = R_RESISTANCE + 1j * (X_L - X_C)
Z_magnitude = np.abs(Z_complex)
I_magnitude = V_INPUT / Z_magnitude

V_output = I_magnitude * X_C
phase_angle = np.angle(Z_complex, deg=True)

f_resonance = 1.0 / (2 * np.pi * np.sqrt(L_INDUCTANCE * C_CAPACITANCE))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(frequencies, V_output, 'b-')
ax1.axvline(f_resonance, color='r', linestyle='--')
ax1.set_ylabel('Voltage Amplitude (V)')
ax1.set_title('Biotic Node RLC Frequency Response')
ax1.grid(True)

ax2.plot(frequencies, phase_angle, 'g-')
ax2.axvline(f_resonance, color='r', linestyle='--')
ax2.axhline(0, color='k', linestyle='-')
ax2.set_xlabel('Excitation Frequency (Hz)')
ax2.set_ylabel('Phase (Degrees)')
ax2.set_xlim(1.0, 30.0)
ax2.grid(True)

plt.tight_layout()
import matplotlib.pyplot as plt
plt.show()