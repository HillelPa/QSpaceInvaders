import random
import os
import numpy as np
import pygame

class QAgent:
    
    def __init__(self, dimensions, factor, test, alpha=1, gamma=0.9, epsilon=0.1, n_actions=4):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_actions = n_actions
        self.test = test

        # Q table : tableau a 7 dimension, 1 etat = 6 premieres dimensions :
        # [player_X][invader_X][invader_Y][bullet_X][buller_Y][bullet_state]
        # 7e dimension est l'action


        if os.path.exists("controller/qtables/qtable"+str(factor)+".npy"):
            self.qtable = np.load("controller/qtables/qtable"+str(factor)+".npy")
        else:
            self.qtable = np.zeros((dimensions[0], dimensions[1], dimensions[2], dimensions[3], dimensions[4], dimensions[5], n_actions))


    def select_action(self, state):
        if self.test :
            pygame.event.get()
        if random.uniform(0, 1) < self.epsilon:
            return np.random.randint(self.n_actions)
        else:
            q_values = self.qtable[state[0]][state[1]][state[2]][state[3]][state[4]][state[5]]
            return np.argmax(q_values)

    def learn(self, state, action, reward, next_state, done):

    
        q_values = self.qtable[state[0]][state[1]][state[2]][state[3]][state[4]][state[5]]
        next_q_values = self.qtable[next_state[0]][next_state[1]][next_state[2]][next_state[3]][next_state[4]][next_state[5]]
        next_action = np.argmax(next_q_values)
        
        target = reward + (1 - done) * self.gamma * next_q_values[next_action]
        td_error = target - q_values[action]
        
        q_values[action] += self.alpha * td_error
        self.qtable[state[0]][state[1]][state[2]][state[3]][state[4]][state[5]] = q_values
    

