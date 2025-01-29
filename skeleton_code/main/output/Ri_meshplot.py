from matplotlib import pyplot as p
import numpy as np
import matplotlib.colors as mcolors

# Load data
height = np.loadtxt('hh.dat')       # Height levels
time   = np.loadtxt('time.dat')     # Time steps
Ri     = np.loadtxt('Ri.dat')       # Ri values

# Ensure correct shape
if Ri.shape[1] != len(height):
    Ri = Ri.T  # Transpose if necessary

# Replace NaNs and clip extreme values
Ri = np.nan_to_num(Ri, nan=0.0)
Ri = np.clip(Ri, -1, 40000)  # Adjust range to expected physical values

# Define custom levels based on the example color scale
levels = np.array([-1, 0, 1, 10, 100, 200, 300, 40000])  # Adjust these based on dataset

# Create a discretized 'viridis' colormap
#cmap = p.get_cmap('viridis', len(levels) - 1)  # Discretize viridis into bins
cmap = p.get_cmap('RdYlBu_r',  len(levels) - 1)
norm = mcolors.BoundaryNorm(levels, cmap.N)  # Ensure color boundaries match

# Create the plot
fig, ax = p.subplots(figsize=(8, 6))
c = ax.contourf(time, height, Ri.T, levels=levels, cmap=cmap, norm=norm)  # Discrete contour plot

# Add colorbar
cb = p.colorbar(c, ax=ax, boundaries=levels, ticks=levels, label='Ri (-)')
ax.set_xlabel('Time (day)')
ax.set_ylabel('h (m)')
ax.set_title('K3: Ri')

# Save and display
p.savefig('Ri_meshplot_o.svg')