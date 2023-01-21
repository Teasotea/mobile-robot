import numpy as np

from constant.constants import GRID_SIZE


class Grid:
    def __init__(self):
        self.matrix = np.zeros(shape=(GRID_SIZE, GRID_SIZE))
        for (i, j), _ in np.ndenumerate(self.matrix):
            if i in [0, GRID_SIZE - 1] or j in [0, GRID_SIZE - 1]:
                self.matrix[i][j] = 1  # FIXME add ENUM for cell types
