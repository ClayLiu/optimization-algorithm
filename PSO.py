import numpy as np
import math
import random
import matplotlib.pyplot as plt
import visdom
from collections import Iterable
import time


class PSO:
    def __init__(self, func, dim, limit, v_max,  p_num, iter_num, w=1, c1=0.2, c2=0.2):
        """
        :param func: 函数
        :param dim: 维度
        :param limit: 接受每个维度的区间上下限，列表形式，可以为单个数值,例子：
                        [(20,30), (30,40), 5]
        :param p_num: 粒子的数量
        :param iter_num: 迭代次数
        :param w: 惯性权重
        :param c1:
        :param c2:
        """
        assert dim == len(limit), "维度和区间不匹配！"
        self.v_max = v_max
        self.func = func
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.dim = dim
        self.p_num = p_num
        self.iter_num = iter_num
        self.limit = limit
        self.position = np.zeros([self.p_num, self.dim])
        self.velocity = np.zeros([self.p_num, self.dim])
        self.pbest = np.zeros([self.p_num, self.dim])
        self.gbest = np.zeros([1, self.dim])
        self.init_Population()

    def init_Population(self):
        a = []
        for item in self.limit:
            if isinstance(item, int):
                _a = np.full((self.p_num, 1), item)
            else:
                _a = np.random.rand(self.p_num, 1) * (item[1] - item[0]) + item[0]
            a.append(_a)
        self.position = np.concatenate(tuple(a), axis=1)
        self.velocity = np.random.rand(*self.position.shape) * self.v_max
        self.pbest = self.position.copy()
        self.gbest = min(self.pbest, key=lambda particle: self.func(*particle)).copy()

    def get_fitness(self):
        return np.array([self.func(*position) for position in self.position])

    def update_position(self):

        for index, item in enumerate(self.position):
            self.velocity[index] = self.w * self.velocity[index] + \
                                   self.c1 * np.random.random() * (self.pbest[index] - self.position[index]) + \
                                   self.c2 * np.random.random() * (self.gbest - self.position[index])

            self.position[index] = self.position[index] + self.velocity[index]

            for i, var in enumerate(item):
                if isinstance(self.limit[i], Iterable):
                    if var < self.limit[i][0]:
                        self.position[index][i] = self.limit[i][0]
                    elif var > self.limit[i][1]:
                        self.position[index][i] = self.limit[i][1]
                elif var != self.limit[i]:
                    self.position[index][i] = self.limit[i]

    def update_best(self):
        global_best_fitness = self.func(*self.gbest)
        person_best_value = np.array([self.func(*particle) for particle in self.pbest])

        for index, particle in enumerate(self.position):
            current_particle_fitness = self.func(*particle)

            if current_particle_fitness < person_best_value[index]:
                person_best_value[index] = current_particle_fitness
                self.pbest[index] = particle.copy()
            if current_particle_fitness < global_best_fitness:
                global_best_fitness = current_particle_fitness
                self.gbest = particle.copy()

    def pso(self):
        self.update_position()
        self.update_best()

    def info(self):
        pass

    def iterator(self):
        for _ in range(self.iter_num):
            self.pso()
            print(self.gbest, func(*self.gbest))


func = lambda x, y:  x**2 + y**2

pso = PSO(func, 2, ((-20, 20), (-20, 20)), 0.5,  1000, 1000, w=1, c1=0.2, c2=0.2)

pso.iterator()