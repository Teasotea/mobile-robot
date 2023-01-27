import random
import time

import pygame

from constant.constants import BLOCK_SIZE as BS


class CanGenerator:
    def __init__(self):
        self.cans = []
        self.img_can = pygame.image.load("src/resources/can.png")
        self.img_can = pygame.transform.scale(self.img_can, (2 * BS, 2 * BS))
        self.last_time = time.time()

    def remove(self, x, y):
        if self.isNotEmpty():
            self.cans.remove((x, y))

    def getCurrentCan(self):
        return self.cans[0] if self.isNotEmpty() else None

    def generateOnTime(self, grid):
        now = time.time()
        if int(now - self.last_time) < 7:
            return
        x, y = self.generate()
        if not grid.matrix[x][y] and not self.hasCanAt(x, y):
            self.cans.append((x, y))
            print(f'Can was generated at {x, y}')
            self.last_time = now

    def generate(self):
        return random.randint(3, 55), random.randint(3, 55)

    def isNotEmpty(self):
        return len(self.cans) != 0

    def isEmpty(self):
        return len(self.cans) == 0

    def isEqual(self, x, y):
        if not self.isNotEmpty():
            return False
        return self.cans[0][0] == x and self.cans[0][1] == y

    def drawCans(self, screen, scroll):
        for can in self.cans:
            screen.blit(self.img_can, ((can[0] - scroll[0]) * BS, (can[1] - scroll[1]) * BS))

    def hasCanNear(self, x, y):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if self.hasCanAt(x + i, y + j):
                    return x + i, y + j
        return None

    def hasCanAt(self, x, y):
        return (x, y) in self.cans

    def generate10(self, grid):
        while len(self.cans) < 10:
            x, y = self.generate()
            if not grid.matrix[x][y] and not self.hasCanAt(x, y):
                self.cans.append((x, y))
