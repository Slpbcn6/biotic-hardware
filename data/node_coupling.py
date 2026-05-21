import numpy as np
import matplotlib.pyplot as plt

L_AUTO = 1.0          
K_DIPOLE = 0.004      

node_positions = np.array([
    [0.0, 0.0],
    [0.2, 0.0],
    [0.0, 0.2],
    [0.2, 0.2]
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

plt.figure(figsize=(7, 6), dpi=150)
im = plt.imshow(M_matrix, cmap='coolwarm', origin='upper', vmin=0.0, vmax=1.0)

for i in range(n_nodes):
    for j in range(n_nodes):
        color = 'white' if M_matrix[i, j] > 0.5 else 'black'
        plt.text(j, i, f"{M_matrix[i, j]:.4f} H", ha="center", va="center", color=color, fontweight='bold')

plt.title("Biotic Node Mutual Coupling Matrix")
plt.xlabel("Target Node (j)")
plt.ylabel("Source Node (i)")
plt.xticks(range(n_nodes), [f"Node {k+1}" for k in range(n_nodes)])
plt.yticks(range(n_nodes), [f"Node {k+1}" for k in range(n_nodes)])

cbar = plt.colorbar(im)
cbar.set_label("Mutual Inductance (Henries)")

plt.tight_layout()
plt.show()