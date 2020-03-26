from multiprocessing import Pool
from multiprocessing import Process
import os, time, random
import register
from algorithm.arithmetic import arithmetic
import math


def wrap(algorithmClass, objectiveFunction, boundsList, constraintFunction, populationSum, iterNum, extremum=False):
    a = algorithmClass(objectiveFunction, boundsList, constraintFunction, populationSum, iterNum, extremum)
    a.iterator()
    a.show()


class calculation:
    def __init__(self, objectiveFunction, boundsList, constraintFunction, populationSum, iterNum, extremum=False):
        self.objectiveFunction = objectiveFunction
        self.boundsList = boundsList
        self.constraintFunction = constraintFunction
        self.populationSum = populationSum
        self.iterNum = iterNum
        self.extremum = extremum
        self.processNum = len(arithmetic.__subclasses__())

    def run(self):
        for algorithmClass in arithmetic.__subclasses__():
            Process(target=wrap, args=(algorithmClass, self.objectiveFunction, self.boundsList, self.constraintFunction, self.populationSum, self.iterNum, self.extremum,)).start()
