import numpy as np
import matplotlib.pyplot as plt

# Read the diameter data (in meters)
diameter_file = "diameter.dat"
diameter = np.loadtxt(diameter_file)

# Convert diameter to nanometers (if needed)
diameter_nm = diameter * 1e9  # Convert to nm

# Read the particle concentration data (in particles per m^3)
conc_file = "particle_conc.dat"
concentrations = np.loadtxt(conc_file)

# Convert concentration from particles per m^3 to particles per cm^3
concentrations_cm3 = concentrations / 1e6

# Calculate the volume of particles (in cubic micrometers)
# Volume (μm³) = (π / 6) * d³, where d is in nanometers (nm)
# Convert to μm³ by dividing the result by 10^9
volume_μm3 = (np.pi / 6) * (diameter_nm ** 3) / 1e9  # Volume in μm³

# Calculate the volume concentration for each time step
# Volume concentration = N * V, where N is concentration and V is volume
volume_concentration = concentrations_cm3 * volume_μm3  # Volume concentration in μm³/cm³

# Sum the volume concentrations across all size bins to get the total volume concentration at each time step
total_volume_concentration = np.sum(volume_concentration, axis=1)  # Sum along size bins for each time step

# Define time steps based on your concentration data
# Assuming each row in concentrations corresponds to a time step, define time values accordingly
time = np.linspace(0, 1, 25)

# Create the plot
plt.figure(figsize=(10, 6))

# Plot volume concentration change over time
plt.plot(time, total_volume_concentration, linestyle='--', color='b')

# Label the plot
plt.xlabel('Time (Days)')
plt.ylabel(r'$PV$ ($\mu$m$^3$/cm$^3$)')
plt.title('Volume Concentration')
plt.xlim(0, max(time))
plt.grid(True, which="both", ls="--")

# Save the plot
plt.savefig("PV.png")
