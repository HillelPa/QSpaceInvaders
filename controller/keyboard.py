import pygame

class KeyboardController():
    def select_action(self, state):
        for event in pygame.event.get():
            # Controling the player movement from the arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return 0
                if event.key == pygame.K_RIGHT:
                    return 1
                if event.key == pygame.K_SPACE:
                    # Fixing the change of direction of bullet
                    return 2
            else:
                return 3