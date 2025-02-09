from matplotlib import pyplot as p
import numpy as np
import matplotlib.colors as mcolors

# Load data
height = np.loadtxt('hh.dat'  )  # Array of height levels (should have size 50)
time   = np.loadtxt('time.dat')  # Array of time steps
Km     = np.loadtxt('Km.dat'  )  # K_m array with dimensions (n_time_steps, n_height_levels)
Km     = np.hstack([Km, Km[:, -1:]])    # Duplicate last column

Kh     = np.loadtxt('Kh.dat'  )  # K_h array with dimensions (n_time_steps, n_height_levels)
Kh     = np.hstack([Kh, Kh[:, -1:]])    # Duplicate last column

# ensure data is transposed correctly
if Km.shape[1] != len(height):
    Km = Km.T  # transpose if necessary to align height with the second dimension

# replace NaNs with zeros
Km = np.nan_to_num(Km, nan=0.0)
# change extreme values to a reasonable range
Km = np.clip(Km, 0, None)  # adjust based on expected range

# Define discrete levels (bins)
levels = np.arange(0, 120, 15)  # Color bins

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
ax.set_title("K3: Km")

# Save and display
p.savefig('meshplot_o.svg')