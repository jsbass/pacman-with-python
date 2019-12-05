from inputs import Inputs
import numpy
import copy
import sys
import random
import traceback
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

                
