from individual_class import Individual
import numpy
import math
import random
import copy
individual_count = 24
class Generation:
    def __init__(self, individuals):
        self.individuals = individuals

    @staticmethod
    def generateWithRandomIndividuals():
        individuals = []
        for i in range(24):
            individuals.append(Individual([
                numpy.multiply(numpy.add(numpy.random.rand(297,8), -0.5), 20), #random matrix between -10 and 10
                numpy.multiply(numpy.add(numpy.random.rand(8,8), -0.5), 20), #random matrix between -10 and 10
                numpy.multiply(numpy.add(numpy.random.rand(8,4), -0.5), 20) #random matrix between -10 and 10
            ]))

        return Generation(individuals)

    def generateNext(self):
        sortedIndividuals = sorted(self.individuals, key=lambda i : i.getScore())
        newIndividuals = []
        # 4/24 added
        newIndividuals.append(sortedIndividuals[0])
        newIndividuals.append(sortedIndividuals[1])
        newIndividuals.append(sortedIndividuals[2])
        newIndividuals.append(sortedIndividuals[3])

        # 8/24 added
        newIndividuals.append(self.breed([sortedIndividuals[0], sortedIndividuals[1]]))
        newIndividuals.append(self.breed([sortedIndividuals[1], sortedIndividuals[2]]))
        newIndividuals.append(self.breed([sortedIndividuals[2], sortedIndividuals[3]]))
        newIndividuals.append(self.breed([sortedIndividuals[3], sortedIndividuals[4]]))

        for i in range(16):
            newIndividuals.append(copy.deepcopy(self.individuals[random.randint(4, 23)]).mutate())
        
        return Generation(newIndividuals)

    def breed(self, individuals):
        if len(individuals) == 0:
            raise "Empty array passed in"

        # lazy but should check each individual has matching layers
        layers = [[]]*len(individuals[0].layers)
        for i in range(len(individuals[0].layers)):
            layers[i] = [[]]*len(individuals[0].layers[i])
            for x in range(len(individuals[0].layers[i])):
                layers[i][x] = [[]]*len(individuals[0].layers[i][x])
                for y in range(len(individuals[0].layers[i][x])):
                    layers[i][x][y] = individuals[random.randint(1, len(individuals)) - 1].layers[i][x][y]

        return Individual(layers)
    
    def __str__(self):
        maxScore = 0
        sumScores = 0
        for i in self.individuals:
            score = i.getScore()
            if score > maxScore:
                maxScore = score
            sumScores += score
        
        string = ''
        string += str(maxScore) + ','
        string += str(sumScores / len(self.individuals))
        return string