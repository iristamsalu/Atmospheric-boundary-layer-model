import numpy as np
from matplotlib import pyplot as p
import random

n = 12
name = "isoprene"

data1 = np.loadtxt('Concentrations_h10.dat')
data2 = np.loadtxt('Concentrations_h50.dat')
data3 = np.loadtxt('Concentrations_h500.dat')
data4 = np.loadtxt('Concentrations_h2000.dat')

time = time_values = np.linspace(0.000, 5.000, 121)

conc1 = data1[:, n]
conc2 = data2[:, n]
conc3 = data3[:, n]
conc4 = data4[:, n]

p.figure(figsize=(8, 8))
p.plot(time, conc1, color = "green")
p.plot(time, conc2, color = "red")
p.plot(time, conc3, color = "blue")
p.plot(time, conc4, color = "purple")
p.xlabel("Days")
p.ylabel("Concentration [molec cm-3]")
p.xlim(3.0, 5.0)
p.ylim(0)
p.title(name)
p.grid(True)
rn = random.random()
p.savefig(name + f'_concentration.png')