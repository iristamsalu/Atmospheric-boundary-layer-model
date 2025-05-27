import numpy as np
import matplotlib.pyplot as plt

PV = np.loadtxt('PV.dat')
# Extract data at 10 m height
PV_hh10 = PV[:, 1]

time_hours = np.linspace(0, 120, 121)  # time in hours
# Extract data for the 5th day
start_hour = 96
end_hour = 120
start_idx = int(start_hour)
end_idx = int(end_hour) + 1
# Convert x-axis to 0–24 h
time_5th_day = time_hours[start_idx:end_idx] - start_hour

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_5th_day, PV_hh10[start_idx:end_idx], '-', color='red', label='10 m')
plt.title("Total PV at 10 m")
plt.xlabel("Time (hours)")
plt.ylabel(r"Volume ($\mathrm{\mu m}^3\,\mathrm{cm}^{-3}$)")
plt.grid(True)
plt.xlim(0, 24)
plt.legend()
plt.tight_layout()
plt.savefig("PV_hyltemossa_h10m.png")
