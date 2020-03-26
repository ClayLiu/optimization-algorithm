from MultiobjectiveUtils import pareto


def init_archive(in_, fitness_, extremum):
    # 初始化储存库个体和储存库个体适应度
    pareto_c = pareto.Pareto_(in_, fitness_, extremum)
    curr_archiving_in, curr_archiving_fit = pareto_c.pareto()
    return curr_archiving_in.copy(), curr_archiving_fit.copy()
