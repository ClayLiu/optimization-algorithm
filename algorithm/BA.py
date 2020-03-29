import numpy as np
import random
import math
from Exceptions.Errors import *
from Common.showUtils import image
from Common.utils import *
from Common.EnumSet import *
from algorithm.arithmetic import arithmetic
from prettytable import PrettyTable

class BatSwarm(arithmetic):
    def __init__(self, objectiveFunction, boudsList, constraintFunction, batSum, iterNum, extremum = False):
        """
        :param objectiveFunction:   目标函数 \n
        :param constraintFunction:  约束条件判断函数 \n
        :param batSum:              蝙蝠个数 \n
        :param boudsList:           x在各维度的取值范围 \n
        """

        self.objectiveFunction = objectiveFunction
        self.constraintFunction = constraintFunction
        self.batSum = batSum
        self.boudsList = boudsList
        self.x_dim = len(boudsList)
        self.iterNum = iterNum
        self.extremum = extremum

        # 超参数
        self.alpha = 0.9        # alpha常数 (0, 1) 
        self.gamma = 0.9        # gamma常数 (0, +∞) 
        self.f_bound = (0, 1)   # 频率范围
        self.v_bounds_list = [(-1, 1)] * self.x_dim


        self.batFrequecy = (np.random.random(batSum) * (f_bound[Bounds().upper] - f_bound[Bounds().lower])) + f_bound[Bounds().lower]
        self.batPositions = generate_population(batSum, boudsList, constraintFunction)
        self.batNewPositions = np.empty_like(self.batPositions, dtype=np.float)
        self.batVelocitys = self.generate_velocitys(batSum, v_bounds_list)
        self.batPulseRate = np.random.random(batSum)
        self.batPulseRate_zero = self.batPulseRate.copy()
        self.batLoudness = np.ones(batSum, dtype=np.float)

        self.fitness = np.zeros(self.bat_num) + 1e10
    
    def generate_velocitys(self, batSum, boundsList):
        span = []
        lower = []
        for bound in boundsList:
            span.append(bound[Bounds().upper] - bound[Bounds().lower])
            lower.append(bound[Bounds().lower])
        
        span = np.array(span)
        lower = np.array(lower)

        velocitys = []
        for i in range(batSum):
            singleBatVelocity = np.random.random(self.x_dim) * span + lower
            velocitys.append(singleBatVelocity)
        
        return np.vstack(velocitys)

    def globalSearchNewPosition(self, self.best_position : np.ndarray, batIndex : int):
        """ 全局搜索解 """
        beta = random.random()
        frequency = self.f_bound[Bounds.lower] + (self.f_bound[Bounds.upper] - self.f_bound[Bounds.lower]) * beta
        
        self.batVelocitys[batIndex] += (self.batPositions[batIndex] - self.best_position) * frequency
        self.batNewPositions[batIndex] = self.batVelocitys[batIndex] + self.batPositions[batIndex]

    def localSearchNewPosition(self, AverageLoudness, batIndex):
        """ 蝙蝠局部游走 """
        # eps 取值在 [-1, 1] 间的随机数
        # eps = (random.random() * 2 - 1)           # 同一随机数
        eps = np.random.random(self.x_dim) * 2 - 1  # 不同一随机数
        self.batNewPositions[batIndex] = self.batPositions[batIndex] + eps * AverageLoudness
        
    def get_fitness(self):
        for batPosition in self.batPositions:
            self.fitness[i] = self.objectiveFunction(*batPosition)
        
        if self.extremum:   # 若为求最大值，则把适应度转为求最小化
            self.fitness = - self.fitness

    def iterator(self):
        
        self.fitnessList = []
        self.fitnessPosition = []

        self.get_fitness()
        best_bat_index = np.argmin(self.fitness)
        self.fitnessList.append(self.fitness[best_bat_index])
        self.best_position = self.batPositions[best_bat_index]
        

        for t in range(1, self.iterNum + 1):
            
            currentAverageLoudness = np.average(self.batLoudness)

            for i in range(self.batSum):
                # 产生新解
                self.globalSearchNewPosition(self.best_position, i)

                if random.random() > self.batPulseRate[i]:
                    self.localSearchNewPosition(currentAverageLoudness, i)

                if random.random() < self.batLoudness[i]:
                    # 判断新解是否符合约束条件
                    try:
                        inspectors(self.batNewPositions[i], self.boudsList, self.constraintFunction)
                    except IllegalVariableError as e:
                        continue
                    except ViolatedConstraintError as e:
                        continue
                    else:
                        # 新解满足约束条件
                        new_fitness = self.objectiveFunction(*self.batNewPositions[i])
                        if new_fitness < self.fitness[i]:
                            self.fitness[i] = new_fitness
                            self.batPositions[i] = self.batNewPositions[i]  # 接受新解
                            
                            if new_fitness < self.fitness[best_bat_index]:
                                best_bat_index = i
                                self.best_position = self.batPositions[i]  # 改变当代最优蝙蝠，代替 迭代后再重新选出最优蝙蝠 的低效做法
                            
                            # update Loudness and PulseRate
                            self.batLoudness[i] *= self.alpha
                            self.batPulseRate[i] = self.batPulseRate_zero[i] * (1 - math.exp(- self.gamma * t))

            best_bat_index = np.argmin(self.fitness)

            self.fitnessList.append(self.fitness[best_bat_index])
            self.fitnessPosition.append(self.best_position)
        

    def show(self):
        print()
        tb = PrettyTable()
        tb.field_names = ["algorithm name", "iterations", "Optimal solution", "optimal value"]
        tb.add_row(["BA", self.iterNum, self.best_position, self.objectiveFunction(*self.best_position)])
        print(tb)