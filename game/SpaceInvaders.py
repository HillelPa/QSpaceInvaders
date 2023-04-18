import pygame
import random
import math
from pygame import mixer
import numpy as np
import os
from time import sleep


def getURL(filename):
    return os.path.dirname(__file__) + "/" + filename

#encodes action as integer : 
#0 : gauche
#1 : droite
#2 : shoot
#3 : pass

#encodes state as np.array(np.array(pixels))

class SpaceInvaders():

    NO_INVADERS = 7 # Nombre d'aliens  
    
    def __init__(self, target_score, no_invaders, display : bool = False, factor = 100):

        # Commenter sur mac
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        
        # player
        self.display = display
        
        # nombre d'actions (left, right, fire, no_action)
        self.na = 4 

        #maj du NO_INVADERS
        self.NO_INVADERS = no_invaders

        # score de fin de partie :
        self.target_score = target_score

        # reduction de la grille par factor 
        self.factor = factor

        # initializing pygame
        pygame.init()

        # creating screen
        self.screen_width = 800
        self.screen_height = 600
        if self.display:
            sleep(1)
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        else:
            sleep(1)
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags=pygame.HIDDEN)

        # caption and icon
        pygame.display.set_caption("Welcome to Space Invaders Game by:- styles")

        # Score
        self.scoreX = 5
        self.scoreY = 5
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        # Game Over
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)

        self.playerImage = pygame.image.load(getURL('data/spaceship.png'))
        self.reset()

    
    def get_player_X(self) -> int:
        return self.player_X

    def get_player_Y(self) -> int:
        return self.player_Y

    def get_indavers_X(self) -> 'List[int]':
        return self.invader_X

    def get_indavers_Y(self) -> 'List[int]':
        return self.invader_Y

    def get_bullet_X(self) -> int:
        return self.bullet_X

    def get_bullet_Y(self) -> int:
        return self.bullet_Y

    def get_bullet_state(self) -> str:
        """Projectile
        - rest = bullet is not moving
        - fire = bullet is moving
        """
        return self.bullet_state

    def full_image(self):
        return pygame.surfarray.array3d(self.screen)

    def get_state(self):
        
        # Stratégie 1 : renvoyé une version réduite des positions de la grille 
        # Position = 543 renvoi 54 si la facteur est de 10

        # Position du joueur : 
        player_X = self.get_player_X()

        # Alien le plus bas :
        """
        lowest_invader_index = np.argmax(self.invader_Y)
        while self.invader_Y[lowest_invader_index] > 600:
            lowest_invader_index = np.argmax(self.invader_Y)

        lowest_invader_X = self.invader_X[lowest_invader_index]
        lowest_invader_Y = self.invader_Y[lowest_invader_index]
        """

        # Alien le plus proche sur l'axe des X 
        closest_invader_X = min(self.invader_X, key=lambda x: abs(x - player_X))
        closest_invader_index = self.invader_X.index(closest_invader_X)
        closest_invader_Y = self.invader_Y[closest_invader_index]

        # Etat du shooter :
        bullet_state = self.get_bullet_state()
        if bullet_state == "rest" :
            bullet_state = 0
        else :
            bullet_state = 1
        
        # Tuple d'etat : (reduced_pX, reduced_iX, reduced_iY, bullet_state)
        # Nombre d'etat possible = (800 * 800 * 600 * 2 / (factor^3))
        reduced_pX = int(player_X/self.factor)
        reduced_iX = int(closest_invader_X/self.factor)
        reduced_iY = int(closest_invader_Y/self.factor)

        return (reduced_pX, reduced_iX, reduced_iY, bullet_state)

    def reset(self):
        """Reset the game at the initial state.
        """
        self.score_val = 0

        self.player_X = 370
        self.player_Y = 523
        self.player_Xchange = 0

        # Invader
        self.invaderImage = []
        self.invader_X = []
        self.invader_Y = []
        self.invader_Xchange = []
        self.invader_Ychange = []
        for _ in range(SpaceInvaders.NO_INVADERS):
            self.invaderImage.append(pygame.image.load(getURL('data/alien.png')))
            self.invader_X.append(random.randint(64, 737))
            self.invader_Y.append(random.randint(30, 180))
            self.invader_Xchange.append(1.2)
            self.invader_Ychange.append(50)

        # Bullet
        # rest - bullet is not moving
        # fire - bullet is moving
        self.bulletImage = pygame.image.load(getURL('data/bullet.png'))
        self.bullet_X = 0
        self.bullet_Y = 500
        self.bullet_Xchange = 0
        self.bullet_Ychange = 3
        self.bullet_state = "rest"

        if self.display:
            self.render()
            pygame.display.update()
    
        return self.get_state()

    def step(self, action):
        """Execute une action et renvoir l'état suivant, la récompense perçue 
        et un booléen indiquant si la partie est terminée ou non.
        """
        is_done = False
        reward = 0

        # RGB
        self.screen.fill((0, 0, 0))
        # Controling the player movement from the arrow keys
        if action == 0: # GO LEFT
            self.player_Xchange = -1.7
        if action == 1: # GO RIGHT
            self.player_Xchange = 1.7
        if action == 2: # FIRE
            self.player_Xchange = 0
            # Fixing the change of direction of bullet
            if self.bullet_state is "rest":
                self.bullet_X = self.player_X
                self.move_bullet(self.bullet_X, self.bullet_Y)
        if action == 3: # NO ACTION 
            self.player_Xchange = 0
    
        # adding the change in the player position
        self.player_X += self.player_Xchange
        for i in range(SpaceInvaders.NO_INVADERS):
            self.invader_X[i] += self.invader_Xchange[i]
    
        # bullet movement
        if self.bullet_Y <= 0:
            self.bullet_Y = 600
            self.bullet_state = "rest"
        if self.bullet_state is "fire":
            self.move_bullet(self.bullet_X, self.bullet_Y)
            self.bullet_Y -= self.bullet_Ychange
    
        # movement of the invader
        for i in range(SpaceInvaders.NO_INVADERS):
            
            if self.invader_Y[i] >= 450:
                if abs(self.player_X-self.invader_X[i]) < 80:
                    for j in range(SpaceInvaders.NO_INVADERS):
                        self.invader_Y[j] = 2000
                    reward = -5
                    is_done = True
                    break
                
            if self.invader_X[i] >= 735 or self.invader_X[i] <= 0:
                self.invader_Xchange[i] *= -1
                self.invader_Y[i] += self.invader_Ychange[i]
                reward = -1
            # Collision
            collision = self.isCollision(self.bullet_X, self.invader_X[i], self.bullet_Y, self.invader_Y[i])
            if collision:
                reward = 3
                self.score_val += 1
                if self.score_val > self.target_score:
                    is_done = True
                    break
                self.bullet_Y = 600
                self.bullet_state = "rest"
                self.invader_X[i] = random.randint(64, 736)
                self.invader_Y[i] = random.randint(30, 200)
                self.invader_Xchange[i] *= -1
    
            self.move_invader(self.invader_X[i], self.invader_Y[i], i)
    
        # restricting the spaceship so that it doesn't go out of screen
        if self.player_X <= 16:
            self.player_X = 16
        elif self.player_X >= 750:
            self.player_X = 750

        self.move_player(self.player_X, self.player_Y)

        if self.display:
            self.render()
    
        if is_done:
            return "", reward, is_done

        return self.get_state(), reward, is_done

    def render(self):
        self.show_score(self.scoreX, self.scoreY)
        pygame.display.update()

    def move_player(self, x, y):
        self.screen.blit(self.playerImage, (x - 16, y + 10))

    def move_invader(self, x, y, i):
        self.screen.blit(self.invaderImage[i], (x, y))

    def move_bullet(self, x, y):
        self.screen.blit(self.bulletImage, (x, y))
        self.bullet_state = "fire"

    def show_score(self, x, y):
        score = self.font.render("Points: " + str(self.score_val), True, (255,255,255))
        self.screen.blit(score, (x , y ))

    def game_over(self):
        game_over_text = self.game_over_font.render("GAME OVER", True, (255,255,255))
        self.screen.blit(game_over_text, (190, 250))


    # Collision Concept
    def isCollision(self, x1, x2, y1, y2):
        distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
        return (distance <= 50)