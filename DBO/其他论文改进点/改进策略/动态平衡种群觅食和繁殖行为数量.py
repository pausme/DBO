# doi :10.1016/j.eswa.2023.121219
# 在这里，原作者使用了一个动态参数来计算种群中繁殖和觅食行为的蜣螂数量

import math


def R(t, t_max):
    return (math.cos(math.pi * (t / t_max)) + 1) * 0.5
