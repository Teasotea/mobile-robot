import random

import numpy as np

from constant.constants import GRID_SIZE
from entity.grid.TCell import TCell


class Grid:
    def __init__(self):
        self.matrix = np.zeros(shape=(GRID_SIZE, GRID_SIZE))
        self.researched = np.zeros(shape=(GRID_SIZE, GRID_SIZE))
        self.total_researched_cells = 0

        n_rows = GRID_SIZE // random.randint(3, 4)
        n_columns = GRID_SIZE // random.randint(3, 4)
        borders = [0, GRID_SIZE - 1]
        for (i, j), _ in np.ndenumerate(self.matrix):
            if i in borders or j in borders:
                self.matrix[i][j] = TCell.WALL.value
            else:
                if i % n_rows == 0 or j % n_columns == 0:
                    self.matrix[i][j] = TCell.WALL.value
                if i % n_rows == 0 and j % n_columns == 4:
                    self.matrix[i][j] = TCell.EMPTY.value
                if i % n_rows == 2 and j % n_columns == 0:
                    self.matrix[i][j] = TCell.EMPTY.value

    def isWall(self, x, y):
        return self.matrix[x][y] == TCell.WALL.value

    def research(self, x, y):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                self.total_researched_cells += 1
                if 0 <= x + i < GRID_SIZE and 0 <= y + j < GRID_SIZE and not self.matrix[x + i][y + j]:
                    self.researched[x + i][y + j] += 1

    def setCharger(self, charger):
        self.matrix[charger.x][charger.y] = TCell.CHARGER.value

    def get_researched_prob_matrix(self):
        return self.researched / self.total_researched_cells
