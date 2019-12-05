import pygame
from app_class import App
from inputs import Inputs
from generation_class import Generation
import os

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

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    if os.path.exists('data/generations.csv'):
        os.remove('data/generations.csv')
    
    with open('data/generations.csv', 'w') as generationsFile:
        generation = Generation.generateWithRandomIndividuals()
        for i in range(100):
            print('starting scoring for individuals in generation ' + str(i))
            fileName = 'data/generation-' + str(i) + '.csv'
            if os.path.exists(fileName):
                os.remove(fileName)
            
            with open(fileName, 'w') as generationFile:
                for individual in generation.individuals:
                    print('scoring next individual')
                    app = App(individual.decide)
                    didQuit = app.run()

                    if didQuit:
                        print('runs stopped manually not continuing')
                        return

                    individual.gameScore = app.player.current_score
                    individual.gameTime = app.time
                    individual.gameScore = 1234
                    individual.gameTime = 5678

                    print(str(individual), file = generationFile)
        
            print(str(generation), file = generationsFile)
            generation = generation.generateNext()
        

if __name__ == '__main__':
    main()