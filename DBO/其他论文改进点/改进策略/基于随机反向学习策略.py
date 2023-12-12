# doi : 10.3390/electronics12214462

import numpy as np


def initialize(x, t, t_max, lb, ub):
    if np.random.random() < t / t_max:
        x = ub + lb - np.random.random() * x
    return x

x = 5
t = 10
t_max = 100
lb = 0
ub = 10

result = initialize(x, t, t_max, lb, ub)
print(result)
