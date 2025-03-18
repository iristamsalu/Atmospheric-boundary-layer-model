import numpy as np
import matplotlib.pyplot as plt

# Read the particle concentration data (in particles per m^3)
conc_file_nucl = "volume_conc_1.dat"
conc_file_cond = "volume_conc_2.dat"
conc_file_coag = "volume_conc_3.dat"
conc_nucl = np.loadtxt(conc_file_nucl)
conc_cond = np.loadtxt(conc_file_cond)
conc_coag = np.loadtxt(conc_file_coag)

# Define time steps based on your concentration data
# Assuming each row in concentrations corresponds to a time step, define time values accordingly
time = np.linspace(0, 1, 25)

# Create the plot
plt.figure(figsize=(10, 3))

# Plot volume concentration change over time
plt.plot(time, conc_nucl, linestyle='-', color='b', label="Only nucleation")
plt.plot(time, conc_cond, linestyle='--', color='red', label="Nucleation and condensation")
plt.plot(time, conc_coag, linestyle='-', color='orange', label="Nucleation, condensation and coagulation")

# Label the plot
plt.xlabel('Time (Days)')
plt.ylabel(r'$PV$ ($\mu$m$^3$/cm$^3$)')
plt.title('Volume Concentration')
plt.xlim(0, max(time))
plt.legend()
plt.grid(True, which="both", ls="--")

# Save the plot
plt.savefig("PV2.png")
