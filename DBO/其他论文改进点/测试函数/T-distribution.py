# t-distribution
from scipy.special import gamma
import math


def P(x, m):
    result = (gamma((m + 1) / 2)) / (math.sqrt(m * math.pi) * 
                                     gamma(m / 2)) * math.pow((1 + x * x / 2), -((m + 1) / 2))
    return result

# 当t(m→∞)→N(0,1),t(m→1)=C(0,1), 
# N(0,1)is Gaussian distribution and C (0,1) is Cauchy distribution.

result = P(0, 20)
print(result)