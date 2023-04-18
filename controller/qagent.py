import random
import os
import numpy as np
import pygame

class QAgent:
    
    def __init__(self, dimensions, factor, alpha=0.1, gamma=0.9, epsilon=0.1, n_actions=4):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_actions = n_actions

        # Q table : tableau a 5 dimension, 1 etat = 4 premieres dimensions :
        # [player_X][invader_X][invader_Y][bullet_state]
        # 5e dimension est l'action


        if os.path.exists("controller/qtables/qtable"+str(factor)+".npy"):
            self.qtable = np.load("controller/qtables/qtable"+str(factor)+".npy")
        else:
            print("pas wouhou")
            self.qtable = np.zeros((dimensions[0], dimensions[1], dimensions[2], dimensions[3], n_actions))
        #self.print_q_table()

    def select_action(self, state):
        pygame.event.get()
        if random.uniform(0, 1) < self.epsilon:
            return np.random.randint(self.n_actions)
        else:
            q_values = self.qtable[state[0]][state[1]][state[2]][state[3]]
            return np.argmax(q_values)

    def learn(self, state, action, reward, next_state, done):

       #print("ICI next_state")
        #print(f"pX = {next_state[0]}, iX = {next_state[1]}, iY = {next_state[2]}, b_s = {next_state[3]}")
    
        q_values = self.qtable[state[0]][state[1]][state[2]][state[3]]
        next_q_values = self.qtable[next_state[0]][next_state[1]][next_state[2]][next_state[3]]
        next_action = np.argmax(next_q_values)
        
        target = reward + (1 - done) * self.gamma * next_q_values[next_action]
        td_error = target - q_values[action]
        
        q_values[action] += self.alpha * td_error
        self.qtable[state[0]][state[1]][state[2]][state[3]] = q_values

        #print(f"We update the state : pX : {state[0]}, iX : {state[1]}, iY : {state[2]}, b_s : {state[3]}")
        #print("qvalues : ", self.qtable[state[0]][state[1]][state[2]][state[3]])
    
    def print_q_table(self):
        for i in range(len(self.qtable)):
            for j in range(len(self.qtable[i])):
                for k in range(len(self.qtable[i][j])):
                    for l in range(len(self.qtable[i][j][k])):
                        print(f"pX : {i}, iX : {j}, iY : {k}, b_s : {l}")
                        for m in range(len(self.qtable[i][j][k][l])):
                            print("action : ", m, " = [",self.qtable[i][j][k][l][m], "]")

