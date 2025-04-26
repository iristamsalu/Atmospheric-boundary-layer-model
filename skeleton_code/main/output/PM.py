import numpy as np
import matplotlib.pyplot as plt

PM_coag = np.loadtxt('PM_coag3.dat')
PM_cond = np.loadtxt('PM_cond.dat')
PM_dep = np.loadtxt('PM_dep.dat')

# 10 m
PM_coag_hh10 = PM_coag[:,1]
PM_cond_hh10 = PM_cond[:,1]
PM_dep_hh10 = PM_dep[:,1]

# 2000 m
PM_coag_hh2000 = PM_coag[:,39]
PM_cond_hh2000 = PM_cond[:,39]
PM_dep_hh2000 = PM_dep[:,39]

time = np.linspace(0, 120, 121)
time = time / 24

plt.figure(figsize=(10, 6))
plt.plot(time[73:], PM_cond_hh10[73:], linestyle="-", label="Nucleation & Condensation", color="blue")
plt.plot(time[73:], PM_coag_hh10[73:], linestyle="-", label="Nucleation, Condensation & Coagulation sink", color="red")
plt.plot(time[73:], PM_dep_hh10[73:], linestyle="-", label="Nucleation, Condensation, Coagulation & Deposition", color="green")

plt.plot(time[73:], PM_cond_hh2000[73:], linestyle="--", label="Nucleation & Condensation", color="blue")
plt.plot(time[73:], PM_coag_hh2000[73:], linestyle="--", label="Nucleation, Condensation & Coagulation sink", color="red")
plt.plot(time[73:], PM_dep_hh2000[73:], linestyle="--", label="Nucleation, Condensation, Coagulation & Deposition", color="green")

plt.legend()
plt.title("Total partcle mass concentraton")
plt.xlabel("Time (days)")
plt.ylabel(r"Total PM ($\mu g \cdot \mathrm{m}^{-3}$)")
plt.grid(True)
plt.xlim(3, 5)
plt.ylim(1.00, 1.65)

plt.savefig("PM.png")