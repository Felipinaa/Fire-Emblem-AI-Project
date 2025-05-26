from numpy import *

#Création de la carte :
i = 5#nombre de lignes
j = 5#nombre de colonnes
map = array([[0]*i]*j)

#Création des unités :
class unit :
    def __init__(name, hp, pos, nb = "unit", attack = 1, move = 1,range = 1):
        name.hp = hp
        name.attack = attack
        name.move = move
        name.pos = pos
        name.range = range
        name.nb = nb
    def __call__(name): #permet d'accéder rapidement aux informations
        return name.hp, name.pos

#La première coordonnée de pos correspond à la ligne, et la deuxième à la colonne (attention : sur la grille, la position 0.0 est en haut !)

pb1= unit(3,[4,0],"pb1")
pb2= unit(3,[4,1],"pb2")
pb3= unit(3,[4,2],"pb3")
pb4= unit(3,[4,3],"pb4")
pb5= unit(3,[4,4],"pb5")

pr1= unit(3,[0,0],"pr1")
pr2= unit(3,[0,1],"pr2")
pr3= unit(3,[0,2],"pr3")
pr4= unit(3,[0,3],"pr4")
pr5= unit(3,[0,4],"pr5")

#Sert à accéder aux unités à travers un dictionnaire pour pouvoir les appeler avec la user input.
red_units=[pr1,pr2,pr3,pr4,pr5]
red_dico = {"r"+str(i): red_units[i] for i in range(len(red_units))}
blue_units=[pb1,pb2,pb3,pb4,pb5]
blue_dico = {"b"+str(i): blue_units[i] for i in range(len(blue_units))}
all_units= red_units + blue_units
all_dico = blue_dico | red_dico 
 
#Positionnement sur le terrain :

def empty_map():
    global map
    map = array([[0]*i]*j)

def hp_maprefresh(l):
    global map
    empty_map()
    for x in l:
        hp, pos= x()
        map[pos[0]][pos[1]] += hp

hp_maprefresh(all_units)

#Actions

def move(unit,dir):
    global all_units
    prov_pos=[0,0] #position provisoire
    if unit.pos[0]>i or unit.pos[1]>j or unit.pos[0]<0 or unit.pos[1]<0:
        return "invalid move : out of bounds"
    elif dir == "left" :
        prov_pos[0], prov_pos[1] = unit.pos[0], unit.pos[1]-1
    elif dir == "right" :
        prov_pos[0], prov_pos[1] = unit.pos[0], unit.pos[1]+1
    elif dir == "up" :
        prov_pos[0], prov_pos[1] = unit.pos[0]-1, unit.pos[1]
    elif dir == "down" :
        prov_pos[0], prov_pos[1] = unit.pos[0]+1, unit.pos[1]
    else:
        return "invalid move"
    check = all_units.copy()
    check.remove(unit)
    for x in check:
        if x.pos == prov_pos:
            return "invalid move : other unit here"
    unit.pos = prov_pos

#Fonction en réalité inutile ?
#def attack(ally,enemy):
#    global possible_units
#    if enemy in possible_units :
#        enemy.hp -= ally.attack
#    else:
#        return "can't attack this unit"

#Fonctions concernant le déroulement :

def forfeit():
   global enemy_units, end_counter
   end_counter = 1

def possible_action(units, case, action="move"):
    global i,j #rappel : nombre de lignes et de colonnes
    x,y = case
    units_pos = [x.pos for x in units]
    if action == "move":
        return ( case not in units_pos ) and ( x>=0 and x<=i and y>=0 and y<=j )
    else :
        return case in units_pos

def get_unit_from_nb(units,nb):
    units_nb = [x.nb for x in units]
    unit_index = units_nb.index(nb)
    return  units[unit_index]  # car les listes sont crées par le même parcours.

def get_unit_from_pos(units,position):
    units_pos = [x.pos for x in units]
    unit_index = units_pos.index(position)
    return units[unit_index] #de même que pour la fonction précédente.

#Déroulement d'un tour :

#Les listes dépendront des tours : on associera au nombre de tours modulo 2 pour savoir quelle équipe joue.

enemy_unit=[]
ally_unit=[]
end_counter=0
nb_turn=0

while end_counter == 0 :
    #Initialisation du jeu/de chaque tour : 
    nb_turn+=1
    #Précise qui joue et fait boucle uniquement par rapport aux unités "ennemis/alliés"
    if nb_turn%2 == 1 :
        ally_unit= blue_units
        enemy_unit= red_units
    else :
        ally_unit = red_units
        enemy_unit = blue_units
    ally_name = [x.nb for x in ally_unit]

    #Choix du personnage à bouger
    while ally_unit :
        print("curent units :",ally_name)
        char_name = input("choose which unit to move : ")
        while not (char_name in ally_name or  char_name not in ["skip turn", "surrender"]) :
            char_name=input("impossible to play, choose another : ")
        if char_name == "skip turn":
            ally_unit = []
        if char_name == "surrender":
            end_counter += 1
        char = all_dico[char_name] 

    #Choix de l'action à faire
        attack_counter = 0
        move_counter = 0
        #Compte les actions réalisés en considérant que seules 2 actions possibles
        #Les inputs doivent contenir l'action et la position de l'action concernée
        while attack_counter == 0 :
            if move_counter == 1 :
                action,place = input("possibility : attack, skip unit turn(skip)") #place correspond à l'emplacement où l'action va agir
                while action not in ["attack","skip"]:
                    action,place = input("fool test")
            else :
                action, place = input("possibility : attack, move, skip turn")
                while action not in ["attack","skip","move"]:
                    action,place = input("fool test")
                    
            #Déroulement de l'action  
            if action == "move":
                while not possible_action(all_units, place, action):
                    action, place = input("can't move there, choose again:")
                char.pos = place 
            elif action == "attack":
                while not possible_action(enemy_unit, place, action) or possible_action(ally_unit, place, action):
                    action = input("no enemy units there/presence of ally units, choose again :")
                enemy_dico_pos = { enemy_unit[i].pos = enemy_unit[i] for i in range(len(enemy_unit)) }  #Permet d'accéder aux unités par leur position
                enemy = enemy_dico_pos[place] #accède à l'unité voulue dont on veut enlever les PV
