import random
from Person import Person
import numpy as np
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
import  plotly as py
# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import InputData as ID
import InputCrossTables as ICT
from collections import Counter

class Individual:
    def __init__(self):
        self.genelength = ID.Total;
        self.genes = self.generate();
        self.fitness = self.getFitness();

    def generate(self):
        age_samples = ID.get_weighted_samples(ID.age5ydf, self.genelength)
        sex_samples = ID.get_weighted_samples(ID.sexdf, self.genelength)
        persons = []
        for i in range(0, self.genelength):
            age = age_samples[i]
            sex = sex_samples[i]
            ethnicity = 'W1'
            religion = 'C'
            person = Person(i + 1, age=age, sex=sex, ethnicity=ethnicity, religion=religion)
            persons.append(person)
        return persons

    def getFitness(self):
        temp = []
        for gene in self.genes:
            temp.append(gene.age + " " + gene.sex)

        predicted_sex_by_age_5yrs = Counter(temp)
        actual_sex_by_age_5yrs = ICT.get_dictionary(ICT.sex_by_age_5yrs)
        predicted = []
        actual = []
        for key, value in actual_sex_by_age_5yrs.items():
            actual.append(value)
            predicted.append(predicted_sex_by_age_5yrs.get(key))
        return self.MAPE(actual, predicted)

    def setFitness(self):
        self.fitness = self.getFitness()

    def MAPE(self, actual, predicted):
        actual = np.array(actual)
        predicted = np.array(predicted)
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        return mape

    def __str__(self) -> str:
        output = ""
        for i in range(0, self.genelength):
            output += self.genes[i].__str__() + "\n"
        return  "{} | {}".format(output, self.fitness)

    def getSingleGene(self, index):
        return self.genes[index]

    def setSingleGene(self, index, value):
        self.genes[index] = value;

    def randomize(self, gene_index):
        gene = self.genes[gene_index]
        gene.age = ID.get_weighted_samples(ID.age5ydf, 1)[0]
        gene.sex = ID.get_weighted_samples(ID.sexdf, 1)[0]
        gene.ethnicity = 'W1'
        gene.religion = 'C'
        # self.fitness = self.getFitness()

# ind = Individual()
# print(ind)