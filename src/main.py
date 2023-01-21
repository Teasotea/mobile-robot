import random
import sys

import numpy as np
import pygame

from constant.constants import BLOCK_SIZE, GRID_SIZE
from entity.robot import Robot


def draw_rectangle(x, y):
    pygame.draw.rect(display, (255, 255, 255), (x, y, BLOCK_SIZE, BLOCK_SIZE))


# TODO add logging system
if __name__ == "__main__":
    # Initialization
    pygame.init()

    display = pygame.display.set_mode((1200, 1200))
    clock = pygame.time.Clock()

    display_scroll = [0, 0]

    # Player
    robot = Robot(GRID_SIZE // 2, GRID_SIZE // 2)
    # TODO add trash collector for robot

    # Grid
    # TODO create Grid class
    grid = np.zeros(shape=(GRID_SIZE, GRID_SIZE))
    for (i, j), _ in np.ndenumerate(grid):
        if i in [0, GRID_SIZE - 1] or j in [0, GRID_SIZE - 1]:
            grid[i][j] = 1

    # Food
    # TODO generate food randomly once in 5 seconds
    foods = list()
    for i in range(10):
        x = random.randint(1, 55)
        y = random.randint(1, 55)
        foods.append((x, y))

    while True:
        # background color
        display.fill((24, 164, 86))

        # press exit button on window
        [sys.exit() if event.type == pygame.QUIT else "" for event in pygame.event.get()]

        robot.main(display)

        # if len(foods) > 0:
        #     food_x, food_y = foods[0]
        #     if robot.x + display_scroll[0] is food_x \
        #             and robot.y + display_scroll[1] is food_y:
        #         foods.pop()
        #         print(f'The can on position {(food_x, food_y)} was collected into trash')
        #
        #     pygame.draw.rect(display, (255, 0, 0), ((foods[0][0] - display_scroll[0]) * BLOCK_SIZE,
        #                                             (foods[0][1] - display_scroll[1]) * BLOCK_SIZE,
        #                                             BLOCK_SIZE, BLOCK_SIZE))

        # draw grid borders
        [draw_rectangle(
            x=(i - display_scroll[0]) * BLOCK_SIZE,
            y=(j - display_scroll[1]) * BLOCK_SIZE
        ) if element else 0 for (i, j), element in np.ndenumerate(grid)]

        # pressed buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and display_scroll[0] > -GRID_SIZE // 2 + 1:
            display_scroll[0] -= 1
        if keys[pygame.K_RIGHT] and display_scroll[0] < (GRID_SIZE - 1) // 2 - 1:
            display_scroll[0] += 1
        if keys[pygame.K_UP] and display_scroll[1] > -GRID_SIZE // 2 + 1:
            display_scroll[1] -= 1
        if keys[pygame.K_DOWN] and display_scroll[1] < (GRID_SIZE - 1) // 2 - 1:
            display_scroll[1] += 1

        clock.tick(20)
        pygame.display.update()
