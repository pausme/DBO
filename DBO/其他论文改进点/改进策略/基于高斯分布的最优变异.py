# doi : 10.3390/electronics12214462

import numpy as np


def fun(x):
    return (x - 1) * (x - 1)


def gaussian_mutation(x, x_rand1, x_rand2):
    x_new = x + (np.random.normal(size=1) * (x_rand1 - x) + np.random.normal(size=1) * (x_rand2 - x)) / 2
    if(fun(x_new) < fun(x)):
        x = x_new
    return x


