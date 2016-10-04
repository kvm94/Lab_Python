import sys
import os
import random

#Fonctions
##########

def effaceEcran():
    """
       Efface l'écran de la console
    """
    if sys.platform.startswith("win"):
        #Si le systéme est Windows
        os.system("cls")
    else:
        #Si le systéme est Linux ou OS X
        os.system("clear")

def afficheLabyrinthe(lab, perso, posPerso, tresor):
    """
       Affichage d'un labyrinthe
       
       lab :      Variable contenant le labyrinthe
       perso :    caractère représentant le personnage
       posPerso : liste contenant la position du personnage [ligne, colonne]
       tresor:   Caractère représantant le trésort.

       pas de valeur de retour
    """
    nLigne = 0
    for ligne in lab:
        for i in range(1, 4):
            ligne = ligne.replace(str(i), tresor)
        if posPerso[1] == nLigne:
            print(ligne[0:posPerso[0]] + perso + ligne[posPerso[0] + 1:])
        else:
            print(ligne)
        nLigne += 1

def verifDeplacement(lab, posCol, posLigne, data):
    """
       Indique  si le déplacement est autorisé ou pas.
       
       lab:      labyrinthe
       posCol:   position du personnage sur les colonnes.
       posLigne: position du personnage sur les lignes.

       Valeurs de retour:
          None:         déplacement interdit.
          [col, ligne]: déplacement autorisé sur la case indiquée par la liste.
    """
    #Calcul de la taille du labyrinthe
    nCols = len(lab[0])
    nLignes = len(lab)
    #Teste si le déplacement conduit le personnage en dehors de l'aire de jeu.
    if posLigne < 0 or posCol < 0 or  \
       posLigne > (nLignes - 1) or posCol > (nCols - 1):
        return None
    elif lab[posLigne][posCol] == "1" or lab[posLigne][posCol] == "2" or lab[posLigne][posCol] == "3":
        #Découverte d'un trésor
        decouverteTresor(lab[posLigne][posCol], data)
        #On recrée la ligne sans le coffre
        lab[posLigne] = lab[posLigne][:posCol] + " " + lab[posLigne][posCol + 1 :] 
        return [posCol, posLigne]
    elif lab[posLigne][posCol] == "$":
        #Combat avec un ennemi
        combat(data)
        #On recrée la ligne l'ennemi
        lab[posLigne] = lab[posLigne][:posCol] + " " + lab[posLigne][posCol + 1 :] 
        return [posCol, posLigne]
    elif lab[posLigne][posCol] == "0":
        return [-1, -1]
    elif lab[posLigne][posCol] != " ":
        return None
    else:
        return [posCol, posLigne]

def choixJoueur(lab, posPerso, data):
    """
       Demande au joueur de saisir son déplacement et vérifie s'il est possible.
       Si ce n'est pas le cas on affiche un message, sinon modife la position
       du personnage dans la liste posPerso.

       lab:      labyrinthe
       posPerso: liste contenant la position du personnage [colonne, ligne]

       Pas de valeur de retour
    """
    choix = input("Votre déplacement : [(h)aut/(b)as/(d)roite/(g)auche/(q)uitter]? ")
    while choix != "h" and choix != "b" and choix != "g" and choix != "d" and choix != "q":
        print("Vueillez rentrer une valeur correct! (h, b, g, d, q)")
        choix = input("Votre déplacement : [(h)aut/(b)as/(d)roite/(g)auche/(q)uitter]? ")
    if choix == "h":
        dep = verifDeplacement(lab, posPerso[0], posPerso[1] -1, data)
    elif choix == "b":
        dep = verifDeplacement(lab, posPerso[0], posPerso[1] +1, data)
    elif choix == "d":
        dep = verifDeplacement(lab, posPerso[0] +1, posPerso[1], data)
    elif choix == "g":
        dep = verifDeplacement(lab, posPerso[0] -1, posPerso[1], data)
    elif choix == "q":
        exit(0)

    if dep == None:
        print("Impossible de se déplacer!")
        input("Appuyer sur une touche pour continuer.")
    else:
        posPerso[0] = dep[0]
        posPerso[1] = dep[1]

def jeu(level, data, perso, posPerso, tresor):
    """
       Boucle principale du jeu. Affiche le labyrinthe dans ses différents états
       après les déplacements du joueur.

       level: labyrinthe
       data: dictionnaire contenant
             -level : le numéro du niveau
             -po : le nombre de pièce d'or
             -pc : le nombre de points de vie
       perso: caractère représentant le personnage
       posPerso: position du personnage dans le labyrinthe
    """
    while True:
        effaceEcran()
        afficheLabyrinthe(level, perso, posPerso, tresor)
        barreScore(data)
        if data["pv"] <= 0:
            effacerEcran()
            print("GAME OVER")
            input()
            exit(0)
        choixJoueur(level, posPerso, data)
        if posPerso == [-1,-1]:
            print("Vous avez passé le niveaux!")
            input("Appuyer sur une touche pour continuer.")
            break

def chargeLabyrinthe(nom):
    """
       Charge le labyrinthe à partir d'un fichier nom.txt

       nom : nom du fichier contenant le labyrinthe (sans l'extention)

       Valeur de retour : une liste contenant les données du labyrinthe.
    """
    try:
        fich = open("levels/" + nom + ".txt", "r")
        data = fich.readlines()
        fich.close()
    except IOError:
        print("Impossible d'ouvrir le fichier " + nom + "!")
        input("Vueillez appuyer sur une touche.")
        exit(1)

    for i in range(len(data)):          ##Suprime les caractère invisible
        data[i] = data[i].strip()

    return data

def barreScore(data):
    """
        Barre de score affichant les données du jeu

        data: dictionnaire de données de la barre score

        Pas de valeur de retour
    """
    print("Level : {:3d}     PO: {:4d}     PV: {:3d} "\
          .format(data["level"], data["or"], data["pv"]))

def decouverteTresor(categorie, data):
    """
       Incrémente le nombre de pièces d'or du joueur en fonction du trésor

       catégorie: type de trésor
                  -1 : entre 1 et 5 po
                  -2 : entre 5 et 10 po
                  -3 : entre 0 et 25 po

        data : contient les données du joueur (pv, or, lvl)
    """
    if categorie == "1":
        data["or"] = data["or"] + random.randint(1, 5)
    elif categorie == "2":
        data["or"] = data["or"] + random.randint(5, 10)
    else:
        data["or"] = data["or"] + random.randint(0, 25)
def combat(data):
    """
       Determine le nombre de pv perdus lors d'un combat

       data : données du joueur (pv, or, lvl)
    """
    de = random.randint(1, 10)
    if de == 1:
        data["pv"] = data["pv"] - random.randint(5, 10)
    elif de >= 2 and de <= 4:
        data["pv"] = data["pv"] - random.randint(1, 5)
