import numpy as np
import matplotlib.pyplot as plt

PM = np.loadtxt('PM.dat')
PM_hh1 = PM[:,0]
time = np.linspace(0, 120, 121)
time = time / 24

plt.figure(figsize=(10, 8))
plt.plot(time[73:], PM_hh1[73:], label="Nucleation, Condensation & Coagulation sink")

plt.legend()
plt.title("Total partcle mass concentraton in the first model layer")
plt.xlabel("Time (days)")
plt.ylabel(r"Total PM ($\mu g \cdot \mathrm{m}^{-3}$)")
plt.grid(True)
plt.xlim(3, 5)

plt.savefig("PM.png")