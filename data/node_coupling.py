import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. DETERMINISTIC PHYSICAL PARAMETERS (Based on parameters.json)
# =============================================================================
L_AUTO = 1.0          # Self-inductance fixated on the principal diagonal (H)
K_DIPOLE = 0.004      # Magnetic coupling constant calibrated for biotic media

# =============================================================================
# 2. TOPOLOGICAL CONFIGURATION OF THE NODE ARRAY (Meters)
# Spatial distribution structured across an organic 20 cm square grid
# =============================================================================
node_positions = np.array([
    [0.0, 0.0],  # Node 1: Origin point
    [0.2, 0.0],  # Node 2: Horizontal adjacent vector
    [0.0, 0.2],  # Node 3: Vertical adjacent vector
    [0.2, 0.2]   # Node 4: Diagonal boundary vector
])

n_nodes = len(node_positions)
M_matrix = np.zeros((n_nodes, n_nodes))

# =============================================================================
# 3. EVALUATION OF THE MUTUAL COUPLING TENSOR (M_ij)
# Strict application of the 1/r^3 near-field magnetic dipolar decay equation
# =============================================================================
for i in range(n_nodes):
    for j in range(n_nodes):
        if i == j:
            # Principal diagonal: Internal hardware self-inductance boundary
            M_matrix[i, j] = L_AUTO
        else:
            # Off-diagonal: Near-Field Magnetic Induction (NFMI) cross-talk
            # Computing the exact Euclidean spatial distance
            r_ij = np.linalg.norm(node_positions[i] - node_positions[j])
            # Dipolar decay attenuation proportional to the cube of distance
            M_matrix[i, j] = K_DIPOLE / (r_ij**3)

# =============================================================================
# 4. GRAPHICAL DIAGNOSTIC GENERATION (High-Resolution Heatmap)
# =============================================================================
plt.figure(figsize=(7, 6), dpi=150)
im = plt.imshow(M_matrix, cmap='coolwarm', origin='upper', vmin=0.0, vmax=1.0)

# Render verified numerical values inside each cell boundary
for i in range(n_nodes):
    for j in range(n_nodes):
        color = 'white' if M_matrix[i, j] > 0.5 else 'black'
        plt.text(j, i, f"{M_matrix[i, j]:.4f} H", ha="center", va="center", color=color, fontweight='bold')

plt.title("Biotic Node Mutual Coupling Matrix ($M_{ij}$)\nDeterministic NFMI 1/$r^3$ Dipolar Decay", fontsize=11, pad=15)
plt.xlabel("Target Node ($j$)", fontsize=10)
plt.ylabel("Source Node ($i$)", fontsize=10)
plt.xticks(range(n_nodes), [f"Node {k+1}" for k in range(n_nodes)])
plt.yticks(range(n_nodes), [f"Node {k+1}" for k in range(n_nodes)])

cbar = plt.colorbar(im)
cbar.set_label("Mutual Inductance (Henries)", rotation=270, labelpad=15)

plt.tight_layout()
plt.savefig("data/node_coupling_matrix.png", dpi=150)
plt.close()
