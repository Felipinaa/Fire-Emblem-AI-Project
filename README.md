# Fire-Emblem-AI-Project

Le but de ce projet est de créer une version simplifiée de Fire Emblem et de créer des stratégies pré-enregistrés pour pouvoir créer une "IA" pouvant jouer au jeu et se développer en jouant 

Par rapport au déroulement du jeu : 

On modélisera le plateau par une matrice d'entiers. Les cases libres seront modélisés par des 0, et les unités par un entier positif non nul représentant leur HP

Le système de tour marche de la façon suivante : le joueur peut déplacer chaque unité sur 1 case dans les 4 directions possibles. Puis, s'il y a une unité ennemi sur les 4 cases autour de lui après avoir bougé, il pourra l'attaquer, ce qui lui fera perdre 1 PV.
Par tour, le joueur peut faire réaliser à toutes ses unités les actions suivantes : bouger, attaquer, bouger et attaquer (mais pas attaquer et bouger) 
Si une unité se fait attaquer quand elle a un 1 PV, elle devient ainsi une case vide et est considérée comme morte.

Le jeu se finit quand un des deux camps n'a plus aucune unité active, ou s'il décide d'abandonner. Le jeu affichera ensuite le vainqueur.
