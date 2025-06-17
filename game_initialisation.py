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

# --- Fonctions ---
# -- Fonctions concernant la carte --


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
        if all_units[unit]['HP'] > 0:
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
