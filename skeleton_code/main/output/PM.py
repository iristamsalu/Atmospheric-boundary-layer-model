import numpy as np
import matplotlib.pyplot as plt

PM_coag = np.loadtxt('PM.dat')
PM_cond = np.loadtxt('PM_cond.dat')
PM_coag_hh1 = PM_coag[:,0]
PM_cond_hh1 = PM_cond[:,0]
time = np.linspace(0, 120, 121)
time = time / 24

plt.figure(figsize=(10, 8))
plt.plot(time[73:], PM_cond_hh1[73:], linestyle="--", label="Nucleation & Condensation")
plt.plot(time[73:], PM_coag_hh1[73:], linestyle="--", label="Nucleation, Condensation & Coagulation sink")

plt.legend()
plt.title("Total partcle mass concentraton in the first model layer")
plt.xlabel("Time (days)")
plt.ylabel(r"Total PM ($\mu g \cdot \mathrm{m}^{-3}$)")
plt.grid(True)
plt.xlim(3, 5)
plt.ylim(1.15, 1.55)

plt.savefig("PM.png")