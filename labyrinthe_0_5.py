#!/usr/bin/python3

import lab

if __name__ == "__main__":            
    #Initialisation
    ###############

    perso ="X"
    tresor ="#"
    nLevelTotal = 5
    data = {
        "or"    : 0,
        "pv"    : 25,
        "level" : None
    }

    #Lancement de la partie
    #######################

    for nLevel in range(1, nLevelTotal + 1):
        posPerso = [1, 1]
        level = lab.chargeLabyrinthe("level_" + str(nLevel))
        data["level"] = nLevel
        lab.jeu(level, data, perso, posPerso, tresor)
    print("Vous avez gagné!")
    input("Appuyer sur une touche pour continuer.")



