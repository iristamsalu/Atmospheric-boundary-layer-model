import numpy as np
import matplotlib.pyplot as plt

# Load diameter in meters and convert to nanometers
diameter_file = "diameter.dat"
diameter_m = np.loadtxt(diameter_file)
diameter_nm = diameter_m * 1e9

# Load particle concentration in #/m3 and convert to #/cm3
conc_file_coag = "particle_conc.dat"
conc_coag = np.loadtxt(conc_file_coag)

# Convert concentration from particles per m^3 to particles per cm^3
conc_coag_cm3 = conc_coag / 1e6

# Select last timestep or average — here using last timestep
latest_conc_coag = conc_coag_cm3[-1, :]


# Plotting
plt.figure(figsize=(10, 8))
plt.plot(diameter_nm, latest_conc_coag, linestyle='--', color='orange', label="Nucleation, Condensation & Coagulation")

# Axes
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Particle Diameter (nm)')
plt.ylabel(r'$\Delta N$ (cm$^{-3}$)')
plt.title('Particle Size Distribution')

# Grid + axis limits
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.xlim(10**0, 10**3)
plt.ylim(10**-6)

# Legend
plt.legend()

# Save plot
plt.tight_layout()
plt.savefig("PSD", dpi=300)