import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


PN = np.loadtxt('PN.dat')
# Extract data at 10 m height
PN_coag_hh10 = PN[:, 1]

time_hours = np.linspace(0, 120, 121)  # time in hours
# Extract data for the 5th day
start_hour = 96
end_hour = 120
start_idx = int(start_hour)
end_idx = int(end_hour) + 1
# Convert x-axis to 0–24 h
time_5th_day = time_hours[start_idx:end_idx] - start_hour


plt.figure(figsize=(10, 6))
plt.plot(time_5th_day, PN_coag_hh10[start_idx:end_idx], '-', color='red', label='10 m')
plt.title("Total PN at 10 m")
plt.xlabel("Time (hours)")
plt.ylabel(r"PN ($\mathrm{cm}^{-3}$)")
plt.grid(True)
plt.xlim(0, 24)
plt.ylim(0, 20e4)

# Format y-axis to match combined plot: x104
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y * 1e-4:.1f}'))
plt.gca().text(0.01, 0.98, r'$\times10^{4}$', transform=plt.gca().transAxes,
               fontsize=12, verticalalignment='top', horizontalalignment='left')

plt.tight_layout()
plt.savefig("PN_hyltemossa_10m.png")
