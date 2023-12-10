# 这里的螺旋搜索策略是采用的是WOA-鲸鱼算法中的Bubble-net attacking-气泡攻击行为
import math


def spiral_search(X, X_best, b, t, t_max, ub, lb):
    X_t = X_best + (math.exp(b * (2 * (1 - t / t_max) - 1)) * math.cos(2 * math.pi * b)) * (X - lb)
    + math.exp(b * (2 * (1 - t / t_max) - 1)) * (X - ub)
    return X_t


X = 20
X_best = 50
b = 1
t = 20
t_max = 100
ub = 0
lb = 100

X_t = spiral_search(X, X_best, b, t, t_max, ub, lb)
print(X_t)