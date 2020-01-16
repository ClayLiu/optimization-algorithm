import numpy as np
import pareto
import archiving
import math


def update_position(position, F, lb, ub, c1):
    # 更新樽海鞘群个体位置
    for j, p in enumerate(position):
        if j < position.shape[0] / 2:
            if np.random.random() >= 0.5:
                position[j] = F + c1 * ((ub - lb) * np.random.random() + lb)
            else:
                position[j] = F - c1 * ((ub - lb) * np.random.random() + lb)

        else:
            position[j, :] = 0.5 * (position[j, :] + position[j - 1, :])

        for index, var in enumerate(p):
            if var < lb[index]:
                position[j][index] = lb[index]
            elif var > ub[index]:
                position[j][index] = ub[index]
    return position.copy()


def update_c1(l, L):
    # 更新c1
    c1 = 2 * math.exp(-(4 * l / L) ** 2)
    return c1


def update_archive(in_, fitness_, archive_in, archive_fitness, thresh, mesh_div, min_, max_, extremum):
    # 首先，计算当前樽海鞘群的pareto边界，将边界个体加入到存档archive中
    pareto_1 = pareto.Pareto_(in_, fitness_, extremum)
    curr_in, curr_fit = pareto_1.pareto()

    # 其次，在存档中根据支配关系进行第二轮筛选，将非边界个体去除
    in_new = np.concatenate((archive_in, curr_in), axis=0)
    fitness_new = np.concatenate((archive_fitness, curr_fit),axis=0)
    pareto_2 = pareto.Pareto_(in_new, fitness_new, extremum)
    curr_archiving_in, curr_archiving_fit = pareto_2.pareto()

    # 最后，判断存档数量是否超过了存档阀值。如果超过了阀值，则清除掉一部分（拥挤度高的个体被清除的概率更大）
    if curr_archiving_in.shape[0] > thresh:
        clear_ = archiving.clear_archiving(curr_archiving_in, curr_archiving_fit, mesh_div, min_, max_)
        curr_archiving_in, curr_archiving_fit = clear_.clear_(thresh)
    return curr_archiving_in.copy(), curr_archiving_fit.copy()


def update_food(archiving_in, archiving_fit, mesh_div, min_, max_):
    # 更新食物源（拥挤度低的个体更容易被选中）
    get_g = archiving.select_food(archiving_in, archiving_fit, mesh_div, min_, max_)
    return get_g.select_food()
