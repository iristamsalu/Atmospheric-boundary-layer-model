import numpy as np
import matplotlib.pyplot as plt

# Read the diameter data (assuming it's a single row of particle diameters in meters)
diameter_file = "diameter.dat"
diameter = np.loadtxt(diameter_file)  # Read the diameters

# Read the particle concentration data (assuming a 2D matrix with concentrations for each size)
conc_file = "particle_conc.dat"
concentrations = np.loadtxt(conc_file)  # Read concentrations (shape: 25, 100)

# Convert the diameter from meters to nanometers (1 meter = 1e9 nanometers)
diameter_nm = diameter * 1e9

# Convert concentration from particles per cubic meter to particles per cubic centimeter (1 m^3 = 1e6 cm^3)
concentrations_cm3 = concentrations / 1e6  # Each column corresponds to concentrations at a particular size

# Sum the concentrations across rows (if you want to aggregate them into a single distribution)
aggregated_concentration = np.sum(concentrations_cm3, axis=0)

# Create the plot for the particle size distribution
plt.figure(figsize=(10, 6))

# Plot concentration vs diameter (log scale for both axes)
plt.plot(diameter_nm, aggregated_concentration, linestyle='-', color='b')

# Labeling the plot
plt.xscale('log')  # Log scale for diameter (nm)
plt.yscale('log')  # Log scale for concentration (cm^3)
plt.xlabel('Particle Diameter (nm)')
plt.ylabel(r'$\Delta N$ (cm$^{-3}$)')
plt.xlim(0)
plt.title('Particle Size Distribution')
plt.grid(True, which="both", ls="--")

# Save the plot as an image (optional)
plt.savefig("particle_size_distribution.png")

