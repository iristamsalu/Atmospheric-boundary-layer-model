import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

PN_coag = np.loadtxt('PN_coag.dat')
PN_cond = np.loadtxt('PN_cond.dat')
PN_coag_hh1 = PN_coag[:, 0]
PN_cond_hh1 = PN_cond[:, 0]
time = np.linspace(0, 120, 121)
time = time / 24

plt.figure(figsize=(10, 8))
plt.plot(time[72:], PN_cond_hh1[72:], linestyle="--", label="Nucleation & Condensation")
plt.plot(time[72:], PN_coag_hh1[72:], linestyle="--", label="Nucleation, Condensation & Coagulation sink")


plt.legend()
plt.title("Total particle number concentration in the first model layer")
plt.xlabel("Time (days)")
plt.ylabel(r"PN ($\mathrm{cm}^{-3}$)")
plt.grid(True)
plt.xlim(3, 5)
plt.ylim(0, 12*10**4)

# Format the y-axis to show values in scientific notation without '10⁴' repeating
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y*1e-4:.1f}'))

# Append '×10⁴' at the end of the y-axis using a secondary label
plt.gca().set_ylabel(r"PN ($\mathrm{cm}^{-3}$)", fontsize=12, labelpad=10)
plt.gca().tick_params(axis='y', labelsize=12)

# Add '×10⁴' at the end of the y-axis in the correct position
plt.gca().text(0.0, 1.05, r'$\times10^{4}$', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left')

plt.tight_layout()
plt.savefig("PN.png")
