import math
from MultiobjectiveUtils import update, init
from MultiobjectiveUtils.show import *
from Common.utils import *


class MCASSA:
    def __init__(self, objectiveFunctionList, boundsLists, constraintFunction, salpSum, iterNum, thresh, mesh_div, extremum):
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
        self.objectiveFunctionList = objectiveFunctionList
        self.dimension = len(boundsLists)
        self.salpSum = salpSum
        self.iterNum = iterNum
        self.constraintFunction = constraintFunction
        self.boundsLists = boundsLists
        self.salpPositions = np.zeros([self.salpSum, self.dimension])
        self.F = np.zeros([1, self.dimension])
        self.c1 = 0.0
        self.boundUppers = np.zeros([self.dimension])
        self.boundLowers = np.zeros([self.dimension])
        self.extremum = extremum
        self.fitness = np.zeros((1, len(self.objectiveFunctionList)))
        self.archive_in = []
        self.archive_fitness = []
        self.thresh = thresh
        self.mesh_div = mesh_div
        self.crazyProbability = float(read_config("MCASSA", "crazyProbability"))
        self.xcraziness = float(read_config("MCASSA", "xcraziness"))
        self.ws = float(read_config("MCASSA", "ws"))
        self.we = float(read_config("MCASSA", "we"))
        self.u = float(read_config("MCASSA", "u"))

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

    def evaluation_fitness(self):
        # 计算适应值
        fitness_curr = []
        for func in self.objectiveFunctionList:
            fitness_curr.append([func(*position) for position in self.salpPositions])
        self.fitness = np.array(fitness_curr).T

    def generate_population(self):
        salpAllPosition = []
        for i in range(self.dimension):
            # 序列生成种子
            sequenceSeed = np.array(list(np.linspace(0, 1, self.salpSum)))
            # sequenceSeed = np.matlib.rand(self.salpNum).tolist()[0] # 随机生成种子
            for j, seed in enumerate(sequenceSeed):
                if seed < 0.5:
                    sequenceSeed[j] = self.u * seed
                else:
                    sequenceSeed[j] = self.u * (1 - seed)
            oneDimensionalPosition = self.boundLowers[i] + (self.boundUppers[i] - self.boundLowers[i]) * sequenceSeed
            salpAllPosition.append(oneDimensionalPosition)
        return np.array(salpAllPosition).T.copy()

    def init_population(self):
        self.get_bounds_lowers()
        self.get_bounds_uppers()
        self.salpPositions = self.generate_population()

        self.evaluation_fitness()
        self.archive_in, self.archive_fitness = init.init_archive(self.salpPositions, self.fitness, self.extremum)

    def update_c1(self, l, L):
        # 更新c1
        c1 = 2 * math.exp(-(4 * l / L) ** 2)
        return c1

    def update_position(self, t):
        for j, position in enumerate(self.salpPositions):
            if j < self.salpPositions.shape[0] / 2:
                self.salpPositions[j] = self.update_leader_salp_position()
            else:
                self.salpPositions[j] = self.update_follower_salp_position(self.salpPositions[j, :],
                                                                           self.salpPositions[j - 1, :], t)

    def update(self, t):
        self.evaluation_fitness()
        self.archive_in, self.archive_fitness = update.update_archive(self.salpPositions, self.fitness, self.archive_in,
                                                                      self.archive_fitness, self.thresh, self.mesh_div,
                                                                      self.boundLowers, self.boundUppers, self.extremum)
        self.F = update.update_food(self.archive_in, self.archive_fitness, self.mesh_div, self.boundLowers, self.boundUppers)
        self.c1 = self.update_c1(t, self.iterNum)
        self.update_position(t)

    def done(self):
        self.init_population()

        for i in range(self.iterNum):

            print(i)

            self.update(i)

        return self.archive_in, self.archive_fitness


func1 = lambda x, y: x
func2 = lambda x, y: (1+y)/x
func = [func1, func2]

constraintFunction = [
    lambda x, y: y+9*x >= 6,
    lambda x, y: -y+9*x >= 1
]
bounds = [[0.1, 1], [0, 5]]



# constraintFunction = lambda x, y: True

salp_num = 30
iter_num = 1000
thresh = 200
mesh_div = 100
extremum = [False, False]
mcassa = MCASSA(func, bounds, constraintFunction, salp_num, iter_num, thresh, mesh_div, extremum)
pareto_in, pareto_fitness = mcassa.done()  # 经过iter_num轮迭代后，pareto边界个体
print("Pareto边界个体:", len(pareto_in), "个")
print(pareto_in)
print("-------------")
print("Pareto边界个体的适应度:")
print(np.array(pareto_fitness))

# showfitness(iter_num, np.array(pareto_fitness))
show_pareto_boundary_individual(np.array(pareto_in))
show_pareto_boundary_individual(np.array(pareto_fitness))