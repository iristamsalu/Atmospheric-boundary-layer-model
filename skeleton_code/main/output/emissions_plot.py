import numpy as np
from matplotlib import pyplot as p

data = np.loadtxt('Emissions.dat')

time = data[:, 0] / 3600 / 24
f_veg_iso = data[:, 1]
f_veg_mono = data[:, 2]

p.figure(figsize=(8, 8))
p.plot(time, f_veg_iso)
p.xlim(3.0, 5.0)
p.savefig('Emissions_plot')