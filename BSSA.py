import numpy as np
import math
from collections.abc import Iterable
import visdom
import time


class BSSA:
    def __init__(self, data, bounds, salp_num, iter_num):
        self.dim = data.shape[1]
        self.salp_num = salp_num
        self.iter_num = iter_num
        self.bounds = bounds
        self.position = np.zeros([self.salp_num, self.dim])
        self.F = np.zeros([1, self.dim])
        self.ub = np.zeros([1, self.dim])
        self.lb = np.zeros([1, self.dim])
        self.c1 = 0.0
        self.binaryV = np.zeros([self.salp_num, self.dim])
        self.init_Population()

    def toBinary(self):
        # S_shaped Function转换到0/1
        t = 1/(1+np.exp(-self.position.copy()))
        self.binaryV = np.where(np.random.random() < t, 0, 1)
        # V_shaped Function转换到0/1

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
        self.toBinary()

    def get_fitness(self):
        pass 

    def iteration(self):
        # win = self.vis.scatter(
        #     X=self.position,
        #     opts={
        #         'markersize': 5,
        #         'title': "0"
        #     },
        # )
        # win_line = self.vis.line(X=np.array([0]), Y=np.array([0]))
        for i in range(1, self.iter_num):

            # 计算fitness，并更新食物源
            if self.extremum == "min":
                self.F = self.position[np.argmin(self.get_fitness()), :].copy()
            else:
                self.F = self.position[np.argmax(self.get_fitness()), :].copy()

            # 计算c1
            self.c1 = 2 * math.exp(-(4*i/self.iter_num)**2)

            # 更新每个樽海鞘个体
            for j, position in enumerate(self.position):
                if j < self.position.shape[0] / 2:
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
            if i % 100 == 0:
                print("第", i, "次迭代进行中...")
            # if i % 2 == 0 and i < 40:
            #     self.vis.scatter(
            #         X=self.position,
            #         # win=win,
            #         opts=dict(
            #             title=str(i)+" 次迭代",
            #             markersize=5
            #         ),
            #
            #
            #     )
            # self.vis.line(X=np.array([i]),
            #               Y=np.array([self.func(*self.F)]),
            #               win=win_line,
            #               update='append',
            #               opts=dict(
            #                   title="SSA适应度曲线",
            #                   markersize=5
            #               ),
            #               )

        print(str(self.iter_num), "次迭代最优解:")
        print(self.F)
        print("--------------")
        print("适应度:")
        print(self.func(*self.F))





bounds = ((-20, 20), (-20, 20), (-20, 20))


# dim = 2
# bounds = ((-20, 20), (-20, 20))
# func = lambda x, y: x**2 + y**2
data = np.loadtxt("./dataset.txt", dtype=float, delimiter=',')
data = data[:, 0:-1].copy()

salp_num = 30
iter_num = 1000

ssa = BSSA(data, bounds, salp_num, iter_num)
ssa.iteration()
