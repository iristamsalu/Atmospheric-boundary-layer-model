import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# Load the data from PN.dat
PM = np.loadtxt('PM_dep.dat')
num_height_levels = PM.shape[1]

# Define the time and height axes
time_total_hours = np.linspace(0, 120, PM.shape[0]) # Total time in hours
time_days = time_total_hours / 24.0 # Time in days
height_file = np.loadtxt('hh.dat')
height = height_file[:]

# Select the time range indices corresponding to Day 3.0 to Day 5.0
time_start_day = 3.0
time_end_day = 5.0
idx_start = np.abs(time_days - time_start_day).argmin()
idx_end = np.abs(time_days - time_end_day).argmin()

# Extract the data and time for the selected range
PM_data_selected = PM[idx_start:idx_end+1, :]
time_days_selected = time_days[idx_start:idx_end+1]

# Create meshgrid for contour plot
T, H = np.meshgrid(time_days_selected, height)

# Define contour levels based on the example colorbar
levels = [0.000, 1.200, 1.225, 1.250, 1.275, 1.300, 1.325, 1.350]
# Use 'viridis' colormap which is similar to the example
cmap = plt.get_cmap('viridis')
norm = mcolors.BoundaryNorm(levels, cmap.N)  # Ensure color boundaries match

# Calculate the actual maximum value in the selected data range
max_val = PM_data_selected.max()

# Create the contour plot
plt.figure(figsize=(8, 6)) # Adjusted figure size slightly
cf = plt.contourf(T, H, PM_data_selected.T, levels=levels, cmap=cmap, norm=norm, extend='max') # Use extend='max' for values above the last level

# Add labels and title
plt.xlabel("Day (d)")
plt.ylabel("Height (m)")
# Add title and max value annotation
plt.title(f"Total particle number concentration\nmax={max_val:.2e}", loc='center')


# Add colorbar
cbar = plt.colorbar(cf, ticks=levels) # Set ticks explicitly
cbar.set_label(r"PM (ug / m$^{-3}$)") # Use LaTeX for units

# Set the x and y axis limits (matching the selected data range)
plt.xlim(time_start_day, time_end_day)
plt.ylim(0, 3000)

# Show the plot
plt.tight_layout(rect=[0, 0, 1, 0.95]) # Adjust layout to prevent title overlap
plt.savefig("PM_heatmap_depo.png")