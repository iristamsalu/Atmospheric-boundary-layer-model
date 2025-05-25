from matplotlib import pyplot as p
import numpy as np
import matplotlib.colors as mcolors

# Load data
height = np.loadtxt('hh.dat')       # 50 height levels
height = height.reshape(-1) 

time   = np.loadtxt('time.dat')     # Time steps
time   = time * 24 

Ri     = np.loadtxt('Ri.dat')       # Ri values (only for 49 altidudes)
Ri = np.hstack([Ri, Ri[:, -1:]])    # Duplicate last column

# Replace NaNs and clip extreme values
Ri = np.nan_to_num(Ri, nan=0.0)
Ri = np.clip(Ri, -1, 40000)  # Adjust range to expected physical values

# Define custom levels based on the example color scale
levels = np.array([-1, 0, 1, 10, 100, 200, 300, 40000])  # Adjust these based on dataset

# Create a discretized 'viridis' colormap
cmap = p.get_cmap('viridis', len(levels) - 1)  # Discretize viridis into bins
norm = mcolors.BoundaryNorm(levels, cmap.N)  # Ensure color boundaries match

# Create the plot
fig, ax = p.subplots(figsize=(8, 6))
c = ax.contourf(time, height, Ri.T, levels=levels, cmap=cmap, norm=norm)  # Discrete contour plot

# Add colorbar
cb = p.colorbar(c, ax=ax, boundaries=levels, ticks=levels, label='Ri (-)')
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Altitude (m)')
ax.set_title('SMEAR II 18.02.2011 \nRichardson number (Ri) with model v3')

# Save and display
p.savefig('Ri_summer.png')