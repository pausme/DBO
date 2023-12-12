# doi : 10.1080/21642583.2019.1708830
# 参考网站 : https://www.jianshu.com/p/09adbd2f778c

import copy
import random
import numpy as np


''' Tent种群初始化函数 '''
def initial(pop, dim, ub, lb):
    X = np.zeros([pop, dim])
    for i in range(pop):
        for j in range(dim):
            X[i, j] = np.random.rand() * (ub[j] - lb[j]) + lb[j]
    return X, lb, ub
            
'''边界检查函数'''
def BorderCheck(X,ub,lb,pop,dim):
    for i in range(pop):
        for j in range(dim):
            if X[i,j]>ub[j]:
                X[i, j] = np.random.rand() * (ub[j] - lb[j]) + lb[j]
            elif X[i,j]<lb[j]:
                X[i, j] = np.random.rand() * (ub[j] - lb[j]) + lb[j]
    return X
    
'''计算适应度函数'''
def CaculateFitness(X,fun):
    pop = X.shape[0]
    fitness = np.zeros([pop, 1])
    for i in range(pop):
        fitness[i] = fun(X[i, :])
    return fitness

'''适应度排序'''
def SortFitness(Fit):
    fitness = np.sort(Fit, axis=0)
    index = np.argsort(Fit, axis=0)
    return fitness,index

'''根据适应度对位置进行排序'''
def SortPosition(X,index):
    Xnew = np.zeros(X.shape)
    for i in range(X.shape[0]):
        Xnew[i,:] = X[index[i],:]
    return Xnew

'''麻雀发现者勘探更新'''
def PDUpdate(X, PDNumber, ST, Max_iter, dim):
    X_new = copy.copy(X)
    R2 = random.random()
    for p in range(PDNumber):
        for j in range(dim):
            if R2 < ST:
                X_new[p, j] = X[p, j] * np.exp(-p / (random.random() * Max_iter))
            else:
               X_new[p, j] = X[p, j] + np.random.randn()
    return X_new
        
'''麻雀加入者更新'''            
def JDUpdate(X, PDNumber, pop, dim):
    X_new = copy.copy(X)
    # 产生-1，1的随机数
    A = np.ones([dim, 1])
    for a in range(dim):
        if (random.random() > 0.5):
            A[a] = -1
    for i in range(PDNumber + 1, pop):
        for j in range(dim):
            if i > (pop - PDNumber) / 2 + PDNumber:
                X_new[i, j] = np.random.randn() * np.exp((X[-1, j] - X[i, j]) / i ** 2)
            else:
                AA = np.mean(np.abs(X[i, :] - X[0, :])*A)
                X_new[i, j] = X[0, j] - AA
    return X_new
            
'''危险更新'''   
def SDUpdate(X, pop, SDNumber, fitness, BestF):
    X_new = copy.copy(X)
    dim = X.shape[1]
    Temp = range(pop)
    RandIndex = random.sample(Temp, pop)
    SDchooseIndex = RandIndex[0:SDNumber]
    for i in range(SDNumber):
        for j in range(dim):
            if fitness[SDchooseIndex[i]] > BestF:
                X_new[SDchooseIndex[i], j] = X[0, j] + np.random.randn() * np.abs(X[SDchooseIndex[i], j] - X[0, j])
            elif fitness[SDchooseIndex[i]] == BestF:
                K = 2 * random.random() - 1
                X_new[SDchooseIndex[i], j] = X[SDchooseIndex[i], j] + K * (
                        np.abs(X[SDchooseIndex[i], j] - X[-1, j]) / (fitness[SDchooseIndex[i]] - fitness[-1] + 10E-8))
    return X_new
              
    

'''麻雀搜索算法'''
def Tent_SSA(pop,dim,lb,ub,Max_iter,fun):
    ST = 0.6 #预警值
    PD = 0.7 #发现者的比列，剩下的是加入者
    SD = 0.2 #意识到有危险麻雀的比重
    PDNumber = int(pop*PD) #发现者数量
    SDNumber = int(pop*SD) #意识到有危险麻雀数量
    X,lb,ub = initial(pop, dim, ub, lb) #初始化种群
    fitness = CaculateFitness(X,fun) #计算适应度值
    fitness,sortIndex = SortFitness(fitness) #对适应度值排序
    X = SortPosition(X,sortIndex) #种群排序
    GbestScore = copy.copy(fitness[0])
    GbestPositon = np.zeros([1,dim])
    GbestPositon[0,:] = copy.copy(X[0,:])
    Curve = np.zeros([Max_iter,1])
    for i in range(Max_iter):
        BestF = fitness[0]
        
        X = PDUpdate(X,PDNumber,ST,Max_iter,dim)#发现者更新

        X = JDUpdate(X,PDNumber,pop,dim) #加入者更新

        X = SDUpdate(X,pop,SDNumber,fitness,BestF) #危险更新

        X = BorderCheck(X,ub,lb,pop,dim) #边界检测

        fitness = CaculateFitness(X,fun) #计算适应度值

        fitness,sortIndex = SortFitness(fitness) #对适应度值排序
        X = SortPosition(X,sortIndex) #种群排序
        if(fitness[0]<=GbestScore): #更新全局最优
            GbestScore = copy.copy(fitness[0])
            GbestPositon[0,:] = copy.copy(X[0,:])
        Curve[i] = GbestScore
    return GbestScore,GbestPositon,Curve


'''适应度函数'''
def fun(X):
    return np.sum(np.square(X))


pop_size = 100
dim_size = 2
lb_num = -100
ub_num = 100
lb = lb_num * np.ones((dim_size, 1))
ub = ub_num * np.ones((dim_size, 1))
Max_iter = 1000
GbestScore, GbestPosition, Curve = Tent_SSA(pop_size, dim_size, lb, ub, Max_iter, fun)
print(GbestScore[0])
print(GbestPosition[0])