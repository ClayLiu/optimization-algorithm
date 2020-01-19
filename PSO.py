import numpy as np
import math
from collections import Iterable
from Common.utils import *


class PSO:
    def __init__(self, func, dim, boundsLists, constraintFunction, v_max,  particleSum, iter_num, w=1, c1=0.2, c2=0.2):
        self.v_max = v_max
        self.dimension = len(boundsList)
        self.constraintFunction = constraintFunction
        self.func = func
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.particleSum = particleSum
        self.iter_num = iter_num
        self.boundsLists = boundsLists
        self.position = np.zeros([self.particleSum, self.dimension])
        self.velocity = np.zeros([self.particleSum, self.dimension])
        self.pbest = np.zeros([self.particleSum, self.dimension])
        self.gbest = np.zeros([1, self.dimension])
        self.init_Population()

    def init_Population(self):
        a = []
        for item in self.boundsLists:
            if isinstance(item, int):
                _a = np.full((self.particleSum, 1), item)
            else:
                _a = np.random.rand(self.particleSum, 1) * (item[1] - item[0]) + item[0]
            a.append(_a)
        self.position = np.concatenate(tuple(a), axis=1)
        self.velocity = np.random.rand(*self.position.shape) * self.v_max
        self.pbest = self.position.copy()
        self.gbest = min(self.pbest, key=lambda particle: self.func(*particle)).copy()

    def generate_particle(self):
        while True:
            singleParticlePosition = []
            for index, dimensionBounds in enumerate(self.boundsLists):
                if isinstance(dimensionBounds, int):
                    singleParticlePosition.append(dimensionBounds)
                else:
                    singleParticlePosition.append(np.random.rand()*(dimensionBounds[Bounds.upper.value] - dimensionBounds[Bounds.lower.value]) + dimensionBounds[Bounds.lower.value])
            try:
                inspectors(singleParticlePosition, self.boundsLists, self.constraintFunction)
            except IllegalVariableError as e:
                continue
            except ViolatedConstraintError as e:
                continue
            break
        return singleParticlePosition

    def get_fitness(self):
        return np.array([self.func(*position) for position in self.position])

    def update_position(self):

        for index, item in enumerate(self.position):
            self.velocity[index] = self.w * self.velocity[index] + \
                                   self.c1 * np.random.random() * (self.pbest[index] - self.position[index]) + \
                                   self.c2 * np.random.random() * (self.gbest - self.position[index])

            self.position[index] = self.position[index] + self.velocity[index]

            for i, var in enumerate(item):
                if isinstance(self.boundsLists[i], Iterable):
                    if var < self.boundsLists[i][0]:
                        self.position[index][i] = self.boundsLists[i][0]
                    elif var > self.boundsLists[i][1]:
                        self.position[index][i] = self.boundsLists[i][1]
                elif var != self.boundsLists[i]:
                    self.position[index][i] = self.boundsLists[i]

    def update_best(self):
        global_best_fitness = self.func(*self.gbest)
        person_best_value = np.array([self.func(*particle) for particle in self.pbest])

        for index, particle in enumerate(self.position):
            current_particle_fitness = self.func(*particle)

            if current_particle_fitness < person_best_value[index]:
                person_best_value[index] = current_particle_fitness
                self.pbest[index] = particle.copy()
            if current_particle_fitness < global_best_fitness:
                global_best_fitness = current_particle_fitness
                self.gbest = particle.copy()

    def pso(self):
        self.update_position()
        self.update_best()

    def info(self):
        pass

    def iterator(self):
        for _ in range(self.iter_num):
            self.pso()
            print(self.gbest, func(*self.gbest))


boundsList = ((-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi))

objectiveFunction = lambda x, y: x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)

constraintFunction = lambda x, y: True

pso = PSO(objectiveFunction, boundsList, constraintFunction, 0.5,  1000, 1000, w=1, c1=0.2, c2=0.2)

pso.iterator()