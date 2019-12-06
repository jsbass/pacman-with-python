import pygame
import random
from .settings import *

vec = pygame.math.Vector2

cellsPerSecond = 1
class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()
        self.decision_history = []

    def update(self, dt):
        self.target = self.set_target() 
        if self.target != self.grid_pos:
            if self.can_change_direction():
                self.pick_direction()
            self.pix_pos += vec(self.direction.x * self.app.cell_width, self.direction.y * self.app.cell_height) * self.speed * dt

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1

    def draw(self):
        # line to target
        pygame.draw.line(self.app.screen, self.colour, self.pix_pos, (int(self.target.x*self.app.cell_width)+self.app.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(self.target.y*self.app.cell_height)+self.app.cell_height//2+TOP_BOTTOM_BUFFER//2))
        # circle next square
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.next_cell.x*self.app.cell_width+self.app.cell_width//2+TOP_BOTTOM_BUFFER//2),
                                int(self.next_cell.y*self.app.cell_height+self.app.cell_height//2+TOP_BOTTOM_BUFFER//2 )), self.radius, 1)
        # direction line
        pygame.draw.line(self.app.screen, self.colour, self.pix_pos, self.pix_pos + self.direction)
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = cellsPerSecond * 2
        else:
            speed = cellsPerSecond
        return speed

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            else:
                return vec(COLS-2, ROWS-2)

    def can_change_direction(self):

        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def pick_direction(self):
        if(self.grid_pos in self.app.pen):
            self.next_cell = self.Euclidian(self.grid_pos, self.app.pen_exit_target, self.direction, self.app.pen_walls)
        elif self.personality == "random":
            self.next_cell = self.get_random_direction()
        elif self.personality == "slow":
            self.next_cell = self.Euclidian(self.grid_pos, self.target, self.direction, self.app.walls)
        elif self.personality == "speedy":
            self.next_cell = self.Euclidian(self.grid_pos, self.target, self.direction, self.app.walls)
        elif self.personality == "scared":
            self.next_cell = self.Euclidian(self.grid_pos, self.target, self.direction, self.app.walls)

        self.direction = (self.next_cell - self.grid_pos)
        if self.direction != vec(0,0):
            self.direction.normalize_ip()

    def find_next_cell_in_path(self, target, method):
        return method(self.grid_pos, target, self.direction if self.direction != vec(0, 0) else vec(1, 0), self.app.walls)

    def Euclidian(self, start, target, direction, walls):
        if(target == start):
            return start
        if direction == vec(0,0):
            possibleTiles = [start + vec(1,0), start + vec(0,1), start + vec(-1,0), start + vec(0, -1)]
        else:
            possibleTiles = [direction + start, vec(direction.y, direction.x) + start, vec(-direction.y, -direction.x) + start]
        possibleTiles = list(filter(lambda t : not walls.__contains__(t), possibleTiles))
        if len(possibleTiles) == 0:
            filter(lambda t : not walls.__contains__(t), [start + direction*-1])
        
        return min(possibleTiles, key=lambda t : t.distance_to(target), default=start)

    def BFS(self, start, target, direction, walls):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        if self.direction == vec(0,0):
            possibleTiles = [self.grid_pos + vec(1,0), self.grid_pos + vec(0,1), self.grid_pos + vec(-1,0), self.grid_pos + vec(0, -1)]
        else:
            possibleTiles = [self.direction + self.grid_pos, vec(self.direction.y, self.direction.x) + self.grid_pos, vec(-self.direction.y, self.direction.x) + self.grid_pos]
        possibleTiles = list(filter(lambda t : not self.app.walls.__contains__(t), possibleTiles))
        if len(possibleTiles) == 0:
            filter(lambda t : not self.app.walls.__contains__(t), [self.grid_pos + self.direction*-1])

        if len(possibleTiles) == 0:
            return self.grid_pos
        
        return possibleTiles[random.randint(0, len(possibleTiles) - 1 )]

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 +
                   self.app.cell_height//2)

    def set_colour(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"
