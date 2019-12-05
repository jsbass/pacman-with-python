import pygame
from game.app_class import App
from game.inputs import Inputs
from generation_class import Generation
from individual_class import Individual
import os
import sys

class ManualPlayer:
    def get_input(self, app):
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

def main(continueRun):
    if not os.path.exists('data'):
        os.makedirs('data')

    generation = None
    startNumber = 1
    if continueRun:
        with open('data/generations.csv', 'r') as generationsFile:
            numLines = len(generationsFile.readlines())
            startNumber = numLines
            with open('data/generation-' + str(numLines) + '.csv', 'r') as generationFile:
                individuals = []
                for line in generationFile.readlines():
                    if line == '':
                        continue
                    individuals.append(Individual.fromString(line))

                generation = Generation(individuals)
    else:
        generation = Generation.generateWithRandomIndividuals()
    
    if os.path.exists('data/generations.csv'):
        os.remove('data/generations.csv')
    
    app = App(None)
    with open('data/generations.csv', 'a+' if continueRun else 'w+') as generationsFile:
        for i in range(startNumber, startNumber+100):
            print('starting scoring for individuals in generation ' + str(i))
            fileName = 'data/generation-' + str(i) + '.csv'
            if os.path.exists(fileName):
                os.remove(fileName)
            
            with open(fileName, 'w+') as generationFile:
                for individual in generation.individuals:
                    print('scoring next individual')
                    app.get_input = individual.decide
                    app.reset()
                    didQuit = app.run()

                    if didQuit:
                        print('runs stopped manually not continuing')
                        app.quit()
                        return

                    individual.gameScore = app.player.current_score
                    individual.gameTime = app.time
                    individual.gameScore = 1234
                    individual.gameTime = 5678

                    print(str(individual), file = generationFile)
        
            print(str(generation), file = generationsFile)
            generation = generation.generateNext()

    app.quit()