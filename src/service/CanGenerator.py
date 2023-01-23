import random
import time

import pygame

from constant.constants import BLOCK_SIZE as BS


class CanGenerator:
    def __init__(self):
        self.cans = []
        self.last_time = time.time()

    def remove(self, x, y):
        if self.isNotEmpty():
            self.cans.remove((x, y))

    def get_current_can(self):
        return self.cans[0] if self.isNotEmpty() else None

    def generate(self, grid):
        now = time.time()
        if int(now - self.last_time) >= 7:
            x, y = random.randint(3, 55), random.randint(3, 55)
            if not grid.matrix[x][y] and not self.has_can_at(x, y):
                self.cans.append((x, y))
                print(f'Can was generated at {x, y}')
                self.last_time = now

    def isNotEmpty(self):
        return len(self.cans) != 0

    def isEqual(self, x, y):
        if not self.isNotEmpty():
            return False
        return self.cans[0][0] == x and self.cans[0][1] == y

    def draw_cans(self, screen, scroll):
        for can in self.cans:
            pygame.draw.rect(screen, (255, 0, 0), (
                (can[0] - scroll[0]) * BS,
                (can[1] - scroll[1]) * BS,
                BS, BS))

    def has_can_at(self, x, y):
        return (x, y) in self.cans
