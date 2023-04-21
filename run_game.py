from time import sleep
from game.SpaceInvaders import SpaceInvaders
from controller.qagent import QAgent
import numpy as np
import argparse
import sys
import csv


def main():
    print("Start")
    parser = argparse.ArgumentParser(description='entrainement à spaceInvaders')
    parser.add_argument('episodes', type=int, help="Nombre d'episodes")
    parser.add_argument('target_score', type=int, help='Score pour gagner la partie')
    parser.add_argument('nb_invaders', type=int, help="Nombre d'invaders")
    parser.add_argument('test', type=int, help="Est ce qu'on teste une partie")
    parser.add_argument('--epsilon', default=0.1, type=float, help="Epsilon (Hyperargumment)")
    parser.add_argument('--alpha', default=0.1, type=float, help="Alpha (Hyperargumment)")
    parser.add_argument('--gamma', default=0.9, type=float, help="Gamma (Hyperargumment)")

    args = parser.parse_args()      

    episodes = args.episodes
    target_score = args.target_score
    no_invaders = args.nb_invaders
    test = args.test
    epsilon = args.epsilon
    alpha = args.alpha
    gamma = args.gamma

    freq_save = 10000

    print("Start Learning")
    game = SpaceInvaders(target_score= target_score, no_invaders= no_invaders, display=test, factor=50)
    factor = game.factor
    reduced_width = int(game.screen_width/factor)
    reduced_height = int(game.screen_height/factor)

    dimensions = (reduced_width, reduced_width, reduced_height, reduced_width, reduced_height, 2)

    controller = QAgent(dimensions, factor, test, alpha=alpha, gamma=gamma, epsilon=epsilon)


    print("Lancement de ", episodes, "episodes")
    print("____________________________________________________________________________________________________")
    
    if episodes < 100:
        dpercent = 1
    else:
        dpercent = episodes/100

    wins = 0
    looses = 0

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
        if game.score_val > target_score:
            wins += 1
        #print(f"Episode {i}, Score: {game.score_val}")

    np.save('controller/qtables/qtable'+str(factor)+'.npy', controller.qtable)
    print("Fin de l'apprentissage")

    # Calcul du win_rate
    win_rate = 100 * wins / episodes

    # ouverture du fichier CSV en mode append
    with open('learning.csv', mode='a', newline='') as file:
        # creation de l'objet writer
        writer = csv.writer(file, delimiter=';')
        
        # ajout de la ligne a écrire dans le fichier
        # Nombre d'episode; score a atteindre; nombre d'aliens; alpha; gamma; espsilon; win_rate
        new_line = [episodes, target_score, no_invaders, alpha, gamma, epsilon, win_rate]
        
        # ecriture de la ligne dans le fichier
        writer.writerow(new_line)

if __name__ == '__main__' :
    main()
