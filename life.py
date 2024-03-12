import pygame
from sys import exit

fieldSize = 50
# 0: cell dead
# 1: cell alive
cellSize = 20 # length of one 
field = [[0 for _ in range(fieldSize)] for _ in range(fieldSize)]
cameraPos = (0, 0)

pygame.init()
screen = pygame.display.set_mode((fieldSize * cellSize + 1 , fieldSize * cellSize + 1))
pygame.display.set_caption("Conway's game of life")
clock = pygame.time.Clock()

# helper functions
def pixelPos2relPos(pos):
    global cellSize
    return ((pos[0] - cameraPos[0]) // cellSize, (pos[1] - cameraPos[1]) // cellSize)

# main functions
def createNewCell(pos):
    global fieldSize
    field[pos[1]][pos[0]] = 1

# visual functions
def drawGrid():
    global cellSize, fieldSize
    endOfGrid = fieldSize * cellSize
    for i in range(fieldSize + 1): 
        pygame.draw.line(screen, "gray", (i * cellSize, 0), (i * cellSize, endOfGrid))
        pygame.draw.line(screen, "gray", (0, i * cellSize), (endOfGrid, i * cellSize))

def drawField():
    global cellSize, field
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell: 
                pygame.draw.rect(screen, "gray", pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize))

def configHandling(filename: str = "config.ini", conf: list = []):
    global config
    if len(conf) == 0:
        try:
            with open(filename, 'r') as f:
                config = f.read()
        except FileNotFoundError:
            configHandling(conf=[])
    else:
        open(filename, 'w').close()  #* empty file; redundant
        with open(filename, 'w') as f:
            f.write(conf)

def listLiveNeighbors(x: int, y: int) -> int:
    alive = 0
    for offsetY in [-1, 0, 1]:
        for offsetX in [-1, 0, 1]:
            if field[offsetY + y][offsetX + x]: alive += 1
    return alive - field[y][x]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # creating a cell
        if pygame.mouse.get_pressed() == (True, False, False):
            # creating a new cell when the user clicks in the position of the mouse
            mPos = pygame.mouse.get_pos()
            createNewCell(pixelPos2relPos(mPos))
            print(listLiveNeighbors(pixelPos2relPos(mPos)[0], pixelPos2relPos(mPos)[1]))

        # deleting a cell
        elif pygame.mouse.get_pressed() == (False, False, True):
            # creating a new cell when the user clicks in the position of the mouse
            mPos = pygame.mouse.get_pos()
            createNewCell(pixelPos2relPos(mPos))


    # visual stuff
    screen.fill(pygame.Color("black"))
    drawGrid()
    drawField()
    pygame.display.update()
    clock.tick(60)
