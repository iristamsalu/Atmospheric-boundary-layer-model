import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import LogLocator, NullLocator

# 1) Load & preprocess data
diam = np.loadtxt("diameter.dat")                 # diameter in meters
psd  = np.loadtxt("particle_conc_10.dat") / 1e6  # #/m³ → #/cm³
time = np.linspace(0, 5, 121)                     # days

# 2) Select time window: day 3 → day 5 (converted to hours)
i0 = np.abs(time - 4).argmin()
i1 = np.abs(time - 5).argmin()
time_hours = (time[i0:i1+1] - time[i0]) * 24      # 0 to 48 hours
T, D = np.meshgrid(time_hours, diam)

# 3) Contour levels and normalization (linear 0 → 2.5e4)
vmin, vmax = 0, 2.5e4
levels = np.linspace(vmin, vmax, 21)

# 4) Draw the filled contours
plt.figure(figsize=(8,5))
cs = plt.contourf(
    T, D,
    psd[i0:i1+1].T,
    levels=levels,
    norm=Normalize(vmin=vmin, vmax=vmax),
    cmap='jet'
)

# 5) Log scale on y axis, ticks at decades
ax = plt.gca()
ax.set_yscale('log')
ax.set_xlim(0, 24)
ax.set_ylim(3e-9, 1e-7)
ax.yaxis.set_major_locator(LogLocator(base=10))
ax.yaxis.set_minor_locator(NullLocator())

# 6) Labels & title
plt.xlabel('Time (h)')
plt.ylabel('Diameter (m)')
plt.title('PSD at 10 m')

# 7) Colorbar 0 → 2 ×10⁴ with labeled ticks
cbar = plt.colorbar(
    cs,
    ticks=[0, 5000, 10000, 15000, 20000],
    spacing='proportional'
)
cbar.set_ticklabels(['0.0', '0.5', '1.0', '1.5', '2.0'])
cbar.set_label(r'$\mathrm{d}N/\mathrm{d}\log_{10} D_p \ (10^{4} \ \mathrm{cm}^{-3})$')

plt.tight_layout()
plt.savefig("hyltemossa_psd_heatmap_10m_hours.png")
