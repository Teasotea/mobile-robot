import sys

import numpy as np
import pygame

from constant.constants import BLOCK_SIZE, ROBOT_START_X, ROBOT_START_Y, GRID_SIZE
from entity.robot import Robot


def draw_rectangle(x, y):
    pygame.draw.rect(display, (255, 255, 255), (x, y, BLOCK_SIZE, BLOCK_SIZE))


if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode((1200, 1200))
    clock = pygame.time.Clock()

    display_scroll = [0, 0]

    player = Robot(ROBOT_START_X, ROBOT_START_Y, BLOCK_SIZE, BLOCK_SIZE)

    grid = np.zeros(shape=(GRID_SIZE, GRID_SIZE))
    for (i, j), _ in np.ndenumerate(grid):
        if i in [0, GRID_SIZE - 1] or j in [0, GRID_SIZE - 1]:
            grid[i][j] = 1

    while True:
        display.fill((24, 164, 86))

        [sys.exit() if event.type == pygame.QUIT else "" for event in pygame.event.get()]

        player.main(display)

        [draw_rectangle(
            x=(i - display_scroll[0]) * BLOCK_SIZE,
            y=(j - display_scroll[1]) * BLOCK_SIZE
        ) if element else 0 for (i, j), element in np.ndenumerate(grid)]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and display_scroll[0] > -ROBOT_START_X // BLOCK_SIZE + 1:
            display_scroll[0] -= 1
        if keys[pygame.K_RIGHT] and display_scroll[0] < 33:
            display_scroll[0] += 1
        if keys[pygame.K_UP] and display_scroll[1] > -ROBOT_START_Y // BLOCK_SIZE + 1:
            display_scroll[1] -= 1
        if keys[pygame.K_DOWN] and display_scroll[1] < 39:
            display_scroll[1] += 1

        clock.tick(20)
        pygame.display.update()
