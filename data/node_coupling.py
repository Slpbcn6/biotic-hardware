import numpy as np
import matplotlib.pyplot as plt

L_AUTO = 1.0                
K_DIPOLE = 0.004            
frequency = 12.5           
c = 3e8                     
wavelength = c / frequency 
k_wave = 2 * np.pi / wavelength

node_positions = np.array([
    [0.0, 0.0, 0.0],
    [0.2, 0.0, 0.0],
    [0.0, 0.2, 0.0],
    [0.2, 0.2, 0.0]
])

n_nodes = len(node_positions)

M_matrix = np.zeros((n_nodes, n_nodes))
for i in range(n_nodes):
    for j in range(n_nodes):
        if i == j:
            M_matrix[i, j] = L_AUTO
        else:
            r_ij = np.linalg.norm(node_positions[i] - node_positions[j])
            M_matrix[i, j] = K_DIPOLE / (r_ij**3)

phases = np.array([0, np.pi/2, np.pi, 3*np.pi/2]) 
amplitudes = np.ones(n_nodes)                    
w = amplitudes * np.exp(1j * phases)              

theta = np.linspace(-np.pi, np.pi, 360)
array_factor = np.zeros_like(theta, dtype=complex)

for idx, t in enumerate(theta):
    k_vec = k_wave * np.array([np.sin(t), np.cos(t), 0])
    phasors = 0.0
    for n in range(n_nodes):
        spatial_phase = np.dot(k_vec, node_positions[n])
        phasors += w[n] * np.exp(1j * spatial_phase)
    array_factor[idx] = phasors

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150, constrained_layout=True)

ax1.scatter(node_positions[:, 0], node_positions[:, 1], color='red', s=200, zorder=3)
for i, (x, y, _) in enumerate(node_positions):
    ax1.text(x+0.01, y+0.01, f"N{i+1}\n$\\Phi$={np.degrees(phases[i]):.0f}°", fontsize=9, fontweight='bold')
ax1.set_title("Network Topology (4 Nodes)")
ax1.set_xlabel("X Axis (meters)")
ax1.set_ylabel("Y Axis (meters)")
ax1.grid(True)
ax1.set_xlim(-0.1, 0.3)
ax1.set_ylim(-0.1, 0.3)

ax2.plot(theta, np.abs(array_factor), color='purple', linewidth=2)
ax2.set_title("Array Factor (AF) - Coherent Interference")
ax2.set_xlabel("Angle $\\theta$ (radians)")
ax2.set_ylabel("Resultant Field Magnitude")
ax2.grid(True)

fig.suptitle("Computational Modeling of Distributed Phased Array (12.5 Hz)", fontsize=14, fontweight='bold')
plt.savefig("data/phased_array_output.png")
plt.show()