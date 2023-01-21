import pygame


class Robot:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def main(self, display):
        pygame.draw.rect(display, (105, 105, 105),
                         (self.x - self.width, self.y - self.height, 3 * self.width, 3 * self.height))
        pygame.draw.rect(display, (0, 0, 0), (self.x, self.y, self.width, self.height))
