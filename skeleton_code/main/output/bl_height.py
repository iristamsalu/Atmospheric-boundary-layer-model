from matplotlib import pyplot as plt
import numpy as np

# Load data
height = np.loadtxt('hh.dat')       # 50 height levels
height = height.reshape(-1) 

time   = np.loadtxt('time.dat')     # Time steps
time   = time * 24

Ri_winter = np.loadtxt('Ri_winter.dat').T
Ri_summer = np.loadtxt('Ri_summer.dat').T


# Find boundary layer height at each time step
boundary_layer_heights_winter = []
boundary_layer_heights_summer = []


for i in range(len(time)):  # Loop over time steps
    idx_winter = np.argmin(np.abs(Ri_winter[:, i] - 0.25))  # Find altitude index where Ri is closest to 0.25
    idx_summer = np.argmin(np.abs(Ri_summer[:, i] - 0.25))  # Find altitude index where Ri is closest to 0.25
    boundary_layer_heights_winter.append(height[idx_winter])
    boundary_layer_heights_summer.append(height[idx_summer])

# Plot evolution of boundary layer height over time
plt.figure(figsize=(10, 5))
plt.plot(time, boundary_layer_heights_winter, label="BL height 18.02.2011 (Ri ≈ 0.25)", color="b")
plt.plot(time, boundary_layer_heights_summer, label="BL height 10.07.2011 (Ri ≈ 0.25)", color="r")
plt.xlabel("Time (hours)")
plt.ylabel("Boundary layer height (m)")
plt.title("Boundary layer (BL) height comparison in winter and in summer at SMEAR II")
plt.legend()
plt.xlim(0,max(time))
plt.grid()
plt.savefig('bl_height.png')