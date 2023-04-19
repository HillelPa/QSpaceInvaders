from time import sleep
from game.SpaceInvaders import SpaceInvaders
from controller.qagent import QAgent
import numpy as np
import argparse
import sys


def main():
    print("Start")
    parser = argparse.ArgumentParser(description='Tester aleatoirement de jouer a SpaceInvaders')
    parser.add_argument('episodes', type=int, help="Nombre d'episodes")
    parser.add_argument('target_score', type=int, help='Score pour gagner la partie')
    parser.add_argument('nb_invaders', type=int, help="Nombre d'invaders")
    parser.add_argument('epsilon', type=float, help="Epsilon (Hyperargumment)")
    parser.add_argument('test', type=bool, help="Est ce qu'on teste une partie")
    args = parser.parse_args()      

    episodes = args.episodes
    target_score = args.target_score
    no_invaders = args.nb_invaders
    epsilon = args.epsilon
    test = args.test

    freq_save = 10000

    print("Start Learning")
    game = SpaceInvaders(target_score= target_score, no_invaders= no_invaders, display=test)
    factor = game.factor
    reduced_width = int(game.screen_width/factor)
    reduced_height = int(game.screen_height/factor)

    dimensions = (reduced_width, reduced_width, reduced_height, reduced_width, reduced_height, 2)

    controller = QAgent(dimensions, factor, test, epsilon=epsilon)


    print("Lancement de ", episodes, "episodes")
    print("____________________________________________________________________________________________________")
    
    if episodes < 100:
        dpercent = 1
    else:
        dpercent = episodes/100

    for i in range(episodes):
        if i % dpercent == 0:
            sys.stdout.write("|")
            sys.stdout.flush()

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
        #print(f"Episode {i}, Score: {game.score_val}")

    np.save('controller/qtables/qtable'+str(factor)+'.npy', controller.qtable)
    print("Fin de l'apprentissage")

if __name__ == '__main__' :
    main()
