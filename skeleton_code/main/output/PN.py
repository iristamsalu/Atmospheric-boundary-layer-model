import numpy as np
import matplotlib.pyplot as plt

PN = np.loadtxt('PN.dat')
PN_hh1 = PN[:,0]
time = np.linspace(0, 120, 121)
time = time / 24

plt.figure(figsize=(10, 5))
plt.plot(time[72:], PN_hh1[72:], label="Nucleation, Condensation & Coagulation sink")

plt.legend()
plt.title("Total partcle number concentraton in the first model layer")
plt.xlabel("Time (days)")
plt.ylabel(r"Total PN ($\mathrm{cm}^{-3}$)")
plt.grid(True)
plt.xlim(3, 5)
plt.ylim(0)

plt.savefig("PN.png")