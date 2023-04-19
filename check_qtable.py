import numpy as np

factor = 100

qtable = np.load("controller/qtables/qtable"+str(factor)+".npy")

for i in range(len(qtable)):
            for j in range(len(qtable[i])):
                for k in range(len(qtable[i][j])):
                    for l in range(len(qtable[i][j][k])):
                        
                        for m in range(len(qtable[i][j][k][l])):
                            for n in range(len(qtable[i][j][k][l][m])):
                                print(f"pX : {i}, iX : {j}, iY : {k}, bX : {l}, bY : {m}, bS : {n}")
                                for o in range(len(qtable[i][j][k][l][m][n])):
                                    print("action : ", o, " = [",qtable[i][j][k][l][m][n][o], "]")

