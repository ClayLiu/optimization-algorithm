import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns


class image():
    def __init__(self, iterNum, fitnessList, fitnessPositoin):
        sns.set_style("whitegrid")
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.ln, = self.ax.plot([], [], animated=False)
        self.iterNum = iterNum
        self.fitnessList = fitnessList
        self.fitnessPosition = fitnessPositoin
        self.xlower = 0
        self.xupper = 0
        self.text = plt.text(self.iterNum*0.8, (self.xupper-self.xlower)*0.8, '', fontsize=10)

    def init(self):
        self.xlower = min(self.fitnessList) - 10
        self.xupper = max(self.fitnessList) + 10
        self.ax.set_xlim(0, self.iterNum)
        self.ax.set_ylim(self.xlower, self.xupper)
        self.text = plt.text(self.iterNum * 0.1, self.xupper-7, '', fontsize=10)
        return self.ln,

    def update(self, frame):
        frame = int(frame)-1
        self.xdata.append(frame)
        self.ydata.append(self.fitnessList[frame])
        self.ln.set_data(self.xdata, self.ydata)
        self.text.set_text("iterations: "+str(frame + 1) + "\n" + "fitness: " + str(self.fitnessList[frame]) + "\n" + "position: "+ self.combining_strings(self.fitnessPosition[frame]))
        return self.ln, self.text,

    def combining_strings(self, list):
        string = ""
        for i,num in enumerate(list):
            if i == len(list)-1:
                string = string + str(num)
            else:
                string = string + str(num)+", "
        return string

    def show(self):
        ani = FuncAnimation(self.fig, self.update, frames=np.linspace(1, self.iterNum, self.iterNum),
                            init_func=self.init, blit=True, interval=10, repeat=False)
        plt.show()

