### Initialisation de la carte et des unités :
import json

# Création de la carte :

with open('map.json', 'r') as file:
    tiles = json.load(file)

all_zones = []
for values in tiles.values():
    all_zones = all_zones + values

# Correspond aux nombres de lignes et de colonnes totaux.
i = max([all_zones[lin][0] for lin in range(len(all_zones))])+1  # Lignes
j = max([all_zones[c][1] for c in range(len(all_zones))])+1  # Colonnes

_map = [['__' for lin in range(i)] for col in range(j)]

# Création des unités :

with open('units.json', 'r') as file:
    units = json.load(file)
    blue_units = units["blue units"]
    red_units = units["red units"]
    all_units = blue_units | red_units

### Fonctions :
## Fonctions concernant la carte :


def map_actualisation():
    global _map, all_units, tiles, i, j
    # Vide la map pour mieux actualiser les hp (anciennement empty_map)
    for lin in range(i):
        for col in range(j):
            if [lin, col] in tiles["free zone"]:
                _map[lin][col] = '__'
            # Le elif est là pour signifier la présence de cases spéciales.
            elif [lin, col] in tiles["blocked zone"]:
                _map[lin][col] = '//'
    # Actualise le nom des unités sur chaque case
    for unit in all_units:
        name, pos = unit, all_units[unit]['position']
        _map[pos[0]][pos[1]] = name
    # Affiche la map :
    for line in _map:
        print(line)

## Fonctions concernant les actions :
# Fonctions de check :


def in_bounds(pos):  # Sert à voir si la position existe
    return ((pos[0] >= 0 and pos[0] < i) and (pos[1] >= 0 and pos[1] < j)) and pos not in tiles["blocked zone"]


def move_possibility(unit_pos, wideness):
    # Contient toutes les positions possibles.
    possible_pos = [unit_pos]
    # File servant à analyser positions où peut aller
    pos_to_check = [unit_pos]
    check_counter = wideness
    global all_units
    all_units_pos = [all_units[key]["position"] for key in all_units]
    while check_counter > 0:
        pos_to_check_aux = pos_to_check.copy()
        # Sert à dire si tout les check d'une itération
        # ont bien été réalisés, pour ensuite sortir de la boucle
        # et y re-rentrer ensuite quand on a check toutes les positions.
        while pos_to_check_aux:
            to_check = pos_to_check_aux.pop()
            neighbor = [[to_check[0]+1, to_check[1]],
                        [to_check[0]-1, to_check[1]],
                        [to_check[0], to_check[1]+1],
                        [to_check[0], to_check[1]-1]]
            for pos in neighbor:
                if in_bounds(pos) and pos not in possible_pos and pos not in all_units_pos:
                    pos_to_check.append(pos)
                    possible_pos.append(pos)
                    # Permet de ne pas répéter de minimiser le nombre de checks
        check_counter -= 1  # Condition de sortie du programme
    return possible_pos


def attack_possibility(unit_pos, enemy_units, range):
    global all_units
    # Très similaire à move possibility
    near_pos = []  # regarde toutes les cases pouvant être atteintes
    pos_to_check = [unit_pos]
    check_counter = range
    while check_counter > 0:  # Boucle servant à construire near_pos
        pos_to_check_aux = pos_to_check.copy()
        while pos_to_check_aux:
            to_check = pos_to_check_aux.pop()
            neighbor = [[to_check[0]+1, to_check[1]],
                        [to_check[0]-1, to_check[1]],
                        [to_check[0], to_check[1]+1],
                        [to_check[0], to_check[1]-1]]
            for pos in neighbor:
                if in_bounds(pos) and pos not in near_pos:
                    pos_to_check.append(pos)
                    near_pos.append(pos)
        check_counter -= 1
    # renvoie la liste des unités pouvant être attaquées.
    return [unit for unit in enemy_units if all_units[unit[0]]['position'] in near_pos]

# Fonctions d'actions :


def attack_user(char_name, enemy_units):
    """ interface d'attaque d'une unité par le joueur """
    global all_units, attack_counter
    unit_place = all_units[char_name]['position']
    attack_range = all_units[char_name]['range']
    damage = all_units[char_name]['attack']
    in_range_enemies = attack_possibility(unit_place, enemy_units, attack_range)
    if not in_range_enemies:
        print("can attack nobody. skipping action.")
    else:
        print("possible enemy to attack : ", *in_range_enemies, sep=" ")
        to_attack = input()
        while to_attack not in [unit[0] for unit in in_range_enemies]:
            to_attack = input("wrong unit, choose again : ")
        all_units[to_attack]['HP'] -= damage
        return 1


def move_user(char_name):
    """ interface de mouvement d'une unité par joueur """
    global ally_units, all_units
    unit_place = all_units[char_name]['position']
    move_range = all_units[char_name]['move']
    # possible_moves est forcément non-vide car contient la case de l'unité.
    possible_moves = move_possibility(unit_place, move_range)
    # On montre les cases pouvant être choisies par un X
    # Plutôt que de simplement print la liste des cases possibles.
    for case in possible_moves:
        _map[case[0]][case[1]] = 'X'
    for line in _map:
        print(line)
    # On accède à all_units pour véritablement changer les stats de l'unité
    str_place = input(
        "possible places to move (X cases) : ")
    int_place = [int(str_place[0]), int(str_place[2])]
    while int_place not in possible_moves:
        str_place = input("can't move there, choose again : ")
        int_place = [int(str_place[0]), int(str_place[2])]  # Aie répétition bof
    all_units[char_name]['position'] = int_place
    return 1


def user_turn(end_counter, surrender, ally_units, enemy_units):
    """ correspond à la boucle caractérisant un tour joué par un joueur """
    global all_units
    while ally_units:
        ally_names = [unit[0] for unit in ally_units]
        # Choix de l'unité :
        map_actualisation()
        print("current/available units:", *ally_units, sep=" ")
        char_name = input("choose unit, skip turn (write skip) or surrender : ")
        while not ((char_name in ally_names) or (char_name in ["skip", "surrender"])):
            char_name = input("can't choose unit, choose again : ")
        if char_name == "skip":
            ally_units = []
            break  # Nécessaire pour exécuter le reste de la boucle.
        elif char_name == "surrender":
            return 1
        else:
            # Choix de l'action :
            # Variables définissant si l'unité à déjà bougé/attaqué
            attack_counter = 0
            move_counter = 0
        while attack_counter == 0:  # Après avoir attaqué, l'unité ne peut plus rien faire.
            if move_counter == 0:
                map_actualisation()
                action = input("possibility : attack, move, skip : ")
                while action not in ["attack", "move", "skip"]:
                    action = input("impossible action, choose again : ")
                if action == "skip":
                    attack_counter += 1
                elif action == "move":
                    move_counter = move_user(char_name)
                    map_actualisation()
                else:  # Cas de l'attaque
                    attack_counter = attack_user(char_name, enemy_units)
            else:  # Quand move_counter == 1
                action = input("possibility: attack, skip : ")
                while action not in ["attack", "skip"]:
                    action = input("impossible action, choose again : ")
                if action == "skip":
                    attack_counter += 1
                else:  # Nécessairement attack
                    attack_counter = attack_user(char_name, enemy_units)
        # Enlève l'unité des unités jouables :
        ally_units.remove((char_name, all_units[char_name]['HP']))
    return 0  # n'a pas surrender
