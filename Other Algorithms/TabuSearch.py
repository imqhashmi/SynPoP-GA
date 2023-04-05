import random
import InputData as ID
import InputCrossTables as ICT
from Person import Person
from collections import Counter
import numpy as np
import plotly.graph_objs as go
import  plotly as py
import plotly.express as px

class TabuSearch:
    def __init__(self):
        self.population_size = ID.Total
        self.tabu_list_size = 1000
        self.num_iterations = 1000

        self.rsamples = ICT.get_weighted_samples(ICT.religion_by_sex_by_age, self.population_size)
        self.esamples = ID.get_weighted_samples(ID.ethnicdf, self.population_size)
        self.ssamples = ICT.get_weighted_samples(ICT.marital_by_sex_by_age, self.population_size)
        self.qsamples = ICT.get_weighted_samples(ICT.qualification_by_sex_by_age, self.population_size)

        self.Rkeys = ['M 0-4 C', 'M 0-4 B', 'M 0-4 H', 'M 0-4 J', 'M 0-4 M', 'M 0-4 S', 'M 0-4 OR', 'M 0-4 NR', 'M 0-4 NS', 'M 5-7 C', 'M 5-7 B', 'M 5-7 H', 'M 5-7 J', 'M 5-7 M', 'M 5-7 S', 'M 5-7 OR', 'M 5-7 NR', 'M 5-7 NS', 'M 8-9 C', 'M 8-9 B', 'M 8-9 H', 'M 8-9 J', 'M 8-9 M', 'M 8-9 S', 'M 8-9 OR', 'M 8-9 NR', 'M 8-9 NS', 'M 10-14 C', 'M 10-14 B', 'M 10-14 H', 'M 10-14 J', 'M 10-14 M', 'M 10-14 S', 'M 10-14 OR', 'M 10-14 NR', 'M 10-14 NS', 'M 15 C', 'M 15 B', 'M 15 H', 'M 15 J', 'M 15 M', 'M 15 S', 'M 15 OR', 'M 15 NR', 'M 15 NS', 'M 16-17 C', 'M 16-17 B', 'M 16-17 H', 'M 16-17 J', 'M 16-17 M', 'M 16-17 S', 'M 16-17 OR', 'M 16-17 NR', 'M 16-17 NS', 'M 18-19 C', 'M 18-19 B', 'M 18-19 H', 'M 18-19 J', 'M 18-19 M', 'M 18-19 S', 'M 18-19 OR', 'M 18-19 NR', 'M 18-19 NS', 'M 20-24 C', 'M 20-24 B', 'M 20-24 H', 'M 20-24 J', 'M 20-24 M', 'M 20-24 S', 'M 20-24 OR', 'M 20-24 NR', 'M 20-24 NS', 'M 25-29 C', 'M 25-29 B', 'M 25-29 H', 'M 25-29 J', 'M 25-29 M', 'M 25-29 S', 'M 25-29 OR', 'M 25-29 NR', 'M 25-29 NS', 'M 30-34 C', 'M 30-34 B', 'M 30-34 H', 'M 30-34 J', 'M 30-34 M', 'M 30-34 S', 'M 30-34 OR', 'M 30-34 NR', 'M 30-34 NS', 'M 35-39 C', 'M 35-39 B', 'M 35-39 H', 'M 35-39 J', 'M 35-39 M', 'M 35-39 S', 'M 35-39 OR', 'M 35-39 NR', 'M 35-39 NS', 'M 40-44 C', 'M 40-44 B', 'M 40-44 H', 'M 40-44 J', 'M 40-44 M', 'M 40-44 S', 'M 40-44 OR', 'M 40-44 NR', 'M 40-44 NS', 'M 45-49 C', 'M 45-49 B', 'M 45-49 H', 'M 45-49 J', 'M 45-49 M', 'M 45-49 S', 'M 45-49 OR', 'M 45-49 NR', 'M 45-49 NS', 'M 50-54 C', 'M 50-54 B', 'M 50-54 H', 'M 50-54 J', 'M 50-54 M', 'M 50-54 S', 'M 50-54 OR', 'M 50-54 NR', 'M 50-54 NS', 'M 55-59 C', 'M 55-59 B', 'M 55-59 H', 'M 55-59 J', 'M 55-59 M', 'M 55-59 S', 'M 55-59 OR', 'M 55-59 NR', 'M 55-59 NS', 'M 60-64 C', 'M 60-64 B', 'M 60-64 H', 'M 60-64 J', 'M 60-64 M', 'M 60-64 S', 'M 60-64 OR', 'M 60-64 NR', 'M 60-64 NS', 'M 65-69 C', 'M 65-69 B', 'M 65-69 H', 'M 65-69 J', 'M 65-69 M', 'M 65-69 S', 'M 65-69 OR', 'M 65-69 NR', 'M 65-69 NS', 'M 70-74 C', 'M 70-74 B', 'M 70-74 H', 'M 70-74 J', 'M 70-74 M', 'M 70-74 S', 'M 70-74 OR', 'M 70-74 NR', 'M 70-74 NS', 'M 75-79 C', 'M 75-79 B', 'M 75-79 H', 'M 75-79 J', 'M 75-79 M', 'M 75-79 S', 'M 75-79 OR', 'M 75-79 NR', 'M 75-79 NS', 'M 80-84 C', 'M 80-84 B', 'M 80-84 H', 'M 80-84 J', 'M 80-84 M', 'M 80-84 S', 'M 80-84 OR', 'M 80-84 NR', 'M 80-84 NS', 'M 85+ C', 'M 85+ B', 'M 85+ H', 'M 85+ J', 'M 85+ M', 'M 85+ S', 'M 85+ OR', 'M 85+ NR', 'M 85+ NS', 'F 0-4 C', 'F 0-4 B', 'F 0-4 H', 'F 0-4 J', 'F 0-4 M', 'F 0-4 S', 'F 0-4 OR', 'F 0-4 NR', 'F 0-4 NS', 'F 5-7 C', 'F 5-7 B', 'F 5-7 H', 'F 5-7 J', 'F 5-7 M', 'F 5-7 S', 'F 5-7 OR', 'F 5-7 NR', 'F 5-7 NS', 'F 8-9 C', 'F 8-9 B', 'F 8-9 H', 'F 8-9 J', 'F 8-9 M', 'F 8-9 S', 'F 8-9 OR', 'F 8-9 NR', 'F 8-9 NS', 'F 10-14 C', 'F 10-14 B', 'F 10-14 H', 'F 10-14 J', 'F 10-14 M', 'F 10-14 S', 'F 10-14 OR', 'F 10-14 NR', 'F 10-14 NS', 'F 15 C', 'F 15 B', 'F 15 H', 'F 15 J', 'F 15 M', 'F 15 S', 'F 15 OR', 'F 15 NR', 'F 15 NS', 'F 16-17 C', 'F 16-17 B', 'F 16-17 H', 'F 16-17 J', 'F 16-17 M', 'F 16-17 S', 'F 16-17 OR', 'F 16-17 NR', 'F 16-17 NS', 'F 18-19 C', 'F 18-19 B', 'F 18-19 H', 'F 18-19 J', 'F 18-19 M', 'F 18-19 S', 'F 18-19 OR', 'F 18-19 NR', 'F 18-19 NS', 'F 20-24 C', 'F 20-24 B', 'F 20-24 H', 'F 20-24 J', 'F 20-24 M', 'F 20-24 S', 'F 20-24 OR', 'F 20-24 NR', 'F 20-24 NS', 'F 25-29 C', 'F 25-29 B', 'F 25-29 H', 'F 25-29 J', 'F 25-29 M', 'F 25-29 S', 'F 25-29 OR', 'F 25-29 NR', 'F 25-29 NS', 'F 30-34 C', 'F 30-34 B', 'F 30-34 H', 'F 30-34 J', 'F 30-34 M', 'F 30-34 S', 'F 30-34 OR', 'F 30-34 NR', 'F 30-34 NS', 'F 35-39 C', 'F 35-39 B', 'F 35-39 H', 'F 35-39 J', 'F 35-39 M', 'F 35-39 S', 'F 35-39 OR', 'F 35-39 NR', 'F 35-39 NS', 'F 40-44 C', 'F 40-44 B', 'F 40-44 H', 'F 40-44 J', 'F 40-44 M', 'F 40-44 S', 'F 40-44 OR', 'F 40-44 NR', 'F 40-44 NS', 'F 45-49 C', 'F 45-49 B', 'F 45-49 H', 'F 45-49 J', 'F 45-49 M', 'F 45-49 S', 'F 45-49 OR', 'F 45-49 NR', 'F 45-49 NS', 'F 50-54 C', 'F 50-54 B', 'F 50-54 H', 'F 50-54 J', 'F 50-54 M', 'F 50-54 S', 'F 50-54 OR', 'F 50-54 NR', 'F 50-54 NS', 'F 55-59 C', 'F 55-59 B', 'F 55-59 H', 'F 55-59 J', 'F 55-59 M', 'F 55-59 S', 'F 55-59 OR', 'F 55-59 NR', 'F 55-59 NS', 'F 60-64 C', 'F 60-64 B', 'F 60-64 H', 'F 60-64 J', 'F 60-64 M', 'F 60-64 S', 'F 60-64 OR', 'F 60-64 NR', 'F 60-64 NS', 'F 65-69 C', 'F 65-69 B', 'F 65-69 H', 'F 65-69 J', 'F 65-69 M', 'F 65-69 S', 'F 65-69 OR', 'F 65-69 NR', 'F 65-69 NS', 'F 70-74 C', 'F 70-74 B', 'F 70-74 H', 'F 70-74 J', 'F 70-74 M', 'F 70-74 S', 'F 70-74 OR', 'F 70-74 NR', 'F 70-74 NS', 'F 75-79 C', 'F 75-79 B', 'F 75-79 H', 'F 75-79 J', 'F 75-79 M', 'F 75-79 S', 'F 75-79 OR', 'F 75-79 NR', 'F 75-79 NS', 'F 80-84 C', 'F 80-84 B', 'F 80-84 H', 'F 80-84 J', 'F 80-84 M', 'F 80-84 S', 'F 80-84 OR', 'F 80-84 NR', 'F 80-84 NS', 'F 85+ C', 'F 85+ B', 'F 85+ H', 'F 85+ J', 'F 85+ M', 'F 85+ S', 'F 85+ OR', 'F 85+ NR', 'F 85+ NS']
        self.EKeys = ['M 0-4 W0', 'M 0-4 W1', 'M 0-4 W2', 'M 0-4 W3', 'M 0-4 M0', 'M 0-4 M1', 'M 0-4 M2', 'M 0-4 M3', 'M 0-4 A0', 'M 0-4 A1', 'M 0-4 A2', 'M 0-4 A3', 'M 0-4 A4', 'M 0-4 B0', 'M 0-4 B1', 'M 0-4 B2', 'M 0-4 O0', 'M 0-4 O1', 'M 5-7 W0', 'M 5-7 W1', 'M 5-7 W2', 'M 5-7 W3', 'M 5-7 M0', 'M 5-7 M1', 'M 5-7 M2', 'M 5-7 M3', 'M 5-7 A0', 'M 5-7 A1', 'M 5-7 A2', 'M 5-7 A3', 'M 5-7 A4', 'M 5-7 B0', 'M 5-7 B1', 'M 5-7 B2', 'M 5-7 O0', 'M 5-7 O1', 'M 8-9 W0', 'M 8-9 W1', 'M 8-9 W2', 'M 8-9 W3', 'M 8-9 M0', 'M 8-9 M1', 'M 8-9 M2', 'M 8-9 M3', 'M 8-9 A0', 'M 8-9 A1', 'M 8-9 A2', 'M 8-9 A3', 'M 8-9 A4', 'M 8-9 B0', 'M 8-9 B1', 'M 8-9 B2', 'M 8-9 O0', 'M 8-9 O1', 'M 10-14 W0', 'M 10-14 W1', 'M 10-14 W2', 'M 10-14 W3', 'M 10-14 M0', 'M 10-14 M1', 'M 10-14 M2', 'M 10-14 M3', 'M 10-14 A0', 'M 10-14 A1', 'M 10-14 A2', 'M 10-14 A3', 'M 10-14 A4', 'M 10-14 B0', 'M 10-14 B1', 'M 10-14 B2', 'M 10-14 O0', 'M 10-14 O1', 'M 15 W0', 'M 15 W1', 'M 15 W2', 'M 15 W3', 'M 15 M0', 'M 15 M1', 'M 15 M2', 'M 15 M3', 'M 15 A0', 'M 15 A1', 'M 15 A2', 'M 15 A3', 'M 15 A4', 'M 15 B0', 'M 15 B1', 'M 15 B2', 'M 15 O0', 'M 15 O1', 'M 16-17 W0', 'M 16-17 W1', 'M 16-17 W2', 'M 16-17 W3', 'M 16-17 M0', 'M 16-17 M1', 'M 16-17 M2', 'M 16-17 M3', 'M 16-17 A0', 'M 16-17 A1', 'M 16-17 A2', 'M 16-17 A3', 'M 16-17 A4', 'M 16-17 B0', 'M 16-17 B1', 'M 16-17 B2', 'M 16-17 O0', 'M 16-17 O1', 'M 18-19 W0', 'M 18-19 W1', 'M 18-19 W2', 'M 18-19 W3', 'M 18-19 M0', 'M 18-19 M1', 'M 18-19 M2', 'M 18-19 M3', 'M 18-19 A0', 'M 18-19 A1', 'M 18-19 A2', 'M 18-19 A3', 'M 18-19 A4', 'M 18-19 B0', 'M 18-19 B1', 'M 18-19 B2', 'M 18-19 O0', 'M 18-19 O1', 'M 20-24 W0', 'M 20-24 W1', 'M 20-24 W2', 'M 20-24 W3', 'M 20-24 M0', 'M 20-24 M1', 'M 20-24 M2', 'M 20-24 M3', 'M 20-24 A0', 'M 20-24 A1', 'M 20-24 A2', 'M 20-24 A3', 'M 20-24 A4', 'M 20-24 B0', 'M 20-24 B1', 'M 20-24 B2', 'M 20-24 O0', 'M 20-24 O1', 'M 25-29 W0', 'M 25-29 W1', 'M 25-29 W2', 'M 25-29 W3', 'M 25-29 M0', 'M 25-29 M1', 'M 25-29 M2', 'M 25-29 M3', 'M 25-29 A0', 'M 25-29 A1', 'M 25-29 A2', 'M 25-29 A3', 'M 25-29 A4', 'M 25-29 B0', 'M 25-29 B1', 'M 25-29 B2', 'M 25-29 O0', 'M 25-29 O1', 'M 30-34 W0', 'M 30-34 W1', 'M 30-34 W2', 'M 30-34 W3', 'M 30-34 M0', 'M 30-34 M1', 'M 30-34 M2', 'M 30-34 M3', 'M 30-34 A0', 'M 30-34 A1', 'M 30-34 A2', 'M 30-34 A3', 'M 30-34 A4', 'M 30-34 B0', 'M 30-34 B1', 'M 30-34 B2', 'M 30-34 O0', 'M 30-34 O1', 'M 35-39 W0', 'M 35-39 W1', 'M 35-39 W2', 'M 35-39 W3', 'M 35-39 M0', 'M 35-39 M1', 'M 35-39 M2', 'M 35-39 M3', 'M 35-39 A0', 'M 35-39 A1', 'M 35-39 A2', 'M 35-39 A3', 'M 35-39 A4', 'M 35-39 B0', 'M 35-39 B1', 'M 35-39 B2', 'M 35-39 O0', 'M 35-39 O1', 'M 40-44 W0', 'M 40-44 W1', 'M 40-44 W2', 'M 40-44 W3', 'M 40-44 M0', 'M 40-44 M1', 'M 40-44 M2', 'M 40-44 M3', 'M 40-44 A0', 'M 40-44 A1', 'M 40-44 A2', 'M 40-44 A3', 'M 40-44 A4', 'M 40-44 B0', 'M 40-44 B1', 'M 40-44 B2', 'M 40-44 O0', 'M 40-44 O1', 'M 45-49 W0', 'M 45-49 W1', 'M 45-49 W2', 'M 45-49 W3', 'M 45-49 M0', 'M 45-49 M1', 'M 45-49 M2', 'M 45-49 M3', 'M 45-49 A0', 'M 45-49 A1', 'M 45-49 A2', 'M 45-49 A3', 'M 45-49 A4', 'M 45-49 B0', 'M 45-49 B1', 'M 45-49 B2', 'M 45-49 O0', 'M 45-49 O1', 'M 50-54 W0', 'M 50-54 W1', 'M 50-54 W2', 'M 50-54 W3', 'M 50-54 M0', 'M 50-54 M1', 'M 50-54 M2', 'M 50-54 M3', 'M 50-54 A0', 'M 50-54 A1', 'M 50-54 A2', 'M 50-54 A3', 'M 50-54 A4', 'M 50-54 B0', 'M 50-54 B1', 'M 50-54 B2', 'M 50-54 O0', 'M 50-54 O1', 'M 55-59 W0', 'M 55-59 W1', 'M 55-59 W2', 'M 55-59 W3', 'M 55-59 M0', 'M 55-59 M1', 'M 55-59 M2', 'M 55-59 M3', 'M 55-59 A0', 'M 55-59 A1', 'M 55-59 A2', 'M 55-59 A3', 'M 55-59 A4', 'M 55-59 B0', 'M 55-59 B1', 'M 55-59 B2', 'M 55-59 O0', 'M 55-59 O1', 'M 60-64 W0', 'M 60-64 W1', 'M 60-64 W2', 'M 60-64 W3', 'M 60-64 M0', 'M 60-64 M1', 'M 60-64 M2', 'M 60-64 M3', 'M 60-64 A0', 'M 60-64 A1', 'M 60-64 A2', 'M 60-64 A3', 'M 60-64 A4', 'M 60-64 B0', 'M 60-64 B1', 'M 60-64 B2', 'M 60-64 O0', 'M 60-64 O1', 'M 65-69 W0', 'M 65-69 W1', 'M 65-69 W2', 'M 65-69 W3', 'M 65-69 M0', 'M 65-69 M1', 'M 65-69 M2', 'M 65-69 M3', 'M 65-69 A0', 'M 65-69 A1', 'M 65-69 A2', 'M 65-69 A3', 'M 65-69 A4', 'M 65-69 B0', 'M 65-69 B1', 'M 65-69 B2', 'M 65-69 O0', 'M 65-69 O1', 'M 70-74 W0', 'M 70-74 W1', 'M 70-74 W2', 'M 70-74 W3', 'M 70-74 M0', 'M 70-74 M1', 'M 70-74 M2', 'M 70-74 M3', 'M 70-74 A0', 'M 70-74 A1', 'M 70-74 A2', 'M 70-74 A3', 'M 70-74 A4', 'M 70-74 B0', 'M 70-74 B1', 'M 70-74 B2', 'M 70-74 O0', 'M 70-74 O1', 'M 75-79 W0', 'M 75-79 W1', 'M 75-79 W2', 'M 75-79 W3', 'M 75-79 M0', 'M 75-79 M1', 'M 75-79 M2', 'M 75-79 M3', 'M 75-79 A0', 'M 75-79 A1', 'M 75-79 A2', 'M 75-79 A3', 'M 75-79 A4', 'M 75-79 B0', 'M 75-79 B1', 'M 75-79 B2', 'M 75-79 O0', 'M 75-79 O1', 'M 80-84 W0', 'M 80-84 W1', 'M 80-84 W2', 'M 80-84 W3', 'M 80-84 M0', 'M 80-84 M1', 'M 80-84 M2', 'M 80-84 M3', 'M 80-84 A0', 'M 80-84 A1', 'M 80-84 A2', 'M 80-84 A3', 'M 80-84 A4', 'M 80-84 B0', 'M 80-84 B1', 'M 80-84 B2', 'M 80-84 O0', 'M 80-84 O1', 'M 85+ W0', 'M 85+ W1', 'M 85+ W2', 'M 85+ W3', 'M 85+ M0', 'M 85+ M1', 'M 85+ M2', 'M 85+ M3', 'M 85+ A0', 'M 85+ A1', 'M 85+ A2', 'M 85+ A3', 'M 85+ A4', 'M 85+ B0', 'M 85+ B1', 'M 85+ B2', 'M 85+ O0', 'M 85+ O1', 'F 0-4 W0', 'F 0-4 W1', 'F 0-4 W2', 'F 0-4 W3', 'F 0-4 M0', 'F 0-4 M1', 'F 0-4 M2', 'F 0-4 M3', 'F 0-4 A0', 'F 0-4 A1', 'F 0-4 A2', 'F 0-4 A3', 'F 0-4 A4', 'F 0-4 B0', 'F 0-4 B1', 'F 0-4 B2', 'F 0-4 O0', 'F 0-4 O1', 'F 5-7 W0', 'F 5-7 W1', 'F 5-7 W2', 'F 5-7 W3', 'F 5-7 M0', 'F 5-7 M1', 'F 5-7 M2', 'F 5-7 M3', 'F 5-7 A0', 'F 5-7 A1', 'F 5-7 A2', 'F 5-7 A3', 'F 5-7 A4', 'F 5-7 B0', 'F 5-7 B1', 'F 5-7 B2', 'F 5-7 O0', 'F 5-7 O1', 'F 8-9 W0', 'F 8-9 W1', 'F 8-9 W2', 'F 8-9 W3', 'F 8-9 M0', 'F 8-9 M1', 'F 8-9 M2', 'F 8-9 M3', 'F 8-9 A0', 'F 8-9 A1', 'F 8-9 A2', 'F 8-9 A3', 'F 8-9 A4', 'F 8-9 B0', 'F 8-9 B1', 'F 8-9 B2', 'F 8-9 O0', 'F 8-9 O1', 'F 10-14 W0', 'F 10-14 W1', 'F 10-14 W2', 'F 10-14 W3', 'F 10-14 M0', 'F 10-14 M1', 'F 10-14 M2', 'F 10-14 M3', 'F 10-14 A0', 'F 10-14 A1', 'F 10-14 A2', 'F 10-14 A3', 'F 10-14 A4', 'F 10-14 B0', 'F 10-14 B1', 'F 10-14 B2', 'F 10-14 O0', 'F 10-14 O1', 'F 15 W0', 'F 15 W1', 'F 15 W2', 'F 15 W3', 'F 15 M0', 'F 15 M1', 'F 15 M2', 'F 15 M3', 'F 15 A0', 'F 15 A1', 'F 15 A2', 'F 15 A3', 'F 15 A4', 'F 15 B0', 'F 15 B1', 'F 15 B2', 'F 15 O0', 'F 15 O1', 'F 16-17 W0', 'F 16-17 W1', 'F 16-17 W2', 'F 16-17 W3', 'F 16-17 M0', 'F 16-17 M1', 'F 16-17 M2', 'F 16-17 M3', 'F 16-17 A0', 'F 16-17 A1', 'F 16-17 A2', 'F 16-17 A3', 'F 16-17 A4', 'F 16-17 B0', 'F 16-17 B1', 'F 16-17 B2', 'F 16-17 O0', 'F 16-17 O1', 'F 18-19 W0', 'F 18-19 W1', 'F 18-19 W2', 'F 18-19 W3', 'F 18-19 M0', 'F 18-19 M1', 'F 18-19 M2', 'F 18-19 M3', 'F 18-19 A0', 'F 18-19 A1', 'F 18-19 A2', 'F 18-19 A3', 'F 18-19 A4', 'F 18-19 B0', 'F 18-19 B1', 'F 18-19 B2', 'F 18-19 O0', 'F 18-19 O1', 'F 20-24 W0', 'F 20-24 W1', 'F 20-24 W2', 'F 20-24 W3', 'F 20-24 M0', 'F 20-24 M1', 'F 20-24 M2', 'F 20-24 M3', 'F 20-24 A0', 'F 20-24 A1', 'F 20-24 A2', 'F 20-24 A3', 'F 20-24 A4', 'F 20-24 B0', 'F 20-24 B1', 'F 20-24 B2', 'F 20-24 O0', 'F 20-24 O1', 'F 25-29 W0', 'F 25-29 W1', 'F 25-29 W2', 'F 25-29 W3', 'F 25-29 M0', 'F 25-29 M1', 'F 25-29 M2', 'F 25-29 M3', 'F 25-29 A0', 'F 25-29 A1', 'F 25-29 A2', 'F 25-29 A3', 'F 25-29 A4', 'F 25-29 B0', 'F 25-29 B1', 'F 25-29 B2', 'F 25-29 O0', 'F 25-29 O1', 'F 30-34 W0', 'F 30-34 W1', 'F 30-34 W2', 'F 30-34 W3', 'F 30-34 M0', 'F 30-34 M1', 'F 30-34 M2', 'F 30-34 M3', 'F 30-34 A0', 'F 30-34 A1', 'F 30-34 A2', 'F 30-34 A3', 'F 30-34 A4', 'F 30-34 B0', 'F 30-34 B1', 'F 30-34 B2', 'F 30-34 O0', 'F 30-34 O1', 'F 35-39 W0', 'F 35-39 W1', 'F 35-39 W2', 'F 35-39 W3', 'F 35-39 M0', 'F 35-39 M1', 'F 35-39 M2', 'F 35-39 M3', 'F 35-39 A0', 'F 35-39 A1', 'F 35-39 A2', 'F 35-39 A3', 'F 35-39 A4', 'F 35-39 B0', 'F 35-39 B1', 'F 35-39 B2', 'F 35-39 O0', 'F 35-39 O1', 'F 40-44 W0', 'F 40-44 W1', 'F 40-44 W2', 'F 40-44 W3', 'F 40-44 M0', 'F 40-44 M1', 'F 40-44 M2', 'F 40-44 M3', 'F 40-44 A0', 'F 40-44 A1', 'F 40-44 A2', 'F 40-44 A3', 'F 40-44 A4', 'F 40-44 B0', 'F 40-44 B1', 'F 40-44 B2', 'F 40-44 O0', 'F 40-44 O1', 'F 45-49 W0', 'F 45-49 W1', 'F 45-49 W2', 'F 45-49 W3', 'F 45-49 M0', 'F 45-49 M1', 'F 45-49 M2', 'F 45-49 M3', 'F 45-49 A0', 'F 45-49 A1', 'F 45-49 A2', 'F 45-49 A3', 'F 45-49 A4', 'F 45-49 B0', 'F 45-49 B1', 'F 45-49 B2', 'F 45-49 O0', 'F 45-49 O1', 'F 50-54 W0', 'F 50-54 W1', 'F 50-54 W2', 'F 50-54 W3', 'F 50-54 M0', 'F 50-54 M1', 'F 50-54 M2', 'F 50-54 M3', 'F 50-54 A0', 'F 50-54 A1', 'F 50-54 A2', 'F 50-54 A3', 'F 50-54 A4', 'F 50-54 B0', 'F 50-54 B1', 'F 50-54 B2', 'F 50-54 O0', 'F 50-54 O1', 'F 55-59 W0', 'F 55-59 W1', 'F 55-59 W2', 'F 55-59 W3', 'F 55-59 M0', 'F 55-59 M1', 'F 55-59 M2', 'F 55-59 M3', 'F 55-59 A0', 'F 55-59 A1', 'F 55-59 A2', 'F 55-59 A3', 'F 55-59 A4', 'F 55-59 B0', 'F 55-59 B1', 'F 55-59 B2', 'F 55-59 O0', 'F 55-59 O1', 'F 60-64 W0', 'F 60-64 W1', 'F 60-64 W2', 'F 60-64 W3', 'F 60-64 M0', 'F 60-64 M1', 'F 60-64 M2', 'F 60-64 M3', 'F 60-64 A0', 'F 60-64 A1', 'F 60-64 A2', 'F 60-64 A3', 'F 60-64 A4', 'F 60-64 B0', 'F 60-64 B1', 'F 60-64 B2', 'F 60-64 O0', 'F 60-64 O1', 'F 65-69 W0', 'F 65-69 W1', 'F 65-69 W2', 'F 65-69 W3', 'F 65-69 M0', 'F 65-69 M1', 'F 65-69 M2', 'F 65-69 M3', 'F 65-69 A0', 'F 65-69 A1', 'F 65-69 A2', 'F 65-69 A3', 'F 65-69 A4', 'F 65-69 B0', 'F 65-69 B1', 'F 65-69 B2', 'F 65-69 O0', 'F 65-69 O1', 'F 70-74 W0', 'F 70-74 W1', 'F 70-74 W2', 'F 70-74 W3', 'F 70-74 M0', 'F 70-74 M1', 'F 70-74 M2', 'F 70-74 M3', 'F 70-74 A0', 'F 70-74 A1', 'F 70-74 A2', 'F 70-74 A3', 'F 70-74 A4', 'F 70-74 B0', 'F 70-74 B1', 'F 70-74 B2', 'F 70-74 O0', 'F 70-74 O1', 'F 75-79 W0', 'F 75-79 W1', 'F 75-79 W2', 'F 75-79 W3', 'F 75-79 M0', 'F 75-79 M1', 'F 75-79 M2', 'F 75-79 M3', 'F 75-79 A0', 'F 75-79 A1', 'F 75-79 A2', 'F 75-79 A3', 'F 75-79 A4', 'F 75-79 B0', 'F 75-79 B1', 'F 75-79 B2', 'F 75-79 O0', 'F 75-79 O1', 'F 80-84 W0', 'F 80-84 W1', 'F 80-84 W2', 'F 80-84 W3', 'F 80-84 M0', 'F 80-84 M1', 'F 80-84 M2', 'F 80-84 M3', 'F 80-84 A0', 'F 80-84 A1', 'F 80-84 A2', 'F 80-84 A3', 'F 80-84 A4', 'F 80-84 B0', 'F 80-84 B1', 'F 80-84 B2', 'F 80-84 O0', 'F 80-84 O1', 'F 85+ W0', 'F 85+ W1', 'F 85+ W2', 'F 85+ W3', 'F 85+ M0', 'F 85+ M1', 'F 85+ M2', 'F 85+ M3', 'F 85+ A0', 'F 85+ A1', 'F 85+ A2', 'F 85+ A3', 'F 85+ A4', 'F 85+ B0', 'F 85+ B1', 'F 85+ B2', 'F 85+ O0', 'F 85+ O1']
        self.SKeys = ['M 24* Single', 'M 24* Married', 'M 24* Partner', 'M 24* Seperated', 'M 24* Divorced', 'M 24* Widowed', 'M 25-34 Single', 'M 25-34 Married', 'M 25-34 Partner', 'M 25-34 Seperated', 'M 25-34 Divorced', 'M 25-34 Widowed', 'M 35-49 Single', 'M 35-49 Married', 'M 35-49 Partner', 'M 35-49 Seperated', 'M 35-49 Divorced', 'M 35-49 Widowed', 'M 50-64 Single', 'M 50-64 Married', 'M 50-64 Partner', 'M 50-64 Seperated', 'M 50-64 Divorced', 'M 50-64 Widowed', 'M 65+ Single', 'M 65+ Married', 'M 65+ Partner', 'M 65+ Seperated', 'M 65+ Divorced', 'M 65+ Widowed', 'F 24* Single', 'F 24* Married', 'F 24* Partner', 'F 24* Seperated', 'F 24* Divorced', 'F 24* Widowed', 'F 25-34 Single', 'F 25-34 Married', 'F 25-34 Partner', 'F 25-34 Seperated', 'F 25-34 Divorced', 'F 25-34 Widowed', 'F 35-49 Single', 'F 35-49 Married', 'F 35-49 Partner', 'F 35-49 Seperated', 'F 35-49 Divorced', 'F 35-49 Widowed', 'F 50-64 Single', 'F 50-64 Married', 'F 50-64 Partner', 'F 50-64 Seperated', 'F 50-64 Divorced', 'F 50-64 Widowed', 'F 65+ Single', 'F 65+ Married', 'F 65+ Partner', 'F 65+ Seperated', 'F 65+ Divorced', 'F 65+ Widowed']
        self.QKeys = ['M 16-24 level1', 'M 16-24 level2', 'M 16-24 apprent', 'M 16-24 level3', 'M 16-24 level4+', 'M 16-24 other', 'M 25-34 no', 'M 25-34 level1', 'M 25-34 level2', 'M 25-34 apprent', 'M 25-34 level3', 'M 25-34 level4+', 'M 25-34 other', 'M 35-49 no', 'M 35-49 level1', 'M 35-49 level2', 'M 35-49 apprent', 'M 35-49 level3', 'M 35-49 level4+', 'M 35-49 other', 'M 50-64 no', 'M 50-64 level1', 'M 50-64 level2', 'M 50-64 apprent', 'M 50-64 level3', 'M 50-64 level4+', 'M 50-64 other', 'M 65+ no', 'M 65+ level1', 'M 65+ level2', 'M 65+ apprent', 'M 65+ level3', 'M 65+ level4+', 'M 65+ other', 'F 16-24 no', 'F 16-24 level1', 'F 16-24 level2', 'F 16-24 apprent', 'F 16-24 level3', 'F 16-24 level4+', 'F 16-24 other', 'F 25-34 no', 'F 25-34 level1', 'F 25-34 level2', 'F 25-34 apprent', 'F 25-34 level3', 'F 25-34 level4+', 'F 25-34 other', 'F 35-49 no', 'F 35-49 level1', 'F 35-49 level2', 'F 35-49 apprent', 'F 35-49 level3', 'F 35-49 level4+', 'F 35-49 other', 'F 50-64 no', 'F 50-64 level1', 'F 50-64 level2', 'F 50-64 apprent', 'F 50-64 level3', 'F 50-64 level4+', 'F 50-64 other', 'F 65+ no', 'F 65+ level1', 'F 65+ level2', 'F 65+ apprent', 'F 65+ level3', 'F 65+ level4+', 'F 65+ other']

        self.current_solution = self.initial_solution()
        self.current_fitness = self.calculate_fitness(self.current_solution)

        self.TabuSearch()

    # Define the initial solution
    def initial_solution(self):
        solution = []
        for i in range(0, self.population_size):
            age = self.rsamples[i].split(' ')[1]
            sex = self.rsamples[i].split(' ')[0]
            ethnicity = self.esamples[i]
            religion = self.rsamples[i].split(' ')[2]
            status = self.ssamples[i].split(' ')[2]
            if age in ['0-4', '5-7', '8-9', '10-14', '15']:
                qual = 'no'
            else:
                qual = self.qsamples[i].split(' ')[2]
            person = Person(i + 1, age=age, sex=sex, ethnicity=ethnicity, religion=religion, status=status,
                            qualification=qual)
            solution.append(person)
        return solution

    def agemap(self, age):
        if age in ['0-4', '5-7', '8-9', '10-14', '15', '16-17', '18-19', '20-24']:
            return "24*"
        elif age in ['25-29', '30-34']:
            return "25-34"
        elif age in ['35-39', '40-44', '45-49']:
            return "35-49"
        elif age in ['50-54', '55-59', '60-64']:
            return "50-64"
        elif age in ['65-69', '70-74', '75-79', '80-84', '85+']:
            return "65+"

    def agemap2(self, age):
        if age in ['16-17', '18-19', '20-24']:
            return "16-24"
        elif age in ['25-29', '30-34']:
            return "25-34"
        elif age in ['35-39', '40-44', '45-49']:
            return "35-49"
        elif age in ['50-54', '55-59', '60-64']:
            return "50-64"
        elif age in ['65-69', '70-74', '75-79', '80-84', '85+']:
            return "65+"
        else:
            return age

    # Define the objective function
    def calculate_fitness(self, persons, plot=False):
        fitness = 0
        actual = {}
        actual_sex_by_age_by_religion = ICT.getdictionary(ICT.religion_by_sex_by_age)
        for rkey in self.Rkeys:
            avalue = actual_sex_by_age_by_religion.get(rkey)
            actual[rkey] = avalue

        actual_sex_by_age_by_ethnic = ICT.getdictionary(ICT.ethnic_by_sex_by_age)
        for ekey in self.EKeys:
            avalue = actual_sex_by_age_by_ethnic.get(ekey)
            actual[ekey] = avalue

        actual_marital_by_sex_by_age = ICT.getdictionary(ICT.marital_by_sex_by_age)
        for skey in self.SKeys:
            avalue = actual_marital_by_sex_by_age.get(skey)
            actual[skey] = avalue

        actual_qualification_by_sex_by_age = ICT.getdictionary(ICT.qualification_by_sex_by_age)
        for qkey in self.QKeys:
            avalue = actual_qualification_by_sex_by_age.get(qkey)
            actual[qkey] = avalue

        predicted = {}
        temp = []
        for person in persons:
            temp.append(person.sex + " " + person.age + " " + person.religion)
        predicted_sex_by_age_by_religion = Counter(temp)
        for rkey in self.Rkeys:
            pvalue = predicted_sex_by_age_by_religion.get(rkey)
            if pvalue == None:
                pvalue = 0
            predicted[rkey] = pvalue

        temp = []
        for person in persons:
            temp.append(person.sex + " " + person.age + " " + person.ethnicity)

        predicted_sex_by_age_by_ethnicity = Counter(temp)
        for ekey in self.EKeys:
            pvalue = predicted_sex_by_age_by_ethnicity.get(ekey)
            if pvalue == None:
                pvalue = 0
            predicted[ekey] = pvalue

        temp = []
        for person in persons:
            temp.append(person.sex + " " + self.agemap(person.age) + " " + person.status)

        predicted_marital_by_sex_by_age = Counter(temp)
        for skey in self.SKeys:
            pvalue = predicted_marital_by_sex_by_age.get(skey)
            if pvalue == None:
                pvalue = 0
            predicted[skey] = pvalue

        temp = []
        for person in persons:
            temp.append(person.sex + " " + self.agemap2(person.age) + " " + person.qualification)

        predicted_qualification_by_sex_by_age = Counter(temp)
        for qkey in self.QKeys:
            pvalue = predicted_qualification_by_sex_by_age.get(qkey)
            if pvalue == None:
                pvalue = 0
            predicted[qkey] = pvalue

        a = np.array(list(actual.values()))
        p = np.array(list(predicted.values()))
        rmse = np.sqrt(((p - a) ** 2).mean())

        if plot==True:
            n_actual = [float(i) / max(a) for i in a]
            n_pred = [float(i) / max(p) for i in p]

            n_actual.sort()
            n_pred.sort()

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(x0='data', name='actual', y=n_actual, line_color='#636EFA'))
            fig.add_trace(
                go.Scatter(x0='data', name='pred', y=n_pred, line_color='#EF553B'))
            fig.update_layout(width=1000, title='RMSE=' + str(rmse))
            py.offline.plot(fig, filename="violen.html")
            fig.show()
        return rmse

    def TabuSearch(self):
        # Define the tabu search algorithm
        tabu_list = []
        best_move = self.current_solution
        best_fitness = self.current_fitness

        for i in range(self.num_iterations):
            # Generate the neighborhood
            neighborhood = []
            for j in range(100):
                new_solution = self.current_solution.copy()
                for k in range(10):
                    rnd = random.randint(0, self.population_size - 1)
                    person = new_solution[rnd]

                    # person.age = self.rsamples[i].split(' ')[1]
                    # person.sex = self.rsamples[i].split(' ')[0]
                    person.ethnicity = self.esamples[i]
                    person.religion = self.rsamples[i].split(' ')[2]
                    person.status = self.ssamples[i].split(' ')[2]
                    if person.age in ['0-4', '5-7', '8-9', '10-14', '15']:
                        person.qualification = 'no'
                    else:
                        person.qualification = self.qsamples[i].split(' ')[2]
                    new_solution[rnd] = person
                    neighborhood.append(new_solution)

                # Select the best move
                for move in neighborhood:
                    if move not in tabu_list:
                        move_fitness = self.calculate_fitness(move)
                        print("Iteration {}: Current={}, Best={}".format(i + 1, move_fitness, best_fitness))
                        if move_fitness < best_fitness:
                            best_move = move
                            best_fitness = move_fitness

                        # Update the tabu list
                        tabu_list.append(move)
                        if len(tabu_list) > self.tabu_list_size:
                            tabu_list.pop(0)

                    # Update the current solution
                    self.current_solution = best_move
                    self.current_fitness = best_fitness

        self.calculate_fitness(self.current_solution, plot=True)

ts = TabuSearch()