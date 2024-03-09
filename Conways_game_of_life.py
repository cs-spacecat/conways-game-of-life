import pygame
from sys import exit

# standard setup
pygame.init()
screen = pygame.display.set_mode((2020, 1100))
pygame.display.set_caption("Conway's game of life")
clock = pygame.time.Clock()

# deciding the size of a cell
cell_size = 20
# list with all the positions of the cell
pos_list = []
# boolean for showing the squares (or not)
display_squares = False
# list with all the colors of the game
color_list = ["purple", "white", "red", "blue", "green", "yellow", "brown", "grey"]
# the color that is currently used
color = 0
# variable for advancing the state of the game continuously
advance_continuously = False
# how fast the program should advance continuously
tempo = 5
# list for the booleans for moving the camera
moving_list = [0, 0, 0, 0]
# counting the frames of the game
frames = 0
# variable for reducing the speed of the camera (otherwise the camera would scroll every frame)
frame_camera_reduce = 0
# variable for reducing the amount of states that are displayed in one second
frame_state_reduce = 0
# font of the game
font = pygame.font.Font("Pixeltype.ttf", 45)

def save_cells_onto_file():
    # function for saving the cells (via transferring them onto a different cell)
    global pos_list
    # opening the file
    with open("saved_cells.txt", "w") as sc:
        for cell in pos_list:
            sc.write(str(cell))
            # writing the words not in one row
            sc.write("\n")

def load_cells():
    # loading in the saved cells from the file saved_cells (just look up Project 2)
    # the tuple (as a string) is going to be stored in two variables that change
    # the comma. These will then be aded as a integer to the tuple
    global pos_list
    with open("saved_cells.txt", "r") as sc: 
        for tuple in sc:
            first_num = ""
            second_num = ""
            iterate_string = tuple
            change_num = False
            
            for c in iterate_string:
                if c in "0123456789":
                    if not change_num: first_num += c
                    else             : second_num += c
                elif c == ",": change_num = True
            
            pos_list.append((int(first_num), int(second_num)))

def paste_copy(number_of_copy, mouse_cell_x, mouse_cell_y):
    # function for pasting predeclared cells
    global pos_list
    copy_list = [
        [(mouse_cell_x + 2, mouse_cell_y), (mouse_cell_x + 2, mouse_cell_y + 1), (mouse_cell_x + 2, mouse_cell_y + 2), (mouse_cell_x + 1, mouse_cell_y + 2), (mouse_cell_x, mouse_cell_y + 1)]

        ]
    # 0: Glider
    for cells in copy_list[number_of_copy]:
        pos_list.append(cells)

