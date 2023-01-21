import pygame
import sys

from constants import BLOCK_SIZE
from robot import Robot

pygame.init()

display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

display_scroll = [0, 0]

player = Robot(400, 300, BLOCK_SIZE, BLOCK_SIZE)

while True:
    display.fill((24, 164, 86))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    player.main(display)

    keys = pygame.key.get_pressed()

    pygame.draw.rect(display, (255, 255, 255), (100 - display_scroll[0], 100 - display_scroll[1], BLOCK_SIZE, BLOCK_SIZE))

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        display_scroll[0] -= BLOCK_SIZE
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        display_scroll[0] += BLOCK_SIZE
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        display_scroll[1] -= BLOCK_SIZE
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        display_scroll[1] += BLOCK_SIZE

    clock.tick(20)
    pygame.display.update()