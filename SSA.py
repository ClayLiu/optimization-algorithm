'''
    author : 刘志杭
'''
import numpy as np
import math
from collections import Iterable
import visdom
import time

class SSA:
    def __init__(self, func, dim, bounds, salp_num, iter_num):
        """
        :param func: 目标函数
        :param dim: 目标函数维度
        :param bounds: 上下限
        :param salp_num: salp个体数量
        :param iter_num: 迭代次数
        """
        assert dim == len(bounds), "维度和区间不匹配！"
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
        self.init_Population()
        self.vis = visdom.Visdom()

    def init_Population(self):
        a = []
        for i, item in enumerate(self.bounds):
            if isinstance(item, int):
                _a = np.full((self.salp_num, 1), item)
                self.ub[:, i] = item
                self.lb[:, i] = item
            else:
                _a = np.random.rand(self.salp_num, 1) * (item[1] - item[0]) + item[0]
                self.ub[:, i] = item[1]
                self.lb[:, i] = item[0]
            a.append(_a)
        self.position = np.concatenate(tuple(a), axis=1)

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
            self.F = self.position[np.argmin(self.get_fitness()), :].copy()
            self.c1 = 2 * math.exp(-(4*i/self.iter_num)**2)
            for j, position in enumerate(self.position):
                if j == 0:
                    if np.random.random() >= 0.5:
                        self.position[j] = self.F + self.c1 * (
                                (self.ub - self.lb) * np.random.random() + self.lb)
                    else:
                        self.position[j] = self.F - self.c1 * (
                                    (self.ub - self.lb) * np.random.random() + self.lb)

                else:
                    self.position[j, :] = 0.5 * (self.position[j, :] + self.position[j-1, :])

                for index, var in enumerate(position):
                    if isinstance(self.bounds[index], Iterable):
                        if var < self.bounds[index][0]:
                            self.position[j][index] = self.bounds[index][0]
                        elif var > self.bounds[index][1]:
                            self.position[j][index] = self.bounds[index][1]
                    elif var != self.bounds[index]:
                        self.position[j][index] = self.bounds[index]
            self.vis.scatter(
                X=self.position,
                win=win,
                opts=dict(
                    opts=dict(
                    legend=['Didnt', 'Update'],
                    xtickmin=-50,
                    xtickmax=50,
                    xtickstep=0.5,
                    ytickmin=-50,
                    ytickmax=50,
                    ytickstep=0.5,
                    markersymbol='cross-thin-open',
                ),

                )
            )
            self.vis.line(X=np.array([i]),
                          Y=np.array([self.func(*self.F)]),
                          win=win_line,
                          update='append')
            print([self.func(*self.F)])





salp_num = 20
dim = 3
position = np.zeros((salp_num, dim))
bounds = ((-20, 20), (-20, 20))
salp_num = 1000
iter_num = 1000
func = lambda x, y: x**2 + y**2

ssa = SSA(func, 2, bounds, salp_num, iter_num)
ssa.iteration()