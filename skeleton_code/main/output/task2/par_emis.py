import numpy as np
import matplotlib.pyplot as plt

data_files = [
    'Emissions_par0.dat',
    'Emissions_par05.dat',
    'Emissions_par1.dat',
    'Emissions_par15.dat',
    'Emissions_par2.dat',
    'Emissions_par25.dat',
    'Emissions_par3.dat'
]

all_data = [np.loadtxt(file) for file in data_files]
par = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

all_avrg_iso = []
all_avrg_mono = []

for el in all_data:
    emis_iso = el[:, 0]
    emis_mono = el[:, 1]
    # Compute mean emissions, last 2 days
    avrg_iso = np.mean(emis_iso[72:])
    avrg_mono = np.mean(emis_mono[72:])
    all_avrg_iso.append(avrg_iso)
    all_avrg_mono.append(avrg_mono)


plt.figure(figsize=(8, 6))
plt.plot(par, all_avrg_iso, marker='o', label='Isoprene', color='blue')
plt.plot(par, all_avrg_mono, marker='s', label='Monoterpenes', color='red')
plt.title('Emission rate vs Radiation Change')
plt.xlabel('PAR multiplier')
plt.ylabel('Average emission rate [molec cm⁻³ s⁻¹]')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('par_emis.png', dpi=300)