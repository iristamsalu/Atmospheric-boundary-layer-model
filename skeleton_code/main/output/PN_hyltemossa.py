import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the file
PN_data = np.loadtxt('PN.dat')

# Sum across each row to get total PN
# PN_total = PN_data.sum(axis=1)
PN_mean = PN_data.mean(axis=1)

# Time setup: 121 timesteps over 5 days
time = np.linspace(0, 120, 121) / 24  # convert hours to days

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time[96:], PN_mean[96:], linestyle="-", color="blue", label="Total PN")

plt.title("Total particle number concentration")
plt.xlabel("Time (days)")
plt.ylabel(r"PN ($\mathrm{cm}^{-3}$)")
plt.grid(True)
# plt.xlim(4, 5)
# plt.ylim(0, 2e4)

# Format y-axis in terms of ×10⁴
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y * 1e-4:.1f}'))
plt.gca().set_ylabel(r"PN ($\mathrm{cm}^{-3}$)", fontsize=12, labelpad=10)
plt.gca().tick_params(axis='y', labelsize=12)
plt.gca().text(0.0, 1.05, r'$\times10^{4}$', transform=plt.gca().transAxes,
               fontsize=12, verticalalignment='top', horizontalalignment='left')

plt.legend()
plt.tight_layout()
plt.savefig("PN_hyltemossa.png")
