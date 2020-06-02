import pygame
import collections
import time

import grid
import astar
import game_state
from macros import *


print("(Leave empty for default)")
init_rows = input("How many rows do you want? (default - 20): ")
init_cols = input("What about Columns? (default - 30): ")
the_maze_question = input("Start with random maze? (y/n): ").lower()
while not (the_maze_question == 'y' or the_maze_question == 'n'):
    print("Sorry, I don't understand...")
    the_maze_question = input("Start with random maze? (y/n): ").lower()

init_rows = init_rows if init_rows else 20
init_cols = init_cols if init_cols else 30

main_grid = grid.Grid(int(init_rows), int(init_cols))

if the_maze_question == 'y':
    main_grid.create_maze()

pygame.init()

#Set the size of pygame
total_height = get_total_pixel_height(main_grid.num_of_rows)
total_width = get_total_pixel_width(main_grid.num_of_cols)
WINDOW_SIZE = (total_width, total_height)
screen = pygame.display.set_mode(WINDOW_SIZE)
#create a title
pygame.display.set_caption("A* Pathfinder")

# Loop until the user clicks the close button.
state = game_state.State()


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not state.done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            button = get_button(pygame.mouse.get_pressed())
            if button == MIDDLE:
                state.run = True
                state.started = True
            else:
                state.mouse_down = True
                node = main_grid.get_node_mouse_pos(pygame.mouse.get_pos())
                if not state.running:
                    if can_drag(node.color):
                        state.dragging = True
                        state.special_to_move = node.color
                    else:
                        state.pos = pygame.mouse.get_pos()
                        state.button = button
                        state.drawing = True

        elif event.type == pygame.MOUSEMOTION and state.mouse_down:
            pos = pygame.mouse.get_pos()
            state.pos = pos
            if state.dragging:
                node = main_grid.get_node_mouse_pos(pos)
                moved = main_grid.move_special_color(pos, state.special_to_move)
                if moved and state.started:
                    state.recalculate = True

        elif event.type == pygame.MOUSEBUTTONUP:
            state.cleanup()

    # --- Game logic should go here

    # Creating and Removing Obstacles
    if state.drawing:
        node = main_grid.get_node_mouse_pos(state.pos)

        if state.button == LEFT: # Creates obstacles
            if is_pathing_color(node.color):
                state.recalculate = True
            main_grid.set_color_mouse_pos(state.pos, OBSTACLE)

        if state.button == RIGHT: # Removes obstacles
            if node.color == OBSTACLE and node.checked:
                state.recalculate = True
            if not is_pathing_color(node.color):
                main_grid.set_color_mouse_pos(state.pos, EMPTY)


    if state.run:
        main_grid.clear_pathing()
        astar_pathing = astar.astar_search(main_grid)
        state.running = True
        state.run = False


    if state.running:
        if astar_pathing:          
            node_coor, color = astar_pathing.popleft()
            main_grid.set_color(node_coor, color)
        else:
            state.running = False


    if state.recalculate:
        main_grid.clear_pathing()
        recalculated_pathing = astar.astar_search(main_grid)
        for node_coor, color in recalculated_pathing:
            main_grid.set_color(node_coor, color)
        state.recalculate = False


    # --- Screen-clearing
    screen.fill(BACKGROUND)
 
    # --- Drawing our grid
    for row in range(main_grid.num_of_rows):
        for col in range (main_grid.num_of_cols):
            node = main_grid.get_node((row,col))
            pygame.draw.rect(
                screen,
                node.color,
                [(MARGIN + WIDTH) * col + MARGIN,
                (MARGIN + HEIGHT) * row + MARGIN,
                WIDTH,
                HEIGHT]
                )

    # --- Update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Set framerate
    clock.tick(100)

pygame.quit()
