import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import LogLocator, NullLocator


diam = np.loadtxt("diameter.dat")                 
psd  = np.loadtxt("particle_conc_10.dat") / 1e6 
time = np.linspace(0, 5, 121)


i0 = np.abs(time - 4).argmin()
i1 = np.abs(time - 5).argmin()
time_hours = (time[i0:i1+1] - time[i0]) * 24
T, D = np.meshgrid(time_hours, diam)

# 3) Contour levels and normalization (linear 0 → 2.5e4)
vmin, vmax = 0, 2.5e4
levels = np.linspace(vmin, vmax, 21)

plt.figure(figsize=(8,5))
cs = plt.contourf(
    T, D,
    psd[i0:i1+1].T,
    levels=levels,
    norm=Normalize(vmin=vmin, vmax=vmax),
    cmap='jet'
)

ax = plt.gca()
ax.set_yscale('log')
ax.set_xlim(0, 24)
ax.set_ylim(3e-9, 1e-7)
ax.yaxis.set_major_locator(LogLocator(base=10))
ax.yaxis.set_minor_locator(NullLocator())

plt.xlabel('Time (h)')
plt.ylabel('Diameter (m)')
plt.title('PSD at 10 m')

cbar = plt.colorbar(
    cs,
    ticks=[0, 5000, 10000, 15000, 20000],
    spacing='proportional'
)
cbar.set_ticklabels(['0.0', '0.5', '1.0', '1.5', '2.0'])
cbar.set_label(r'$\mathrm{d}N/\mathrm{d}\log_{10} D_p \ (10^{4} \ \mathrm{cm}^{-3})$')

plt.tight_layout()
plt.savefig("psd_heatmap_10m.png")
