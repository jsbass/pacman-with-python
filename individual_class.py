from game.inputs import Inputs
import numpy
import copy
import sys
import random
import traceback

expectedStringSize = 297*8 + 8*8 + 4*8 + 3
class Individual:
    def __init__(self, layers):
        self.layers = layers #array of weight matrices [(297x8), (8x8), (8x4)]
        self.gameScore = 0
        self.gameTime = 0

    def getScore(self):
        return self.gameScore

    def decide(self, state):
        #transform game state into net input
        try:
            output = numpy.array(state.getGameState())
            for layer in self.layers:
                output = numpy.matmul(output, layer)
            
            return Inputs(numpy.where(output == numpy.amax(output))[0][0] + 1)
        except:
            traceback.print_exc()
            raise
            return Inputs.NONE


    def mutate(self):
        for layer in self.layers:
            for row in layer:
                for w in row:
                    w *= (random.random() - 0.5) * .2

        return self

    @staticmethod
    def fromString(string):
        values = string.split(',')
        if len(values) != expectedStringSize:
            raise 'string value not correct size. expected: {}, actual: {}'.format(expectedStringSize, len(values))
        layers = [[[]]*8, [[]]*8, [[]]*4]
        
        index = 0
        for i in range(8):
            layers[0][i] = [0]*297
            for j in range(297):
                layers[0][i][j] = values[index]
                index += 1

        for i in range(8):
            layers[1][i] = [0]*8
            for j in range(8):
                layers[1][i][j] = values[index]
                index += 1

        for i in range(8):
            layers[2][i] = [0]*4
            for j in range(4):
                layers[2][i][j] = values[index]
                index += 1

        individual = Individual(layers)
        individual.gameScore = values[index]
        individual.gameTime = values[index+1]
        return individual


    def __str__(self):
        string = ''""''
        for layer in self.layers:
            for row in layer:
                for w in row:
                    string += (str(w) + ',')

        string += str(self.gameScore) + ','
        string += str(self.gameTime) + ','
        string += str(self.getScore())

        return string

                
