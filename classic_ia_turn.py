from game_initialisation import move_possibility, attack_possibility
from math import sqrt

# Fonctionnement général :
# Cette IA sert de modèle particulièrement basique en terme d'action, et ne marche même pas
# avec le concept de rewards.
# Son fonctionnement est le suivant :
# Pour chaque unité, elle va chercher l'unité adverse la plus proche avec le moins de PV
# pour s'y diriger (càd choisir un chemin pouvant réduire la distance, sinon elle reste immobile).
# Après avoir bougé, elle attaquera l'unité (si possible) ayant le moins de PV dans celles possibles.


# Fonctions auxiliaires :


def dist(pos1, pos2):
    """ fonction distance basique """
    return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def min_w_ind(L):
    """ fonction minimum renvoyant le minimum et son index """
    if not L:
        return None
    else:
        ind = 0
        mini = L[0]
        for i in range(1, len(L)):
            if L[i] < mini:
                ind = i
                mini = L[i]
        return ind, mini


def closest_enemy(pos, enemy_units, all_units):
    """ trouve l'ennemi le plus proche et renvoie la distance minimale
        par rapport à la position et son nom """
    enemy_positions = [all_units[enemy]['position'] for (enemy, enemy_hp) in enemy_units]
    enemy_names = [enemy for (enemy, enemy_hp) in enemy_units]  # all my homies hate dico.keys()
    enemy_dist = [dist(pos, enemy_pos) for enemy_pos in enemy_positions]
    ind, d_min = min_w_ind(enemy_dist)
    return d_min, enemy_names[ind]


def optimal_path(m_list, enemy_pos):
    """ trouve le mouvement permettant de se rapprocher le plus de l'unité voulue """
    possible_choice = [dist(pos, enemy_pos) for pos in m_list]
    return m_list[min_w_ind(possible_choice)[0]]


def classic_ia_turn(ally_units, enemy_units, all_units):
    for (unit, unit_hp) in ally_units:
        # Mouvement de l'unité :
        pos = all_units[unit]['position']
        d_min, enemy = closest_enemy(pos, enemy_units, all_units)
        m_pos = move_possibility(pos, all_units[unit]['move'], all_units)
        choice = optimal_path(m_pos, all_units[enemy]['position'])
        all_units[unit]['position'] = choice  # Bouge l'unité
        # Attaque de l'unité :
        pos = all_units[unit]['position']  # Update la position de l'unité
        possible_enemy = attack_possibility(pos, enemy_units, all_units[unit]['range'], all_units)
        enemy_hp = [enemy[1] for enemy in possible_enemy]
        if enemy_hp:
            lowest_hp_enemy = possible_enemy[min_w_ind(enemy_hp)[0]][0]
            all_units[lowest_hp_enemy]['HP'] -= all_units[unit]['attack']
