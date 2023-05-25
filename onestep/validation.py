import numpy as np
import cantera as ct

chemfoam = np.loadtxt('chemFoam.out',skiprows=0)

gas = ct.Solution('oneStepMech_Taileb_IG.cti')
gas.TPX = 1410.0, 205e6, 'R:1'
r = ct.IdealGasConstPressureReactor(gas)

sim = ct.ReactorNet([r])


states = ct.SolutionArray(gas, extra=['t'])

t = 0
while t < 1e-3:
    t = sim.step()
    states.append(r.thermo.state, t=sim.time)


import matplotlib.pyplot as plt
plt.semilogx(states.t, states.T, label='Cantera, CP reactor')
plt.semilogx(chemfoam[:,0], chemfoam[:,1],'o', label='chemFoam')
plt.xlabel('Time (ms)')
plt.ylabel('Temperature (K)')
plt.legend()
plt.savefig('validation.png',dpi=300,bbox_inches='tight')
plt.show()