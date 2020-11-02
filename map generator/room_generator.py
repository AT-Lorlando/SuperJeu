import numpy as np
import numpy.linalg as alg
import random
import csv

fichier = "map_generator.txt"
fichier_lire = open(fichier, "w")


tab = list(fichier_csv)
print(type(tab), ("\n\n"))
# d?termine le nombre de ligne ( taille de la matrice nbL*2 NB:0,1,2)
nbL = 0                   # initialisation du nombre de ligne
# row correspond ? une ligne, type list, row affiche la totalit?, row[x] affiche la premi?re valeur de la ligne
for row in fichier_csv:
    print(row)
    nbL = nbL+1           # calcul du nombre de lignes dans le fichier texte

for i in range(nbL):
    for j in range(2):
        tab[i][j] = tab[i][j].replace(".", ",")
print(tab[1][1], type(tab))
