# doi : 10.3390/electronics12214462

import numpy as np


def initialize(x, t, t_max, lb, ub):
    if np.random.random() < t / t_max:
        x = ub + lb - np.random.random() * x
    return x
