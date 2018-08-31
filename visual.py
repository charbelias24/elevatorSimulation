import sys, pygame
import time

#maxFloors = int(input ("please enter the height of the building : "))

pygame.init()

size = width, height = 720, 720

speed = [2, 2]

white = 255, 255, 255
black = 0, 0, 0

base_y = 500
base_x = 160

screen = pygame.display.set_mode(size)

base = pygame.image.load("pictures/base.png")
floor = pygame.image.load("pictures/floor.png")
roof = pygame.image.load("pictures/roof.png")

def draw(elevators_floor):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(white)

    drawBuilding("optimize", maxFloors)
    drawBuilding("normal", maxFloors)

    #font = pygame.font.SysFont('Calibri', 25, True, False)
    #text = font.render("My text",True, black)
    #screen.blit(text, [250, 250])

    x = base_x + 5
    y = base_y + 2

    width = 18
    height = 8

    y_move = 12
    x_move = 19

    y_pos = [y, y, y]
    x_pos = [x, x, x]

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

    pygame.display.flip()

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
'''
while True:
    for i in range (maxFloors):
        for j in range (maxFloors):
            for k in range (maxFloors):
                draw([i,j,k])

'''
