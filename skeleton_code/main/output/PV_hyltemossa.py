import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the file
PV_data = np.loadtxt('PV.dat')

# Sum across each row to get total PV
PV_total = PV_data.sum(axis=1)

# Time setup: 121 timesteps over 5 days
time = np.linspace(0, 120, 121) / 24  # convert hours to days

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time[96:], PV_total[96:], linestyle="-", color="blue", label="Total PV")

plt.title("Total particle volume concentration")
plt.xlabel("Time (days)")
plt.ylabel(r"Volume ($\mathrm{\mu m}^3\,\mathrm{cm}^{-3}$)")
plt.grid(True)
# plt.xlim(4, 5)
# plt.ylim(0, 2e4)


plt.legend()
plt.tight_layout()
plt.savefig("PV_hyltemossa.png")
