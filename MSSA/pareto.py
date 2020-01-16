import numpy as np


class Pareto_:
    def __init__(self, in_data, fitness_data, extremum):
        """
        :param in_data:
        :param fitness_data:
        :param extremum:
        """
        self.in_data = in_data  # 樽海鞘群坐标信息
        self.fitness_data = fitness_data  # 樽海鞘群适应值信息
        self.cursor = -1  # 初始化游标位置
        self.len_ = in_data.shape[0]  # 樽海鞘群的数量
        self.bad_num = 0  # 非优解的个数
        self.extremum = extremum # 目标函数极值

    def next(self):
        # 将游标的位置前移一步，并返回所在检索位的樽海鞘坐标、适应值
        self.cursor = self.cursor + 1
        return self.in_data[self.cursor], self.fitness_data[self.cursor]

    def hasNext(self):
        # 判断是否已经检查完了所有个体
        return self.len_ > self.cursor + 1 + self.bad_num

    def remove(self):
        # 将非优解从数据集删除，避免反复与其进行比较。
        self.fitness_data = np.delete(self.fitness_data, self.cursor, axis=0)
        self.in_data = np.delete(self.in_data, self.cursor, axis=0)
        # 游标回退一步
        self.cursor = self.cursor - 1
        # 非优解个数，加1
        self.bad_num = self.bad_num + 1

    def pareto(self):
        while self.hasNext():
            # 获取当前位置的樽海鞘的位置和适应度
            in_curr, fitness_curr = self.next()
            # 判断当前粒子是否pareto最优
            if not self.judge(fitness_curr, self.fitness_data, self.cursor):
                self.remove()
        return self.in_data, self.fitness_data

    def judge(self, fitness_curr, fitness_data, cursor):
        # 当前樽海鞘的适应值fitness_curr与数据集fitness_data进行比较，判断是否为非劣解
        for i in range(len(fitness_data)):
            if i == cursor:
                continue
            # 如果数据集中存在一个樽海鞘可以完全支配当前解，则证明当前解为劣解，返回False
            if not self.compare(fitness_curr, fitness_data[i]):
                return False
        return True

    def compare(self, fitness_curr, fitness_ref):
        # 判断fitness_curr是否可以被fitness_ref完全支配
        for i in range(len(fitness_curr)):
            assert self.extremum[i] == "min" or self.extremum[i] == "max", "只能指定max或者min"
            if self.extremum[i] == "min":
                if fitness_curr[i] < fitness_ref[i]:
                    return True
            else:
                if fitness_curr[i] > fitness_ref[i]:
                    return True
        return False
