import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt


# def showfitness(iterNum, fitnessList):
#     x = range(1, iterNum + 1)
#     fig = plt.figure()
#
#     for i in range(2):
#         plt.plot(x, fitnessList[:, i])
#
#     plt.show()

def show_pareto_boundary_individual(positionList):
    plt.scatter(positionList[:, 0], positionList[:, 1])
    plt.show()

