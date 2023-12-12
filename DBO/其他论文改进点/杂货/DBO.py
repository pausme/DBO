# doi : 10.1007/s11227-022-04959-6
# 参考网站 : https://github.com/Lancephil/Dung-Beetle-Optimizer
import numpy as np
import math
import copy


'''种群初始化'''
def init(pop, dim, ub, lb):
    X = np.zeros([pop, dim])
    for i in range(pop):
        for j in range(dim):
            X[i, j] = np.random.rand() * (ub[j] - lb[j]) + lb[j]
    return X


'''计算适应度值'''
def Fitness(X, fun):
    pop = X.shape[0]
    fitness = np.zeros([pop, 1])
    for i in range(pop):
        fitness[i] = fun(X[i, :])
    return fitness

'''得到种群适应度值的下标'''
def Fitness_Sort(Fit):
    fitness = np.sort(Fit, axis=0)
    index = np.argsort(Fit, axis=0)
    return fitness, index


'''根据适应度来进行排序'''
def SortPosition(X, index):
    pop = X.shape[0]
    X_new = np.zeros(X.shape)
    for i in range(pop):
        X_new[i, :] = X[index[i], :]
    return X_new


'''蜣螂滚球行为与舞蹈行为'''
def BRupdate(X, XLast, pNum, GworstPosition):
    X_new = copy.copy(X)
    r2 = np.random.rand(1) # 判断蜣螂执行有障碍行为还是无障碍行为
    dim = X.shape[1]
    b = 0.3 # 可调参 表明当前位置的置信度
    k = 0.1 # 可调参 表明偏转系数
    for i in range(pNum):
        if r2 < 0.9:
            # 执行无障碍行为 即滚球
            a = np.random.rand(1)
            if a > 0.1:
                a = 1
            else:
                a = -1
            X_new[i, :] = X[i, :] + b * np.abs(X[i, :] - GworstPosition[0, :]) + a * k * (XLast[i, :])
        else:
            # 执行有障碍行为 即跳舞
            temp = np.random.randint(180, size=1)
            if temp == 0 or temp == 90 or temp == 180:
                # # 保持不变
                # for j in range(dim):
                #     X_new[i, j] = X[i, j]
                pass
            theta = temp * math.pi / 180
            X_new[i, :] = X[i, :] + math.tan(theta) * np.abs(X[i, :] - XLast[i, :])

    # 防止蜣螂超过搜索空间
    for i in range(pNum):
        for j in range(dim):
            X_new[i, j] = np.clip(X_new[i, j], lb[j], ub[j])
    return X_new


'''蜣螂繁殖行为'''
def SPupdate(X, pNum, t, iterations, fitness):
    X_new = copy.copy(X)
    dim = X.shape[1]
    R = 1 - t / iterations
    bestIndex = np.argmin(fitness)  # 找到X中最小适应度的索引
    bestX = X[bestIndex, :]  # 找到X中具有最有适应度的蜣螂位置
    lbStar = bestX * (1 - R)
    ubStar = bestX * (1 + R)
    for j in range(dim):
        lbStar[j] = np.clip(lbStar[j], lb[j], ub[j])
        ubStar[j] = np.clip(ubStar[j], lb[j], ub[j])

    for i in range(pNum + 1, 12):
        X_new[i, :] = bestX + (np.random.rand(1, dim)) * (X[i, :] - lbStar + (np.random.rand(1, dim)) * (X[i, :] - ubStar))
        for j in range(dim):
            X_new[i, j] = np.clip(X_new[i, j], lbStar[j], ubStar[j])
    return X_new


'''蜣螂觅食行为'''
def FAupdate(X, t, iterations, GbestPosition):
    X_new = copy.copy(X)
    dim = X.shape[1]
    R = 1 - t / iterations
    lbl = GbestPosition[0, :] * (1 - R)
    ubl = GbestPosition[0, :] * (1 + R)
    for j in range(dim):
        lbl[j] = np.clip(lbl[j], lb[j], ub[j])
        ubl[j] = np.clip(ubl[j], lb[j], ub[j])
    for i in range(13, 19):
        X_new[i, :] = X[i, :] + (np.random.rand(1, dim)) * (X[i, :] - lbl) + (np.random.rand(1, dim)) * (X[i, :] - ubl)
        for j in range(dim):
            X_new[i, j] = np.clip(X_new[i, j], lbl[j], ubl[j])
    return X_new


'''蜣螂偷窃行为'''
def THupdate(X, GbestPosition, fitness):
    X_new = copy.copy(X)
    dim = X.shape[1]
    bestIndex = np.argmin(fitness)  # 找到X中最小适应度的索引
    bestX = X[bestIndex, :]  # 找到X中具有最有适应度的蜣螂位置
    for i in range(20, pop):
        # 这里取 g = 0.5
        X_new[i, :] = GbestPosition[0, :] + np.random.randn(1, dim) * (np.abs(X[i, :] - GbestPosition[0, :]) + np.abs(X[i, :] - bestX)) / 2
        for j in range(dim):
            X_new[i, j] = np.clip(X_new[i, j], lb[j], ub[j])
    return X_new


'''主函数'''
def dbo(pop, dim, lb, ub, iterations, fun):
    P_percent = 0.2
    pNum = round(P_percent * pop)
    X = init(pop, dim, ub, lb)
    fitness = Fitness(X, fun)
    fitness, sortIndex = Fitness_Sort(fitness)
    X = SortPosition(X, sortIndex)
    X_Last = X # X(t-1)
    GbestScore = copy.copy(fitness[0]) # 记录最小适应度值
    GbestPosition = np.zeros([1, dim])
    GbestPosition[0, :] = copy.copy(X[0, :])

    GworstScore = copy.copy(fitness[-1]) # 记录最大适应度值
    GworstPosition = np.zeros([1, dim])
    GworstPosition[0, :] = copy.copy(X[-1, :])

    Curve = np.zeros((iterations, 1))

    for t in range(iterations):
        BestF = fitness[0]
        X = BRupdate(X, X_Last, pNum, GworstPosition)
        fitness = Fitness(X, fun)
        X = SPupdate(X, pNum, t, iterations, fitness)
        X = FAupdate(X, t, iterations, GbestPosition)
        fitness = Fitness(X, fun)
        X = THupdate(X, GbestPosition, fitness)
        fitness = Fitness(X, fun)
        fitness, sortIndex = Fitness_Sort(fitness)
        X = SortPosition(X, sortIndex)
        X_Last = X
        if(fitness[0] <= GbestScore):
            GbestScore = copy.copy(fitness[0])
            GbestPosition[0, :] = copy.copy(X[0, :])
        Curve[t] = GbestScore

        if (t) % 50 == 0:
            print("第%d代搜索的结果为:%f" % (t, GbestScore[0]))
    return GbestScore, GbestPosition, Curve


'''适应度函数'''
def fun(X):
    return np.sum(np.square(X))

pop = 30
dim = 2
iterations = 1000
lb_num = -100
ub_num = 100
lb = lb_num * np.ones((dim, 1))
ub = ub_num * np.ones((dim, 1))

GbestScore, GbestPosition, Curve = dbo(pop, dim, lb, ub, iterations, fun=fun)
print(GbestScore[0])
print(GbestPosition[0])