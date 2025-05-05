import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --- Load Data for PN ---
PN_coag = np.loadtxt('PN_dep.dat')
num_height_levels = PN_coag.shape[1]

# Define the time and height axes for PN
time_total_hours = np.linspace(0, 120, PN_coag.shape[0])  # Total time in hours
time_days = time_total_hours / 24.0  # Time in days
height_file = np.loadtxt('hh.dat')
height = height_file[:]

# Select the time range indices corresponding to Day 3.0 to Day 5.0 for PN
time_start_day = 3.0
time_end_day = 5.0
idx_start = np.abs(time_days - time_start_day).argmin()
idx_end = np.abs(time_days - time_end_day).argmin()

# Extract the data and time for the selected range for PN
PN_data_selected = PN_coag[idx_start:idx_end+1, :]
time_days_selected = time_days[idx_start:idx_end+1]

# Create meshgrid for contour plot for PN
T, H = np.meshgrid(time_days_selected, height)

# Define contour levels for PN based on the example colorbar
levels_PN = [0, 1000, 10000, 20000, 30000, 32000, 34000, 36000, 38000]
cmap_PN = plt.get_cmap('viridis')

# Calculate the actual maximum value in the selected data range for PN
max_val_PN = PN_data_selected.max()

# --- Load Data for PM ---
PM = np.loadtxt('PM_dep.dat')
num_height_levels_PM = PM.shape[1]

# Define the time and height axes for PM
time_total_hours_PM = np.linspace(0, 120, PM.shape[0])  # Total time in hours
time_days_PM = time_total_hours_PM / 24.0  # Time in days
height_file_PM = np.loadtxt('hh.dat')
height_PM = height_file_PM[:]

# Select the time range indices corresponding to Day 3.0 to Day 5.0 for PM
idx_start_PM = np.abs(time_days_PM - time_start_day).argmin()
idx_end_PM = np.abs(time_days_PM - time_end_day).argmin()

# Extract the data and time for the selected range for PM
PM_data_selected = PM[idx_start_PM:idx_end_PM+1, :]
time_days_selected_PM = time_days_PM[idx_start_PM:idx_end_PM+1]

# Create meshgrid for contour plot for PM
T_PM, H_PM = np.meshgrid(time_days_selected_PM, height_PM)

# Define contour levels for PM based on the example colorbar
levels_PM = [0.000, 1.200, 1.225, 1.250, 1.275, 1.300, 1.325, 1.350]
cmap_PM = plt.get_cmap('viridis')
norm_PM = mcolors.BoundaryNorm(levels_PM, cmap_PM.N)  # Ensure color boundaries match

# Calculate the actual maximum value in the selected data range for PM
max_val_PM = PM_data_selected.max()

# --- Plotting PN and PM Contour Plots in Subplots ---
fig, axs = plt.subplots(1, 2, figsize=(16, 6))

# Plot PN heatmap
cf_PN = axs[0].contourf(T, H, PN_data_selected.T, levels=levels_PN, cmap=cmap_PN, extend='max')
axs[0].set_xlabel("Day (d)")
axs[0].set_ylabel("Height (m)")
axs[0].set_title(f"Total Particle Number Concentration\nmax={max_val_PN:.2e}", loc='center')
axs[0].set_xlim(time_start_day, time_end_day)
axs[0].set_ylim(0, 3000)

# Plot PM heatmap
cf_PM = axs[1].contourf(T_PM, H_PM, PM_data_selected.T, levels=levels_PM, cmap=cmap_PM, norm=norm_PM, extend='max')
axs[1].set_xlabel("Day (d)")
axs[1].set_ylabel("Height (m)")
axs[1].set_title(f"Total Particle Mass Concentration\nmax={max_val_PM:.2e}", loc='center')
axs[1].set_xlim(time_start_day, time_end_day)
axs[1].set_ylim(0, 3000)

# Add colorbars
cbar_PN = plt.colorbar(cf_PN, ax=axs[0], ticks=levels_PN)
cbar_PN.set_label(r"PN (# cm$^{-3}$)")  # Use LaTeX for units

cbar_PM = plt.colorbar(cf_PM, ax=axs[1], ticks=levels_PM)
cbar_PM.set_label(r"PM ($\mu g/m^{-3}$)")  # Use LaTeX for units

# Adjust layout to avoid title overlap
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to prevent title overlap

# Save the figure
plt.savefig("combined_plots_i.png")
