import numpy as np
import matplotlib.pyplot as plt

# Load diameter in meters and convert to nanometers
diameter_file = "diameter.dat"
diameter_m = np.loadtxt(diameter_file)
diameter_nm = diameter_m * 1e9

# Load particle concentration in #/m³ and convert to #/cm³
conc_file_nucl = "particle_conc_1.dat"
conc_file_cond = "particle_conc_2.dat"
conc_file_coag = "particle_conc_3.dat"
conc_nucl = np.loadtxt(conc_file_nucl)
conc_cond = np.loadtxt(conc_file_cond)
conc_coag = np.loadtxt(conc_file_coag)

# Convert concentration from particles per m^3 to particles per cm^3
conc_nucl_cm3 = conc_nucl / 1e6
conc_cond_cm3 = conc_cond / 1e6
conc_coag_cm3 = conc_coag / 1e6

# Select last timestep or average — here using last timestep
latest_conc_nucl = conc_nucl_cm3[-1, :]
latest_conc_cond = conc_cond_cm3[-1, :]
latest_conc_coag = conc_coag_cm3[-1, :]


# Plotting
plt.figure(figsize=(10, 8))
plt.plot(diameter_nm, latest_conc_nucl, linestyle='-', color='b', label="Only Nucleation")
plt.plot(diameter_nm, latest_conc_cond, linestyle='-', color='red', label="Nucleation & Condensation")
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