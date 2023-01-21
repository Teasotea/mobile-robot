import pygame

from constant.constants import BLOCK_SIZE


class Robot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def main(self, display):
        pygame.draw.rect(display, (105, 105, 105),
                         ( (self.x - 1) * BLOCK_SIZE, (self.y - 1) * BLOCK_SIZE, 3 * BLOCK_SIZE, 3 * BLOCK_SIZE))
        pygame.draw.rect(display, (0, 0, 0), (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
