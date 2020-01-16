# encoding: utf-8
import numpy as np
import mssa
import visdom


fit_1 = lambda x, y: 1-np.exp(-(((x-y)**2/2)**0.5)**2/0.5)*np.exp(-((((x+y)**2/2)**0.5)-np.sqrt(200))**2/250)
fit_2 = lambda x, y: 1-np.exp(-(((x-y)**2/2)**0.5)**2/5)*np.exp(-(((x+y)**2/2)**0.5)**2/350)

func1 = lambda x, y: x ** 2 + y ** 2
func2 = lambda x, y: x ** 3 + y ** 3

func = [func1, func2]
funct = [fit_1, fit_2]
dim = 2
bounds = [[-50, 50], [-50, 50]]
salp_num = 30
iter_num = 100
thresh = 100
mesh_div = 100
extremum = ["min", "min"]
mssa = mssa.MSSA(func, dim, bounds, salp_num, iter_num, thresh, mesh_div, extremum)
pareto_in, pareto_fitness = mssa.done()  # 经过iter_num轮迭代后，pareto边界个体
print("Pareto边界个体:", pareto_in.shape[0], "个")
print(pareto_in)
print("-------------")
print("Pareto边界个体的适应度:")
print(pareto_fitness)


