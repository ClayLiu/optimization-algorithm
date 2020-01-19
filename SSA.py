import numpy as np
import math
import sys
from Common.utils import *


class SSA:
    def __init__(self, objectiveFunction, boundsList, constraintFunction, salpSum, iterNum, extremum=False):
        """
        :param extremum: false -> min  true -> max
        """
        self.objectiveFunction = objectiveFunction
        self.dimension = len(boundsList)
        self.salpSum = salpSum
        self.iterNum = iterNum
        self.boundsLists = boundsList
        self.salpPositions = np.zeros([self.salpSum, self.dimension])
        self.F = np.zeros([self.dimension])
        self.boundUppers = np.zeros([self.dimension])
        self.boundLowers = np.zeros([self.dimension])
        self.c1 = 0.0
        self.constraintFunction = constraintFunction
        self.extremum = extremum
        self.init_population()

    def init_population(self):
        self.salpPositions = generate_population(self.salpSum, self.boundsLists, self.constraintFunction)
        self.get_bounds_lowers()
        self.get_bounds_uppers()

    def get_bounds_uppers(self):
        for index, singlebound in enumerate(self.boundsLists):
            if isinstance(singlebound, int):
                self.boundUppers[index] = singlebound
            else:
                self.boundUppers[index] = singlebound[Bounds.upper]

    def get_bounds_lowers(self):
        for index, singlebound in enumerate(self.boundsLists):
            if isinstance(singlebound, int):
                self.boundLowers[index] = singlebound
            else:
                self.boundLowers[index] = singlebound[Bounds.lower]

    def get_fitness(self):
        return np.array([self.objectiveFunction(*position) for position in self.salpPositions])

    def update_leader_salp_position(self):
        while True:
            if np.random.random() >= 0.5:
                position = self.F + self.c1 * (
                        (self.boundUppers - self.boundLowers) * np.random.random() + self.boundLowers)
            else:
                position = self.F - self.c1 * (
                        (self.boundUppers - self.boundLowers) * np.random.random() + self.boundLowers)
            try:
                inspectors(position, self.boundsLists, self.constraintFunction)
            except ViolatedConstraintError:
                continue
            except IllegalVariableError:
                position = convert_position_to_legal(position, self.boundsLists)
            break
        return position

    def update_follower_salp_position(self, currentPosition, lastPosition):
        while True:
            position = 0.5 * (currentPosition + lastPosition)
            try:
                inspectors(position, self.boundsLists, self.constraintFunction)
            except ViolatedConstraintError:
                continue
            except IllegalVariableError:
                position = convert_position_to_legal(position, self.boundsLists)
            break
        return position

    def iteration(self):
        for i in range(self.iterNum):
            print("正在进行第" + str(i+1) + "次")
            if self.extremum:
                self.F = self.salpPositions[np.argmax(self.get_fitness()), :].copy()
            else:
                self.F = self.salpPositions[np.argmin(self.get_fitness()), :].copy()

            self.c1 = 2*math.exp(- (4*i / self.iterNum)**2)

            for j, position in enumerate(self.salpPositions):
                if j < self.salpPositions.shape[0] / 2:
                    self.salpPositions[j] = self.update_leader_salp_position()
                else:
                    self.salpPositions[j] = self.update_follower_salp_position(self.salpPositions[j, :], self.salpPositions[j - 1, :])

        print()
        print(str(self.iterNum), "次迭代最优解:")
        print(self.F)
        print("--------------")
        print("适应度:")
        print(self.objectiveFunction(*self.F))


# 定义变量的约束
# boundsList = ((-10, 10), (-10, 10), (0, 150), (50, 240))
boundsList = ((-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi))
# 定义目标函数
# objectiveFunction = lambda x1, x2, x3, x4: 0.6221*x1*x3*x4 + 1.7781*x2*x3**2 + 3.1661*x4*x1**2 + 19.84*x3*x1**2
objectiveFunction = lambda x, y: x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)
# 定义变量间的约束，可以为单个lambda函数，也可以为lambda函数列表
constraintFunction = lambda x, y: True
# constraintFunction = [
#     lambda x1, x2, x3, x4: -x1 + 0.0193*x3 <= 0,
#     lambda x1, x2, x3, x4: -x2 + 0.00954*x3 <= 0,
#     lambda x1, x2, x3, x4: (-math.pi*x4*x3**2) - (4/3) * math.pi*x3**3 + 1296000 <= 0,
#     lambda x1, x2, x3, x4: x4 - 240 <= 0
# ]


salpSum = 30
iterNum = 1000

ssa = SSA(objectiveFunction, boundsList, constraintFunction, salpSum, iterNum)
ssa.iteration()
