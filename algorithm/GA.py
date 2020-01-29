from Common.utils import *
from algorithm.GAutils.decode import Decode
from algorithm.GAutils.encode import Encode
from algorithm.GAutils.utils import *
import random
from algorithm.A import arithmetic


class GA(arithmetic):
    # 种群的设计
    def __init__(self, objectiveFunction, boundsList, constraintFunction, populationSize, generationNum,
                 extremum=False):

        super(GA, self).__init__()
        self.populationChromosome = []  # 种群的染色体,字符串形式存储
        self.populationNumber = []  # 种群染色体对应的数值

        self.fitness = []
        self.decimalDigits = float(read_config("GA", "decimalDigits"))
        self.objectiveFunction = objectiveFunction
        self.boundsList = boundsList
        self.constraintFunction = constraintFunction
        self.extremum = extremum
        self.populationSize = populationSize
        self.crossoverProbability = float(read_config("GA", "crossoverProbability"))
        self.mutationProbability = float(read_config("GA", "mutationProbability"))
        self.generationNum = generationNum
        self.fitness = np.array([])
        self.populationSurvivalProbability = np.array([])
        self.bestIndividual = []
        self.decode = Decode(self.boundsList, self.decimalDigits)
        self.encode = Encode(self.boundsList, self.decimalDigits)
        self.crossoverPointsNumber = int(read_config("GA", "crossoverPointsNumber"))
        self.mutatePointsNumber = int(read_config("GA", "mutatePointsNumber"))
        self.crossoverOperator = int(read_config("GA", "crossoverOperator"))
        self.init_population()

    def init_population(self):

        self.populationNumber = generate_population(self.populationSize, self.boundsList, self.constraintFunction)
        for individual in self.populationNumber:
            self.populationChromosome.append(self.encode.grayListEncode(individual))
        self.evaluate()
        # print(self.populationChromosome)
        # self.iterator()

    def get_fitness(self):
        return np.array([self.objectiveFunction(*position) for position in self.populationNumber])

    def evaluate(self):
        """用于评估种群中每个个体的适应度并计算出生存概率"""
        self.fitness = self.get_fitness()
        self.populationSurvivalProbability = []
        if self.extremum:
            fitnessTotal = np.sum(self.fitness)
            for fitness in self.fitness:
                self.populationSurvivalProbability.append(fitness / fitnessTotal)
        else:
            fitnessTotal = np.sum(1 / self.fitness)
            for fitness in self.fitness:
                self.populationSurvivalProbability.append((1 / fitness) / fitnessTotal)

    # 轮盘赌博机（选择）
    def roulette_wheel_selection(self):
        r, i, probabilitySum = np.random.random(), 0, 0
        for survivalProbability in self.populationSurvivalProbability:
            if probabilitySum > r:
                return i
            else:
                probabilitySum = probabilitySum + survivalProbability
                i = i + 1
        return i-1

    def point_crossover(self, chrom1, chrom2, points):
        """随机单、多点交叉"""
        chromosome1, chromosome2 = chrom1, chrom2
        if chrom1 != chrom2 and np.random.random() < self.crossoverProbability:
            chromosome1, chromosome2 = "", ""
            chromLength = len(chrom1)

            # 生成随机不重复升序排列切点列表，首端为0
            pointsList = random.sample(range(1, chromLength + 1), points)
            pointsList.append(0)
            pointsList.append(chromLength + 1)
            pointsList.sort()

            for i, point in enumerate(pointsList):
                if i != 0:
                    if i % 2 == 0:
                        chromosome1 = chromosome1 + shear(chrom2, pointsList[i-1], point)
                        chromosome2 = chromosome2 + shear(chrom1, pointsList[i-1], point)
                    else:
                        chromosome1 = chromosome1 + shear(chrom1, pointsList[i-1], point)
                        chromosome2 = chromosome2 + shear(chrom2, pointsList[i-1], point)

        return chromosome1, chromosome2

    def and_or_crossover(self, chrom1, chrom2, intervalLength):
        chromosome1, chromosome2 = chrom1, chrom2
        if chrom1 != chrom2 and np.random.random() < self.crossoverProbability:
            chrom1, chrom2 = self.encode.binstr_to_num(chrom1), self.encode.binstr_to_num(chrom2)
            chromosome1, chromosome2 = chrom1 & chrom2, chrom1 | chrom2
            chromosome1, chromosome2 = self.encode.num_to_binstr(chromosome1), self.encode.num_to_binstr(chromosome2)
            chromosome1, chromosome2 = self.encode.fill_zeros(chromosome1, intervalLength), self.encode.fill_zeros(chromosome2, intervalLength)
        return chromosome1, chromosome2

    # 单，多点变异
    def mutate(self, chrom, points):
        if np.random.random() < self.mutationProbability:
            chromLength = len(chrom)
            pointsList = random.sample(range(1, chromLength + 1), points)

            for point in pointsList:
                if chrom[point-1] == "1":
                    chrom = chrom[0:point - 1] + "0" + chrom[point:]
                else:
                    chrom = chrom[0:point - 1] + "1" + chrom[point:]
        return chrom

    # 保留最佳个体
    def retained_best_individual(self):
        if self.extremum:
            self.bestIndividual.append(self.fitness[np.argmax(self.fitness)])
        else:
            self.bestIndividual.append(self.fitness[np.argmin(self.fitness)])

    # 进化过程
    def evolve(self):
        newPopulation = []
        self.evaluate()
        individualNumber = 0
        while True:
            newIndividuals = [[], []]
            legalIndividuals = []
            # 选择两个个体，进行交叉与变异，产生新的种群
            idv1 = self.roulette_wheel_selection()
            idv2 = self.roulette_wheel_selection()

            for i, bounds in enumerate(self.boundsList):

                if not isinstance(bounds, int):
                    # 交叉
                    if self.crossoverOperator == 0:
                        chrom1, chrom2 = self.point_crossover(self.populationChromosome[idv1][i], self.populationChromosome[idv2][i], self.crossoverPointsNumber)
                    elif self.crossoverOperator == 1:
                        chrom1, chrom2 = self.and_or_crossover(self.populationChromosome[idv1][i], self.populationChromosome[idv2][i], self.crossoverPointsNumber)
                    # 变异
                    chrom1, chrom2 = self.mutate(chrom1, 1), self.mutate(chrom2, self.mutatePointsNumber)

                else:
                    # 区间为一个整数，则不作处理
                    chrom1, chrom2 = self.populationChromosome[idv1][i], self.populationChromosome[idv2][i]

                newIndividuals[0].append(chrom1)
                newIndividuals[1].append(chrom2)

            # 上下限控制
            for newIndividual in newIndividuals:
                numberList = self.decode.grayListDecode(newIndividual)
                try:
                    inspectors(numberList, self.boundsList, self.constraintFunction)
                except ViolatedConstraintError:
                    continue
                except IllegalVariableError:
                    numberList = convert_position_to_legal(numberList, self.boundsList)
                # print(numberList)
                # print(self.boundsList)
                chromList = self.encode.grayListEncode(numberList)
                legalIndividuals.append(chromList)

            for legalIndividual in legalIndividuals:
                newPopulation.append(legalIndividual)

            individualNumber = individualNumber + len(legalIndividuals)
            if individualNumber >= self.populationSize:
                break

        # 保留最佳个体
        self.retained_best_individual()

        # 更新换代：用种群进化生成的新个体集合 self.new_individuals 替换当前个体集合
        self.populationChromosome = newPopulation.copy()
        self.populationNumber = []
        for chromosome in self.populationChromosome:
            self.populationNumber.append(self.decode.grayListDecode(chromosome))

    def iterator(self):
        for i in range(self.generationNum):
            self.evolve()
            # print(np.min(self.fitness))

        # print()
        print("GA:", np.min(self.bestIndividual))

#
# boundsList = ((-2, 2), (-2, 2))
#
# # objectiveFunction = lambda x, y: 20 + x**2 + y**2 - 10*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y))
#
# objectiveFunction = lambda x, y: x**2 + y**2
#
# constraintFunction = lambda x, y: True
#
# populationSize = 100
# generationNum = 100
#
# # 交叉方式 0/1 -> point_crossover/and_or_crossover，交叉基因点位数量，变异基因点位数量
# pop = GA(objectiveFunction, boundsList, constraintFunction, populationSize, generationNum, extremum=False)
# pop.iterator()
