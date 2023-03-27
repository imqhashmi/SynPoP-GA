from Population import Population
from Individual import Individual
import random
import plotly.express as px
import plotly as py

class GeneticAlgorithm:
    def __init__(self, popsize):
        self.uniformRate = 0.6;
        self.mutationRate = 0.9;
        self.tournamentSize = 25;
        self.elitism = True;

        self.popsize = popsize
        self.population = Population(self.popsize, isNew=True)
        self.generation_count = 1
        count=0
        while self.population.getFittest().fitness > 0:
            print("Generation: ", str(self.generation_count), " Fitness: ",  str(self.population.getFittest().fitness));
            if count%5==0:
                self.population.getFittest().plot()
            self.population = self.evolve()
            self.generation_count+=1
            count+=1
    def evolve(self):
        elitism_offset = 0
        newpopulation = Population(self.population.size, False)
        if self.elitism:
            newind = self.population.getFittest()
            newpopulation.addIndividual(newind)
            newpopulation.setGenelength(newind.genelength)
            elitism_offset = 1

        for i in range(elitism_offset, self.population.size):
            individial_1 = self.tournamentselection()
            individial_2 = self.tournamentselection()
            individual = self.crossover(individial_1, individial_2)
            newpopulation.addIndividual(individual)

        for i in range(elitism_offset, self.population.size):
           self.mutate(newpopulation.getIndividual(i))

        newpopulation.updateFitness()
        return newpopulation

    def crossover(self, ind1:Individual, ind2:Individual):
        result = Individual()
        for i in range(0, result.genelength):
            if (random.uniform(0, 1) < self.uniformRate):
                result.setSingleGene(i,ind1.getSingleGene(i))
            else:
                result.setSingleGene(i, ind2.getSingleGene(i))
        return result

    def mutate(self, individual:Individual):
        for i in range(0, individual.genelength):
            if (random.uniform(0,1) < self.mutationRate):
                individual.randomize(i)

    def tournamentselection(self):
        tournament = Population(size=self.tournamentSize, isNew=False)
        for i in range(0, self.tournamentSize):
            randomselection = random.randint(0, self.population.size-1)
            tournament.addIndividual(self.population.getIndividual(randomselection))
        fittest = tournament.getFittest()
        return fittest


g = GeneticAlgorithm(popsize=50)