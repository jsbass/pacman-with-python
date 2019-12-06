from individual_class import Individual
import numpy
import math
import random
import copy

class Generation:
    def __init__(self, individuals, numOfTopIndividuals = None):
        self.individuals = individuals
        self.numOfTopIndividuals = numOfTopIndividuals if numOfTopIndividuals != None else len(individuals)//4

    @staticmethod
    def generateWithRandomIndividuals(num, numTopIndividuals = None):
        individuals = []
        for i in range(num):
            individuals.append(Individual([
                numpy.multiply(numpy.add(numpy.random.rand(297,8), -0.5), 20), #random matrix between -10 and 10
                numpy.multiply(numpy.add(numpy.random.rand(8,8), -0.5), 20), #random matrix between -10 and 10
                numpy.multiply(numpy.add(numpy.random.rand(8,4), -0.5), 20) #random matrix between -10 and 10
            ]))

        return Generation(individuals, numTopIndividuals)

    def generateNext(self):
        sortedIndividuals = sorted(copy.deepcopy(self.individuals), key=lambda i : i.getScore())
        newIndividuals = []
        # 4/24 added
        for i in range(self.numOfTopIndividuals):
            newIndividuals.append(sortedIndividuals[i].mutate(0, .1*i))
        
        i = 0
        while len(newIndividuals) < len(self.individuals):
            newIndividuals.append(self.breed([self.individuals[i], self.individuals[i+1]]).mutate(0, .05*i)) # get more wild as we go
            i += 1
        
        return Generation(newIndividuals, self.numOfTopIndividuals)

    def breed(self, individuals):
        if len(individuals) == 0:
            raise "Empty array passed in"

        # lazy but should check each individual has matching layers
        layers = [[]]*len(individuals[0].layers)
        for i in range(len(individuals[0].layers)):
            layers[i] = numpy.empty(individuals[0].layers[i].shape)
            for x in range(individuals[0].layers[i].shape[0]):
                for y in range(individuals[0].layers[i].shape[1]):
                    layers[i][x][y] = individuals[random.randint(1, len(individuals)) - 1].layers[i].item((x,y))

        return Individual(layers)
    
    def __str__(self):
        minScore = None
        maxScore = None
        sumScores = 0

        minCalcScore = None
        maxCalcScore = None
        sumCalcScores = 0

        minTime = None
        maxTime = None
        sumTime = 0

        for i in self.individuals:
            score = i.getScore()
            if maxCalcScore == None or score > maxCalcScore:
                maxCalcScore = score
            if minCalcScore == None or score < minCalcScore:
                minCalcScore = score
            sumCalcScores += score

            if maxScore == None or i.gameScore > maxScore:
                maxScore = i.gameScore
            if minScore == None or i.gameScore < minScore:
                minScore = i.gameScore
            sumScores += i.gameScore

            if maxTime == None or i.gameTime > maxTime:
                maxTime = i.gameTime
            if minTime == None or i.gameTime < minTime:
                minTime = i.gameTime
            sumTime += i.gameTime
        
        items = [
            minScore, maxScore, sumScores / len(self.individuals),
            minTime, maxTime, sumTime / len(self.individuals),
            minCalcScore, maxCalcScore, sumCalcScores / len(self.individuals)
        ]
        return ','.join(map(str, items))