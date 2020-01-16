import numpy as np
import pareto


def init_salp(salp_num, bounds):
    # 根据区间随机生成个体
    a = []
    ub = []
    lb = []
    for i, item in enumerate(bounds):
        if isinstance(item, int):
            _a = np.full((salp_num, 1), item)
            ub.append(item)
            lb.append(item)
        else:
            _a = np.random.rand(salp_num, 1) * (item[1] - item[0]) + item[0]
            ub.append(item[1])
            lb.append(item[0])
        a.append(_a)
    position = np.concatenate(tuple(a), axis=1)
    return position, np.array(ub), np.array(lb)


def init_archive(in_, fitness_, extremum):
    # 初始化储存库个体和储存库个体适应度
    pareto_c = pareto.Pareto_(in_, fitness_, extremum)
    curr_archiving_in, curr_archiving_fit = pareto_c.pareto()
    return curr_archiving_in.copy(), curr_archiving_fit.copy()


