import numpy as np
import matplotlib.pyplot as plt


PM_cond = np.loadtxt('PM_cond.dat')
PM_coag = np.loadtxt('PM_coag.dat')
PM_coag_cs = np.loadtxt('PM_coag_cs10-4.dat')
PM_dep = np.loadtxt('PM_dep.dat')

# 10 m
PM_cond_hh10 = PM_cond[:,1]
PM_coag_hh10 = PM_coag[:,1]
PM_coag_cs_hh10 = PM_coag_cs[:,1]
PM_dep_hh10 = PM_dep[:,1]

# 2000 m
PM_cond_hh2000 = PM_cond[:,39]
PM_coag_hh2000 = PM_coag[:,39]
PM_coag_cs_hh2000 = PM_coag_cs[:,39]
PM_dep_hh2000 = PM_dep[:,39]

time = np.linspace(0, 120, 121)
time = time / 24

plt.figure(figsize=(10, 6))
plt.plot(time[73:], PM_cond_hh10[73:], linestyle="-", label="Nucleation & Condensation at 10 m", color="blue")
plt.plot(time[73:], PM_coag_hh10[73:], linestyle="-", label="Nucleation, Condensation & Coagulation sink at 10 m", color="red")
plt.plot(time[73:], PM_coag_cs_hh10[73:], linestyle="-", label="Nucleation, Condensation & Coagulation sink, CS=0.001 at 10 m", color="orange")
plt.plot(time[73:], PM_dep_hh10[73:], linestyle="-", label="Nucleation, Condensation, Coagulation & Deposition at 10 m", color="green")

plt.plot(time[73:], PM_cond_hh2000[73:], linestyle="--", label="Nucleation & Condensation", color="blue")
plt.plot(time[73:], PM_coag_hh2000[73:], linestyle="--", label="Nucleation, Condensation & Coagulation sink at 2000 m", color="red")
plt.plot(time[73:], PM_coag_cs_hh2000[73:], linestyle="--", label="Nucleation, Condensation & Coagulation sink, CS=0.001 at 2000 m", color="orange")
plt.plot(time[73:], PM_dep_hh2000[73:], linestyle="--", label="Nucleation, Condensation, Coagulation & Deposition at 2000 m", color="green")

plt.legend()
plt.title("Total partcle mass concentraton")
plt.xlabel("Time (days)")
plt.ylabel(r"Total PM ($\mu g \cdot \mathrm{m}^{-3}$)")
plt.grid(True)
plt.xlim(3, 5)
plt.ylim(1.00, 1.65)

plt.savefig("PM.png")