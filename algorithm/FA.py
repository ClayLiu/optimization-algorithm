import math
import random
import numpy as np
from Common.EnumSet import *
from Common.for_image import get_fig
from Common.utils import *
from Exceptions.Errors import *

SUPER_HUGE_NUM = 999999999999999999999999.0

def __get_o_distance__(vector_1 : np.ndarray, vector_2 : np.ndarray):
    return np.sqrt(np.sum((vector_1 - vector_2) ** 2))

class FireflySwarm():
    def __init__(self, objectiveFunction, constraintFunction, fireflyQuantity, x_bounds_list, alpha, gamma, maximumAttractiveness):
        """
        :param objectiveFunction:       目标函数 \n
        :param constraintFunction:      约束条件函数 \n
        :param fireflyQuantity:         萤火虫个数 \n
        :param x_bounds_list:           x 在各维的取值范围 \n
        :param alpha:                   步长因子 取值范围为[0, 1] \n
        :param gamma:                   光吸收系数 取值范围为[0, 1] \n
        :param maximunAttractiveness:   最大吸引度 \n
        """
        
        self.objectiveFunction = objectiveFunction
        self.constraintFunction = constraintFunction
        self.fireflyQuantity = fireflyQuantity
        self.x_bounds_list = x_bounds_list
        self.gamma = gamma
        self.alpha = alpha

        self.fireflyPositions = generate_population(fireflyQuantity, x_bounds_list, constraintFunction)
        self.fireflyPositions_new = self.fireflyPositions.copy()
        self.fireflyBrightness = np.empty(fireflyQuantity)
        self.fireflyRelativeBrightness = np.zeros((fireflyQuantity, fireflyQuantity))
        self.fireflyDistance = np.zeros((fireflyQuantity, fireflyQuantity))

        self.relativeBrightnessFormula = lambda I, r : I * math.exp(- gamma * r)                # 相对亮度度量函数
        self.attractivenessFormula = lambda r : maximumAttractiveness * math.exp(- gamma * r)   # 吸引度计算函数

    def get_fireflyDistance(self):
        self.fireflyDistance -= self.fireflyDistance    # 全阵置零
        for i in range(0, self.fireflyQuantity - 1):
            for j in range(i + 1, self.fireflyQuantity):
                x_i = self.fireflyPositions[i]
                x_j = self.fireflyPositions[j]
                
                self.fireflyDistance[i][j] = __get_o_distance__(x_i, x_j)
        self.fireflyDistance += self.fireflyDistance.transpose()

    def get_brightness(self):
        for i, fireflyPosition in enumerate(self.fireflyPositions):
            self.fireflyBrightness[i] = self.objectiveFunction(*fireflyPosition)

    def get_relativeBrightness(self):
        """
        前提条件: brightness, distance 已更新\n
        计算相对亮度（结合亮度和距离度量）\n
        每一列为萤火虫所看到的相对亮度值\n
        结果保存至 self.fireflyRelativeBrightness\n
        """
        self.fireflyRelativeBrightness -= self.fireflyRelativeBrightness + SUPER_HUGE_NUM # 全阵置超小值
        for i in range(0, self.fireflyQuantity - 1):
            for j in range(i + 1, self.fireflyQuantity):
                firefly_i_j_distance = self.fireflyDistance[i][j]
                
                if self.fireflyBrightness[i] > self.fireflyBrightness[j]:
                    relativeBrightness = self.relativeBrightnessFormula(self.fireflyBrightness[i], firefly_i_j_distance)
                    self.fireflyRelativeBrightness[i][j] = relativeBrightness
                else:
                    relativeBrightness = self.relativeBrightnessFormula(self.fireflyBrightness[j], firefly_i_j_distance)
                    self.fireflyRelativeBrightness[j][i] = relativeBrightness
        
    def iteration(self, iter_num : int):
        best_brightness_value_history = []
        for t in range(0, iter_num + 1):
            self.get_brightness()
            self.get_fireflyDistance()
            self.get_relativeBrightness()

            best_brightness_value_history.append(np.max(self.fireflyBrightness))

            for i in range(0, self.fireflyQuantity):
                firefly_i_see = self.fireflyRelativeBrightness[:, i]
                firefly_i_see_argsorted = np.argsort(firefly_i_see)
                brightest_i_see_index = firefly_i_see_argsorted[0]  # i 所看到相对亮度最大的萤火虫的索引
                
                # 如果 i 没有看到比它更亮的，说明它是最亮的
                if self.fireflyBrightness[brightest_i_see_index] == - SUPER_HUGE_NUM:       # 最亮者，随机游走
                    self.fireflyPositions_new[i] += self.alpha * (random.random() - 0.5)
                else:                                                                               # 其他亮者，被牵着走
                    for index in firefly_i_see_argsorted:
                        if self.fireflyBrightness[index] > self.fireflyBrightness[i]:
                            attractiveness = self.attractivenessFormula(self.fireflyDistance[i][index])
                            self.fireflyPositions_new[i] += attractiveness * (self.fireflyPositions[index] - self.fireflyPositions[i]) + self.alpha * (random.random() - 0.5)
                        else:
                            break
                try:
                    inspectors(self.fireflyPositions_new[i], self.x_bounds_list, self.constraintFunction)
                except IllegalVariableError as e:
                    self.fireflyPositions_new[i] = convert_position_to_legal(self.fireflyPositions_new[i], self.x_bounds_list)
                except ViolatedConstraintError as e:
                    self.fireflyPositions_new[i] = np.array(generate_individual(self.x_bounds_list, self.constraintFunction))

            self.fireflyPositions = self.fireflyPositions_new.copy()

        self.get_brightness()
        best_brightness_value_history.append(np.max(self.fireflyBrightness))
        best_firefly_index = np.argmax(self.fireflyBrightness)
        best_position = self.fireflyPositions[best_firefly_index]
        best_brightness = self.fireflyBrightness[best_firefly_index]
        return best_position, best_brightness, best_brightness_value_history


if __name__ == '__main__':
    t2_f = lambda x, y : - (x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2))
    x_bound = [
        (-2 * math.pi, 2 * math.pi),
        (-2 * math.pi, 2 * math.pi)
    ]
    no_con = lambda x, y : True
    test = FireflySwarm(t2_f, no_con, 100, x_bound, 0.02, 1.0, 1.0)
    best_position, best_brightness, best_brightness_value_history = test.iteration(200)
    print(best_position, best_brightness)
    # print(best_brightness_value_history)
    get_fig(best_brightness_value_history, 'FA_result.png')
