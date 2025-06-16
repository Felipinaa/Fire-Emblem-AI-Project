import json
# On les importe séparément par souci de clarté/ de différentiation.
from game_initialisation import red_units, blue_units, all_units
from game_initialisation import map_actualisation, move_user, attack_user

# Déroulement du tour :
# Initialisation des variables


end_counter = 0
nb_turn = 0
# On passe par une variable surrender
# car quitter la boucle avec un break ne change pas les valeurs ?
surrender = 0

# Boucle principale :
# Manque plus qu'à show map plus souvent
while end_counter != 1:
    # Mise en place du tour :
    nb_turn += 1
    # Les unitées alliées correspondent aux unités qu'on peut utiliser
    # C'est pour cela que la boucle est défini sur sa taille.
    # Tandis que les unités ennemies seront celles qu'on pourra attaquer.
    # On copie uniquement les noms pour pouvoir modifier les stats des unités
    # à partir de "all_units".
    if nb_turn % 2 == 1:
        ally_units = [(unit, blue_units[unit]['HP'])
                      for unit in blue_units if blue_units[unit]['HP'] != 0]
        ally_names = [unit[0] for unit in ally_units]
        enemy_units = [(unit, red_units[unit]['HP'])
                       for unit in red_units if red_units[unit]['HP'] != 0]
        enemy_names = [unit[0] for unit in enemy_units]
    else:
        ally_units = [(unit, red_units[unit]['HP'])
                      for unit in red_units if red_units[unit]['HP'] != 0]
        ally_names = [unit[0] for unit in ally_units]
        enemy_units = [(unit, blue_units[unit]['HP'])
                       for unit in blue_units if blue_units[unit]['HP'] != 0]
        enemy_names = [unit[0] for unit in enemy_units]
    # Début du tour :
    while ally_units:
        # Choix de l'unité :
        map_actualisation()
        print("current/available units:", *ally_units, sep=" ")
        char_name = input("choose unit, skip turn (write skip) or surrender : ")
        while not ((char_name in ally_names) or (char_name in ["skip", "surrender"])):
            char_name = input("can't choose unit, choose again : ")
        if char_name == "skip":
            ally_units = []
            break
        elif char_name == "surrender":
            surrender += 1
            end_counter += 1
            break  # Breaks nécessaires pour ne pas exécuter le reste de la boucle
        else:
            # Choix de l'action :
            # Variables définissant si l'unité à déjà bougé/attaqué
            attack_counter = 0
            move_counter = 0
            unit_place = all_units[char_name]['position']
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
    # Analyse des HP des unités :
    blue_units_hp = [blue_units[unit]['HP'] for unit in blue_units]
    red_units_hp = [red_units[unit]['HP'] for unit in red_units]
    # On en a techniquement pas besoin, mais sert pour la clarté et pour après.
    blue_winner = all([hp == 0 for hp in blue_units_hp])
    red_winner = all([hp == 0 for hp in red_units_hp])
    if blue_winner or red_winner:
        end_counter += 1

# Fin de la partie :

if surrender == 1:
    if nb_turn % 2 == 1:
        red_winner = True
    else:
        blue_winner = True

if blue_winner:
    print("Blue won in", nb_turn)
else:
    print("Red won in", nb_turn)

# Transcription des résultats

with open('results.json', 'r+') as f:
    data = json.load(f)
    nb_former_game = int([key for key in data.keys()][-1][-1])
    data['game ' + str(nb_former_game+1)] = [nb_turn, all_units]
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
