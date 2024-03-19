from typing import Literal, Any  # moar typehints
import pygame
from sys import exit

fieldSize = 10
cameraPos = (0, 0)
cellSize = 20  # size of one cell

# 0: cell dead
# 1: cell alive
field = [[0 for _ in range(fieldSize)] for _ in range(fieldSize)]  # field grid

pygame.init()
screen = pygame.display.set_mode((fieldSize * cellSize + 1, fieldSize * cellSize + 1))
pygame.display.set_caption("Conway's game of life")
clock = pygame.time.Clock()

# helper functions
def pixelPos2relPos(pos: list) -> tuple[int, int]:
    global cellSize
    return ((pos[0] - cameraPos[0]) // cellSize, (pos[1] - cameraPos[1]) // cellSize)

# main functions
def createNewCell(pos: list[int, int], state: Literal[1, 0]) -> None:
    global fieldSize
    field[pos[1]][pos[0]] = state

# visual functions
def drawGrid() -> None:
    global cellSize, fieldSize
    endOfGrid = fieldSize * cellSize
    for i in range(fieldSize + 1):
        pygame.draw.line(screen, "gray", (i * cellSize, 0), (i * cellSize, endOfGrid))
        pygame.draw.line(screen, "gray", (0, i * cellSize), (endOfGrid, i * cellSize))

def drawField() -> None:
    global cellSize, field
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, "gray", pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize))

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
            try:
                if tempfield[offsetY + y][offsetX + x]:
                    alive += 1
            except IndexError:
                pass
    return alive - tempfield[y][x]

def handleCells(x: int, y: int, tempfield) -> None:
    global field
    neighbors = listNeighbors(x, y, tempfield)

    if tempfield[y][x]:  # if cell is alive
        if neighbors <= 1 or neighbors >= 4:
            field[y][x] = 0
    else:
        if neighbors == 3:
            field[y][x] = 1

def apply_Cells() -> None:
    tempfield = field[:]  # so that the new cells dont interfere w/ the old ones
    for y, row in enumerate(tempfield):
        for x, _ in enumerate(row):
            handleCells(x, y, tempfield)


def main() -> None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # creating a cell
            if pygame.mouse.get_pressed() == (True, False, False):
                # creating a new cell when the user clicks in the position of the mouse
                mPos = pygame.mouse.get_pos()
                createNewCell(pixelPos2relPos(mPos), 1)
                print(listNeighbors(*pixelPos2relPos(mPos), field))

            # deleting a cell
            elif pygame.mouse.get_pressed() == (False, False, True):
                # deleting cell when the user clicks in the position of the mouse
                mPos = pygame.mouse.get_pos()
                createNewCell(pixelPos2relPos(mPos), 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    apply_Cells()


        # visual stuff
        screen.fill(pygame.Color("black"))
        drawGrid()
        drawField()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
