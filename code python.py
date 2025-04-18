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


red_units=[pr1,pr2,pr3,pr4,pr5]
blue_units=[pb1,pb2,pb3,pb4,pb5]
all_units= red_units + blue_units

#Positionnement sur le terpr1rain :

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

def attack(ally,ennemy):
    global possible_units
    if ennemy in possible_units :
        ennemy.hp -= ally.attack
    else:
        return "can't attack this unit"

#Fonctions concernant le déroulement:

def forfeit():
   global ennemy_units, end_counter
   end_counter = 1

#Déroulement d'un tour :

#Les listes dépendront des tour : on associera au nombre de tour modulo 2 pour savoir quel équipe joue.

ennemy_unit=[]
ally_unit=[]
end_counter=0
nb_turn=0
while end_counter == 0 :
    nb_turn+=1
    #Précise qui joue et fait boucle uniquement par rapport aux unités "ennemis/alliés"
    if nb_turn%2 == 1 :
        ally_unit= blue_units
        ennemy_unit= red_units
    else :
        ally_unit = red_units
        ennemy_unit = blue_unit
    ally_name = [x.nb for x in ally_unit]
    while ally_unit !=[]:
        print(ally_name)
        char = input("choose which unit to move : ")
        while char not in ally_name :
            char=input("impossible to play, choose another : ")
        attack_counter = 0
        move_counter = 0
        #Compte les actions réalisés en considérant que seules 2 actions possibles
        #Les input doivent contenir l'action et la position de l'action concerné
        while attack_counter == 0 :
            if move_counter == 1 :
                action, direction = input("possibility : attack, skip turn")
                while action != "attack" or action != "skip":
                    action,direction = input("fool test")
            else :
                action, direction = input("possibility : attack, move, skip turn")
            if action == "move":
                unit_pos = [x.pos for x in all_units]
                if direction in unit_pos :
                    action = input("can't move there, choose again:")


