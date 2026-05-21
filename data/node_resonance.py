import numpy as np

L_INDUCTANCE = 1.0              
C_CAPACITANCE = 162e-6          
f_resonance = 12.5 

R_loss_range = np.linspace(100.0, 1000.0, 100)
R_radiation = 1e-9 

efficiency = R_radiation / (R_radiation + R_loss_range)

print("--- NODE-LEVEL EFFICIENCY PARAMETRIC ANALYSIS ---")
print(f"Base Coupling Frequency: {f_resonance} Hz")
print(f"Theoretical Radiation Resistance (Rr): {R_radiation} Ohms")
print(f"Maximum individual radiation efficiency: {efficiency[0]:.2e}")
print(f"Minimum individual radiation efficiency: {efficiency[-1]:.2e}")
print("Model conclusion: Systemic Array gain is strictly required.")