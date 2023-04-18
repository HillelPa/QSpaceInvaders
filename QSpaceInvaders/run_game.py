from time import sleep
from game.SpaceInvaders import SpaceInvaders
from controller.keyboard import KeyboardController
from controller.random_agent import RandomAgent
from controller.qagent import QAgent
import numpy as np

def main():
    print("Start")
    episodes = 100
    target_score = 50
    freq_save = 1000


    #controller = KeyboardController()

    learning = False
    witness_experience = True 

    if witness_experience:
        print("start temoin")
        game = SpaceInvaders(target_score= target_score, display=False)
        controller = RandomAgent(game.na)
        learning = False
        wins = 0
        looses = 0
        print("Lancement de ", episodes, "episodes")
        #print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        print("____________________________________________________________________________________________________")
        for i in range(episodes):
            if i % (episodes/100) == 0:
                print("|", end="")
            state = game.reset()
            is_done = False
            while not is_done:
                action = controller.select_action(state)
                state, reward, is_done = game.step(action)
                sleep(0.0001)
            if game.score_val > target_score :
                print("WIN")
                wins += 1
            else :
                print("LOOSE")
                looses += 1
        print()
        print(f"Pour {episodes} games jouées aléatoirement on obtiens {(wins*100)/(wins+looses)}% de parties gagnées")

    if learning :
        print("Start Learning")
        game = SpaceInvaders(target_score= target_score, display=False)
        factor = game.factor
        reduced_width = int(game.screen_width/factor)
        reduced_height = int(game.screen_height/factor)

        dimensions = (reduced_width, reduced_width, reduced_height, 2)

        controller = QAgent(dimensions, factor)

        for i in range(episodes):
            n = 0
            state = game.reset()
            is_done = False
            while not is_done:
                action = controller.select_action(state)
                next_state, reward, is_done = game.step(action)
                if not is_done:
                    controller.learn(state, action, reward, next_state, is_done)
                state = next_state
                if n%freq_save == 0:
                    np.save('controller/qtables/qtable'+str(factor)+'.npy', controller.qtable)
                n += 1
                sleep(0.0001)
            print(f"Episode {i}, Score: {game.score_val}")

        print("Fin de l'apprentissage")

    # normal game 

    print("Game normale")
    game = SpaceInvaders(target_score= target_score, display=True)
    state = game.reset()
    is_done = False
    while not is_done:
        action = controller.select_action(state)
        state, reward, is_done = game.step(action)
        sleep(0.0001)
    print()
    print("score = ", game.score_val)


if __name__ == '__main__' :
    main()
