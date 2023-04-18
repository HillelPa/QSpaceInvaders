import numpy as np
import pygame

class RandomAgent():
    """ 
    A random agent.
    """

    def __init__(self, num_actions):
        self.num_actions = num_actions

    def select_action(self):
        #pygame.event.get()
        return np.random.randint(self.num_actions)
