# doi :10.16088/j.issn.1001-6600.2023091602
# 在这里我们使用t-分布来作为mutation来增强种群的搜索能力

import random
from scipy.special import gamma
import scipy.stats as stats


# 在这里我们使用 scipy中t分布方法
def T(df, x):
    return stats.t.pdf(x, df)
# def T(x, m):
#     result = (gamma((m + 1) / 2)) / (math.sqrt(m * math.pi) * 
#                                      gamma(m / 2)) * math.pow((1 + x * x / 2), -((m + 1) / 2))
#     return result


def P(w1, w2, t, t_max):
    return w1 - w2 * (t_max - t) / t_max


def fun(x):
    return (x-1) * (x-1)

w1 = 0.5
w2 = 0.1
x = 0
for t in range(100):
    a = random.random()
    if(a >= P(w1, w2, t, 100)):
        x_t = x + (x * T(t, t))
        if (fun(x_t) <= fun(x)):
            x = x_t
    print(f"第{t}次迭代后，x的值为{x}\n")
