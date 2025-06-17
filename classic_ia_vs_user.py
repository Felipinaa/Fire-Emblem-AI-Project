import json
from game_initialisation import red_units, blue_units, all_units
from user_turn import user_turn
from classic_ia_turn import classic_ia_turn

# Initialisation des variables :

end_counter = 0
surrender = 0
nb_turn = 0


while end_counter != 1:
    nb_turn += 1
    # On considère que le joueur joue en premier, donc sur les tours impairs.
    if nb_turn % 2 == 1:
        ally_units = [(unit, blue_units[unit]['HP'])
                      for unit in blue_units if blue_units[unit]['HP'] > 0]
        enemy_units = [(unit, red_units[unit]['HP'])
                       for unit in red_units if red_units[unit]['HP'] > 0]
        surrender = user_turn(ally_units, enemy_units)
    else:
        ally_units = [(unit, red_units[unit]['HP'])
                      for unit in red_units if red_units[unit]['HP'] != 0]
        enemy_units = [(unit, blue_units[unit]['HP'])
                       for unit in blue_units if blue_units[unit]['HP'] != 0]
        classic_ia_turn(ally_units, enemy_units)
    # Analyse des HP des unités :
    blue_units_hp = [blue_units[unit]['HP'] for unit in blue_units]
    red_units_hp = [red_units[unit]['HP'] for unit in red_units]
    # On en a techniquement pas besoin, mais sert pour la clarté et pour après.
    blue_winner = all([hp == 0 for hp in blue_units_hp])
    red_winner = all([hp == 0 for hp in red_units_hp])
    if blue_winner or red_winner or (surrender == 1):
        end_counter += 1

if surrender == 1:
    if nb_turn % 2 == 1:
        red_winner = True
    else:
        blue_winner = True

if not blue_winner:
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
