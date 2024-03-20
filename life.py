from typing import Literal, Any  # more typehints
import pygame
from sys import exit
import copy

# sizes 
fieldSize = 100 # 50
cellSize = 40 # size of one cell
screenSize = (1600, 900)
cameraPos: tuple[int, int] = (-(fieldSize * cellSize - screenSize[0]) / 2, -(fieldSize * cellSize - screenSize[1]) / 2)
# 0: dead cell,  1: alive cell 
field = [[0 for _ in range(fieldSize)] for _ in range(fieldSize)]  # field grid
# speed of panning (2 doubles the seed and 0.5 halfs the dafualt speed)
panSpeed = 0.1

pygame.init()
# screen = pygame.display.set_mode((fieldSize * cellSize + 1, fieldSize * cellSize + 1))
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Conway's game of life")
clock = pygame.time.Clock()

# helper functions
# returns the relative position on the grid given the pixel position on the screen
def pixelPos2relPos(pos: tuple[int, int]) -> tuple[int, int]:
    global cellSize
    return (int((pos[0] - cameraPos[0]) // cellSize), int((pos[1] - cameraPos[1]) // cellSize))

# similar to pixelPos2relPos but with exact values
def pixelPos2relPosEx(pos: tuple[int, int]) -> tuple[int, int]:
    global cellSize
    return ((pos[0] - cameraPos[0]) / cellSize, (pos[1] - cameraPos[1]) / cellSize)

# returns the pixel posiiton on screen given a relative position in the grid 
def relPos2pixelPos(pos: tuple[int, int]) -> tuple[int, int]:
    global cellSize
    return ((pos[0] * cellSize) + cameraPos[0], (pos[1] * cellSize) + cameraPos[1])

# main functions
def createNewCell(pos: list[int, int], state: Literal[1, 0]) -> None:
    global fieldSize
    field[pos[1]][pos[0]] = state

# visual functions
def drawGrid() -> None:
    global cellSize, fieldSize
    endOfGrid = fieldSize * cellSize
    for i in range(fieldSize + 1): 
        pygame.draw.line(screen, "gray", (i * cellSize + cameraPos[0], cameraPos[1]), (i * cellSize + cameraPos[0], endOfGrid + cameraPos[1]))
        pygame.draw.line(screen, "gray", (cameraPos[0], i * cellSize + cameraPos[1]), (endOfGrid + cameraPos[0], i * cellSize + cameraPos[1]))

def drawField() -> None:
    global cellSize, field
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell:
                currentPos = relPos2pixelPos((x, y))
                pygame.draw.rect(screen, "gray", pygame.Rect(currentPos[0], currentPos[1], cellSize, cellSize))

def zoom(scrollDelta: int) -> None:
    global cellSize, cameraPos
    mPos = pygame.mouse.get_pos()
    oldRelPos = pixelPos2relPosEx(mPos)
    cellSize += scrollDelta * 2
    newRelPos = pixelPos2relPosEx(mPos)
    cameraPos = (
        (newRelPos[0] - oldRelPos[0]) * cellSize + cameraPos[0],
        (newRelPos[1] - oldRelPos[1]) * cellSize + cameraPos[1])

def configHandling(filename: str = "config.ini", conf: list = []) -> Any:
    global config
    if len(conf) == 0:
        try:
            with open(filename, 'r') as f:
                config = f.read()
        except FileNotFoundError:  # if no file is found, create one
            configHandling(conf=[])
    else:
        open(filename, 'w').close()  #* empty file; redundant
        with open(filename, 'w') as f:
            f.write(conf)

def listNeighbors(x: int, y: int, tempfield) -> int:
    alive = 0
    for offsetY in [-1, 0, 1]:
        for offsetX in [-1, 0, 1]:
            if tempfield[y + offsetY][x + offsetX]:
                alive += 1
    return alive - tempfield[y][x]

def handleCell(x: int, y: int, tempField) -> None:
    global field
    # skippin the cell if its on the edge of the grid
    if x == 0 or x == fieldSize - 1 or y == 0 or y == fieldSize - 1: return

    neighbors = listNeighbors(x, y, tempField)

    if tempField[y][x]:  # if cell is alive
        if neighbors <= 1 or neighbors >= 4:
            field[y][x] = 0
    else:
        if neighbors == 3:
            field[y][x] = 1

# advances the field by one generation
def advanceGeneration() -> None:
    global field
    tempField = copy.deepcopy(field)  # so that the new cells dont interfere w/ the old ones
    for y, row in enumerate(tempField):
        for x, _ in enumerate(row):
            handleCell(x, y, tempField)


def main() -> None:
    global cameraPos, cellSize, panSpeed
    while True:
        delta = pygame.mouse.get_rel() # needs to be calculatd every iteration in order to work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # creating a cell
            if pygame.mouse.get_pressed() == (True, False, False):
                # creating a new cell when the user clicks in the position of the mouse
                mPos = pygame.mouse.get_pos()
                createNewCell(pixelPos2relPos(mPos), 1)
            # deleting a cell
            elif pygame.mouse.get_pressed() == (False, False, True):
                # deleting cell when the user clicks in the position of the mouse
                mPos = pygame.mouse.get_pos()
                createNewCell(pixelPos2relPos(mPos), 0)
            # panning
            elif pygame.mouse.get_pressed() == (False, True, False):
                # panning with the middle mouse button
                cameraPos = (cameraPos[0] + panSpeed * delta[0], cameraPos[1] + panSpeed * delta[1]); 
            # zooming
            if event.type == pygame.MOUSEWHEEL:
                scrollDelta = event.y
                zoom(scrollDelta)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    advanceGeneration()

        # visual stuff
        screen.fill(pygame.Color("black"))
        drawGrid()
        drawField()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
