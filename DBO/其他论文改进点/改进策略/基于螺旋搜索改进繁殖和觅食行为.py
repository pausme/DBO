# doi:https://doi.org/10.21203/rs.3.rs-2988123/v1

# 创新点非常大胆 直接更改了原作者的公式 不是通过上下界来更新，而是通过与局部最优解的差来更新
# 好吧看差了 只是添加一个螺旋搜索在繁殖和觅食行为中

import math
import random
import numpy as np


# 螺旋搜索因子s
def spiral_search_factor(t, t_max):
    c = 1
    l = random.random() * 2 - 1
    res = math.exp(C(c, t, t_max) * l)  * math.cos(2 * math.pi * l)
    return res


# 改进后的繁殖行为
def update_spawning(x, x_best, t, t_max, ub, lb):
    x_t = x_best + spiral_search_factor(t, t_max) * random.random() * (x - lb)
    + spiral_search_factor(t, t_max) * random.random() * (x - ub)
    return x_t


# 改进后的觅食行为
def update_foraging(x, t, t_max, lb, ub):
    x_t = spiral_search_factor(t, t_max) * x + np.random.normal(size=1) * (x - lb)
    + np.random.normal(size=1) * (x - ub)
    return x_t


# 螺旋形状因子
def C(c, t, t_max):
    return math.exp(c * math.cos(math.pi * t / t_max))


