import pygame
from app_class import *

def Player:
    WEIGHTS1 = []; # 258x8
    WEIGHTS2 = []; # 8x4
    def get_input(self, app):
        # get model input from app state
        # calculate player's output using weights
        # return output based on neural net output
        print('getting input')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Inputs.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return Inputs.LEFT
                if event.key == pygame.K_RIGHT:
                    return Inputs.RIGHT
                if event.key == pygame.K_UP:
                    return Inputs.UP
                if event.key == pygame.K_DOWN:
                    return Inputs.DOWN

    return Inputs.NONE

def GenerationHandler:
    generations = [];
    def createGeneration(self, prevGen):
        return ['newplayer1', 'newplayer2']

    def play(play)
if __name__ == '__main__':