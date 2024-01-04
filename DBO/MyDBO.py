# doi : 10.1007/s11227-022-04959-6
# 参考网站 : https://github.com/Lancephil/Dung-Beetle-Optimizer
import numpy as np
import math
import matplotlib.pyplot as plt


'''种群初始化'''
def init(pop, dim, ub, lb):
    X = np.zeros((pop, dim))
    for i in range(pop):
        X[i, :] = lb + (ub - lb) * np.random.rand(1, dim)
    return X


'''计算适应度值'''
def Fitness(X, fun):
    fitness = np.zeros((pop, 1))
    for i in range(pop):
        fitness[i, 0] = fun(X[i, :])
    return fitness


def Bounds(s, Lb, Ub):
    temp = s
    for i in range(len(s)):
        if temp[i] < Lb[0, i]:
            temp[i] = Lb[0, i]
        elif temp[i] > Ub[0, i]:
            temp[i] = Ub[0, i]
    return temp


def swapfun(ss):
    temp = ss
    o = np.zeros((1,len(temp)))
    for i in range(len(ss)):
        o[0,i]=temp[i]
    return o


'''蜣螂滚球行为与舞蹈行为'''
def BRupdate(X, pX, XX, pNum, worseX, fitness):
    r2 = np.random.rand(1) # 判断蜣螂执行有障碍行为还是无障碍行为
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
            X[i, :] = pX[i, :] + b * np.abs(pX[i, :] - worseX) + a * k * (XX[i, :])
        else:
            # 执行有障碍行为 即跳舞
            temp = np.random.randint(180, size=1)
            if temp == 0 or temp == 90 or temp == 180:
                X[i, :] = pX[i, :]
            theta = temp * math.pi / 180
            X[i, :] = pX[i, :] + math.tan(theta) * np.abs(pX[i, :] - XX[i, :])

    # 防止蜣螂超过搜索空间
    # for i in range(pNum):
        # for j in range(dim):
        #     X[i, j] = np.clip(pX[i, j], lb[0, j], ub[0, j])
        X[i, :] = Bounds(X[i, :], lb, ub)

        # 适应度更新
        # print(fitness[i, 0])
        fitness[i, 0] = fun(X[i, :])
        


'''蜣螂繁殖行为'''
def SPupdate(X, pX, pNum, t, iterations, fitness, bestXX):
    R = 1 - t / iterations
    # bestIndex = np.argmin(fitness)  # 找到X中最小适应度的索引
    # bestX = X[bestIndex, :]  # 找到X中具有最有适应度的蜣螂位置
    lbStar = bestXX * (1 - R)
    ubStar = bestXX * (1 + R)

    # for j in range(dim):
    #     lbStar[j] = np.clip(lbStar[j], lb[0, j], ub[0, j])
    #     ubStar[j] = np.clip(ubStar[j], lb[0, j], ub[0, j])

    lbStar = Bounds(lbStar, lb, ub)
    ubStar = Bounds(ubStar, lb, ub)

    xLB=swapfun(lbStar)
    xUB=swapfun(ubStar)

    for i in range(pNum + 1, 12):
        X[i, :] = bestXX + (np.random.rand(1, dim)) * (pX[i, :] - lbStar) + (np.random.rand(1, dim)) * (pX[i, :] - ubStar)
        # for j in range(dim):
        #     X[i, j] = np.clip(pX[i, j], lb[0, j], ub[0, j])
    
        X[i, :] = Bounds(X[i, :], xLB, xUB)

        # 适应度更新
        fitness[i, 0] = fun(X[i, :])
    return X


'''蜣螂觅食行为'''
def FAupdate(X, pX, t, iterations, fitness, bestX):
    R = 1 - t / iterations
    lbl = bestX * (1 - R)
    ubl = bestX * (1 + R)

    # for j in range(dim):
    #     lbl[j] = np.clip(lbl[j], lb[0, j], ub[0, j])
    #     ubl[j] = np.clip(ubl[j], lb[0, j], ub[0, j])

    lbl = Bounds(lbl, lb, ub)
    ubl = Bounds(lbl, lb, ub)

    for i in range(13, 19):
        X[i, :] = pX[i, :] + ((np.random.rand(1)) * (pX[i, :] - lbl) + ((np.random.rand(1, dim)) * (pX[i, :] - ubl)))
        # for j in range(dim):
        #     X[i, j] = np.clip(pX[i, j], lbl[j], ubl[j])
    
        X[i, :] = Bounds(X[i, :] , lb, ub)
        # 适应度值更新
        fitness[i, 0] = fun(X[i, :])
    return X


'''蜣螂偷窃行为'''
def THupdate(X, pX, fitness, bestX, bestXX):
    for i in range(20, pop):
        # 这里取 g = 0.5
        X[i, :] = bestX + np.random.randn(1, dim) * (np.abs(pX[i, :] - bestX) + np.abs(pX[i, :] - bestXX)) / 2
        # for j in range(dim):
        #     X[i, j] = np.clip(pX[i, j], lb[0, j], ub[0, j])

        X[i, :] = Bounds(X[i, :], lb, ub)
        #适应度值更新
        fitness[i, 0] = fun(X[i, :])
    return X


'''主函数'''
def dbo(pop, dim, lb, ub, iterations, fun):
    P_percent = 0.2
    pNum = round(P_percent * pop)
    X = init(pop, dim, ub, lb)
    # print(X)
    fitness = Fitness(X, fun)
    # print(fitness)
    pFit = fitness
    pX = X
    XX = pX
    fMin = np.min(fitness[:, 0])
    bestI = np.argmin(fitness[:, 0])
    bestX = X[bestI, :] # 这个估计是 global best
    # print(bestX)
    Convergence_curve = np.zeros((1, iterations))

    for t in range(iterations):
        # BestF = fitness[0]
        fMax = np.max(pFit[:, 0])
        worstI = np.argmax(pFit[:, 0])
        worseX = X[worstI, :]
        # print(worseX)
        # print(fitness)
        BRupdate(X, pX, XX, pNum, worseX, fitness)
        
        bestII = np.argmin(fitness[:, 0])
        bestXX = X[bestII, :] # 这个估计是current best
        
        SPupdate(X, pX, pNum, t, iterations, fitness, bestXX)
        
        FAupdate(X, pX, t, iterations, fitness, bestX)

        THupdate(X, pX, fitness, bestX, bestXX)

        XX = pX

        for i in range(pop):
            if fitness[i, 0] < pFit[i, 0]:
                pFit[i, 0] = fitness[i, 0]
                pX[i, :] = X[i, :]

            if pFit[i, 0] < fMin:
                fMin = pFit[i, 0]
                bestX = pX[i, :]

        Convergence_curve[0, t] = fMin

    return fMin, bestX, Convergence_curve


'''适应度函数'''
def fun(X):
    return np.sum(np.square(X))


pop = 30
dim = 100
iterations = 100000
lb_num = -100
ub_num = 100
lb = lb_num * np.ones((1, dim))
ub = ub_num * np.ones((1, dim))

[fMin, bestX, Convergence_curve] = dbo(pop, dim, lb, ub, iterations, fun=fun)
print(fMin)
print(bestX)

thr1 = np.arange(len(Convergence_curve[0, :]))
plt.plot(thr1, Convergence_curve[0, :])
plt.xlabel('num')
plt.ylabel('object value') 
plt.title('line')
plt.show()
