import matplotlib.pyplot as plt
import numpy as np


def x2y(xi, lb, ub):
    # 这里给定 X 求出对应 Y
    return (xi - lb) / (ub - lb)


def y2y(yi, alpha):
    # 这里是给定 Y 通过映射来得到下一个 Y
    for i in range(dim):
        if 0 < yi[0, i] and yi[0, i] <= (1 - alpha):
            yi[0, i] = yi[0, i] / (1 - alpha)
        elif yi[0, i] > (1 - alpha) and yi[0, i] < 1:
            yi[0, i] = (yi[0, i] - 1 + alpha) / alpha
        else:
            pass


def y2x(yi, lb, ub):
    # 这里是给定 Y 的值后求出对应的 X
    xi = lb + (ub - lb) * yi
    return xi
    

pop = 30
dim = 10
ub = 100 * np.ones((1, dim))
lb = -100 * np.ones((1, dim))
alpha=0.4
x1 = (ub - lb) * np.random.random((1, dim)) + lb
temp = np.zeros((pop, dim))
y_t = x2y(x1, lb, ub)
# print(y_t)
temp[0] = x1
for i in range(pop-1):
    y2y(y_t, alpha)
    temp[i+1] = y2x(y_t, lb, ub)

print(temp)
