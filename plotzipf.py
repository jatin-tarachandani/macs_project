import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

N = 20
domain = np.arange(1, N+1)

z1 = stats.zipfian.pmf(domain, a=0.6, n=N)
z2 = stats.zipfian.pmf(domain, a=1.0, n=N)
z3 = stats.zipfian.pmf(domain, a=1.4, n=N)

#plot these 3 on log log scale


plt.rcParams.update({'font.size': 24})


# plt.figure(figsize=(3,2))
plt.plot(domain, z1, label='α=0.6')
plt.plot(domain, z2, label='α=1.0')
plt.plot(domain, z3, label='α=1.4')
plt.xscale('linear')
plt.yscale('linear')
plt.legend()
plt.xlabel('Rank')
plt.ylabel('Probability')
plt.title("Zipf pmf for differing α (n=20)")

plt.show()