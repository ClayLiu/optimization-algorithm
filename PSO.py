import numpy as np
import math
from collections import Iterable
from Common.utils import *


class PSO:
    def __init__(self, func, boundsLists, constraintFunction, velocityMax,  particleSum, iterNum, w=1, c1=0.2, c2=0.2, extremum=False):
        self.velocityMax = velocityMax
        self.dimension = len(boundsList)
        self.constraintFunction = constraintFunction
        self.func = func
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.particleSum = particleSum
        self.iterNum = iterNum
        self.boundsLists = boundsLists
        self.particleSwarmPosition = np.zeros([self.particleSum, self.dimension])
        self.velocity = np.zeros([self.particleSum, self.dimension])
        self.particleBest = np.zeros([self.particleSum, self.dimension])
        self.globalBest = np.zeros([self.dimension])
        self.extremum = extremum
        self.init_population()

    def init_population(self):
        self.particleSwarmPosition = generate_population(self.particleSum, self.boundsLists, self.constraintFunction)
        self.velocity = np.random.rand(*self.particleSwarmPosition.shape) * self.velocityMax
        self.particleBest = self.particleSwarmPosition.copy()
        self.globalBest = self.get_global_best()

    def get_global_best(self):
        if self.extremum:
            globalBest = max(self.particleBest, key=lambda particle: self.func(*particle)).copy()
        else:
            globalBest = min(self.particleBest, key=lambda particle: self.func(*particle)).copy()
        return globalBest

    def get_fitness(self):
        return np.array([self.func(*position) for position in self.particleSwarmPosition])

    def update_position(self):
        for index, singlePosition in enumerate(self.particleSwarmPosition):
            self.velocity[index] = self.w * self.velocity[index] + \
                                   self.c1 * np.random.random() * (self.particleBest[index] - self.particleSwarmPosition[index]) + \
                                   self.c2 * np.random.random() * (self.globalBest - self.particleSwarmPosition[index])

            self.particleSwarmPosition[index] = self.particleSwarmPosition[index] + self.velocity[index]

            for i, var in enumerate(singlePosition):
                if isinstance(self.boundsLists[i], Iterable):
                    if var < self.boundsLists[i][0]:
                        self.particleSwarmPosition[index][i] = self.boundsLists[i][0]
                    elif var > self.boundsLists[i][1]:
                        self.particleSwarmPosition[index][i] = self.boundsLists[i][1]
                elif var != self.boundsLists[i]:
                    self.particleSwarmPosition[index][i] = self.boundsLists[i]

            while True:
                self.velocity[index] = self.w * self.velocity[index] + \
                                       self.c1 * np.random.random() * (self.particleBest[index] - self.particleSwarmPosition[index]) + \
                                       self.c2 * np.random.random() * (self.globalBest - self.particleSwarmPosition[index])

                position = self.particleSwarmPosition[index] + self.velocity[index]
                try:
                    inspectors(position, self.boundsLists, self.constraintFunction)
                except ViolatedConstraintError:
                    continue
                except IllegalVariableError:
                    position = self.convert_variable_to_legal(position)
                break
            return position

    def update_best(self):
        global_best_fitness = self.func(*self.globalBest)
        person_best_value = np.array([self.func(*particle) for particle in self.particleBest])

        for index, particle in enumerate(self.particleSwarmPosition):
            current_particle_fitness = self.func(*particle)

            if current_particle_fitness < person_best_value[index]:
                person_best_value[index] = current_particle_fitness
                self.particleBest[index] = particle.copy()
            if current_particle_fitness < global_best_fitness:
                global_best_fitness = current_particle_fitness
                self.globalBest = particle.copy()

    def pso(self):
        self.update_position()
        self.update_best()

    def info(self):
        pass

    def iterator(self):
        for _ in range(self.iterNum):
            self.pso()
            print(self.globalBest, func(*self.globalBest))


boundsList = ((-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi))

objectiveFunction = lambda x, y: x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)

constraintFunction = lambda x, y: True

pso = PSO(objectiveFunction, boundsList, constraintFunction, 0.5,  1000, 1000, w=1, c1=0.2, c2=0.2)

pso.iterator()