import matplotlib.pyplot as plt
import numpy as np

nucleation = np.loadtxt("PN_1.dat")
condensation = np.loadtxt("PN_2.dat")
coagulation = np.loadtxt("PN_3.dat")
PN_nucl = nucleation
PN_cond = condensation
PN_coag = coagulation 
time = np.linspace(0, 1, 25)

plt.figure(figsize=(10,3))
plt.plot(time, PN_nucl, label="Only Nucleation", color="b")
plt.plot(time, PN_cond, label="Nucleation & Condensation", linestyle="--", color="red")
plt.plot(time, PN_coag, label="Nucleation, Condensation & Coagulation sink", color="orange")
plt.legend()
plt.xlabel("Time (days)")
plt.ylabel(r"Total PN ($\mathrm{cm}^{-3}$)")
plt.xlim(0,1)
plt.ylim(0)
plt.grid(True)
plt.savefig("PN.png")