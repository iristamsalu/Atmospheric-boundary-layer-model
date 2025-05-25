import numpy as np
import matplotlib.pyplot as plt

data_files = [
    'Emissions_min20.dat',
    'Emissions_min10.dat',
    'Emissions_orig.dat',
    'Emissions_plus10.dat',
    'Emissions_plus20.dat',
    'Emissions_plus30.dat',
    'Emissions_plus40.dat'
]

all_data = [np.loadtxt(file) for file in data_files]
temp = [-20, -10, 0, 10, 20, 30, 40]

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
plt.plot(temp, all_avrg_iso, marker='o', label='Isoprene', color='blue')
plt.plot(temp, all_avrg_mono, marker='s', label='Monoterpenes', color='red')
plt.title('Emission rate vs Temperature Change')
plt.xlabel('Temperature change (K)')
plt.ylabel('Average emission rate [molec cm⁻³ s⁻¹]')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('temp_emis.png', dpi=300)