import sys, pygame
import time

maxFloors = int(input ("please enter the height of the building : "))

class Visual:
    def __init__(self):
        pygame.init()
        self.size = width, height = 720, 720
        self.speed = [2, 2]
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.base_y = 500
        self.base_x = 160
        self.screen = pygame.display.set_mode(size)
        self.base = pygame.image.load("pictures/base.png")
        self.floor = pygame.image.load("pictures/floor.png")
        self.roof = pygame.image.load("pictures/roof.png")
        self.font = pygame.font.SysFont("Calibri", 14, True, False)

    def draw(self, simulations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        screen.fill(white)

        draw_building(simulation[0], optimized=False)
        draw_building(simluation[1], optimized=True)

    def draw_building(self, simulation, optimized):
        x = base_x + 350 if optimized else base_x
        screen.blit(base, (x - 4, base_y))
        for i in range (0, simulation.total_floors):
            screen.blit(floor, (x, (base_y - 12) - (i * 12)))
        screen.blit(roof, (x, (base_y - 12) - ((maxFloors + 1) * 12)))
        screen.blit(floor, (x, (base_y + 40)))

    def draw_elevator_square(self):
        x = self.base_x + 5
        y = self.base_y + 2

        width = 18
        height = 8

        y_move = 12
        x_move = 19

        y_pos = [y]*3
        x_pos = [x]*3

        for i, elevator_floor in enumerate(elevators_floor):
            y_pos[i] -= elevator_floor * y_move





'''
def draw_normal_building(simulation):
    for i, elevator_floor in enumerate(x.curr_floor for x in simulation.elevators):
        y_pos[i] -= elevator_floor * y_move

def draw_optimized_building(simulation):
    for i, elevator_floor in enumerate():
        y_pos[i] -= elevator_floor * y_move
'''



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
        optimizedRect[i] = pygame.rect.Rect((x_pos[i]+ 350, y_pos[i], width, height))

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
