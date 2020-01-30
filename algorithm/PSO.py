import math
from Common.utils import *
import numpy as np
from algorithm.A import arithmetic


class PSO(arithmetic):
    def __init__(self, objectiveFunction, boundsLists, constraintFunction, particleSum, iterNum, extremum=False):
        self.dimension = len(boundsLists)
        self.constraintFunction = constraintFunction
        self.objectiveFunction = objectiveFunction
        self.particleSum = particleSum
        self.iterNum = iterNum
        self.boundsLists = boundsLists
        self.particleSwarmPosition = np.zeros([self.particleSum, self.dimension])
        self.velocity = np.zeros([self.particleSum, self.dimension])
        self.particleBestPosition = np.zeros([self.particleSum, self.dimension])
        self.globalBestPosition = np.zeros([self.dimension])
        self.extremum = extremum
        self.c1 = float(read_config("PSO", "c1"))
        self.c2 = float(read_config("PSO", "c2"))
        self.w = float(read_config("PSO", "w"))
        self.velocityMax = float(read_config("PSO", "velocityMax"))
        self.init_population()

    def init_population(self):
        self.particleSwarmPosition = np.array(generate_population(self.particleSum, self.boundsLists, self.constraintFunction))
        self.velocity = np.random.rand(self.particleSum, self.dimension) * self.velocityMax
        self.particleBestPosition = self.particleSwarmPosition.copy()
        self.globalBestPosition = self.get_global_best_position()
        # self.iterator()

    def get_global_best_position(self):
        if self.extremum:
            globalBestPosition = max(self.particleBestPosition, key=lambda particle: self.objectiveFunction(*particle)).copy()
        else:
            globalBestPosition = min(self.particleBestPosition, key=lambda particle: self.objectiveFunction(*particle)).copy()
        return globalBestPosition

    def get_all_particles_fitness(self):
        return np.array([self.objectiveFunction(*position) for position in self.particleSwarmPosition])

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
        globalBestFitness = self.objectiveFunction(*self.globalBestPosition)
        personBestFitness = np.array([self.objectiveFunction(*particle) for particle in self.particleBestPosition])

        for index, singleParticle in enumerate(self.particleSwarmPosition):
            current_particle_fitness = self.objectiveFunction(*singleParticle)

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

            # print("正在进行第", i, "次迭代")

        print("PSO", self.globalBestPosition, self.objectiveFunction(*self.globalBestPosition))

# boundsList = ((-2*math.pi, 2*math.pi), (-2*math.pi, 2*math.pi))
#
# objectiveFunction = lambda x, y: x**2 + y**2 + 25 * (math.sin(x) ** 2 + math.sin(y) ** 2)
#
# constraintFunction = lambda x, y: True
#
# particleSum = 1000
# iterNum = 1000
#
# pso = PSO(objectiveFunction, boundsList, constraintFunction,  particleSum, iterNum, extremum=False)
#
# pso.iterator()