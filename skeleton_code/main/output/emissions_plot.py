import numpy as np
from matplotlib import pyplot as p

data = np.loadtxt('Emissions_min5.dat')

time = time_values = np.linspace(0.000, 5.000, 121)
f_veg_iso = data[:, 0]
f_veg_mono = data[:, 1]

p.figure(figsize=(8, 8))
p.plot(time, f_veg_iso)
p.plot(time, f_veg_mono)
p.xlim(3.0, 5.0)
p.ylim(0)
p.title('Emission rates')
p.xlabel('Day')
p.ylabel('Emission rate [molec cm-3 s-1]')
p.savefig('Emissions_min5.png')