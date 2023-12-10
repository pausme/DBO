import scipy.integrate as integrate
import math


def F(x):
    alpha = beta = 0.5
    res = (1 / result[0]) * (pow(x, alpha-1)) * (math.pow((1-x), beta-1))
    return res


def Beta_function(t):
    alpha = beta = 0.5 # 在这里更改alpha和beta的参数
    return (math.pow(t, alpha-1)) * (math.pow(1-t, beta-1))


result = integrate.quad(Beta_function, 0, 1)
print(result[0])
res = F(0.5)
print(res)