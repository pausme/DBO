# 使用ACO算法实现TSP旅行商问题
import math
import numpy as np
import matplotlib.pyplot as plt


class ACO(object):
    def __init__(self, num_city, data):
        self.m = 50  # 蚂蚁数量
        self.alpha = 0.5  # 信息素重要程度因子
        self.beta = 5  # 启发函数重要因子
        self.rho = 0.1  # 信息素挥发因子

        self.Q = 1  # 常量系数
        self.num_city = num_city  # 城市规模
        self.location = data  # 城市坐标
        self.Tau = np.zeros([num_city, num_city])  # 信息素矩阵
        self.Table = [[0 for _ in range(num_city)] for _ in range(self.m)]  # 生成的蚁群  使用二维列表来记录蚁群城市
        self.iter = 1  # 迭代次数
        self.iter_max = 200  # 最大迭代数
        self.dis_mat = self.compute_dis_mat(num_city, self.location)  # 计算城市之间的距离矩阵
        self.Eta = 1. / self.dis_mat  # 启发式函数  必报warning,因为无法判断传入的分母是否为0

    # 轮盘赌选择
    def rand_choose(self, p):
        x = np.random.rand()
        for i, t in enumerate(p):
            x -= t
            if x <= 0:
                break
        return i

    # 初始化信息素
    def compute_information(self,num_city):
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    self.Tau[i][j] = 0
                else:
                    self.Tau[i][j] = num_city / self.Eta[i][j]

    # 生成蚁群
    def get_ants(self, num_city,best_lenth):
        self.compute_information(num_city)
        # 初始化蚁群个体城市位置
        for i in range(self.m):
            start = np.random.randint(num_city - 1)
            self.Table[i][0] = start
            unvisit = list([x for x in range(num_city) if x != start])  # 未访问城市集合
            current = start
            j = 1
            while len(unvisit) != 0:
                P = []
                # 通过信息素计算城市之间的转移概率
                for v in unvisit:
                    P.append(self.Tau[current][v] ** self.alpha * self.Eta[current][v] ** self.beta)  # 概率计算 !!  把初始信息素矩阵更换就行
                P_sum = sum(P)
                P = [x / P_sum for x in P]
                # 轮盘赌选择一个一个城市
                index = self.rand_choose(P) # 返回轮盘赌的城市num
                current = unvisit[index]
                self.Table[i][j] = current
                unvisit.remove(current)
                j += 1

    # 计算不同城市之间的距离
    def compute_dis_mat(self, num_city, location):
        dis_mat = np.zeros((num_city, num_city))
        for i in range(num_city):
            for j in range(num_city):
                if i == j:
                    dis_mat[i][j] = np.inf  # 无穷大
                    continue
                a = location[i]
                b = location[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))  # zip函数+列表推导式 求出各城市欧式距离
                dis_mat[i][j] = tmp
        return dis_mat

    # 计算一条路径的长度  计算Lk
    def compute_pathlen(self, path, dis_mat):
        a = path[0]
        b = path[-1]
        result = dis_mat[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += dis_mat[a][b]
        return result

    # 计算一个群体的长度
    def compute_paths(self, paths):
        result = []
        for one in paths:
            length = self.compute_pathlen(one, self.dis_mat)
            result.append(length)
        return result

    # 更新信息素
    def update_Tau(self):
        delta_tau = np.zeros([self.num_city, self.num_city])
        paths = self.compute_paths(self.Table)
        for i in range(self.m):
            for j in range(self.num_city - 1):
                a = self.Table[i][j]
                b = self.Table[i][j + 1]
                delta_tau[a][b] = delta_tau[a][b] + self.Q / paths[i]
            a = self.Table[i][0]
            b = self.Table[i][-1]
            delta_tau[a][b] = delta_tau[a][b] + self.Q / paths[i]
        self.Tau = (1 - self.rho) * self.Tau + delta_tau

    def aco(self):
        best_lenth = math.inf  # math.inf返回浮点正无穷大
        best_path = None
        for cnt in range(self.iter_max):
            # 生成新的蚁群
            self.get_ants(self.num_city,best_lenth)  # out>>self.Table  得到各蚂蚁城市路径表-二维列表
            self.paths = self.compute_paths(self.Table)  # 得到各蚂蚁Lk长度-列表
            # 取该蚁群的最优解
            tmp_lenth = min(self.paths)
            tmp_path = self.Table[self.paths.index(tmp_lenth)]
            # 更新最优解
            if tmp_lenth < best_lenth:
                best_lenth = tmp_lenth
                best_path = tmp_path
            # 更新信息素
            self.update_Tau()
            # 保存结果
            print(cnt, best_lenth)
        return best_lenth, best_path

    def run(self):
        best_length, best_path, = self.aco()
        return self.location[best_path], best_length,

data = np.array([[565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0], [845.0, 655.0],
                        [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0], [580.0, 1175.0], [650.0, 1130.0],
                        [1605.0, 620.0], [1220.0, 580.0], [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0],
                        [725.0, 370.0], [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
                        [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0], [975.0, 580.0],
                        [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0], [660.0, 180.0], [410.0, 250.0],
                        [420.0, 555.0], [575.0, 665.0], [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0],
                        [685.0, 610.0], [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
                        [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0], [555.0, 815.0],
                        [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0], [605.0, 625.0], [595.0, 360.0],
                        [1340.0, 725.0], [1740.0, 245.0]])

city_name=[]
data = data[:, 1:]

# 加上一行因为会回到起点
show_data = np.vstack([data, data[0]])  # 级联
aco = ACO(num_city=data.shape[0], data=data.copy())
Best_path, Best, = aco.run()
print(Best)
