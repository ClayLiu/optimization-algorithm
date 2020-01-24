import numpy as np
import math
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
        self.particleBestPosition = np.zeros([self.particleSum, self.dimension])
        self.globalBestPosition = np.zeros([self.dimension])
        self.extremum = extremum
        self.init_population()

    def init_population(self):
        self.particleSwarmPosition = generate_population(self.particleSum, self.boundsLists, self.constraintFunction)
        self.velocity = np.random.rand(*self.particleSwarmPosition.shape) * self.velocityMax
        self.particleBestPosition = self.particleSwarmPosition.copy()
        self.globalBestPosition = self.get_global_best_position()

    def get_global_best_position(self):
        if self.extremum:
            globalBestPosition = max(self.particleBestPosition, key=lambda particle: self.func(*particle)).copy()
        else:
            globalBestPosition = min(self.particleBestPosition, key=lambda particle: self.func(*particle)).copy()
        return globalBestPosition

    def get_all_particles_fitness(self):
        return np.array([self.func(*position) for position in self.particleSwarmPosition])

    def calculate_position_and_velocity(self, velocity, singlePosition, particleBestPosition):

        while True:
            currentVelocity = self.w * velocity + \
                                   self.c1 * np.random.random() * (
                                               particleBestPosition - singlePosition) + self.c2 * np.random.random() * (self.globalBestPosition - singlePosition)
            for i, v in enumerate(currentVelocity):
                if v > self.velocityMax:
                    currentVelocity[i] = self.velocityMax

            singleposition = singlePosition + currentVelocity


            try:
                inspectors(singleposition, self.boundsLists, self.constraintFunction)
            except ViolatedConstraintError:
                continue
            except IllegalVariableError:
                singleposition = convert_position_to_legal(singleposition, self.boundsLists)
            break

        return singleposition, currentVelocity

    def update_position(self):

        for index, singlePosition in enumerate(self.particleSwarmPosition):
            self.particleSwarmPosition[index], self.velocity[index] = self.calculate_position_and_velocity(self.velocity[index], singlePosition, self.particleBestPosition[index])


    def update_best(self):
        globalBestFitness = self.func(*self.globalBestPosition)
        personBestFitness = np.array([self.func(*particle) for particle in self.particleBestPosition])

        for index, singleParticle in enumerate(self.particleSwarmPosition):
            current_particle_fitness = self.func(*singleParticle)

            if self.extremum:
                if current_particle_fitness > personBestFitness[index]:
                    personBestFitness[index] = current_particle_fitness
                    self.particleBestPosition[index] = singleParticle.copy()
                if current_particle_fitness > globalBestFitness:
                    globalBestFitness = current_particle_fitness
                    self.globalBestPosition = singleParticle.copy()
            else:
                if current_particle_fitness < personBestFitness[index]:
                    personBestFitness[index] = current_particle_fitness
                    self.particleBestPosition[index] = singleParticle.copy()
                if current_particle_fitness < globalBestFitness:
                    globalBestFitness = current_particle_fitness
                    self.globalBestPosition = singleParticle.copy()

    def pso(self):
        self.update_position()
        self.update_best()

    def iterator(self):
        for i in range(self.iterNum):
            self.pso()

            print("正在进行第", i, "次迭代")
        print(self.globalBestPosition, self.func(*self.globalBestPosition))


boundsList = ((-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi))

objectiveFunction = lambda x, y: x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)

constraintFunction = lambda x, y: True

particleSum = 1000
iterNum = 1000


pso = PSO(objectiveFunction, boundsList, constraintFunction, 0.5,  particleSum, iterNum, w=1, c1=0.2, c2=0.2)

pso.iterator()