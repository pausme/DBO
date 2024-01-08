import numpy as np
# from cec2017.functions import f1
import dbo as fun1
import sys
import matplotlib.pyplot as plt

    
def main(argv):
    SearchAgents_no=30 # 种群数
    Function_name='F8' # 适应值函数
    Max_iteration=1000 # 迭代次数
 
    [fobj,lb,ub,dim]=fun1.Parameters(Function_name)
    [fMin,bestX,DBO_curve]=fun1.DBO(SearchAgents_no,Max_iteration,lb,ub,dim,fobj)
    print(['最优值为：',fMin])
    print(['最优变量为：',bestX])
    thr1=np.arange(len(DBO_curve[0,:]))

    plt.plot(thr1, DBO_curve[0,:])

    plt.xlabel('num')
    plt.ylabel('object value') 
    plt.title('line')
 
    plt.show()
if __name__=='__main__':
	main(sys.argv)

