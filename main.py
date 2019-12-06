import pygame
from game.app_class import App
from game.inputs import Inputs
from generation_class import Generation
from individual_class import Individual
import os, sys, argparse, shutil

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

def main(continueRun, name, numGenerations, individualsInGeneration, topForBreeding):
    dataDir = 'data/{}'.format(name)

    generation = None
    startNumber = 0
    if continueRun:
        with open(os.path.join(dataDir,'generations.csv'), 'r') as generationsFile:
            metadata = generationsFile.readline().rstrip().split(',')
            print('metadata', metadata)
            topForBreeding = int(metadata[0]) if (metadata[0] != 'None') else None
            numLines = len(generationsFile.readlines())
            startNumber = numLines
            print('continuing from generation ' + str(startNumber))
            with open(os.path.join(dataDir, 'generation-{}.csv'.format(str(numLines))), 'r') as generationFile:
                individuals = []
                for line in generationFile.readlines():
                    if line == '':
                        continue
                    individuals.append(Individual.fromString(line))

                generation = Generation(individuals)
    else:
        if(os.path.exists(dataDir)):
            shutil.rmtree(dataDir)
        os.makedirs(dataDir)
        generation = Generation.generateWithRandomIndividuals(individualsInGeneration, topForBreeding)
    
    print('starting learning process with the following values:')
    print('previous generations', startNumber)
    print('name', name)
    print('number of generations', numGenerations)
    print('individuals in a generation', individualsInGeneration)
    print('number of top individuals bred into next gen', topForBreeding)

    app = App(None)
    with open(os.path.join(dataDir, 'generations.csv'), 'a+' if continueRun else 'w+') as generationsFile:
        if not continueRun:
            print(topForBreeding, file=generationsFile)
        for i in range(startNumber+1, startNumber+100):
            print('starting scoring for individuals in generation ' + str(i))

            with open(os.path.join(dataDir, 'generation-{}.csv'.format(i)), 'w+') as generationFile:
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

                    print(str(individual), file = generationFile)
        
            print(str(generation), file = generationsFile)
            generation = generation.generateNext()

    app.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="runs machine learning for pacman")
    parser.add_argument('--numGenerations', type=int, help='number of generations to run', default=100)
    parser.add_argument('--numIndividuals', type=int, help='number of individuals in a generation. Ignored if continuing', default=10)
    parser.add_argument('--numToBreed', type=int, help='number of top scorers to breed into new generation. Ignored if continuing. If this is not passed, the number will be calculated from the number of individuals', default=None)
    parser.add_argument('--continue', '-c', action='store_true', dest='cont')
    parser.add_argument('--name', '-n', default='default', help='name of run to prevent overwriting')
    args = parser.parse_args()
    main(args.cont, args.name, args.numGenerations, args.numIndividuals, args.numToBreed)