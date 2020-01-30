import numpy as np
import random


class mesh_crowd(object):
    def __init__(self, curr_archiving_in, curr_archiving_fit, mesh_div, lb, ub):
        """
        :param curr_archiving_in:
        :param curr_archiving_fit:
        :param mesh_div: 等分因子
        :param lb: 目标函数下界，应传入列表[a, b, c]
        :param ub:
        """
        self.curr_archiving_in = curr_archiving_in  # 当前存档中所有的坐标
        self.curr_archiving_fit = curr_archiving_fit    # 当前存档中所有个体的适应度
        self.mesh_div = mesh_div  # 等分因子，默认值为10等分
        self.num_ = self.curr_archiving_in.shape[0]  # 存档中个体的数量
        self.id_archiving = np.zeros(self.num_)  # 各个个体的id编号，检索位与curr_archiving的检索位为相对应
        self.crowd_archiving = np.zeros(self.num_)  # 拥挤度矩阵，用于记录当前个体所在网格的总个体数，检索位与curr_archiving的检索为相对应
        self.probability_archiving = np.zeros(self.num_)  # 各个个体被选为食物源的概率，检索位与curr_archiving的检索位为相对应
        self.food_in = np.zeros((1, self.curr_archiving_in.shape[1]))  # 初始化food矩阵_坐标
        self.food_fit = np.zeros((1, self.curr_archiving_fit.shape[1]))  # 初始化food矩阵_适应值
        self.lb = lb
        self.ub = ub

    def cal_mesh_id(self, in_):
        # 计算网格编号id
        # 首先，将每个维度按照等分因子进行等分离散化，获取粒子在各维度上的编号。按照10进制将每一个维度编号等比相加（如过用户自定义了mesh_div_num的值，则按照自定义），计算出值
        id_ = 0
        for i in range(self.curr_archiving_in.shape[1]):
            id_dim = int((in_[i] - self.lb[i]) * self.mesh_div / (self.ub[i] - self.lb[i]))
            id_ = id_ + id_dim * (self.mesh_div ** i)
        return id_

    def divide_archiving(self):
        # 进行网格划分，为每个粒子定义网格编号
        for i in range(self.num_):
            self.id_archiving[i] = self.cal_mesh_id(self.curr_archiving_in[i])

    def get_crowd(self):
        index_ = (np.linspace(0, self.num_ - 1, self.num_)).tolist()  # 定义一个数组存放个体群的索引号，用于辅助计算
        index_ = list(map(int, index_))
        while len(index_) > 0:
            index_same = [index_[0]]  # 存放本次子循环中与index[0]个体具有相同网格id所有检索位
            for i in range(1, len(index_)):
                if self.id_archiving[index_[0]] == self.id_archiving[index_[i]]:
                    index_same.append(index_[i])
            number_ = len(index_same)  # 本轮网格中的总个体数
            for i in index_same:  # 更新本轮网格id下的所有个体的拥挤度
                self.crowd_archiving[i] = number_
                index_.remove(i)  # 删除本轮网格所包含的个体对应的索引号，避免重复计算


class select_food(mesh_crowd):
    def __init__(self, curr_archiving_in, curr_archiving_fit, mesh_div_num, lb, ub):
        super(select_food, self).__init__(curr_archiving_in, curr_archiving_fit, mesh_div_num, lb, ub)
        self.divide_archiving()
        self.get_crowd()

    def get_probability(self):
        self.probability_archiving = 10.0 / (self.crowd_archiving ** 3)
        self.probability_archiving = self.probability_archiving / np.sum(self.probability_archiving)  # 所有个体的被选概率的总和为1

    def select_food_index(self):
        random_pro = random.uniform(0.0, 1.0)  # 生成一个0到1之间的随机数
        for i in range(self.num_):
            if random_pro <= np.sum(self.probability_archiving[0:i + 1]):
                return i  # 返回检索值

    def select_food(self):
        self.get_probability()
        food_index = self.select_food_index()
        self.food_in = self.curr_archiving_in[food_index]
        return self.food_in.copy()


class clear_archiving(mesh_crowd):
    def __init__(self, curr_archiving_in, curr_archiving_fit, mesh_div_num, lb, ub):
        super(clear_archiving, self).__init__(curr_archiving_in, curr_archiving_fit, mesh_div_num, lb, ub)
        self.divide_archiving()
        self.get_crowd()
        self.thresh = 0

    def get_probability(self):
        self.probability_archiving = self.crowd_archiving ** 2
        self.probability_archiving = self.probability_archiving / np.sum(self.probability_archiving)

    def get_clear_index(self):  # 按概率清除个体，拥挤度高的个体被清除的概率越高
        len_clear = self.curr_archiving_in.shape[0] - self.thresh  # 需要清除掉的个体数量
        clear_index = []
        while len(clear_index) < len_clear:
            random_pro = random.uniform(0.0, 1.0)  # 生成一个0到1之间的随机数
            for i in range(self.num_):
                if random_pro <= np.sum(self.probability_archiving[0:i + 1]):
                    if i not in clear_index:
                        clear_index.append(i)  # 记录检索值
                        break
        return clear_index

    def clear_(self, thresh):
        assert thresh > 0, "储存库大小必须大于0"
        self.thresh = thresh
        self.get_probability()
        clear_index = self.get_clear_index()
        self.curr_archiving_in = np.delete(self.curr_archiving_in, clear_index, axis=0)
        self.curr_archiving_fit = np.delete(self.curr_archiving_fit, clear_index, axis=0)
        self.num_ = self.curr_archiving_in.shape[0]
        return self.curr_archiving_in.copy(), self.curr_archiving_fit.copy()
