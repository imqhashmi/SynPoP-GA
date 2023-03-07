import random
import numpy
from Person import Person
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import InputData as ID
import InputCrossTables as ICT
from collections import Counter
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import  plotly as py
import plotly.express as px

class Individual:
    def __init__(self):
        self.genelength = ID.Total;
        self.genes = self.generateAll();
        self.fitness = self.getFitness();

    def generate(self, id):
        # age_samples = ID.get_weighted_samples(ID.age5ydf, self.genelength)
        # sex_samples = ID.get_weighted_samples(ID.sexdf, self.genelength)
        ages = ['0-4', ' 5-7', ' 8-9', ' 10-14', '15', ' 16-17', ' 18-19', ' 20-24', ' 25-29', ' 30-34', ' 35-39', ' 40-44', ' 45-49', ' 50-54', ' 55-59', ' 60-64', ' 65-69', ' 70-74', ' 75-79', ' 80-84', ' 85+']
        sexes = ['M', 'F']
        age = random.sample(ages, 1)[0]
        sex = random.sample(sexes, 1)[0]
        ethnicity = 'W1'
        religion = 'C'
        return Person(id, age=age, sex=sex, ethnicity=ethnicity, religion=religion)
    def generateAll(self):
        age_samples = ID.get_weighted_samples(ID.age5ydf, self.genelength)
        sex_samples = ID.get_weighted_samples(ID.sexdf, self.genelength)

        # ages = ['0-4', '5-7', '8-9', '10-14', '15', '16-17', '18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
        # sexes = ['M', 'F']

        persons = []
        for i in range(0, self.genelength):
            # age = random.sample(ages, 1)[0]
            # sex = random.sample(sexes, 1)[0]
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

        keys = ['0-4 M', '0-4 F', '5-7 M', '5-7 F', '8-9 M', '8-9 F', '10-14 M', '10-14 F', '15 M', '15 F', '16-17 M', '16-17 F', '18-19 M', '18-19 F', '20-24 M', '20-24 F', '25-29 M', '25-29 F', '30-34 M', '30-34 F', '35-39 M', '35-39 F', '40-44 M', '40-44 F', '45-49 M', '45-49 F', '50-54 M', '50-54 F', '55-59 M', '55-59 F', '60-64 M', '60-64 F', '65-69 M', '65-69 F', '70-74 M', '70-74 F', '75-79 M', '75-79 F', '80-84 M', '80-84 F', '85+ M', '85+ F']

        for key in keys:
            avalue = actual_sex_by_age_5yrs.get(key)
            pvalue = predicted_sex_by_age_5yrs.get(key)
            if pvalue==None:
                pvalue=0

            actual.append(avalue)
            predicted.append(pvalue)

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
        gene = self.generate(gene_index)

    def summary(self):
        temp = []
        for gene in self.genes:
            temp.append(gene.age + " " + gene.sex)

        predicted_sex_by_age_5yrs = Counter(temp)
        predicted = []

        keys = ['0-4 M', '0-4 F', '5-7 M', '5-7 F', '8-9 M', '8-9 F', '10-14 M', '10-14 F', '15 M', '15 F', '16-17 M',
                '16-17 F', '18-19 M', '18-19 F', '20-24 M', '20-24 F', '25-29 M', '25-29 F', '30-34 M', '30-34 F',
                '35-39 M', '35-39 F', '40-44 M', '40-44 F', '45-49 M', '45-49 F', '50-54 M', '50-54 F', '55-59 M',
                '55-59 F', '60-64 M', '60-64 F', '65-69 M', '65-69 F', '70-74 M', '70-74 F', '75-79 M', '75-79 F',
                '80-84 M', '80-84 F', '85+ M', '85+ F']

        for key in keys:
            pvalue = predicted_sex_by_age_5yrs.get(key)
            if pvalue == None:
                pvalue = 0

            print(key, pvalue)
    def plot(self):
        temp = []
        for gene in self.genes:
            temp.append(gene.age + " " + gene.sex)

        predicted_sex_by_age_5yrs = Counter(temp)
        actual_sex_by_age_5yrs = ICT.get_dictionary(ICT.sex_by_age_5yrs)

        plot = []

        keys = ['0-4 M', '0-4 F', '5-7 M', '5-7 F', '8-9 M', '8-9 F', '10-14 M', '10-14 F', '15 M', '15 F', '16-17 M',
                '16-17 F', '18-19 M', '18-19 F', '20-24 M', '20-24 F', '25-29 M', '25-29 F', '30-34 M', '30-34 F',
                '35-39 M', '35-39 F', '40-44 M', '40-44 F', '45-49 M', '45-49 F', '50-54 M', '50-54 F', '55-59 M',
                '55-59 F', '60-64 M', '60-64 F', '65-69 M', '65-69 F', '70-74 M', '70-74 F', '75-79 M', '75-79 F',
                '80-84 M', '80-84 F', '85+ M', '85+ F']

        for key in keys:
            avalue = actual_sex_by_age_5yrs.get(key)
            pvalue = predicted_sex_by_age_5yrs.get(key)
            if pvalue == None:
                pvalue = 0

            a = {'key': key, 'count': avalue, 'category': 'actual'}
            p = {'key': key, 'count': pvalue, 'category': 'predicted'}
            plot.append(a)
            plot.append(p)

        df = pd.DataFrame(plot)
        fig = px.bar(df, x="key", y="count", color="category", barmode="group")
        py.offline.plot(fig, filename="bar.html")
        fig.show()

# ind = Individual()
# ind.summary()


