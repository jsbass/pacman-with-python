import pygame
import sys, copy, math, os, time

from .player_class import *
from .enemy_class import *
from .inputs import Inputs

vec = pygame.math.Vector2

class App:
    def __init__(self, get_input):
        pygame.init()
        self.gameStateArray = [1]*(287+2+2*(4)) # coins state, player pos, enemy pos = 297
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.player = None
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.pen = []
        self.pen_exit_target = None
        self.pen_walls = []
        self.coins = []
        self.coinsStart = []
        self.enemies = []
        self.time = 0
        self.get_input = get_input
        self.input = Inputs.NONE
        self.load()
        self.reset()
    
    def quit(self):
        pygame.quit()

    # possibly get rid of this and store the functioning game state as this kind of array
    def getGameState(self):
        return self.gameStateArray

    def getTimeDiff(self):
        t = time.time()
        diff = t - self.last_time
        self.last_time = t
        return round(diff, 4)
    
    # run then return back for analysis 
    def run(self):
        self.last_time = time.time()
        self.reset()
        self.running = True
        count = 0
        quitReturn = False #tracks whether the game was quit manually
        while self.running:
            # alternate these between real time and fixed interval
            # dt = self.clock.tick(60) / 1000
            dt = .1
            self.time += dt
            self.playing_events()
            self.playing_update(dt)
            if(count == 0):
                self.playing_draw()
            count = (count + 1) % 5
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    quitReturn = True
            
        return quitReturn

############################ HELPER FUNCTIONS ##################################

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'maze.png'))
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        with open(os.path.join(os.path.dirname(__file__), 'walls.txt'), 'r') as file:
            coinCount = 0
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1": # regular wall
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C": # coin
                        coinCount += 1
                        self.coinsStart.append((coinCount, vec(xidx, yidx)))
                    elif char == "P":
                        self.player = Player(self, vec(xidx, yidx))
                    elif char in ["2", "3", "4", "5"]: # enemies
                        self.enemies.append(Enemy(self, vec(xidx, yidx), int(char)-2))
                        self.pen.append(vec(xidx, yidx)) # assume enemy tile is part of pen
                    elif char == "S":
                        self.pen.append(vec(xidx, yidx))
                    elif char == "E": #target for exiting pen
                        self.pen_exit_target = vec(xidx, yidx)
                        coinCount += 1
                        self.coinsStart.append((coinCount, vec(xidx, yidx)))
                    elif char == "A": #pen walls/regular wall
                        self.pen_walls.append(vec(xidx, yidx))
                        self.walls.append(vec(xidx, yidx))
                    elif char == "B": #pen exit
                        self.walls.append(vec(xidx, yidx))
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))

    def reset(self):
        self.time = 0
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        
        self.gameStateArray = self.gameStateArray = [1]*(287+2+2*(4)) # coins state, player pos, enemy pos = 297
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = copy.deepcopy(self.coinsStart)
        self.gameStateArray = [1]*(287+2+2*(4))
        self.gameStateArray[287] = self.player.grid_pos.x
        self.gameStateArray[288] = self.player.grid_pos.y

        for i, enemy in enumerate(self.enemies):
            self.gameStateArray[288+2*i] = enemy.grid_pos.x
            self.gameStateArray[288+2*i+1] = enemy.grid_pos.y

########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        event = self.get_input(self)
        if event == Inputs.QUIT:
            self.running = False
        else:
            self.input = event

    def playing_update(self, dt):
        if self.input == Inputs.LEFT:
            self.player.move(vec(-1, 0))
        elif self.input == Inputs.RIGHT:
            self.player.move(vec(1, 0))
        elif self.input == Inputs.UP:
            self.player.move(vec(0, -1))
        elif self.input == Inputs.DOWN:
            self.player.move(vec(0, 1))
        self.player.update(dt)
        self.gameStateArray[287] = self.player.grid_pos.x
        self.gameStateArray[288] = self.player.grid_pos.y

        coinRemovalIndices = []
        for i, coin in enumerate(self.coins):
            if(self.player.grid_pos == coin[1]):
                coinRemovalIndices.append(i)

        for index in coinRemovalIndices:
            coin = self.coins.pop(index)
            self.player.current_score += 1
            self.gameStateArray[coin[0]] = 0

        for i, enemy in enumerate(self.enemies):
            enemy.update(dt)
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()
                break

            self.gameStateArray[288+2*i] = enemy.grid_pos.x
            self.gameStateArray[288+2*i+1] = enemy.grid_pos.y

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [15, 0], 15, WHITE, START_FONT)
        self.draw_text('TIME: {}'.format(math.floor(self.time)), self.screen, [250, 0], 15, WHITE, START_FONT)
        self.draw_text('DECISION: {}'.format(self.input.name), self.screen, [250+150, 0], 15, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.running = False
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin[1].x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin[1].y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)
