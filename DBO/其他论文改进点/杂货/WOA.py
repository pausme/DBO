# doi : 10.1016/j.advengsoft.2016.01.008
# 参考网站 : https://zhuanlan.zhihu.com/p/347741616
import numpy as np
import matplotlib.pyplot as plt


def sampleGeneartor():
    X = np.arange(0, 5, 0.01)
    Y = X**3 - 4*X**2 + 1*X - 3
    e = np.random.normal(0, 2, 500)
    Y = Y + e
    plt.scatter(X, Y, 0.5)
    return X, Y


class woa():
    #初始化
    def __init__(self, X_train, Y_train, LB=np.array([-5, -5, -5, -5]),\
                 UB= np.array([5, 5, 5, 5]), dim=4, b=1, whale_num=20, max_iter=500):
        self.X_train = X_train
        self.Y_train = Y_train
        self.LB = LB
        self.UB = UB
        self.dim = dim
        self.whale_num = whale_num
        self.max_iter = max_iter
        self.b = b
        #Initialize the locations of whale
        self.X = np.random.uniform(0, 1, (whale_num, dim))*(UB - LB) + LB
        self.gBest_score = np.inf
        self.gBest_curve = np.zeros(max_iter)
        self.gBest_X = np.zeros(dim) 
    
    #适应度函数  
    def fitFunc(self, input):
        a = input[0]; b = input[1]; c = input[2]; d = input[3]
        Y_Hat = a*self.X_train**3 + b*self.X_train**2 + c*self.X_train + d 
        fitFunc = np.sum((Y_Hat - self.Y_train)**2)/np.shape(Y_Hat)[0]
        return fitFunc   
        
    #优化模块  
    def opt(self):
        t = 0
        while t < self.max_iter:
            for i in range(self.whale_num):
                self.X[i, :] = np.clip(self.X[i, :], self.LB, self.UB) #Check boundries
                fitness = self.fitFunc(self.X[i, :])
                # Update the gBest_score and gBest_X
                if fitness < self.gBest_score:
                    self.gBest_score = fitness
                    self.gBest_X = self.X[i, :].copy()
            
            a = 2*(self.max_iter - t)/self.max_iter
            #Update the location of whales
            for i in range(self.whale_num):
                p = np.random.uniform()
                R1 = np.random.uniform()
                R2 = np.random.uniform()
                A = 2*a*R1 - a
                C = 2*R2
                l = 2*np.random.uniform() - 1
                
                if p >= 0.5:
                    D = abs(self.gBest_X - self.X[i, :])
                    self.X[i, :] = D*np.exp(self.b*l)*np.cos(2*np.pi*l)+self.gBest_X
                else:
                    if abs(A) < 1:
                        D = abs(C*self.gBest_X - self.X[i, :])
                        self.X[i, :] = self.gBest_X - A*D
                    else:
                        rand_index = np.random.randint(low=0, high=self.whale_num)
                        X_rand = self.X[rand_index, :]
                        D = abs(C*X_rand - self.X[i, :])
                        self.X[i, :] = X_rand - A*D
        
            self.gBest_curve[t] = self.gBest_score       
            if (t%100 == 0) :
                print('At iteration: ' + str(t))  
            t+=1 
        return self.gBest_curve, self.gBest_X
    

'''
main function
'''
X, Y = sampleGeneartor()
fitnessCurve, para = woa(X, Y, dim=4, whale_num=60, max_iter=2000).opt()
yPre = para[0]*X**3 + para[1]*X**2 + para[2]*X + para[3] 
plt.scatter(X, yPre, 0.5)

plt.figure()
plt.plot(fitnessCurve, linewidth='0.5')
plt.show()