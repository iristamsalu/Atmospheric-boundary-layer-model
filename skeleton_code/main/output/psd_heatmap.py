import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator, FormatStrFormatter, NullLocator

# Load and preprocess
diam = np.loadtxt("diameter.dat") * 1e9
psd = np.loadtxt("particle_conc_2000.dat") / 1e6
time = np.linspace(0, 5, 121)
i0, i1 = np.abs(time - 3).argmin(), np.abs(time - 5).argmin()
T, D = np.meshgrid(time[i0:i1+1], diam)

# Plot
plt.figure(figsize=(8, 5))
cs = plt.contourf(T, D, psd[i0:i1+1].T, levels=[1,10,100,500,1e3,5e3,1e4,2e4,4e4,8e4],
                  norm=LogNorm(), cmap='gist_rainbow', extend='max')
plt.yscale('log')
plt.xlim(4, 5)
plt.ylim(1, 1000)
plt.xlabel('Day (d)')
plt.ylabel('Diameter (nm)')
plt.title('PSD at 2000 m')
plt.gca().yaxis.set_major_locator(LogLocator())
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_minor_locator(NullLocator())
plt.colorbar(cs, label='dN/dlog₁₀Dp (# cm⁻³)')
plt.tight_layout()
plt.savefig('hyltemossa_psd_heatmap.png')
