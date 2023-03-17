# TODO build Base class
import copy
import random

import numpy as np
import pandas as pd

from entity.charger.Charger import Charger
from entity.robot.Robot import Robot
from service.stats.Collector import Collector


class QLearning:
    def __init__(self, grid, cans, robot: Robot, scroll, charger: Charger):
        self.grid = grid
        self.robot = robot
        self.cans = cans
        self.temp_cans = copy.deepcopy(cans)
        self.charger = charger
        self.current_pos = [1, 1]
        self.collector = Collector()

        # Hyperparams
        self.n_episodes = 500  # 10000
        self.max_iter_episode = 5000
        self.exploration_proba = 0.9
        self.exploration_decreasing_decay = 0.001
        self.min_exploration_proba = 0.01
        self.gamma = 0.99
        self.lr = 0.1

    # def robotCoordinates(self):
    #     robot_x, robot_y = (30,30)#self.robot.getCurrentPosition()
    #     print(robot_x + self.scroll[0], robot_y + self.scroll[1])
    #     return (1,1)#robot_x + self.scroll[0], robot_y + self.scroll[1]

    @property
    def possibleDirections(self):
        return [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

    # def getState(self):
    #     #0 - high, 1 - low
    #     return 1 if self.robot.battery.current <= 200 else 0

    def restoreCans(self):
        self.temp_cans = self.cans[:]

    def step(self, action, cans):
        reward = 0

        # TODO: implement check whether there is a wall
        # FIXME: rewrite this
        if 60 > self.current_pos[0] + self.possibleDirections[action][0] >= 0 \
                and 60 > self.current_pos[1] + self.possibleDirections[action][1] >= 0:
            self.current_pos[0] += self.possibleDirections[action][0]
            self.current_pos[1] += self.possibleDirections[action][1]
        else:
            reward -= 100

        next_state = self.current_pos[0] * self.current_pos[1]  # fix this

        # if self.robot.battery.current == 0:
        #     reward -= 500

        if not self.collector.isVisited(self.current_pos):
            reward += 20

        # S(low), R_search_cans (-10); if high - +10
        if action == 0:
            reward -= 25

        # FIXME if current position in unused cans
        current = (self.current_pos[0], self.current_pos[1])
        if current in cans:
            print("REWARD", len(cans))
            reward += 200
            cans.remove(current)
        elif self.grid.isWall(current[0], current[1]):
            reward -= 100

        # if state == 1 and self.currentPos == self.charger.getChargerPosition():
        #     reward += 10

        if self.robot.trash.isNotFull():
            done = False
        else:
            done = True
        # elif self.robotCoordinates == self.charger.getChargerPosition():
        #    done = True
        self.collector.visit(self.current_pos)
        return next_state, reward, done

    def build_QTable(self):
        n_observations = 60 * 60  # - 283, 60x60 board - bricks and 2 states
        n_actions = len(self.possibleDirections)
        return np.zeros((n_observations, n_actions))

    def learn(self):
        QTable = self.build_QTable()
        total_rewards_episode = list()

        for e in range(self.n_episodes):
            # we initialize the first state of the episode
            # start = self.robotCoordinates()
            current_state = 0  # env.reset()
            cans = self.temp_cans[:]
            total_episode_reward = 0

            for i in range(self.max_iter_episode):

                if np.random.uniform(0, 1) < self.exploration_proba:
                    action = random.choice(
                        range(len(self.possibleDirections))  # Choose random action
                    )
                else:
                    action = np.argmax(QTable[current_state, :])  # Choose the best action in QTable

                # print(current_state, action, QTable[current_state, action])

                next_state, reward, done = self.step(action, cans)

                # print(self.current_pos)
                # print(next_state, reward, done)

                # We update our Q-table using the Q-learning iteration
                QTable[current_state, action] = (1 - self.lr) * QTable[current_state, action] \
                                                + self.lr * (reward + self.gamma * max(QTable[next_state, :]))
                total_episode_reward += reward
                current_state = next_state
                # If the episode is finished, we leave the for loop
                if done:
                    break

            # We update the exploration proba using exponential decay formula
            self.exploration_proba = max(self.min_exploration_proba, np.exp(-self.exploration_decreasing_decay * e))
            total_rewards_episode.append(total_episode_reward)

        self.saveState(QTable)
        return total_rewards_episode, QTable

    def getCollector(self):
        return self.collector

    def saveState(self, qtable):
        df = pd.DataFrame(qtable)
        df.to_csv("data/qtable.csv")