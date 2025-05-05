import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load sata
# PN and PM
PN_cond = np.loadtxt('PN_cond.dat')
PN_coag = np.loadtxt('PN_coag.dat')
PN_coag_cs = np.loadtxt('PN_coag_cs10-4.dat')
PN_dep = np.loadtxt('PN.dat')

PM_cond = np.loadtxt('PM_cond.dat')
PM_coag = np.loadtxt('PM_coag.dat')
PM_coag_cs = np.loadtxt('PM_coag_cs10-4.dat')
PM_dep = np.loadtxt('PM.dat')

# Deposition velocity
vd_particle = np.loadtxt('dep_v_particle.dat')
vd_gas = np.loadtxt('dep_v_gas.dat')
diameter_nm = np.loadtxt("diameter.dat") * 1e9

# Time and height
time = np.linspace(0, 120, 121) / 24  # in days
height = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
          100, 120, 140, 160, 180, 200, 230, 260, 300, 350,
          400, 450, 500, 550, 600, 650, 700, 800, 900, 1000,
          1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000,
          2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]

# Extract relevant data
# PN vertical (day 5)
PN_cond_day5 = PN_cond[-1] * 1e-5
PN_coag_day5 = PN_coag[-1] * 1e-5
PN_coag_cs_day5 = PN_coag_cs[-1] * 1e-5
PN_dep_day5 = PN_dep[-1] * 1e-5

# PM vertical (day 5)
PM_cond_day5 = PM_cond[-1]
PM_coag_day5 = PM_coag[-1]
PM_coag_cs_day5 = PM_coag_cs[-1]
PM_dep_day5 = PM_dep[-1]

# PN time series
PN_cond_hh10 = PN_cond[:, 1]
PN_coag_hh10 = PN_coag[:, 1]
PN_coag_cs_hh10 = PN_coag_cs[:, 1]
PN_dep_hh10 = PN_dep[:, 1]

PN_cond_hh2000 = PN_cond[:, 39]
PN_coag_hh2000 = PN_coag[:, 39]
PN_coag_cs_hh2000 = PN_coag_cs[:, 39]
PN_dep_hh2000 = PN_dep[:, 39]

# PM time series
PM_cond_hh10 = PM_cond[:, 1]
PM_coag_hh10 = PM_coag[:, 1]
PM_coag_cs_hh10 = PM_coag_cs[:, 1]
PM_dep_hh10 = PM_dep[:, 1]

PM_cond_hh2000 = PM_cond[:, 39]
PM_coag_hh2000 = PM_coag[:, 39]
PM_coag_cs_hh2000 = PM_coag_cs[:, 39]
PM_dep_hh2000 = PM_dep[:, 39]

# Deposition velocities
vd_SO2 = vd_gas[:, 0]
vd_O3 = vd_gas[:, 1]
vd_HNO3 = vd_gas[:, 2]
vd_isoprene = vd_gas[:, 3]
vd_apinene = vd_gas[:, 4]
vd_particle_last = vd_particle[-1]

# Plotting
fig, axs = plt.subplots(3, 2, figsize=(16, 14))

# 1. PN Vertical Profile
axs[0, 0].plot(PN_cond_day5, height, label="Nuc. & Cond.", color='blue')
axs[0, 0].plot(PN_coag_day5, height, label="+ Coag.", color='red')
axs[0, 0].plot(PN_coag_cs_day5, height, label="CS=0.001", color='orange')
axs[0, 0].plot(PN_dep_day5, height, label="+ Dep.", color='green')
axs[0, 0].set_xlabel(r"PN ($\times10^5$ cm$^{-3}$)")
axs[0, 0].set_ylabel("Height (m)")
axs[0, 0].set_xlim(0, 1.2)
axs[0, 0].set_ylim(0, 3000)
axs[0, 0].set_title("PN Vertical Profile (Day 5)")
axs[0, 0].grid(True)
axs[0, 0].legend()

# 2. PM Vertical Profile
axs[0, 1].plot(PM_cond_day5, height, color='blue')
axs[0, 1].plot(PM_coag_day5, height, color='red')
axs[0, 1].plot(PM_coag_cs_day5, height, color='orange')
axs[0, 1].plot(PM_dep_day5, height, color='green')
axs[0, 1].set_xlabel(r"PM ($\mu g/m^3$)")
axs[0, 1].set_xlim(1.0, 1.65)
axs[0, 1].set_ylim(0, 3000)
axs[0, 1].set_title("PM Vertical Profile (Day 5)")
axs[0, 1].grid(True)

