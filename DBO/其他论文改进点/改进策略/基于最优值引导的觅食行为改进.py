# doi :10.1109/ACCESS.2023.3313930
# 感觉这个创新点 类似于梯度下降 EM SGD算法那方面 感觉是有点想法在里面的

import numpy as np


def update_foraging(x, x_best, lb, ub, M):
    # 在这里说明一下 M为该创新点的超参数 取多少合适还是需要实验探究
    x_t = x + np.random.normal(size=1) * (x - lb) + np.random.normal(size=1) * (x - ub)\
    + np.random.random() * M * (x_best - x)

    return x_t

