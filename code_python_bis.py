import array

# Création de la carte :
# On considère une map carrée :
j = 5  # Nombre de colonnes
i = 5  # Nombre de lignes
map = array([[0]*i]*j)

# Création des unités :
# On passera par un dictionnaire de dictionnaire pour chaque camp :
# Les clés du dictionnaire correspondent aux noms des unités.
# Les valeurs correspondantes aux caractéristiques de chaque unité sont :
# 1 : HP, 2 : Position, 3 : Attaque, 4 : Capacité à se déplacer, 5: Porté
# On considérera des unités toutes pareilles pour la simulation

# En considérant que les unités bleues sont en haut du plateau
# et les unitées rouges en bas :

blue_units = {"b" + str(i):
                {"HP": 3, "position": [0, i], "attack": 1, "move": 1, "range": 1}
                  for i in range(5)}
red_units = {"r" + str(i):
                {"HP": 3, "position": [4, i], "attack": 1, "move": 1, "range": 1}
                for i in range(5)}
all_units = blue_units | red_units

# Fonctions concernant l'affichage :


def empty_map():
    global map
    map = array([[0]*i]*j)


def hp_maprefresh(L):
    global map
    empty_map()
    for unit in L:
        hp, pos = unit["HP"], unit["position"]
        map[pos[0]][pos[1]] += hp

# Actions concernant les unités :


def in_bounds(pos):  # Sert à voir si la position existe
    return (pos[0] >= 0 and pos[0] < i) and (pos[1] >= 0 and pos[1] < j)


def move_possibility(unit_pos, wideness):
    possible_pos = [unit_pos]  # Contient toutes les positions possibles.
    pos_to_check = [unit_pos]  # File servant à analyser positions où peut aller
    global all_units
    all_units_pos = [all_units[i]["position"] for i in range(len(all_units))]
    while wideness > 0:
        pos_to_check_aux = pos_to_check.copy()
        # Sert à dire si tout les check d'une itération
        # ont bien été réalisés, pour ensuite sortir de la boucle
        # et y re-rentrer ensuite quand on a check tout les trucs
        while pos_to_check_aux:
            to_check = pos_to_check_aux.pop()
            neighbor = [[to_check[0]+1, to_check[1]],
                        [to_check[0]-1, to_check[1]],
                        [to_check[0], to_check[1]+1],
                        [to_check[0], to_check[1]-1]]
            for pos in neighbor:
                if pos in possible_pos and in_bounds(pos) and pos not in all_units_pos and pos not in possible_pos:
                    pos_to_check.append(pos)
                    possible_pos.append(pos)
                    # Permet de ne pas répéter de minimiser le nombre de checks
        wideness -= 1  # Condition de sortie du programme
    return possible_pos

# Déroulement du tour :
# Initialisation des variables


end_counter = 0
nb_turn = 0

# Boucle principale :

while end_counter != 0:
    # Mise en place du tour :
    nb_turn += 1
    # Les unitées alliées correspondent aux unités qu'on peut utiliser
    # C'est pour cela que la boucle est défini sur sa taille.
    # Tandis que les unités ennemies seront celles qu'on pourra attaquer.
    # On copie uniquement les noms pour pouvoir modifier les stats des unités
    # à partir de "all_units".
    if nb_turn % 2 == 1:
        ally_units = blue_units.keys()
        enemy_units = red_units.keys()
    else:
        ally_units = red_units.keys()
        enemy_units = blue_units.keys()
    # Début du tour :
    while ally_units:
        # Choix de l'unité :
        print("current units:", end=" ")
        print((unit_name for unit_name in ally_units), sep=", ")
        char_name = input("choose unit, skip turn (write skip) or surrender")
        if char_name == "skip":
            ally_units = []
        elif char_name == "surrender":
            end_counter += 1
        else:
            # Choix de l'action :
            # Variables définissant si l'unité à déjà bougé/attaqué
            attack_counter = 0
            move_counter = 0
            while attack_counter == 0:  # Après avoir attaqué, l'unité ne peut plus rien faire.
                if move_counter == 0:
                    action = input("possibility : attack, move, skip")
                    if action == "skip":
                        attack_counter += 1
                    #  elif action == "move":
