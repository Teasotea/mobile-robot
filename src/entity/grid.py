import numpy as np
import random

from constant.constants import GRID_SIZE


class Grid:
    def __init__(self):
        self.matrix = np.zeros(shape=(GRID_SIZE, GRID_SIZE))
        self.researched = np.zeros(shape=(GRID_SIZE, GRID_SIZE))

        n_rows = GRID_SIZE // random.randint(3, 4)
        n_columns = GRID_SIZE // random.randint(3, 4)
        borders = [0, GRID_SIZE - 1]
        for (i, j), _ in np.ndenumerate(self.matrix):
            # room borders
            if i % n_rows == 0 or j % n_columns == 0:
                prob = random.randint(1, 10)
                self.matrix[i][j] = 1 if prob > 1 else 0
            # grid borders
            if i in borders or j in borders:
                self.matrix[i][j] = 1  # FIXME add ENUM for cell types

    def isWall(self, x, y):
        return self.matrix[x][y] == 1

    def research(self, x, y):
        for i in range(x - 1, x + 1):
            for j in range(y - 1, y + 1):
                self.researched[i][j] = 1


