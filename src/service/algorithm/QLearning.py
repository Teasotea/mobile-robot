# TODO build Base class
import copy
import random

import numpy as np
import pandas as pd

from constant.Reward import Reward
from constant.State import State
from entity.charger.Charger import Charger
from entity.robot.Robot import Robot
from service.stats.Collector import Collector


class QLearning:
    def __init__(self, grid, cans, robot: Robot, charger: Charger):
        self.grid = grid
        self.robot = robot
        self.cans = cans
        self.temp_cans = copy.deepcopy(cans)
        self.charger = charger
        self.current_pos = [1, 1]
        self.collector = Collector()

        # Hyperparams
        self.n_episodes = 5000  # 10000
        self.max_iter_episode = 1000
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

    def isNotOutOfRange(self, action):
        return 60 > self.current_pos[0] + self.possibleDirections[action][0] >= 0 \
               and 60 > self.current_pos[1] + self.possibleDirections[action][1] >= 0

    def isOutOfRange(self, action):
        return not self.isNotOutOfRange(action)

    def step(self, action, cans):
        """
        TODO: We should take into account battery changes. Now we don't consider it at all.
        """
        reward = 0
        next_state = (self.current_pos[0] + 1) * (self.current_pos[1] + 1)

        if self.isOutOfRange(action):
            return next_state, -500, False

        self.current_pos[0] += self.possibleDirections[action][0]
        self.current_pos[1] += self.possibleDirections[action][1]

        if not self.collector.isVisited(self.current_pos):
            reward += 50

        reward += Reward.WAITING if action == State.WAITING else 0

        # FIXME if current position in unused cans
        current = (self.current_pos[0], self.current_pos[1])
        if current in cans:
            if len(cans) <= 4:
                print("REWARD", len(cans))
            reward += Reward.CAN_COLLECTED
            cans.remove(current)
        elif self.grid.isWall(current[0], current[1]):
            reward -= 100

        done = self.robot.trash.isFull()

        self.collector.visit(self.current_pos)
        return next_state, reward, done

    def build_QTable(self):
        n_observations = 61 * 61  # - 283, 60x60 board - bricks and 2 states
        n_actions = len(self.possibleDirections)
        return np.zeros((n_observations, n_actions))

    def learn(self):
        QTable = self.build_QTable()
        total_rewards_episode = list()

        for e in range(self.n_episodes):
            # we initialize the first state of the episode
            # start = self.robotCoordinates()
            current_state = 0
            cans = self.temp_cans[:]
            total_episode_reward = 0

            for i in range(self.max_iter_episode):

                if np.random.uniform(0, 1) < self.exploration_proba:
                    action = random.choice(
                        range(len(self.possibleDirections))  # Choose random action
                    )
                else:
                    action = np.argmax(QTable[current_state, :])  # Choose the best action in QTable

                next_state, reward, done = self.step(action, cans)

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
