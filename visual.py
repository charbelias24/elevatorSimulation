from structure import *
import sys, pygame

import time

class Visual:
    def __init__(self, simulations):
        pygame.init()
        self.simulations = simulations
        self.size = width, height = 720, 720
        self.speed = [2, 2]
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.base_y = 500
        self.base_x = 160
        self.screen = pygame.display.set_mode(self.size)
        self.base = pygame.image.load("pictures/base.png")
        self.floor = pygame.image.load("pictures/floor.png")
        self.roof = pygame.image.load("pictures/roof.png")
        self.background = pygame.image.load("pictures/background.png")
        self.x_addition = 350

    def draw(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self.screen.fill(self.white)
            #self.screen.blit(self.background)
            self.draw_building(optimized=0)
            self.draw_building(optimized=1)

            self.draw_floor_number(optimized=0)
            self.draw_floor_number(optimized=1)

            self.draw_floor_people(optimized=0)
            self.draw_floor_people(optimized=1)

            self.draw_elevator_people(optimized=0)
            self.draw_elevator_people(optimized=1)

            self.draw_elevator_square(optimized=0)
            self.draw_elevator_square(optimized=1)

            pygame.display.flip()
            sleep(0.001)

    def draw_floor_number(self, optimized):
        floor_number = {}
        font = pygame.font.SysFont('Arial', 14, True, False)
        x_addition = self.x_addition if optimized else 0
        tmp = len(self.simulations[optimized].floors.values())

        for i, floor in enumerate(self.simulations[optimized].floors.values()):
            floor_number[i] = font.render(str(tmp - floor.floor_nb - 3), True, self.black)
            self.screen.blit(floor_number[i], [self.base_x - 15 + x_addition, ((self.base_y + 12) - 12 * i)])

    def draw_floor_people(self, optimized):
        floor_people = {}
        font = pygame.font.SysFont('Arial', 14, True, False)
        x_addition = self.x_addition if optimized else 0

        for i, floor in enumerate(list(self.simulations[optimized].floors.values())[::-1]):
            floor_people[i] = font.render(str(len(floor.people)), True, self.black)
            self.screen.blit(floor_people[i], [self.base_x + 75 + x_addition, ((self.base_y + 12) - 12 * i)])

    def draw_elevator_people(self, optimized):
        elevator_people = {}
        font = pygame.font.SysFont('Arial', 14, True, False)
        x_addition = self.x_addition if optimized else 0

        for i, elevator in enumerate(self.simulations[optimized].elevators):
            elevator_people[i] = font.render(str(len(elevator.people)), True, self.black)
            self.screen.blit(elevator_people[i], [(self.base_x + 9 + (20 * i)) + x_addition, self.base_y + 25])

    def draw_building(self, optimized):
        x = self.base_x + self.x_addition if optimized else self.base_x
        self.screen.blit(self.base, (x - 4, self.base_y))

        for i in range (0, Simulation.total_floors - 1):
            self.screen.blit(self.floor, (x, (self.base_y - 12) - (i * 12)))
        self.screen.blit(self.roof, (x, (self.base_y - 12) - ((Simulation.total_floors) * 12)))
        self.screen.blit(self.floor, (x, (self.base_y + 40)))

    def draw_elevator_square(self, optimized):
        x = self.base_x + 5
        y = self.base_y + 2

        width = 18
        height = 8

        y_move = 12
        x_move = 19

        y_pos = [y]*3
        x_pos = [x]*3

        for i, elevator_floor in enumerate(x.curr_floor for x in self.simulations[optimized].elevators):
            y_pos[i] -= elevator_floor * y_move

        x_addition = 350 if optimized else 0
        for i in range(3):
            x_pos[i] += i * x_move + x_addition

        elevator_rect = [0]*3

        for i in range(3):
            elevator_rect[i] = pygame.rect.Rect((x_pos[i], y_pos[i], width, height))
            pygame.draw.rect(self.screen, [255, 255, 0], elevator_rect[i])

"""

def drawBuilding(mode, maxFloors):

    if mode == "normal":
        x = base_x
    else:
        x = base_x + 350

    screen.blit(base, (x - 4, base_y))

    for i in range (0, maxFloors):
        screen.blit(floor, (x, (base_y - 12) - (i * 12)))

    screen.blit(roof, (x, (base_y - 12) - ((maxFloors + 1) * 12)))
    screen.blit(floor, (x, (base_y + 40)))

def draw(elevators_floor):

    #draw_normal_building(simulation[0], 0)
    #draw_optimized_building(simulation[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(white)

    drawBuilding("optimize", maxFloors)
    drawBuilding("normal", maxFloors)

    floor_people = {}
    elevator_people = {}

    x = base_x + 5
    y = base_y + 2

    width = 18
    height = 8

    y_move = 12
    x_move = 19

    y_pos = [y, y, y]
    x_pos = [x, x, x]

    font = pygame.font.SysFont("Calibri", 14, True, False)

    for i, elevator_floor in enumerate(elevators_floor):
        y_pos[i] -= elevator_floor * y_move

    for i in range(3):
        x_pos[i] += i * x_move

    normalRect = [0,0,0]
    optimizedRect = [0,0,0]

    for i in range(3):
        normalRect[i] = pygame.rect.Rect((x_pos[i], y_pos[i], width, height))
        optimizedRect[i] = pygame.rect.Rect((x_pos[i] + 350, y_pos[i], width, height))

        pygame.draw.rect(screen, [255, 255, 0], normalRect[i])
        pygame.draw.rect(screen, [0, 255, 0], optimizedRect[i])

        #elevator_people[i] = font.render(str(elevators_floor[1]),True, black)
        #screen.blit(elevator_people[i], [((base_x + 5) + (25 * i)), (base_y + 26)])

    for i in range (maxFloors):
        #screen.blit(floor_people[i], [base_x - 10, (base_y - 22)])
        floor_people[i] = font.render(str(elevators_floor[1]),True, black)
        screen.blit(floor_people[i], [base_x - 10, ((base_y - 10) - 12 * i)])

    pygame.display.flip()



while True:
    for i in range (maxFloors):
        for j in range (maxFloors):
            for k in range (maxFloors):
                draw([i,j,k])
"""
