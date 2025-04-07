import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load data (assuming PN_hh and PM_hh are 1D arrays with heights)
height = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
          100, 120, 140, 160, 180, 200, 230, 260, 300, 350,
          400, 450, 500, 550, 600, 650, 700, 800, 900, 1000,
          1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000,
          2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]  # Heights in meters

PN_all = np.loadtxt('PN_coag.dat')
PM_all = np.loadtxt('PM_coag.dat')
PN_cond = np.loadtxt('PN.dat')
PM_cond = np.loadtxt('PM.dat')

PN_all_day5 = PN_all[-1]
PM_all_day5 = PM_all[-1]
PN_cond_day5 = PN_cond[-1]
PM_cond_day5 = PM_cond[-1]

# Plot Total Particle Number Concentration (PN)
plt.figure(figsize=(6, 10))
plt.plot(PN_all_day5, height, label="Nucleation, Condensation, Coagulation sink", color='brown')
plt.plot(PN_cond_day5, height, label="Nucleation & Condensation", color='blue')
plt.xlabel(r'Total PN (cm$^{-3}$)', fontsize=12, labelpad=10)
plt.ylabel('Height (m)', fontsize=12, labelpad=10)
plt.title('Vertical profiles of the total particle number after 5 days', fontsize=14, pad=15)
plt.grid(True)
plt.legend(loc="lower left")
plt.xlim(0*10**4, 15*10**4)
plt.ylim(0, 3000)
plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
plt.gca().ticklabel_format(style='sci', axis='x', scilimits=(4,4))
plt.tight_layout()
plt.savefig('vertical_profile_PN.png')


# Plot Total Particle Mass Concentration (PM)
plt.figure(figsize=(5, 10))
plt.plot(PM_all_day5, height, label="Nucleation, Condensation, Coagulation sink", color='brown')
plt.plot(PM_cond_day5, height, label="Nucleation & Condensation", color='blue')
plt.xlabel(r'PM ($\mu g/m^3$)')
plt.ylabel('Height (m)')
plt.title('Vertical profiles of the total particle mass conc after 5 days')
plt.grid(True)
plt.legend(loc="lower left")
plt.xlim
plt.ylim(0, 3000)
plt.savefig('vertical_profile_PM.png')
