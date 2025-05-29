import numpy as np
import matplotlib.pyplot as plt

vd_particle = np.loadtxt('dep_v_particle.dat')
vd_gas = np.loadtxt('dep_v_gas.dat')

# Gases
vd_SO2 = vd_gas[:,0]
vd_O3 = vd_gas[:,1]
vd_HNO3 = vd_gas[:,2]
vd_isoprene = vd_gas[:,3]
vd_apinene = vd_gas[:,4]

time = np.linspace(0, 120, 121)
time = time / 24

# Particles
# at last timestep
vd_particle_last = vd_particle[-1]

diameter_file = "diameter.dat"
diameter_m = np.loadtxt(diameter_file)
diameter_nm = diameter_m * 1e9

plt.figure(figsize=(10, 6))
plt.plot(time[73:], vd_SO2[73:], linestyle="-", label="SO2", color="orange")
plt.plot(time[73:], vd_O3[73:], linestyle="-", label="O3", color="purple")
plt.plot(time[73:], vd_HNO3[73:], linestyle="-", label="HNO3", color="red")
plt.plot(time[73:], vd_isoprene[73:], linestyle="--", label="isoprene", color="blue")
plt.plot(time[73:], vd_apinene[73:], linestyle="--", label="apinene", color="green")
plt.legend()
plt.yscale("log")
plt.title("Gas Dry Deposition Velocity (m/s)")
plt.xlabel("Time (days)")
plt.ylabel("Deposition Velocity m/s")
plt.grid(True)
plt.xlim(3, 5)
plt.ylim(10**-9, 10**-1)
plt.savefig("dep_v_gas.png")

# Plot particle deposition
plt.figure(figsize=(10, 6))
plt.plot(diameter_nm, vd_particle_last, linestyle="-", label="After 5 days", color="blue")
plt.legend()
plt.xscale("log")
plt.yscale("log")
plt.title("Particle Dry Deposition Velocity (m/s)")
plt.xlabel("Diameter (nm)")
plt.ylabel("Deposition Velocity (m/s)")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.xlim(3, 3000)        # Diameter from ~3 nm to 3000 nm
plt.ylim(2e-4, 2e-2)   
plt.tight_layout()
plt.savefig("dep_v_particle.png")