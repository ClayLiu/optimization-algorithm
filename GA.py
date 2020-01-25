import math
import numpy as np
from Common.utils import *
from GAutils.encode import *
from GAutils.decode import *
import random


class GA:
    # 种群的设计
    def __init__(self, populationSize, crossoverProbability, mutatioProbability, generationNum,
                 decimalDigits, objectiveFunction, boundsList, constraintFunction, crossoverOperator, extremum=False):

        self.populationChromosome = []  # 种群的染色体,字符串形式存储
        self.populationNumber = []  # 种群染色体对应的数值

        self.fitness = []
        self.decimalDigits = decimalDigits
        self.objectiveFunction = objectiveFunction
        self.boundsList = boundsList
        self.constraintFunction = constraintFunction
        self.extremum = extremum
        self.populationSize = populationSize
        self.crossoverProbability = crossoverProbability
        self.mutationProbability = mutatioProbability
        self.generationNum = generationNum
        self.fitness = np.array([])
        self.populationSurvivalProbability = np.array([])
        self.bestIndividual = []
        self.crossoverOperator = crossoverOperator
        self.init_population()

    def init_population(self):
        self.populationNumber = generate_population(self.populationSize, self.boundsList, self.constraintFunction)
        for individual in self.populationNumber:
            self.populationChromosome.append(grayEncodeForList(individual, self.boundsList, decimalDigits=6))
        self.evaluate()
        print(self.populationChromosome)

    def get_fitness(self):
        return np.array([self.objectiveFunction(*position) for position in self.populationNumber])

    def evaluate(self):
        """用于评估种群中每个个体的适应度并计算出生存概率"""
        self.fitness = self.get_fitness()
        fitnessTotal = np.sum(self.fitness)

        self.populationSurvivalProbability = []
        for fitness in self.fitness:
            self.populationSurvivalProbability.append(fitness / fitnessTotal)

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

    def and_or_crossover(self, chrom1, chrom2):
        chromosome1, chromosome2 = chrom1, chrom2
        if chrom1 != chrom2 and np.random.random() < self.crossoverProbability:
            chrom1, chrom2 = binarystring_to_number(chrom1), binarystring_to_number(chrom2)
            chromosome1, chromosome2 = chrom1 & chrom2, chrom1 | chrom2
        return chromosome1, chromosome2

    # 单，多点变异
    def mutate(self, chrom, points):
        if np.random.random() < self.mutationProbability:
            chromosome = ""
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
        self.bestIndividual.append(np.argmax(self.fitness))

    def correct_individual(self, individual):
        individualNumber = []
        for chrom in individual:
            individualNumber.append(binarystring_to_number(chrom))

        individualNumber = grayDecodeFromList(individualNumber, self.boundsList, self.decimalDigits)
        inspectors(individualNumber, self.boundsList, self.constraintFunction)

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

            for i, bounds in enumerate(boundsList):

                if not isinstance(bounds, int):
                    # 交叉
                    chrom1, chrom2 = self.point_crossover(self.populationChromosome[idv1][i], self.populationChromosome[idv2][i], 2)
                    # 变异
                    chrom1, chrom2 = self.mutate(chrom1, 1), self.mutate(chrom2, 1)

                else:
                    # 区间为一个整数，则不作处理
                    chrom1, chrom2 = self.populationChromosome[idv1][i], self.populationChromosome[idv2][i]

                newIndividuals[0].append(chrom1)
                newIndividuals[1].append(chrom2)

            # TO-DO 上下限控制
            for newIndividual in newIndividuals:
                numberList = chromList_to_numberList(newIndividual, self.boundsList, self.decimalDigits)
                try:
                    inspectors(numberList, self.boundsList, self.constraintFunction)
                except ViolatedConstraintError:
                    continue
                except IllegalVariableError:
                    numberList = convert_position_to_legal(numberList, self.boundsList)
                chromList = numberList_to_chromList(numberList, self.boundsList, self.decimalDigits)
                legalIndividuals.append(chromList)

            for legalIndividual in legalIndividuals:
                newPopulation.append(legalIndividual)

            individualNumber = individualNumber + len(legalIndividuals)
            if individualNumber >= self.populationSize:
                break

        # 保留最佳个体
        self.retained_best_individual()

        # 更新换代：用种群进化生成的新个体集合 self.new_individuals 替换当前个体集合

        self.populationChromosome = newPopulation
        self.populationNumber = []
        for chromosome in self.populationChromosome:
            self.populationNumber.append(grayDecodeFromList(chromList_to_numberList(chromosome), self.boundsList, self.decimalDigits))

    def run(self):
        for i in range(self.generationNum):
            self.evolve()
            print(i, max(self.fitness))


boundsList = ((-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi))

objectiveFunction = lambda x, y: x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)

constraintFunction = lambda x, y: True


# 种群的个体数量为 50，染色体长度为 25，交叉概率为 0.8，变异概率为 0.1,进化最大世代数为 150
pop = GA(30, 0.8, 0.1, 150, 6, objectiveFunction, boundsList, constraintFunction, "point_crossover", extremum=False)
pop.run()
