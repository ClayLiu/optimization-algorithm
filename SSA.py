import numpy as np
import math
import sys

from Exceptions.Errors import *
from Common.EnumSet import Bounds
from inspect import isfunction


class SSA:
    def __init__(self, objectiveFunction, boundsList, constraintFunction, salpSum, iterNum, extremum=False):
        """
        :param extremum: false -> min  true -> max
        """
        self.objectiveFunction = objectiveFunction
        self.dimension = len(boundsList)
        self.salpSum = salpSum
        self.iterNum = iterNum
        self.boundsList = boundsList
        self.salpPositions = np.zeros([self.salpSum, self.dimension])
        self.F = np.zeros([self.dimension])
        self.boundUppers = np.zeros([self.dimension])
        self.boundLowers = np.zeros([self.dimension])
        self.c1 = 0.0
        self.constraintFunction = constraintFunction
        self.extremum = extremum
        self.init_population()

    def inspectors(self, variablesList):

        # 检查变量间是否符合约束
        if isfunction(self.constraintFunction):
            if not self.constraintFunction(*variablesList):
                raise ViolatedConstraintError
        else:
            for constraintfunction in self.constraintFunction:
                if not constraintfunction(*variablesList):
                    raise ViolatedConstraintError

        # 检查单个变量是否符合约束
        if len(variablesList) != len(self.boundsList):
            raise MismatchError
        for index, dimensionBounds in enumerate(self.boundsList):
            if isinstance(dimensionBounds, int):
                if variablesList[index] != dimensionBounds:
                    raise IllegalVariableError
            else:
                if variablesList[index] < dimensionBounds[Bounds.lower.value] or variablesList[index] > dimensionBounds[Bounds.upper.value]:
                    raise IllegalVariableError

    def generate_salp(self):
        while True:
            singleSalpPosition = []
            for index, dimensionBounds in enumerate(self.boundsList):
                if isinstance(dimensionBounds, int):
                    singleSalpPosition.append(dimensionBounds)
                else:
                    singleSalpPosition.append(np.random.rand()*(dimensionBounds[Bounds.upper.value] - dimensionBounds[Bounds.lower.value]) + dimensionBounds[Bounds.lower.value])
            try:
                self.inspectors(singleSalpPosition)
            except IllegalVariableError as e:
                continue
            except ViolatedConstraintError as e:
                continue
            break
        return singleSalpPosition

    def init_population(self):
        positions = []
        for i in range(self.salpSum):
            # print("正在生成第"+str(i+1)+"个salp")
            try:
                positions.append(self.generate_salp())
            except MismatchError as e:
                print(e.info)
                sys.exit(1)
        self.salpPositions = np.array(positions)
        self.get_bounds_lowers()
        self.get_bounds_uppers()
        # print(self.salpPositions)

    def get_bounds_uppers(self):
        for index, singlebound in enumerate(self.boundsList):
            if isinstance(singlebound, int):
                self.boundUppers[index] = singlebound
            else:
                self.boundUppers[index] = singlebound[Bounds.upper.value]

    def get_bounds_lowers(self):
        for index, singlebound in enumerate(self.boundsList):
            if isinstance(singlebound, int):
                self.boundLowers[index] = singlebound
            else:
                self.boundLowers[index] = singlebound[Bounds.lower.value]

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
                self.inspectors(position)
            except ViolatedConstraintError:
                continue
            except IllegalVariableError:
                position = self.convert_variable_to_legal(position)
            break
        return position

    def update_follower_salp_position(self, currentPosition, lastPosition):
        while True:
            position = 0.5 * (currentPosition + lastPosition)
            try:
                self.inspectors(position)
            except ViolatedConstraintError:
                continue
            except IllegalVariableError:
                position = self.convert_variable_to_legal(position)
            break
        return position

    def convert_variable_to_legal(self, position):
        for index, var in enumerate(position):
            if isinstance(self.boundsList[index], int):
                if var != self.boundsList[index]:
                    position[index] = self.boundsList[index]
            else:
                if var < self.boundLowers[index]:
                    position[index] = self.boundLowers[index]
                elif var > self.boundUppers[index]:
                    position[index] = self.boundUppers[index]

        return position

    def iteration(self):
        for i in range(self.iterNum):
            print("正在进行第" + str(i+1) + "次")
            # print("所有坐标: " + str(self.salpPositions))
            # print("F: " + str(self.F))
            if self.extremum:
                self.F = self.salpPositions[np.argmax(self.get_fitness()), :].copy()
            else:
                self.F = self.salpPositions[np.argmin(self.get_fitness()), :].copy()

            self.c1 = 2*math.exp(- (4*i / self.iterNum)**2)

            for j, position in enumerate(self.salpPositions):
                # print("单个坐标:"+str(position))
                # print()
                if j < self.salpPositions.shape[0] / 2:
                    self.salpPositions[j] = self.update_leader_salp_position()
                else:
                    self.salpPositions[j] = self.update_follower_salp_position(self.salpPositions[j, :], self.salpPositions[j - 1, :])

            # print("当前最优解: ")
            # print(self.F)
            # print("当前适应度: ")
            # print(self.objectiveFunction(*self.F))


        print()
        print(str(self.iterNum), "次迭代最优解:")
        print(self.F)
        print("--------------")
        print("适应度:")
        print(self.objectiveFunction(*self.F))


# 定义变量的约束
# boundsList = ((-10, 10), (-10, 10), (0, 150), (50, 240))
boundsList = [(-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi)]
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
