import math
from Common.utils import *
from algorithm.arithmetic import arithmetic
from Common.showUtils import image
from prettytable import PrettyTable

class CASSA(arithmetic):
    def __init__(self, objectiveFunction, boundsLists, constraintFunction, salpNum, iterNum, extremum=False):
        self.objectiveFunction = objectiveFunction
        self.dimension = len(boundsLists)
        self.salpNum = salpNum
        self.iterNum = iterNum
        self.boundsLists = boundsLists
        self.salpAllPosition = np.zeros([self.salpNum, self.dimension])
        self.F = np.zeros([self.dimension])
        self.boundUppers = np.zeros([self.dimension])
        self.boundLowers = np.zeros([self.dimension])
        self.constraintFunction = constraintFunction
        self.extremum = extremum
        self.c1 = 0.0
        self.crazyProbability = float(read_config("CASSA", "crazyProbability"))
        self.xcraziness = float(read_config("CASSA", "xcraziness"))
        self.ws = float(read_config("CASSA", "ws"))
        self.we = float(read_config("CASSA", "we"))
        self.u = float(read_config("CASSA", "u"))

        self.fitnessList = []
        self.fitnessPosition = []
        self.image = image(self.iterNum, self.fitnessList, self.fitnessPosition)

        self.init_population()

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

    def init_population(self):
        self.get_bounds_uppers()
        self.get_bounds_lowers()

        salpAllPosition = []
        for i in range(self.dimension):
            # 序列生成种子
            sequenceSeed = np.array(list(np.linspace(0, 1, self.salpNum)))
            # sequenceSeed = np.matlib.rand(self.salpNum).tolist()[0] # 随机生成种子
            for j, seed in enumerate(sequenceSeed):
                if seed < 0.5:
                    sequenceSeed[j] = self.u * seed
                else:
                    sequenceSeed[j] = self.u * (1 - seed)
            oneDimensionalPosition = self.boundLowers[i] + (self.boundUppers[i] - self.boundLowers[i]) * sequenceSeed
            salpAllPosition.append(oneDimensionalPosition)
        self.salpAllPosition = np.array(salpAllPosition).T.copy()
        # self.iterator()

    def get_fitness(self):
        return np.array([self.objectiveFunction(*position) for position in self.salpAllPosition])

    def get_p(self, c4):
        if c4 > self.crazyProbability:
            p = 0
        else:
            p = 1
        return p

    def get_sign(self, c4):
        if c4 < 0.5:
            sign = 1
        else:
            sign = -1

        return sign

    def get_weight(self, t):
        w = self.ws * (self.ws - self.we) * (self.iterNum - t) / self.iterNum
        return w

    def update_leader_salp_position(self):
        while True:
            c4 = np.random.random()
            if np.random.random() >= 0.5:
                position = self.F + self.get_p(c4) * self.get_sign(c4) * self.xcraziness * self.c1 * (
                        (self.boundUppers - self.boundLowers) * np.random.random(self.dimension) + self.boundLowers)
            else:
                position = self.F - self.get_p(c4) * self.get_sign(c4) * self.xcraziness * self.c1 * (
                        (self.boundUppers - self.boundLowers) * np.random.random(self.dimension) + self.boundLowers)
            try:
                inspectors(position, self.boundsLists, self.constraintFunction)
            except ViolatedConstraintError:
                continue
            except IllegalVariableError:
                position = convert_position_to_legal(position, self.boundsLists)
            break
        return position

    def update_follower_salp_position(self, currentPosition, lastPosition, t):
        while True:
            position = 0.5 * (currentPosition + self.get_weight(t) * lastPosition)
            try:
                inspectors(position, self.boundsLists, self.constraintFunction)
            except ViolatedConstraintError:
                continue
            except IllegalVariableError:
                position = convert_position_to_legal(position, self.boundsLists)
            break
        return position

    def iterator(self):
        for t in range(self.iterNum):
            if self.extremum:
                self.F = self.salpAllPosition[np.argmax(self.get_fitness()), :].copy()
            else:
                self.F = self.salpAllPosition[np.argmin(self.get_fitness()), :].copy()

            self.c1 = 2 * math.exp(-(4*t/self.iterNum)**2)

            for j, position in enumerate(self.salpAllPosition):
                if j < self.salpAllPosition.shape[0] / 2:
                    self.salpAllPosition[j] = self.update_leader_salp_position()

                else:
                    self.salpAllPosition[j, :] = self.update_follower_salp_position(self.salpAllPosition[j, :], self.salpAllPosition[j-1, :], t)

            self.fitnessList.append(self.objectiveFunction(*self.F))
            self.fitnessPosition.append(self.F)
        # print(str(self.iterNum), "次迭代最优解:")
        # print(self.F)
        # print("--------------")
        # print("适应度:")
        # print(self.objectiveFunction(*self.F))
        # print("CASSA:", self.F, self.objectiveFunction(*self.F))

    def show(self):
        print()
        tb = PrettyTable()
        tb.field_names = ["algorithm name", "iterations", "Optimal solution", "optimal value"]
        tb.add_row(["CASSA", self.iterNum, self.F, self.objectiveFunction(*self.F)])
        print(tb)

        # self.image.show()


# boundsList = ((-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi))
#
# objectiveFunction = lambda x, y: x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)
# # objectiveFunction = lambda x, y: 20 + x**2 + y**2 - 10*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y))
# # objectiveFunction = lambda x, y: -abs(math.sin(x)*math.cos(y)*math.exp(abs(1 - ((x**2+y**2)**0.5))/math.pi))
# constraintFunction = lambda x, y: True
#
# salpNum = 30
# iterNum = 1000
#
# ssa = CASSA(objectiveFunction, boundsList, constraintFunction, salpNum, iterNum,)
# ssa.iterator()
# ssa.show()
