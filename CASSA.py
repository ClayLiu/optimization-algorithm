import numpy as np
import math
from collections.abc import Iterable
import visdom
import time
import numpy.matlib


class CASSA:
    def __init__(self, func, dim, bounds, salp_num, iter_num, extremum="min"):
        """
        :param func: 目标函数
        :param dim: 目标函数维度
        :param bounds: 上下限
        :param salp_num: salp个体数量
        :param iter_num: 迭代次数
        :param extremum: max or min
        """
        assert dim == len(bounds), "维度和区间不匹配！"
        assert extremum == "min" or extremum == "max", "只能输入min或者max！"
        self.func = func
        self.dim = dim
        self.salp_num = salp_num
        self.iter_num = iter_num
        self.bounds = bounds
        self.position = np.zeros([self.salp_num, self.dim])
        self.F = np.zeros([1, self.dim])
        self.ub = np.zeros([1, self.dim])
        self.lb = np.zeros([1, self.dim])
        self.c1 = 0.0
        self.extremum = extremum
        self.pcr = 0.3
        self.xcra = 0.0001
        self.ws = 0.9
        self.we = 0.4
        self.u = 2
        self.init_Population()
        self.vis = visdom.Visdom()

    def init_Population(self):
        for i, item in enumerate(self.bounds):
            if isinstance(item, int):
                self.ub[:, i] = item
                self.lb[:, i] = item
            else:
                self.ub[:, i] = item[1]
                self.lb[:, i] = item[0]

        a = []
        for i in range(self.dim):
            y = list(np.linspace(0, 1, self.salp_num))  # 序列生成种子
            # y = np.matlib.rand(self.salp_num).tolist()[0] # 随机生成种子
            for j, var in enumerate(y):
                y[j] = self.u * var if var < 0.5 else self.u * (1-var)
            x = self.lb[:, i] + (self.ub[:, i] - self.lb[:, i]) * y
            a.append(x)
        self.position = np.array(a).T.copy()

    def get_fitness(self):
        return np.array([self.func(*position) for position in self.position])

    def iteration(self):
        win = self.vis.scatter(
            X=self.position,
            opts={
                'markersize': 5,
                'title': "0"
            },
        )
        win_line = self.vis.line(X=np.array([0]), Y=np.array([0]))
        for i in range(1, self.iter_num):
            if self.extremum == "min":
                self.F = self.position[np.argmin(self.get_fitness()), :].copy()
            else:
                self.F = self.position[np.argmax(self.get_fitness()), :].copy()
            self.c1 = 2 * math.exp(-(4*i/self.iter_num)**2)
            for j, position in enumerate(self.position):
                if j < self.position.shape[0] / 2:
                    c4 = np.random.random()
                    if c4 > self.pcr:
                        p = 0
                    else:
                        p = 1
                    if c4 < 0.5:
                        sign = 1
                    else:
                        sign = -1
                    if np.random.random() >= 0.5:
                        self.position[j] = self.F + p * sign * self.xcra * self.c1 * (
                                (self.ub - self.lb) * np.random.random() + self.lb)
                    else:
                        self.position[j] = self.F - p * sign * self.xcra * self.c1 * (
                                    (self.ub - self.lb) * np.random.random() + self.lb)

                else:
                    w = self.ws * (self.ws-self.we) * (self.iter_num-i) / self.iter_num
                    self.position[j, :] = 0.5 * (self.position[j, :] + w * self.position[j-1, :])

                for index, var in enumerate(position):
                    if isinstance(self.bounds[index], Iterable):
                        if var < self.bounds[index][0]:
                            self.position[j][index] = self.bounds[index][0]
                        elif var > self.bounds[index][1]:
                            self.position[j][index] = self.bounds[index][1]
                    elif var != self.bounds[index]:
                        self.position[j][index] = self.bounds[index]
            if i % 100 == 0:
                print("第", i, "次迭代进行中...")
            if i % 2 == 0 and i < 40:
                self.vis.scatter(
                    X=self.position,
                    # win=win,
                    opts=dict(
                        title=str(i)+" 次迭代",
                        markersize=5
                    ),


                )
            self.vis.line(X=np.array([i]),
                          Y=np.array([self.func(*self.F)]),
                          win=win_line,
                          update='append',
                          opts=dict(
                              title="SSA适应度曲线",
                              markersize=5
                          ),
                          )

        print(str(self.iter_num), "次迭代最优解:")
        print(self.F)
        print("--------------")
        print("适应度:")
        print(self.func(*self.F))




# dim = 3
# bounds = ((-20, 20), (-20, 20), (-20, 20))
# func = lambda x, y, z: x**2 + y**2 + z**2

dim = 2
bounds = ((-20, 20), (-20, 20))
func = lambda x, y: x**2 + y**2


salp_num = 20
position = np.zeros((salp_num, dim))
salp_num = 30
iter_num = 100

ssa = CASSA(func, dim, bounds, salp_num, iter_num, "min")
ssa.iteration()
