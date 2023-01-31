# build Base class 
import numpy as np
import random

from entity.grid.TCell import TCell
from entity.robot.Robot import Robot
from entity.charger.Charger import Charger

import pandas as pd


class QLearning:
    def __init__(self, grid, cans, robot: Robot, scroll, charger:Charger):
        self.grid = grid
        self.robot = robot
        self.cans = cans
        self.charger = charger
        self.currentPos = [1,1]

        # Hyperparams
        self.n_episodes = 10000
        self.max_iter_episode = 100
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
    
    def step(self, action):
        reward = 0

        #TODO: implement check whether there is a wall
        #FIXME: rewrite this
        if 60 > self.currentPos[0] + self.possibleDirections[action][0] >=0 and 60> self.currentPos[1] + self.possibleDirections[action][1] >=0 :
            self.currentPos[0] += self.possibleDirections[action][0]
            self.currentPos[1] += self.possibleDirections[action][1]
        else:
            reward -= 100

        # state = self.getState()

        next_state =  self.currentPos[0] * self.currentPos[1]#fix this

        if self.robot.battery.current == 0:
            reward -= 500
       
        #TODO:if unknown cell +10
        #S(low), R_search_cans (-10); if high - +10
        if action == 0:
            reward -= 25

        if tuple(self.currentPos) in self.cans: #if can +200
            print("REWARD")
            reward += 200

        # if state == 1 and self.currentPos == self.charger.getChargerPosition():
        #     reward += 10
        
        if self.robot.trash.isNotFull():
            done = False
        else:
            done = True
        #elif self.robotCoordinates == self.charger.getChargerPosition():
        #    done = True

        return next_state, reward, done

    def build_QTable(self):
        #Initialize the Q-table to 0
        n_observations = 60*60 #- 283, 60x60 board - bricks and 2 states  
        n_actions = len(self.possibleDirections)
        return np.zeros((n_observations, n_actions))

    def learn(self):
        QTable = self.build_QTable()
        total_rewards_episode = list()

        for e in range(self.n_episodes):
            #we initialize the first state of the episode
            # start = self.robotCoordinates()
            start = self.currentPos
            current_state = 0 #env.reset()
            done = False
    
            #sum the rewards that the agent gets from the environment
            total_episode_reward = 0
    
            for i in range(self.max_iter_episode): 
            # we sample a float from a uniform distribution over 0 and 1
            # if the sampled flaot is less than the exploration proba
            #     the agent selects arandom action
            # else
            #     he exploits his knowledge using the bellman equation 
        
                if np.random.uniform(0,1) < self.exploration_proba:
                    action = random.choice(range(len(self.possibleDirections)))#env.action_space.sample() #choose random action
                else:
                    action = np.argmax(QTable[current_state,:]) #choose the best action
                
                #print(current_state, action, QTable[current_state, action])

                next_state, reward, done = self.step(action)

                print(self.currentPos)
                print(next_state, reward, done)

                # We update our Q-table using the Q-learning iteration
                QTable[current_state, action] = (1-self.lr) * QTable[current_state, action] +self.lr*(reward + self.gamma*max(QTable[next_state,:]))
                total_episode_reward = total_episode_reward + reward
                # If the episode is finished, we leave the for loop
                if done:
                    break
                current_state = next_state
    
            #We update the exploration proba using exponential decay formula 
            exploration_proba = max(self.min_exploration_proba, np.exp(-self.exploration_decreasing_decay*e))
            total_rewards_episode.append(total_episode_reward)
            print("Training finished.\n")
            print(QTable)
            print(total_rewards_episode)
            df = pd.DataFrame(QTable)
            df.to_csv("qt2.csv")

        return total_rewards_episode, QTable

    # def solve(self):

    #     return path
