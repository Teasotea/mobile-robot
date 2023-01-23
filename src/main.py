import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pygame

from constant.constants import BLOCK_SIZE as BS, GRID_SIZE
from entity.charger.Charger import Charger
from entity.grid.Grid import Grid
from entity.robot.Battery import Battery
from entity.robot.Robot import Robot
from service.CanGenerator import CanGenerator


def draw_rectangle(x, y, grid, scroll, display):
    if grid.matrix[x][y] == 1:
        img_brick_wall = pygame.image.load("src/resources/brick-wall.png")
        img_brick_wall = pygame.transform.scale(img_brick_wall, (BS, BS))
        display.blit(img_brick_wall, ((x - scroll[0]) * BS, (y - scroll[1]) * BS))
    if grid.matrix[x][y] == 2:
        img_charger = pygame.image.load("src/resources/charger.png")
        display.blit(img_charger, ((x - scroll[0] - 1) * BS, (y - scroll[1] - 1) * BS))


def handle_pressed_keys(keys, robot, display_scroll):
    if not robot.can_move():
        return display_scroll
    changed = False
    if keys[pygame.K_LEFT] \
            and not grid.isWall(robot.x + display_scroll[0] - 1, robot.y + display_scroll[1]):
        display_scroll[0] -= 1
        changed = True
    if keys[pygame.K_RIGHT] \
            and not grid.isWall(robot.x + display_scroll[0] + 1, robot.y + display_scroll[1]):
        display_scroll[0] += 1
        changed = True
    if keys[pygame.K_UP] \
            and not grid.isWall(robot.x + display_scroll[0], robot.y + display_scroll[1] - 1):
        display_scroll[1] -= 1
        changed = True
    if keys[pygame.K_DOWN] \
            and not grid.isWall(robot.x + display_scroll[0], robot.y + display_scroll[1] + 1):
        display_scroll[1] += 1
        changed = True

    if changed:
        grid.research(robot.x + display_scroll[0], robot.y + display_scroll[1])

    return display_scroll


def handle_exit(grid):
    probs = grid.get_researched_prob_matrix()
    plt.imshow(probs, cmap='hot', interpolation='nearest')
    plt.show()

    sys.exit()


if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode((1200, 1200))
    pygame.display.set_caption('Mobile Robot')

    clock = pygame.time.Clock()

    display_scroll = [-GRID_SIZE // 2 + 1, -GRID_SIZE // 2 + 1]

    robot = Robot(GRID_SIZE // 2, GRID_SIZE // 2)

    grid = Grid()
    charger = Charger(1, 1)
    grid.setCharger(charger)

    can_generator = CanGenerator()

    last_charged = time.time()
    while True:
        display.fill((24, 164, 86))

        [handle_exit(grid) if event.type == pygame.QUIT else "" for event in pygame.event.get()]

        robot.main(display)

        can_generator.generate(grid)

        if can_generator.isNotEmpty():
            x = robot.x + display_scroll[0]
            y = robot.y + display_scroll[1]
            can = can_generator.has_can_near(x, y)
            if can is not None and robot.can_collect_can():
                can_generator.remove(can[0], can[1])
                robot.collect_can()
            else:
                can_generator.draw_cans(display, display_scroll)

        [draw_rectangle(
            x=i,
            y=j,
            grid=grid,
            scroll=display_scroll,
            display=display
        ) if element > 0 else 0 for (i, j), element in np.ndenumerate(grid.matrix)]

        robot.update(display)

        if abs(robot.x - (charger.x - display_scroll[0])) <= 1 \
                and abs(robot.y - (charger.y - display_scroll[1])) <= 1:
            robot.get_battery(5)
            robot.clean_cans()
            last_charged = time.time()
        else:
            diff = int(time.time() - last_charged)
            robot.dying_damage(diff * 10)
            last_charged += diff

        keys = pygame.key.get_pressed()
        display_scroll = handle_pressed_keys(keys, robot, display_scroll)

        clock.tick(15)
        pygame.display.update()
