from matplotlib import pyplot as p
import numpy as np
import matplotlib.colors as mcolors

# Load data
height = np.loadtxt('hh.dat'  )  # Array of height levels (should have size 50)
time   = np.loadtxt('time.dat')  # Array of time steps
Km     = np.loadtxt('Km.dat'  )  # K_m array with dimensions (n_time_steps, n_height_levels)
Kh     = np.loadtxt('Kh.dat'  )  # K_h array with dimensions (n_time_steps, n_height_levels)

# Ensure data is reshaped/transposed correctly
if Km.shape[1] != len(height):
    Km = Km.T  # Transpose if necessary to align height with the second dimension

# Replace NaNs with zeros
Km = np.nan_to_num(Km, nan=0.0)
# Clip extreme values to a reasonable range
Km = np.clip(Km, 0, None)  # Adjust based on expected range

# Define discrete levels (bins)
levels = np.arange(0, 175, 25)  # Color bins: 0-20, 20-40, ..., 160-180

# Create a discretized "viridis" colormap
cmap = p.get_cmap("viridis", len(levels) - 1)  # Discretize viridis into bins
norm = mcolors.BoundaryNorm(levels, cmap.N)  # Ensure color boundaries match

# Create the plot
fig, ax = p.subplots(figsize=(8, 6))
c = ax.contourf(time, height, Km.T, levels=levels, cmap=cmap, norm=norm)  # Discrete contour plot

# Add colorbar
cb = p.colorbar(c, ax=ax, boundaries=levels, ticks=levels, label=r"$K_m$ (m$^2$ s$^{-1}$)")
ax.set_xlabel("Time (day)")
ax.set_ylabel("h (m)")
ax.set_title("K3: Km with Discrete Viridis Colors")

# Save and display
p.savefig('figure_discrete_mesh.svg')