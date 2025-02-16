import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('concentrations.dat')
time_values = np.linspace(0.000, 5.000, 121)

data_dict = {
    "O3": data[:, 0],
    "O1D": data[:, 1],
    "OH": data[:, 2],
    "REST": data[:, 3],
    "NO2": data[:, 4],
    "NO": data[:, 5],
    "CH2O": data[:, 6],
    "HO2": data[:, 7],
    "CO": data[:, 8],
    "CO2": data[:, 9],
    "CH4": data[:, 10],
    "CH3O2": data[:, 11],
    "isoprene": data[:, 12],
    "RO2": data[:, 13],
    "MVK": data[:, 14],
    "H2O2": data[:, 15],
    "HNO3": data[:, 16],
    "NO3": data[:, 17],
    "N2O5": data[:, 18],
    "SO2": data[:, 19],
    "H2SO4": data[:, 20],
    "H2SO4_p": data[:, 21],
    "apinene": data[:, 22],
    "HNO3_p": data[:, 23],
    "ELVOC": data[:, 24]
}


fig, axes = plt.subplots(5, 5, figsize=(10, 10))
axes = axes.flatten()
species_names = list(data_dict.keys())
for i in range(len(species_names)):
    species = species_names[i]
    axes[i].plot(time_values, data_dict[species])
    axes[i].set_title(species, fontsize=8)
    axes[i].tick_params(labelsize=6)
    axes[i].set_xlim(0,5)
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('concentrations.png')



