
import numpy as np
import init
import update
import visdom
import time

class MSSA:
    def __init__(self, func, dim, bounds, salp_num, iter_num, thresh, mesh_div, extremum):
        """
        :param func: 目标函数列表:  [func1, func2, func3]
        :param dim: 变量个数(维度)
        :param bounds: 变量上下限: [[20, 30], [30, 40], [40, 50]]
        :param salp_num: 樽海鞘个体数
        :param iter_num: 迭代次数
        :param extremum: 目标函数求解极值: ["max", "min", "max"]
        :param thresh: 储存库大小
        :param mesh_div: 等分因子
        """
        assert dim == len(bounds), "变量个数和区间数不匹配！"
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
        self.fitness = np.zeros((1, len(self.func)))
        self.archive_in = []
        self.archive_fitness = []
        self.thresh = thresh
        self.mesh_div = mesh_div
        self.vis = visdom.Visdom()

    def evaluation_fitness(self):
        # 计算适应值
        fitness_curr = []
        for func in self.func:
            fitness_curr.append([func(*position) for position in self.position])
        self.fitness = np.array(fitness_curr).T

    def initialize(self):
        # 初始化樽海鞘群坐标
        self.position, self.ub, self.lb = init.init_salp(self.salp_num, self.bounds)
        self.evaluation_fitness()
        self.archive_in, self.archive_fitness = init.init_archive(self.position, self.fitness, self.extremum)

    def update(self, l):
        self.evaluation_fitness()
        self.archive_in, self.archive_fitness = update.update_archive(self.position, self.fitness, self.archive_in,
                                                                      self.archive_fitness, self.thresh, self.mesh_div,
                                                                      self.lb, self.ub, self.extremum)
        self.F = update.update_food(self.archive_in, self.archive_fitness, self.mesh_div, self.lb, self.ub)
        self.c1 = update.update_c1(l, self.iter_num)
        self.position = update.update_position(self.position, self.F, self.lb, self.ub, self.c1)

    def done(self):
        self.initialize()
        win = self.vis.scatter(
            X=self.archive_fitness,
            opts={
                'markersize': 5,
                'markercolor': np.array([[0, 0, 255]]),
                'title': "pareto边界个体分布"
            },
        )

        for i in range(1, self.iter_num + 1):
            if i % 10 == 0:
                print("第", i, "次迭代进行中...")

            self.vis.scatter(
                X=self.fitness,
                opts={
                    'markersize': 5,
                    'markercolor': np.array([[59, 89, 152]]),
                    'title': "pareto边界个体分布"
                },
                win=win,
                update='append'
            )
            self.update(i)

        self.vis.scatter(
            X=self.archive_fitness,
            opts={
                'markersize': 5,
                'title': "pareto边界个体分布",
                'markercolor': np.array([[255, 0, 0]]),
            },
            update='append',
            win=win
        )

        self.vis.scatter(
            X=self.archive_in,
            opts={
                'markersize': 5,
                # 'markercolor': np.array([[0, 255, 0]]),
                'title': "可行解分布"
            },
        )

        return self.archive_in, self.archive_fitness
