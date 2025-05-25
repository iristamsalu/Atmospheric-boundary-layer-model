import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator, NullFormatter

# your grid‐values
cs_vals  = np.array([0.0001, 0.001, 0.01])
so2_vals = np.array([0.05,   0.5,   5.0])

# 2) filenames[i][j] must be the file for so2_vals[i], cs_vals[j]:
filenames = [
    # so2 = 0.05 → files for cs = 0.0001, 0.001, 0.01
    [ 'Concentrations_h50_basebase.dat',
      'Concentrations_h50_basehigh.dat',
      'Concentrations_h50_baselow.dat' ],
    # so2 = 0.5
    [ 'Concentrations_h50_highbase.dat',
      'Concentrations_h50_highhigh.dat',
      'Concentrations_h50_highlow.dat' ],
    # so2 = 5.0
    [ 'Concentrations_h50_lowbase.dat',
      'Concentrations_h50_lowhigh.dat',
      'Concentrations_h50_lowlow.dat' ]
]

# pre‐allocate array
H2so4_avg = np.zeros((len(so2_vals), len(cs_vals)))

# build mesh
CSg, SO2g = np.meshgrid(cs_vals, so2_vals)

fig, ax = plt.subplots(figsize=(6,5))

# 1) use a LogNorm color‐scale so color reflects orders of magnitude
pcm = ax.pcolormesh(
    CSg, SO2g, H2so4_avg,
    norm=LogNorm(vmin=H2so4_avg.min(), vmax=H2so4_avg.max()),
    cmap='viridis', shading='auto'
)

# 2) log axes
ax.set_xscale('log')
ax.set_yscale('log')

# 3) nice tick locators
ax.xaxis.set_major_locator(LogLocator(base=10))
ax.xaxis.set_minor_locator(LogLocator(base=10, subs=(2,3,4,5,6,7,8,9)))
ax.yaxis.set_major_locator(LogLocator(base=10))
ax.yaxis.set_minor_locator(LogLocator(base=10, subs=(2,3,4,5,6,7,8,9)))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.yaxis.set_minor_formatter(NullFormatter())

# 4) labels & title
ax.set_xlabel('Condensation sink of H$_2$SO$_4$')
ax.set_ylabel('[SO$_2$] (ppb)')
ax.set_title('[H$_2$SO$_4$] at different CS & [SO$_2$]')

# 5) colorbar
cbar = fig.colorbar(pcm, ax=ax, extend='both')
cbar.set_label('Avg [H$_2$SO$_4$] (10 AM–2 PM, days 4–5)')

plt.tight_layout()
plt.show()