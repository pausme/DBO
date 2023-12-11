# t-distribution
from scipy.special import gamma
import math
import scipy.stats as stats


# 自己根据定义所写的方法
def P(x, m):
    result = (gamma((m + 1) / 2)) / (math.sqrt(m * math.pi) * 
                                     gamma(m / 2)) * math.pow((1 + x * x / 2), -((m + 1) / 2))
    return result

# 当t(m→∞)→N(0,1),t(m→1)=C(0,1), 
# N(0,1)is Gaussian distribution and C (0,1) is Cauchy distribution.

# 使用scipy中t分布方法
def T(df, x):
    # df 为自由度 ， x为输入值
    return stats.t.pdf(x, df)

result = P(0, 20)
result1 = T(20, 0)
print(result, result1)
