import numpy as np

from constant.constants import GRID_SIZE


class Collector:
    def __init__(self):
        self.visited = np.zeros(shape=(GRID_SIZE, GRID_SIZE))
        self.total_count = 0

    def isVisited(self, vertex):
        x, y = vertex
        return self.visited[x][y]

    # def isVisited(self, x, y):
    #     return self.visited[x][y] > 0

    def visit(self, vertex):
        x, y = vertex
        self.visited[x][y] += 1
        self.total_count += 1

    def getResearchedProbMatrix(self):
        return self.visited / self.total_count