def check_for_copy_inputs(pressed_key):
    # function for determinig if the user has pressed a number (and the copy the cells with the according copy slot)
    # dictionary for getting the number in pygame.K_[number] e.g.: pygame.K_0: 0
    global cell_size
    # checking if the key is a number from 1 to 10
    if pressed_key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,]:
        # transferring the inputs to actual numbers 
        dic = {
            pygame.K_0: 0,
            pygame.K_1: 1,
            pygame.K_2: 2,
            pygame.K_3: 3,
            pygame.K_4: 4,
            pygame.K_5: 5,
            pygame.K_6: 6,
            pygame.K_7: 7,
            pygame.K_8: 8,
            pygame.K_9: 9 
            } 
        copy_index = dic[pressed_key]
        # actually pasting the copies (via the function)
        paste_copy(copy_index, pygame.mouse.get_pos()[0] // cell_size, pygame.mouse.get_pos()[1] // cell_size)

def around_cell(x, y):
    # function for returning a list with the positions of the cells around the cell which is the parameter
    # used for checking the cells around the targeted cell
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

def amount_neighbours(x, y):
    # function for determining how many neighbours a cell has
    global pos_list
    n = 0
    for cell in around_cell(x, y):
        if cell in pos_list:
            n += 1
    return n

def list_of_dead_neighbours(x, y):
    # function that returns a list of all dead neighbours
    lis = []
    for cell in around_cell(x, y):
        if cell not in pos_list:
            lis.append(cell)
    return lis

def new_cell_possible(x, y):
    # function for determining if a new cell can spawn around the targeted cell
    global pos_list
    ret_list = []
    # determining if there are exactly two neighbours
    if amount_neighbours(x, y) == 2 or amount_neighbours(x, y) == 1:
        # iterating over the dead neighbours to see if one of them has exactly three neighbours
        for cell in list_of_dead_neighbours(x, y):
            if amount_neighbours(cell[0], cell[1]) == 3:
                # if so then adding the cell to a list that will be returned
                ret_list.append(cell)
        return ret_list
    else:
        return "none"

def cell_is_alive(x, y):
    # function for checking if the clicked cell already exists
    global pos_list
    for pos in pos_list: if pos == (x, y): return True
    return False
    # alternative solution lmao: return [(0, 0) for pos in pos_list if pos == (x, y)]

def display_all_cells():
    # function for displaying all cells (via iterating over them in the pos_list)
    global pos_list, cell_size, color_list, color
    for pos in pos_list:
        # drawing the rectangle from the position of the cell and the lengths (and heights) by multiplying
        # with the cell size)
        pygame.draw.rect(screen, pygame.Color(color_list[color]),
                         pygame.rect.Rect(pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size))

def create_new_cell(x, y):
    # creating a new cell with the position as a parameter
    global pos_list
    # checking if the cell is already there
    if not cell_is_alive(x, y):
        pos_list.append((x, y))
    # "killing" the cell if it is already alive
    else:
        pos_list.remove((x, y))

def advance_state():
    # function for advancing the state of the game by one (killing overcrowded or isolated cells and creating new ones)
    global pos_list
    # checking for every currently living cell
    dead_cells = []
    new_cells = []
    for pos in pos_list:
        # checking if the cell should die (if it has one or zero or four or more neighbouring cells)
        neighbouring_cells = amount_neighbours(pos[0], pos[1])
        if neighbouring_cells <= 1 or neighbouring_cells >= 4:
            # appending the cell into the dead_cells list to delete it later
            dead_cells.append(pos)
        # checking if the conditions are met for a new cell to be created
        if not new_cell_possible(pos[0], pos[1]) == "none":
            # adding the cells to a list of cells which will be created
            # (sometimes there are two that's why the for statement)
            for new_cell in new_cell_possible(pos[0], pos[1]):
                if new_cell not in new_cells:
                    new_cells.append(new_cell)
    # creating a list to iterate over
    iterate_list = pos_list.copy()
    # now deleting the cells that should be deleted
    for cell2 in iterate_list:
        # checking if the cell should be deleted
        if cell2 in dead_cells:
            pos_list.remove(cell2)
    # creating the cells that should be created
    for new_cell2 in new_cells:
        pos_list.append(new_cell2)

def make_squares():
    # function for making the field of the game
    global cell_size
    x = cell_size
    for i in range(2020 // cell_size):
        pygame.draw.line(screen, pygame.Color(color_list[color]), (x, 0), (x, 1100), 1)
        x += cell_size
    x = cell_size
    for i in range(1100 // cell_size):
        pygame.draw.line(screen, pygame.Color(color_list[color]), (0, x), (2020, x))
        x += cell_size

def change_cell_size(operator):
    # function for changing the cell_size when the user scrolls
    # bigger when the user scrolls up and vice versa
    global cell_size
    if operator == "plus":
        if cell_size < 100:
            cell_size += 1
    elif operator == "minus":
        if cell_size > 2:
            cell_size -= 1

def move_camera(change_x, change_y):
    # function for moving the "camera"
    global pos_list
    iterate_list = pos_list.copy()
    for cell in iterate_list:
        # converting the tuple to a list so we can change it
        c = list(cell)
        # changing the list
        c[0] += change_x
        c[1] += change_y
        pos_list.append(tuple(c))
        pos_list.remove(cell)

def moving_camera_continuously():
    # function for iterating over the moving list and moving the camera accordingly
    global moving_list
    if moving_list[0] == 1:
        move_camera(0, 1)
    if moving_list[1] == 1:
        move_camera(0, -1)
    if moving_list[2] == 1:
        move_camera(1, 0)
    if moving_list[3] == 1:
        move_camera(-1, 0)

def updating_bool_for_camera(button, pressed_or_released):
    # function for checking what character of wasd is pressed and if the corresponding booleans should be True or False
    global moving_list
    if button == pygame.K_w:
        moving_list[0] = pressed_or_released
    if button == pygame.K_s:
        moving_list[1] = pressed_or_released
    if button == pygame.K_a:
        moving_list[2] = pressed_or_released
    if button == pygame.K_d:
        moving_list[3] = pressed_or_released

def inputs_for_zooming(user_inputs):
    # function for checking if the cell_size should be made bigger or smaller
    # event.button (in this function user_inputs) returns what button on the mouse was pressed (1: leftclick,
    # 2: middleclick, 3: rightclick, # 4: scroll up, 5: scroll down
    # changing the cell size if the user scrolls
    if user_inputs == 4:
        change_cell_size("plus")
    if user_inputs == 5:
        change_cell_size("minus")

def change_color():
    # the name says it all
    global color
    if not color == 7:
        color += 1
    else:
        color = 0

def display_tempo():
    # function for displaying the tempo in the top right corner of the game
    global tempo, color, screen, color_list, font
    text = font.render(f"Tempo: {tempo}", True, pygame.Color(color_list[color]))
    rect = text.get_rect(topleft=(0, 0))
    screen.blit(text, rect)

def display_running():
    # function for displaying the tempo in the top right corner of the game
    global tempo, color, screen, color_list, font
    text = font.render("fast mode", True, pygame.Color(color_list[color]))
    rect = text.get_rect(topright=(2020, 0))
    screen.blit(text, rect)

def execute_standard_functions():
    # function purely to make the code (the game loop) more readable
    # background color (has to be set otherwise you can't easily delete the cells)
    global frame_camera_reduce, clock, frame_state_reduce, frames, display_squares, tempo
    screen.fill(pygame.Color("black"))
    # displaying the background squares
    if display_squares:
        make_squares()
    # displaying all cells
    display_all_cells()
    # making the camera faster if the cells are smaller
    frame_camera_reduce = round(cell_size * 0.1)
    if frame_camera_reduce == 0:
        frame_camera_reduce = 1
    # moving the camera if at least one direction is pressed
    if frames % frame_camera_reduce == 0:
        if not moving_list == [0, 0, 0, 0]:
            moving_camera_continuously()
    # taking control over the speed of the continuous advancing of the game state
    frame_state_reduce = 20 - tempo * 2 + 1
    # displaying the tempo of the game
    display_tempo()
    # advancing continuously if the user wants at capped frames
    if advance_continuously:
        display_running()
        if frames % frame_state_reduce == 0:
            advance_state()
    # updating the screen
    pygame.display.update()
    # updating the frames of the game
    if not frames == 128:
        frames += 1
    else:
        frames = 0
    # keeping the games at 120 fps
    clock.tick(120)

def change_tempo(change):
    # function for changing the speed/tempo of the continuous advancing
    global tempo
    tempo += change
    if tempo == 11:
        tempo = 10
    elif tempo == 0:
        tempo = 1

def exit_game():
    # I think this is kinda obvious isn't it?
    save_cells_onto_file()
    pygame.quit()
    exit()

# loading the cells
load_cells()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        if event.type == pygame.KEYDOWN:
            # printing the pos_list if the user wants
            if event.key == pygame.K_t:
                print(f"Cell_list: {pos_list}")
            # changing the color of the game
            if event.key == pygame.K_c:
                change_color()
            # deleting all cells if the user presses "b"
            if event.key == pygame.K_b:
                pos_list = []
            # making the squares invisible when the user presses "v"
            if event.key == pygame.K_v:
                display_squares = not display_squares
            # advancing the state of the game by one if the user presses right
            if event.key == pygame.K_RIGHT:
                advance_state()
            # advancing the state of the game continuously if the user presses "space"
            if event.key == pygame.K_SPACE:
                advance_continuously = not advance_continuously
            # turning the booleans for the camera on if pressed
            updating_bool_for_camera(event.key, 1)
            if event.key == pygame.K_UP:
                change_tempo(1)
            if event.key == pygame.K_DOWN:
                change_tempo(-1)
            # closing the game if the user presses escape
            if event.key == pygame.K_ESCAPE:
                exit_game()
            # checking if the user wants to copy anything
            check_for_copy_inputs(event.key)
        if event.type == pygame.KEYUP:
            # moving the camera using wasd
            updating_bool_for_camera(event.key, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed() == (True, False, False):
                # creating a new cell when the user clicks in the position of the mouse
                create_new_cell(pygame.mouse.get_pos()[0] // cell_size, pygame.mouse.get_pos()[1] // cell_size)
            # zooming
            inputs_for_zooming(event.button)
    # doing everything that needs to be done every frame
    execute_standard_functions()
