import numpy as np

ub = np.ones((1, 10)) * 100
lb = np.ones((1, 10)) * -100
x = np.random.random((1, 10))
print(x[0, 1])
print(x.shape)
# X = np.clip(x, ub[0, :], lb[0, :])
# print(X)

for i in range(10):
    x[0, i] = np.clip(x[0, i], ub[0, i], lb[0, i])
print(x)