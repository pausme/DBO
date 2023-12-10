# 在之前我们直接使用clip函数来直接使超过的种群等于边界
# 在这里我们使用基于莱维飞行的越界赋值策略来改进
import numpy as np
from scipy.stats import levy


x = 20
ub = 10
lb = 0

# 原
# x = np.clip(x, lb, ub)
# print(x)

# 新
# 在这里我们使用的是 alpha = 0.5，beta = 1的标准莱维飞行函数
if x < lb:
    x = max(lb, levy().rvs(size=1) * lb)
elif x > ub:
    x = min(ub, levy().rvs(size=1) * ub)
print(x)