# 3. PN Time Series
axs[1, 0].plot(time[72:], PN_cond_hh10[72:], '-', color='blue')
axs[1, 0].plot(time[72:], PN_coag_hh10[72:], '-', color='red')
axs[1, 0].plot(time[72:], PN_coag_cs_hh10[72:], '-', color='orange')
axs[1, 0].plot(time[72:], PN_dep_hh10[72:], '-', color='green')
axs[1, 0].plot(time[72:], PN_cond_hh2000[72:], '--', color='blue')
axs[1, 0].plot(time[72:], PN_coag_hh2000[72:], '--', color='red')
axs[1, 0].plot(time[72:], PN_coag_cs_hh2000[72:], '--', color='orange')
axs[1, 0].plot(time[72:], PN_dep_hh2000[72:], '--', color='green')
axs[1, 0].set_xlim(3, 5)
axs[1, 0].set_ylim(0, 12e4)
axs[1, 0].set_xlabel("Time (days)")
axs[1, 0].set_ylabel(r"PN ($\mathrm{cm}^{-3}$)")
axs[1, 0].set_title("PN Time Series")
axs[1, 0].grid(True)
axs[1, 0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y*1e-4:.1f}'))
axs[1, 0].text(0.01, 0.98, r'$\times10^{4}$', transform=axs[1, 0].transAxes,
              fontsize=10, verticalalignment='top')

# 4. PM Time Series
axs[1, 1].plot(time[73:], PM_cond_hh10[73:], '-', color='blue')
axs[1, 1].plot(time[73:], PM_coag_hh10[73:], '-', color='red')
axs[1, 1].plot(time[73:], PM_coag_cs_hh10[73:], '-', color='orange')
axs[1, 1].plot(time[73:], PM_dep_hh10[73:], '-', color='green')
axs[1, 1].plot(time[73:], PM_cond_hh2000[73:], '--', color='blue')
axs[1, 1].plot(time[73:], PM_coag_hh2000[73:], '--', color='red')
axs[1, 1].plot(time[73:], PM_coag_cs_hh2000[73:], '--', color='orange')
axs[1, 1].plot(time[73:], PM_dep_hh2000[73:], '--', color='green')
axs[1, 1].set_xlim(3, 5)
axs[1, 1].set_ylim(1.0, 1.65)
axs[1, 1].set_xlabel("Time (days)")
axs[1, 1].set_ylabel(r"PM ($\mu g/m^3$)")
axs[1, 1].set_title("PM Time Series")
axs[1, 1].grid(True)

# 5. Gas Deposition Velocity
axs[2, 0].plot(time[73:], vd_SO2[73:], '-', label="SO2", color="orange")
axs[2, 0].plot(time[73:], vd_O3[73:], '-', label="O3", color="purple")
axs[2, 0].plot(time[73:], vd_HNO3[73:], '-', label="HNO3", color="red")
axs[2, 0].plot(time[73:], vd_isoprene[73:], '--', label="isoprene", color="blue")
axs[2, 0].plot(time[73:], vd_apinene[73:], '--', label="apinene", color="green")
axs[2, 0].set_yscale("log")
axs[2, 0].set_xlim(3, 5)
axs[2, 0].set_ylim(1e-9, 1e-1)
axs[2, 0].set_title("Gas Deposition Velocity")
axs[2, 0].set_xlabel("Time (days)")
axs[2, 0].set_ylabel("Velocity (m/s)")
axs[2, 0].legend()
axs[2, 0].grid(True, which="both", linestyle="--", linewidth=0.5)

# 6. Particle Deposition Velocity
axs[2, 1].plot(diameter_nm, vd_particle_last, '-', color='blue', label="After 5 days")
axs[2, 1].set_xscale("log")
axs[2, 1].set_yscale("log")
axs[2, 1].set_xlim(3, 3000)
axs[2, 1].set_ylim(2e-4, 2e-2)
axs[2, 1].set_title("Particle Deposition Velocity")
axs[2, 1].set_xlabel("Diameter (nm)")
axs[2, 1].set_ylabel("Velocity (m/s)")
axs[2, 1].grid(True, which="both", linestyle="--", linewidth=0.5)
axs[2, 1].legend()

plt.suptitle("Particle and Gas Processes Overview", fontsize=18)
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig("combined_plots_ii.png")
