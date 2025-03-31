import numpy as np
import matplotlib.pyplot as plt

# Load data (assuming PN_hh and PM_hh are 1D arrays with heights)
height =   [    0,   10,   20,   30,   40,   50,   60,   70,   80,   90,
                100,  120,  140,  160,  180,  200,  230,  260,  300,  350,
                400,  450,  500,  550,  600,  650,  700,  800,  900, 1000,
                1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000,
                2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]  # Heights in meters
PN_all = np.loadtxt('PN.dat')
# PN_2 = np.loadtxt('PN_2.dat')
PM_all = np.loadtxt('PM.dat') 
# PM_2 = np.loadtxt('PM_2.dat') 

PN_all_day5 = PN_all[-1]
PM_all_day5 = PM_all[-1]

# Create figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(8, 6), sharey=True)
fig.suptitle('Final (after 5 days) vertical profiles of the total particle number and total particle mass conc.')

# Plot Total Particle Number Concentration (PN)
# axes[0].plot(PN_2, height, label="Nucleation, Condensation", color='blue')
axes[0].plot(PN_all_day5, height, label="Nucleation, Condensation, Coagulation sink", color='brown')
axes[0].set_xlabel(r'Total PN (cm$^{-3}$)')
axes[0].set_ylabel('Height (m)')
axes[0].grid(True)
axes[0].legend(loc="lower left")

# Plot Total Particle Mass Concentration (PM)
# axes[1].plot(PM_2, height, label="Nucleation, Condensation", color='blue')
axes[1].plot(PM_all_day5, height, label="Nucleation, Condensation, Coagulation sink", color='brown')
axes[1].set_xlabel(r'PM ($\mu g/m^3$)')
axes[1].grid(True)

# Adjust layout and save
fig.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=2)
plt.tight_layout()
plt.savefig('vertical_profiles.png')
