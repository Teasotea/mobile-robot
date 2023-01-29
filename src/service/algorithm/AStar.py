from entity.grid.TCell import TCell
from entity.robot.Robot import Robot


class AStar:
    def __init__(self, grid, cans, robot: Robot, scroll):
        self.grid = grid
        self.cans = cans
        self.robot = robot
        self.scroll = scroll

    @property
    def robotCoordinates(self):
        robot_x, robot_y = self.robot.getCurrentPosition()
        return robot_x + self.scroll[0], robot_y + self.scroll[1]

    @property
    def destination(self):
        return 2, 2

    def manhattanHeuristic(self, can):
        robot_x, robot_y = self.robotCoordinates
        can_x, can_y = can
        return abs(robot_x - can_x) + abs(robot_y - can_y)

    @property
    def nextCan(self):
        min_dist = 10000
        min_can = -1
        for can in self.cans:
            if can == self.destination and len(self.cans) > 1:
                continue
            manh_dist = self.manhattanHeuristic(can)
            if manh_dist < min_dist:
                min_dist, min_can = manh_dist, can
        self.cans.remove(min_can)
        return min_can

    @property
    def possibleDirections(self):
        return [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

    def getSuccessors(self, current):
        successors = []
        for direction in self.possibleDirections:
            x, y = current[0] + direction[0], current[1] + direction[1]
            if self.grid.matrix[x][y] == TCell.EMPTY.value:
                successors.append((x, y))
        return successors

    def getPath(self, path, end):
        result = []
        temp = end
        while temp != -1:
            result.append(temp)
            temp = path[temp]
        return result[::-1]

    def solve(self):
        minimal_path = []
        self.cans.append(self.destination)

        while len(self.cans) > 0:
            start = self.robotCoordinates
            end = self.nextCan

            visited, current = [start], [start]
            path = dict()
            path[start] = -1

            while len(current) > 0 and end not in visited:
                v = current.pop(0)
                for successor in self.getSuccessors(v):
                    if successor not in visited:
                        visited.append(successor)
                        current.append(successor)
                        path[successor] = v

            if end in visited:
                self.updateScroll(end)
                minimal_path += self.getPath(path, end)
            else:
                print(f"No path between {start} and {end}")

        return minimal_path

    def updateScroll(self, pos):
        self.scroll[0] = pos[0] - self.robot.x
        self.scroll[1] = pos[1] - self.robot.y
