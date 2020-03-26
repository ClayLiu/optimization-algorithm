import numpy as np
import random
import math
import tqdm
from Exceptions.Errors import *
from Common.for_image import get_fig
from Common.utils import *
from Common.EnumSet import *

class BatSwarm():
    def __init__(self, objectiveFunction, constraintFunction, batQuantity, alpha, gamma, x_bounds_list, v_bounds_list, f_bound : tuple):
        """
        :param objectiveFunction:   目标函数 \n
        :param constraintFunction:  约束条件判断函数 \n
        :param batQuantity:         蝙蝠个数 \n
        :param alpha:               alpha常数 (0, 1) \n
        :param gamma:               gamma常数 (0, +∞) \n
        :param x_bounds_list:       x在各维度的取值范围 \n
        :param v_bounds_list:       v在各维度的取值范围 \n
        :param f_bound:             f的取值范围 \n
        """

        self.objectiveFunction = objectiveFunction
        self.constraintFunction = constraintFunction
        self.batQuantity = batQuantity
        self.x_bounds_list = x_bounds_list
        self.v_bounds_list = v_bounds_list
        self.f_bound = f_bound
        self.x_dim = len(x_bounds_list)

        self.alpha = alpha
        self.gamma = gamma

        self.batFrequecy = (np.random.random(batQuantity) * (f_bound[Bounds().upper] - f_bound[Bounds().lower])) + f_bound[Bounds().lower]
        self.batPositions = generate_population(batQuantity, x_bounds_list, constraintFunction)
        self.batNewPositions = np.empty_like(self.batPositions, dtype=np.float)
        self.batVelocitys = self.generate_velocitys(batQuantity, v_bounds_list)
        self.batPulseRate = np.random.random(batQuantity)
        self.batPulseRate_zero = self.batPulseRate.copy()
        self.batLoudness = np.ones(batQuantity, dtype=np.float)

        self.fitness = np.zeros(self.bat_num) + 1e10
    
    def generate_velocitys(self, batQuantity, boundsList):
        span = []
        lower = []
        for bound in boundsList:
            span.append(bound[Bounds().upper] - bound[Bounds().lower])
            lower.append(bound[Bounds().lower])
        
        span = np.array(span)
        lower = np.array(lower)

        velocitys = []
        for i in range(batQuantity):
            singleBatVelocity = np.random.random(self.x_dim) * span + lower
            velocitys.append(singleBatVelocity)
        
        return np.vstack(velocitys)

    def globalSearchNewPosition(self, best_position : np.ndarray, batIndex : int):
        """ 全局搜索解 """
        beta = random.random()
        frequency = self.f_bound[Bounds.lower] + (self.f_bound[Bounds.upper] - self.f_bound[Bounds.lower]) * beta
        
        self.batVelocitys[batIndex] += (self.batPositions[batIndex] - best_position) * frequency
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

    def iteration(self, iter_num : int):
        
        best_fitness_value_history = []
        
        self.get_fitness()
        best_bat_index = np.argmin(self.fitness)
        best_fitness_value_history.append(self.fitness[best_bat_index])
        best_position = self.batPositions[best_bat_index]
        print(best_position, self.fitness[best_bat_index])

        for t in tqdm.tqdm(range(1, iter_num + 1)):
            
            currentAverageLoudness = np.average(self.batLoudness)

            for i in range(self.batQuantity):
                # 产生新解
                self.globalSearchNewPosition(best_position, i)

                if random.random() > self.batPulseRate[i]:
                    self.localSearchNewPosition(currentAverageLoudness, i)

                if random.random() < self.batLoudness[i]:
                    # 判断新解是否符合约束条件
                    try:
                        inspectors(self.batNewPositions[i], self.x_bounds_list, self.constraintFunction)
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
                                best_position = self.batPositions[i]  # 改变当代最优蝙蝠，代替 迭代后再重新选出最优蝙蝠 的低效做法
                            
                            # update Loudness and PulseRate
                            self.batLoudness[i] *= self.alpha
                            self.batPulseRate[i] = self.batPulseRate_zero[i] * (1 - math.exp(- self.gamma * t))

            best_bat_index = np.argmin(self.fitness)
            best_fitness_value_history.append(self.fitness[best_bat_index])
        
        return best_position, self.fitness[best_bat_index], best_fitness_value_history
