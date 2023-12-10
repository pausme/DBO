import matplotlib.pyplot as plt
from scipy.special import gamma
import numpy as np
import math

x = np.arange(1, 1000, 0.01)
y = []
beta = 3/2 
alpha_u = math.pow(
    (gamma(1 + beta) * math.sin(math.pi * beta / 2) / (gamma(((1 + beta) / 2) * beta * math.pow(2, (beta - 1) / 2)))),
    (1 / beta)
)
alpha_v = 1

for i in x:
    u = np.random.normal(0, alpha_u, 1)
    v = np.random.normal(0, alpha_v, 1)
    step = 0.05 * (u * alpha_u / math.pow(abs(v), (1 / beta)))

    y.append(step)

plt.plot(x, y, label="Levy Flight")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()