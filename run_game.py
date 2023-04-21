from time import sleep
from game.SpaceInvaders import SpaceInvaders
from controller.random_agent import RandomAgent
import argparse
import csv
import sys

def main():
    print("Start")

    parser = argparse.ArgumentParser(description='Tester aleatoirement de jouer a SpaceInvaders')
    parser.add_argument('episodes', type=int, help="Nombre d'episodes")
    parser.add_argument('target_score', type=int, help='Score pour gagner la partie')
    parser.add_argument('nb_invaders', type=int, help="Nombre d'invaders")
    parser.add_argument('display', type=int, help="Est ce qu'on affiche")
    args = parser.parse_args()      

    episodes = args.episodes
    target_score = args.target_score
    no_invaders = args.nb_invaders
    display = args.display

    print("start temoin")
    print(display)
    game = SpaceInvaders(target_score= target_score, no_invaders=no_invaders, display=display)
    controller = RandomAgent(game.na, display)
    wins = 0
    looses = 0
    print("Lancement de ", episodes, "episodes")
    print("____________________________________________________________________________________________________")
    for i in range(episodes):
        game.reset()
        is_done = False
        while not is_done:
            action = controller.select_action()
            is_done = game.step(action)
            sleep(0.0001)
        

        if game.score_val > target_score :
            wins += 1
        else :
            looses += 1

        if i % (episodes/100) == 0:
            sys.stdout.write("|")
            sys.stdout.flush()
    
    win_rate = (wins*100)/(wins+looses)
    print()
    print(f"Pour {episodes} games jouées aléatoirement on obtiens {win_rate}% de parties gagnées")
    
    # ouvrir le fichier CSV des resultats
    with open('witness.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # écrire une nouvelle ligne dans le fichier
        writer.writerow([episodes, target_score, no_invaders, win_rate])


if __name__ == '__main__' :
     main()

