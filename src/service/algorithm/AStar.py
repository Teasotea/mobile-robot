import numpy as np

from entity.robot.Robot import Robot


class AStar:
    def __init__(self, grid, cans, robot: Robot):
        self.grid = grid
        self.cans = cans
        self.robot = robot

    def nullHeuristic(self):
        return 0

    def manhattanHeuristic(self, can):
        robot_x, robot_y = self.robot.getCurrentPosition()
        can_x, can_y = can
        return abs(robot_x - can_x) + abs(robot_y - can_y)

    def pickCan(self):
        min_dist = 10000
        min_can = -1
        for can in self.cans:
            manh_dist = self.manhattanHeuristic(can)
            if manh_dist < min_dist:
                min_dist, min_can = manh_dist, can
        self.cans.remove(min_can)
        return min_can

    def possibleDirections(self):
        return [
            (0, 0),
            (1, 0),
            (0, 1),
            (-1, 0),
            (-1, 0)
        ]

    def getSuccessors(self, current):
        # current = self.robot.getCurrentPosition()
        successors = []
        for direction in self.possibleDirections():
            possible_successor = current + direction
            if self.grid.matrix[possible_successor[0]][possible_successor[1]]:
                successors.append(possible_successor)
        return successors

    def solve(self):
        minimal_path = []
        destination = (1, 1)

        self.cans.append(destination)

        while len(self.cans) > 0:
            dist, path, visited = dict(), dict(), dict()

            start = self.robot.getCurrentPosition()
            end = self.pickCan()

            visited = [start]
            current = [start]
            while len(current) > 0:
                v = current.pop()
                for successor in self.getSuccessors(v):
                    if successor not in visited:
                        visited.append(successor)
                        current.append(successor)
                        dist[successor] += 1
                        path[successor] = v
            if end in dist.keys():
                self.robot.moveTo(end)
                print("path found")
            else:
                print("No path...")

        # restore path and visualize it
        # stats for solution
