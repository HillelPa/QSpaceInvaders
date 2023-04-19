import numpy as np
import pygame

class RandomAgent():
    """ 
    A random agent.
    """

    def __init__(self, num_actions, display):
        self.num_actions = num_actions
        self.display = display

    def select_action(self):
        if self.display :
            pygame.event.get()
        return np.random.randint(self.num_actions)
