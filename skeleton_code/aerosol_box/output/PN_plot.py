import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("PN.dat")
particle_conc = data
time = np.linspace(0, 1, 25)

plt.figure(figsize=(10,4))
plt.plot(time, particle_conc, label="Only nucleation")
plt.xlabel("Time (days)")
plt.ylabel(r"Total PN ($\mathrm{cm}^{-3}$)")
plt.xlim(0,1)
plt.ylim()
plt.grid(True)
plt.savefig("PN.png")