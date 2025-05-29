import numpy as np
import matplotlib.pyplot as plt

# === Configuration ===
species_name = "H2SO4"
species_index = 20              # Change based on the column position of a chemical species
num_height_levels = 50         
time_total_hours_span = 120    # Total duration in hours

# === Load and Reshape Data ===
data = np.loadtxt('Concentrations.dat')  # shape: (timesteps * height_levels, num_species)
concentration_flat = data[:, species_index]  # Extract the desired species

num_timesteps = concentration_flat.shape[0] // num_height_levels
concentrations = concentration_flat.reshape((num_timesteps, num_height_levels))

# === Define Time and Height Axes ===
time_total_hours = np.linspace(0, time_total_hours_span, num_timesteps)
time_days = time_total_hours / 24.0
height_file = np.loadtxt('hh.dat')
height = height_file[:]

# === Select Time Range: Day 3.0 to Day 5.0 ===
time_start_day = 3.0
time_end_day = 5.0
idx_start = np.abs(time_days - time_start_day).argmin()
idx_end = np.abs(time_days - time_end_day).argmin()

# Extract data in selected time range
concentration_selected = concentrations[idx_start:idx_end+1, :] * 10**-7
print(concentration_selected)
time_days_selected = time_days[idx_start:idx_end+1]

# === Create Meshgrid for Contour Plot ===
T, H = np.meshgrid(time_days_selected, height)

# === Plotting ===
plt.figure(figsize=(8, 6))

# Contour levels and colormap
levels = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
cmap = plt.get_cmap('viridis')
max_val = concentration_selected.max()

# Transpose data for plotting: shape (height, time)
cf = plt.contourf(T, H, concentration_selected.T, levels=levels, cmap=cmap, extend='max')

# Labels and Title
plt.xlabel("Day (d)")
plt.ylabel("Height (m)")
plt.title(f"{species_name} Concentration\nmax = {max_val:.2e} x10^7", loc='center')

# Colorbar
cbar = plt.colorbar(cf, ticks=levels)
cbar.set_label(r"Concentration (# cm$^{-3}$)")

# Axis limits
plt.xlim(time_start_day, time_end_day)
plt.ylim(0, 3000)

# Layout and Save
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("chemistry_heatmap.png")
