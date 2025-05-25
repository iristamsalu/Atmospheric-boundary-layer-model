import numpy as np
import matplotlib.pyplot as plt

cs_vals = [0.0001, 0.001, 0.01]
so2_vals = [0.05, 0.5, 5.0]

filenames = [
    ['Concentrations_h2000_lowlow.dat',
     'Concentrations_h2000_baselow.dat',
     'Concentrations_h2000_highlow.dat'],
    ['Concentrations_h2000_lowbase.dat',
     'Concentrations_h2000_basebase.dat',
     'Concentrations_h2000_highbase.dat'],
    ['Concentrations_h2000_lowhigh.dat',
     'Concentrations_h2000_basehigh.dat',
     'Concentrations_h2000_highhigh.dat']
]

H2so4_avg = np.zeros((len(so2_vals), len(cs_vals)))
idx = np.concatenate((np.arange(82, 87), np.arange(106, 111)))

for i in range(len(so2_vals)):
    for j in range(len(cs_vals)):
        data = np.loadtxt(filenames[i][j])
        H2so4_avg[i, j] = data[idx, 20].mean()

cs_edges = np.logspace(np.log10(min(cs_vals)), np.log10(max(cs_vals)), len(cs_vals)+1)
so2_edges = np.logspace(np.log10(min(so2_vals)), np.log10(max(so2_vals)), len(so2_vals)+1)
CSe, SO2e = np.meshgrid(cs_edges, so2_edges)

plt.figure(figsize=(6,5))
pcm = plt.pcolormesh(CSe, SO2e, H2so4_avg, cmap='viridis', shading='flat')
plt.xscale('log')
plt.yscale('log')
plt.xticks(cs_vals, ['1e-4', '1e-3', '1e-2'])
plt.yticks(so2_vals, ['0.05', '0.5', '5.0'])
plt.xlabel('Condensation sink of H$_2$SO$_4$ (s$^{-1}$)')
plt.ylabel('[SO$_2$] (ppb)')
cbar = plt.colorbar(pcm)
cbar.set_label('Avg [H$_2$SO$_4$] (molecules cm$^{-3}$)')
plt.title('[H$_2$SO$_4$] at 2000 m vs. CS and [SO$_2$]')
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.savefig('cs_so2_h2000.png')
