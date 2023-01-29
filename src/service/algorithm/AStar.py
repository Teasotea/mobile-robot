import numpy as np

from entity.robot.Robot import Robot


class AStar:
    def __init__(self, grid, cans, robot: Robot, scroll):
        self.grid = grid
        self.cans = cans
        self.robot = robot
        self.scroll = scroll

    def nullHeuristic(self):
        return 0

    @property
    def robotCoordinates(self):
        robot_x, robot_y = self.robot.getCurrentPosition()
        return robot_x + self.scroll[0], robot_y + self.scroll[1]

    def manhattanHeuristic(self, can):
        robot_x, robot_y = self.robotCoordinates
        can_x, can_y = can
        return abs(robot_x - can_x) + abs(robot_y - can_y)

    def pickCan(self):
        min_dist = 10000
        min_can = -1
        for can in self.cans:
            if can == (2, 2) and len(self.cans) > 1:
                continue
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
            (0, -1)
        ]

    def getSuccessors(self, current):
        # current = self.robot.getCurrentPosition()
        successors = []
        for direction in self.possibleDirections():
            possible_successor = current[0] + direction[0], current[1] + direction[1]
            if self.grid.matrix[possible_successor[0]][possible_successor[1]] == 0:
                successors.append(possible_successor)
        return successors

    def solve(self):
        minimal_path = []
        destination = (2, 2)

        self.cans.append(destination)

        while len(self.cans) > 0:
            dist, path = dict(), dict()

            start = self.robotCoordinates
            end = self.pickCan()

            visited = [start]
            current = [start]
            path[start] = -1
            while len(current) > 0:
                if end in visited:
                    break
                v = current.pop(0)
                for successor in self.getSuccessors(v):
                    if successor not in visited:
                        visited.append(successor)
                        current.append(successor)
                        # dist[successor] += 1
                        path[successor] = v
            if end in visited:
                self.scroll[0] = end[0] - self.robot.x
                self.scroll[1] = end[1] - self.robot.y

                ans = []
                temp = end
                while temp != -1:
                    ans.append(temp)
                    temp = path[temp]
                ans = ans[::-1]
                minimal_path += ans
                if end == destination:
                    print(ans)
            else:
                print(f"No path between {start} and {end}")

        return minimal_path
