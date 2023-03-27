from Individual import Individual
import numpy as np
import random
class Population:
    def __init__(self, size, isNew=True):
        self.size = size
        self.individuals = []
        self.genelength = 0
        randomchance = 0.5
        if isNew==True:
            for i in range(0, self.size):
                individual = Individual()
                self.individuals.append(individual)
            self.setGenelength(self.individuals[0].genelength)

    def setGenelength(self, length):
        self.genelength = length

    def addIndividual(self, ind:Individual):
        self.individuals.append(ind)

    def getIndividuals(self):
        return self.individuals

    def getIndividual(self, index):
        return self.individuals[index]

    def updateFitness(self):
        for i in range(0, self.size):
            self.individuals[i].setFitness()

    def getFittest(self):
        fittest = self.individuals[0]
        for i in range (1, self.size):
            nextindividual = self.getIndividual(i)
            if fittest.fitness >= nextindividual.fitness:
                fittest = nextindividual
        return fittest

    def print(self):
        for individual in self.individuals:
            print(individual)

# P = Population(size=5, isNew=True)
# P.print()