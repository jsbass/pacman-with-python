import pygame
from app_class import *

def get_input(app):
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

if __name__ == '__main__':
    app = App(get_input)
    app.run()