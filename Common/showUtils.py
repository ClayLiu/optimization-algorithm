import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import FuncAnimation


# def update_points(num):
#     '''
#     更新数据点
#     '''
#     point_ani.set_data(x[num], num)
#     return point_ani,

# x = np.linspace(0, 2 * np.pi, 100)
# y = np.sin(x)
#
# fig = plt.figure(tight_layout=True)
# plt.plot(x, y)
# point_ani, = plt.plot(x[0], y[0], "ro")
# plt.grid(ls="--")
# # 开始制作动画
# ani = animation.FuncAnimation(fig, update_points, np.arange(0, 100), interval=100, blit=True)
#
# # ani.save('sin_test2.gif', writer='imagemagick', fps=10)
# plt.show()

# def show(boundsList,iterNum):
from Common.EnumSet import *


class image():
    def __init__(self, boundsList, iterNum):
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.ln, = self.ax.plot([], [], 'r-', animated=False)
        self.boundsList = boundsList
        self.dimension = len(boundsList)
        self.iterNum = iterNum

    def init(self):
        self.ax.set_xlim(self.boundsList[0][0], self.boundsList[0][1])
        self.ax.set_ylim(self.boundsList[1][0], self.boundsList[1][1])
        return self.ln,

    def update(self, frame):
        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.ln.set_data(self.xdata, self.ydata)
        return self.ln,

    def show(self, updateFunc):
        ani = FuncAnimation(self.fig, updateFunc, frames=np.linspace(0, self.iterNum),
                            init_func=self.init, blit=True)
        plt.show()

