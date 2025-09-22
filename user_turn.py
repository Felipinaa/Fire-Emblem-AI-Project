from game_initialisation import _map, map_actualisation, attack_possibility, move_possibility


def attack_user(char_name, enemy_units, all_units):
    """ interface d'attaque d'une unité par le joueur """
    unit_place = all_units[char_name]['position']
    attack_range = all_units[char_name]['range']
    damage = all_units[char_name]['attack']
    in_range_enemies = attack_possibility(unit_place, enemy_units, attack_range, all_units)
    if not in_range_enemies:
        print("can attack nobody. skipping action.")
    else:
        print("possible enemy to attack : ", *in_range_enemies, sep=" ")
        to_attack = input()
        while to_attack not in [unit[0] for unit in in_range_enemies]:
            to_attack = input("wrong unit, choose again : ")
        all_units[to_attack]['HP'] -= damage


def move_user(char_name, ally_units, all_units):
    """ interface de mouvement d'une unité par joueur """
    unit_place = all_units[char_name]['position']
    move_range = all_units[char_name]['move']
    # possible_moves est forcément non-vide car contient la case de l'unité.
    possible_moves = move_possibility(unit_place, move_range, all_units)
    # On montre les cases pouvant être choisies par un X.
    for case in possible_moves:
        _map[case[0]][case[1]] = 'X'
    for line in _map:
        print(line)
    # On accède à all_units pour véritablement changer les stats de l'unité
    str_place = input(
        "possible places to move (X cases) : ")
    move_done = False
    while not move_done:
        try:
            x_pos, y_pos = int(str_place[0]), int(str_place[2])
            int_place = [x_pos, y_pos]
            while int_place not in possible_moves:
                str_place = input("can't move there, choose again : ")
                x_pos, y_pos = int(str_place[0]), int(str_place[2])
                int_place = [x_pos, y_pos]
            all_units[char_name]['position'] = int_place
            move_done = True
        except ValueError:  # Seule erreur possible
            print("Wrong input : not a position")
            str_place = input("possible place to move (X cases) : ")


def user_turn(ally_units, enemy_units, all_units):
    """ correspond à la boucle caractérisant un tour joué par un joueur """
    while ally_units:
        ally_names = [unit[0] for unit in ally_units]
        # Choix de l'unité :
        map_actualisation(all_units)
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
                map_actualisation(all_units)
                action = input("possibility : attack, move, skip : ")
                while action not in ["attack", "move", "skip"]:
                    action = input("impossible action, choose again : ")
                if action == "skip":
                    attack_counter += 1
                elif action == "move":
                    move_user(char_name, ally_units, all_units)
                    move_counter += 1
                    map_actualisation(all_units)
                else:  # Cas de l'attaque
                    attack_user(char_name, enemy_units, all_units)
                    attack_counter += 1
            else:  # Quand move_counter == 1
                action = input("possibility: attack, skip : ")
                while action not in ["attack", "skip"]:
                    action = input("impossible action, choose again : ")
                if action == "attack":
                    attack_user(char_name, enemy_units, all_units)
                attack_counter += 1  # Pas besoin de prendre en compte skip
        # Enlève l'unité des unités jouables :
        ally_units.remove((char_name, all_units[char_name]['HP']))
    return 0  # n'a pas surrender
