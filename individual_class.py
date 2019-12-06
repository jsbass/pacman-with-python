from game.inputs import Inputs
import numpy
import copy, sys, random, traceback, math, base64

class Individual:
    def __init__(self, layers):
        self.layers = []
        for layer in layers:
            self.layers.append(numpy.matrix(layer))
        self.gameScore = 0
        self.gameTime = 0

    def getScore(self):
        return self.gameScore * (1-1/(1+math.exp(-0.03*(self.gameTime - 400)))) #exponenetial decay to drive finish times to under 5 minutes

    def decide(self, state):
        # timeout after 10 minutes
        if(state.time > 600):
            self.did_timeout = True
            return Inputs.QUIT
        
        #transform game state into net input
        try:
            output = numpy.array(state.getGameState())
            for layer in self.layers:
                output = numpy.matmul(output, layer)
            
            return Inputs(numpy.where(output == numpy.amax(output))[0][0] + 1)
        except:
            traceback.print_exc()
            return Inputs.NONE


    def mutate(self, mean, sd):
        for layer in self.layers:
            for row in layer:
                for w in row:
                    w *= numpy.random.normal(mean, sd)

        return self

    @staticmethod
    def fromString(string):
        #score,time,score,[shapex,shapey,name,bytes]
        values = string.split(',')
        layers = [[[]]*8, [[]]*8, [[]]*8]
        if len(values) < 7 or (len(values) - 4) % 4 != 0:
            raise Exception('exception reading individual from string. string split size mismatch. size: {}'.format(len(values)))
        
        score = int(values[0])
        time = float(values[1])
        # calculated score = values[2]
        numLayers = (len(values) - 4)//4
        layers = []
        for i in range(numLayers):
            shape = (int(values[4+i*4]), int(values[4+i*4+1]))
            name = values[4+i*4+2]
            layers.append(numpy.frombuffer(base64.b64decode(values[4+i*4+3].encode()), dtype=name).reshape(shape))

        individual = Individual(layers)
        individual.gameScore = score
        individual.gameTime = time
        return individual


    def __str__(self):
        items = [str(self.gameScore), str(self.gameTime), str(self.getScore()), str(len(self.layers))]
        for layer in self.layers:
            items.append(str(layer.shape[0]))
            items.append(str(layer.shape[1]))
            items.append(str(layer.dtype.name))
            items.append(base64.b64encode(layer.tobytes()).decode())
        return ','.join(items)

                
