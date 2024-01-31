from random import choice,randint
from tools.importexport import *
import math
_ = False


def AND_Crushing_Merge(crushedlist: list,mergedlist: list) :
    """Fusionne deux liste ou deux liste de liste en ecrasant les valeur de la première selon l'operateur logique AND"""
    if crushedlist == [] or mergedlist == [] :
        return crushedlist if crushedlist != [] else mergedlist
    try:
        if isinstance(crushedlist[0], list) and isinstance(mergedlist[0], list):
            rliste = []
            for k in range(len(crushedlist)):
                templist = []
                for i in range (len(crushedlist[0])) :
                    if crushedlist[k][i] == mergedlist[k][i]:
                        templist.append(crushedlist[k][i])
                    elif not mergedlist[k][i]:
                        templist.append(crushedlist[k][i])
                    elif not crushedlist[k][i]:
                        templist.append(mergedlist[k][i])
                    elif crushedlist[k][i] and mergedlist[k][i] and crushedlist[k][i] != mergedlist[k][i]:
                        templist.append(mergedlist[k][i])
                rliste.append(templist)
            return rliste
        else :
            rliste = []
            for i in range (len(crushedlist)) :
                if crushedlist[i] == mergedlist[i]:
                    rliste.append(crushedlist[i])
                elif not mergedlist[i]:
                    rliste.append(crushedlist[i])
                elif not crushedlist[i]:
                    rliste.append(mergedlist[i])
                elif crushedlist[i] and mergedlist[i] and crushedlist[i] != mergedlist[i]:
                    rliste.append(mergedlist[i])
            return rliste
    except:
        raise ValueError('Values must be lists or lists of lists with the same lenth')

class Save:
    """class qui permet de recuperer les valeur contenu dans les fichier du jeu"""
    def __init__(self, mapliste, objectsdict, mob_dict, salles, select, start) -> None:
        self.mapliste = mapliste
        self.objectsdict = objectsdict
        self.mob_dict = mob_dict
        self.salles = salles
        self.select = select
        self.start = start

class DebugMode: #class qui permetais de voir tout les ajout du jeu mais qui n'est pas a jour (ancien système) elle est pour l'instant utilisé null part
    def  __init__(self) -> None: #elle ne sert qu'au developpeur
        self.ghost = []
        self.interact = {}
        self.annim = []
        self.mob_pos= {'b':[],'g':[],'n':[],'a':[],'m':[],'mb':[],'mg':[],'mw':[],'o':[],'r':[],'_':[],'w':[]}
        self.salles = [[['gris','grisfonce'],[(3,21),(3,22),(4,21),(4,22)],(3,20),'d','y'],
                       [['gris','marron'],[(9,21),(9,22),(10,21),(10,22)],(9,20),'d','y'],
                        [['jour','marron'],[(15,21),(15,22),(16,21),(16,22)],(15,20),'d','y']]
        self.select = ['gris','grisfonce']
        self.default_select = ['jour','gris']
        self.map =  [[1, 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  1,  _,  2,  _,  3,  _, 53,  _,  4,  _,  5,  _,  6,  _,  7,  _,  8,  _,  9,  _, 10,  _, 11,  _, 12,  _, 14,  _, 15,  _, 16,  _, 17,  _, 18,  _, 19,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _, 20,  _, 21,  _, 22,  _, 23,  _, 24,  _, 25,  _, 26,  _, 27,  _, 28,  _, 29,  _, 30,  _, 31,  _, 32,  _, 33,  _, 34,  _, 35,  _, 36,  _, 37,  _, 39,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],     
                    [ 1, _, 40,  _, 41,  _, 42,  _, 43,  _, 44,  _, 45,  _, 46,  _, 47,  _, 48,  _, 49,  _, 50,  _, 51,  _, 52,  _, 53,  _, 54,  _, 55,  _, 56,  _, 57,  _, 58,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _, 59,  _, 60,  _, 61,  _, 62,  _, 63,  _, 38,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  1, 11,  1,  1,  _,  _,  1, 43,  1,  1,  _,  _,  1, 41,  1,  1,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  1,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  1,  1,  1,  1,  _,  _,  1,  1,  1,  1,  _,  _,  1,  1,  1,  1,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1, _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1,'_',  1,'g',  1,'b',  1,'n',  1,'a',  1,'m',  1,'mb',  1,'mw',  1,'o',  1,'r',  1,'w', 1,_,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  1],
                    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]]
        
        for j, col in enumerate(self.map) :
            for i, val in enumerate(col) :
                if val ==  11 or val == 43 or val == 41 :
                    print((i,j))
                    self.interact[(i,j)] =  val +1 
                if val == 56 :
                    self.annim.append(((j,i, [d for d in range(56,64)] + [56], 80, True, False)))
                if isinstance(val, str) :
                    self.mob_pos[val].append((i+0.5,j))
                    self.map[j][i] = _




#chaque niveau est instancier de la meme manière dans une class 
class Niveau1: #niveau un jouable dans le mode histoire 
    def  __init__(self) -> None:
        '''definition de tout les objets utiles au jeu'''
        load = load_object('data/levels/level1/level1.data')
        loadpatch = load_object('data/levels/level1/level1.patch')
        self.ghost = []
        self.interact = {}
        self.annim = []
        self.spawn = load.start
        self.mob_pos= load.mob_dict
        self.obj_handle = {elm: [(x/30+0.5,y/30+0.5) for x,y in load.objectsdict[elm]] for elm in load.objectsdict}
        self.salles = loadpatch.salles
        self.select = ['jour','gris']
        self.default_select = ['jour','gris']
        self.map =  AND_Crushing_Merge(load.mapliste, loadpatch.mapliste)
        self.map[-2][-1] = 1
        for j, col in enumerate(self.map) : #définition des variations de textures
            for i, val in enumerate(col) :
                if val ==  1 : self.map[j][i] = choice([ 1, 1, 1,2])
                if val ==  3 : self.map[j][i] = choice([ 3, 3, 3,4])
                if val == 5 : self.map[j][i] = choice([5,5,5,6,6])
                if val == 16 : self.map[j][i] = choice([randint(16,29),randint(16,29),randint(16,29),randint(47,48)])
                if val == 30 : self.map[j][i] = choice([randint(30,32), randint(30,32), randint(163,165)]) 
                if val == 33 : self.map[j][i] = randint(33,34)
                if val == 35 : self.map[j][i] = randint(35,38)
                if val == 64 : self.map[j][i] = randint(64,67)
                if val == 70 : self.map[j][i] = randint(70,73)
                if val == 81 : self.map[j][i] = randint(81,94)
                if val == 96 : self.map[j][i] = randint(96,109)
                if val == 115 : self.map[j][i] = choice([115,115,115,116])
                if val == 119 : self.map[j][i] = randint(119,124)
                if val == 127 : self.map[j][i] = randint(127,128)
                if val == 129 : self.map[j][i] = randint(129,130)
                if val == 131 : self.map[j][i] = randint(131,132)
                if val == 135 : self.map[j][i] = randint(135,136)
                if val == 138 : self.map[j][i] = randint(138,139)
                if val == 142 : self.map[j][i] = randint(142,144)
                if val == 145 : self.map[j][i] = randint(145,147)
                if val == 149 : self.map[j][i] = randint(149,150)
                if val == 151 : self.map[j][i] = choice([randint(151,155),randint(151,155), randint(151,155), randint(157,159)])
                if val == 174 : self.map[j][i] = randint(172,174)
                if val ==  11 or val == 43 or val == 41 : self.interact[(i,j)] =  val +1 
                if val == 56 : self.annim.append(((j,i, [d for d in range(56,64)] + [56], 80, True, False)))
                if val == 182 : self.annim.append(((j,i, [d for d in range(182,190)] + [182], 80, True, False)))
                if val == 190 : self.annim.append(((j,i, [d for d in range(190,198)] + [190], 80, True, False)))
                if val == 198 : self.annim.append(((j,i, [d for d in range(198,217)] + [198], 80, True, False)))
                if val == 221 : self.annim.append(((j,i, [d for d in range(221,239)] + [221], 80, True, False)))
                if val == 239 : self.annim.append(((j,i, [d for d in range(239,247)] + [239], 80, True, False)))
                if val == 247 : self.annim.append(((j,i, [d for d in range(247,253)] + [247], 80, True, False)))
                if val == 253 : self.annim.append(((j,i, [d for d in range(253,271)] + [253], 80, True, False)))
                if val == 271 : self.annim.append(((j,i, [d for d in range(271,284)] + [271], 80, True, False)))



class Niveau2: #niveau 2 pas jouable est pas a jour (ancien système)
    def  __init__(self) -> None:
        self.ghost = []
        self.interact = {}
        self.annim = []
        self.mob_pos= {'b':[],'g':[],'n':[],'a':[],'m':[],'mb':[],'mg':[],'mw':[],'o':[],'r':[],'_':[],'w':[]}
        self.salles = []
        self.select = ['gris','grisfonce']
        self.default_select = ['gris','grisfonce']
        self.map =  [[16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
                    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 28, 30, 16, 56, 16,  1, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _, 29, 51, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, _,  _,  _,  _,  _,  _,  _,  _,  _, 16],
                    [35,  _,  _,  _,  _, 30, 30,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _, 35, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _, 50, 30,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16],
                    [33,  _,  _,  _,  _, 35, 30, 16, 16, 16, 16, 16, 16, 16, 16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [33,  _,  _,  _,  _, 16, 30,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16, 16, 49, 41, 49, 16,  _,  _, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16, 16,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16, 16, 16, 16, 16, 16,  _,  _, 16, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _, 16,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _, 16,  _,  _, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _, 16,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _, 16,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _, 16, 16, 16, 16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16, 16, 16, 16, 16, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _,  _, 16,  _,  _,  _,  _,  _,  _,  _, 16],
                    [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]]

        for j, col in enumerate(self.map) :
            for i, val in enumerate(col) :
                if val ==  1 :
                    self.map[j][i] = choice([ 1, 1, 1,2])
                if val ==  3 :
                    self.map[j][i] = choice([ 3, 3, 3,4])
                if val == 5 :
                    self.map[j][i] = choice([5,5,5,6,6])
                if val == 16 :
                    self.map[j][i] = choice([randint(16,29),randint(16,29),randint(16,29),randint(47,48)])
                if val == 30 :
                    self.map[j][i] = randint(30,32)
                if val == 33 :
                    self.map[j][i] = randint(33,34)
                if val == 35 :
                    self.map[j][i] = randint(35,38)
                if val ==  11 or val == 43 or val == 41 :
                    self.interact[(i,j)] =  val +1 
                if val == 56 :
                    self.annim.append(((j,i, [d for d in range(56,64)] + [56], 80, True, False)))
                if isinstance(val, str) :
                    self.mob_pos[val].append((i+0.5,j))
                    self.map[j][i] = _

class DebugModeEntities: #Map de debug pour les objets, ne sert que pour le debug et donc n'est utilisé nul part pour l'instant
    def __init__(self) -> None:
        load = load_object('data/debug_mode/debug_entitees.data')
        self.ghost = []
        self.interact = {}
        self.annim = []
        self.spawn = load.start
        self.mob_pos= load.mob_dict
        self.obj_handle = {elm: [(x/30+0.5,y/30+0.5) for x,y in load.objectsdict[elm]] for elm in load.objectsdict}
        for mob in self.mob_pos :
            if mob == 'worm' :
                self.obj_handle['mush'] = [(elm[0]+0.5,elm[1]+0.5) for elm in self.mob_pos[mob]]
            if mob == 'mage' :
                self.obj_handle['zelda'] = [(elm[0]+0.5,elm[1]+0.5) for elm in self.mob_pos[mob]]
        self.mob_pos = {}
        self.salles = load.salles
        self.select = ['jour','gris']
        self.default_select = ['jour','gris']
        self.map =  load.mapliste

class Niveauinf1: #map du mode infini
    def  __init__(self) -> None:
        load = load_object('data/infinit_mode_levels/inf_level1.data')
        self.ghost = []
        self.interact = {}
        self.annim = []
        self.spawn = 17.5,5.5
        self.mob_pos= load.mob_dict
        poses = [(pos[0]+0.5,pos[1]+0.5) for pos in self.mob_pos['bouler']] #on dispose aleatoirement les monstre
        self.mob_pos['bouler']=[]
        for i in range(12):
            p = choice(poses)
            self.mob_pos[choice(list(self.mob_pos.keys()))]= self.mob_pos[choice(list(self.mob_pos.keys()))] + [p]
            poses.remove(p)
        self.obj_handle = {elm: [(x/30+0.5,y/30+0.5) for x,y in load.objectsdict[elm]] for elm in load.objectsdict}
        self.salles = load.salles
        self.select = ['gris','grisfonce']
        self.default_select = ['gris','grisfonce']
        self.map =  load.mapliste
        for j, col in enumerate(self.map) :
            for i, val in enumerate(col) :
                if val ==  3 : self.map[j][i] = choice([ 3, 3, 3,4])
                if val == 5 : self.map[j][i] = choice([5,5,5,6,6])
                if val == 16 : self.map[j][i] = choice([randint(16,29),randint(16,29),randint(16,29),randint(47,48)])
                if val == 30 : self.map[j][i] = choice([randint(30,32), randint(30,32), randint(163,165)]) 
                if val == 33 : self.map[j][i] = randint(33,34)
                if val == 35 : self.map[j][i] = randint(35,38)
                if val == 64 : self.map[j][i] = randint(64,67)
                if val == 70 : self.map[j][i] = randint(70,73)
                if val == 81 : self.map[j][i] = randint(81,94)
                if val == 96 : self.map[j][i] = randint(96,109)
                if val == 115 : self.map[j][i] = choice([115,115,115,116])
                if val == 119 : self.map[j][i] = randint(119,124)
                if val == 127 : self.map[j][i] = randint(127,128)
                if val == 129 : self.map[j][i] = randint(129,130)
                if val == 131 : self.map[j][i] = randint(131,132)
                if val == 135 : self.map[j][i] = randint(135,136)
                if val == 138 : self.map[j][i] = randint(138,139)
                if val == 142 : self.map[j][i] = randint(142,144)
                if val == 145 : self.map[j][i] = randint(145,147)
                if val == 149 : self.map[j][i] = randint(149,150)
                if val == 151 : self.map[j][i] = choice([randint(151,155),randint(151,155), randint(151,155), randint(157,159)])
                if val == 174 : self.map[j][i] = randint(172,174)
                if val ==  11 or val == 43 or val == 41 : self.interact[(i,j)] =  val +1 
                if val == 56 : self.annim.append(((j,i, [d for d in range(56,64)] + [56], 80, True, False)))
                if val == 182 : self.annim.append(((j,i, [d for d in range(182,190)] + [182], 80, True, False)))
                if val == 190 : self.annim.append(((j,i, [d for d in range(190,198)] + [190], 80, True, False)))
                if val == 198 : self.annim.append(((j,i, [d for d in range(198,217)] + [198], 80, True, False)))
                if val == 221 : self.annim.append(((j,i, [d for d in range(221,239)] + [221], 80, True, False)))
                if val == 239 : self.annim.append(((j,i, [d for d in range(239,247)] + [239], 80, True, False)))
                if val == 247 : self.annim.append(((j,i, [d for d in range(247,253)] + [247], 80, True, False)))
                if val == 253 : self.annim.append(((j,i, [d for d in range(253,271)] + [253], 80, True, False)))
                if val == 271 : self.annim.append(((j,i, [d for d in range(271,284)] + [271], 80, True, False)))

class Niveauinf2: #map du mode infini
    def  __init__(self) -> None:
        load = load_object('data/infinit_mode_levels/inf_level2.data')
        self.ghost = []
        self.interact = {}
        self.annim = []
        self.spawn = 2.5,2.5
        self.mob_pos= load.mob_dict
        poses = [(pos[0]+0.5,pos[1]+0.5) for pos in self.mob_pos['bouler']] #on dispose aleatoirement les monstre
        self.mob_pos['bouler']=[]
        for i in range(12):
            p = choice(poses)
            self.mob_pos[choice(list(list(self.mob_pos.keys()) + [key for key in self.mob_pos.keys() if key != 'golemglace' and key != 'golem' and key != 'metal' and key != 'metalb' and key != 'metalg' and key != 'metalw' and key != 'mage']))]= self.mob_pos[choice(list(self.mob_pos.keys()))] + [p]
            poses.remove(p)
        self.obj_handle = {elm: [(x/30+0.5,y/30+0.5) for x,y in load.objectsdict[elm]] for elm in load.objectsdict}
        self.salles = load.salles
        self.select = ['nuit','vert']
        self.default_select = ['nuit','vert']
        self.map =  load.mapliste
        self.map[-2][-1] = 1
        for j, col in enumerate(self.map) :
            for i, val in enumerate(col) :
                if val ==  1 or val ==2: self.map[j][i] = choice([ 1, 1, 1,2])
                if val ==  3 : self.map[j][i] = choice([ 3, 3, 3,4])
                if val == 5 : self.map[j][i] = choice([5,5,5,6,6])
                if val == 16 : self.map[j][i] = choice([randint(16,29),randint(16,29),randint(16,29),randint(47,48)])
                if val == 30 : self.map[j][i] = choice([randint(30,32), randint(30,32), randint(163,165)]) 
                if val == 33 : self.map[j][i] = randint(33,34)
                if val == 35 : self.map[j][i] = randint(35,38)
                if val == 64 : self.map[j][i] = randint(64,67)
                if val == 70 : self.map[j][i] = randint(70,73)
                if val == 81 : self.map[j][i] = randint(81,94)
                if val == 96 : self.map[j][i] = randint(96,109)
                if val == 115 : self.map[j][i] = choice([115,115,115,116])
                if val == 119 : self.map[j][i] = randint(119,124)
                if val == 127 : self.map[j][i] = randint(127,128)
                if val == 129 : self.map[j][i] = randint(129,130)
                if val == 131 : self.map[j][i] = randint(131,132)
                if val == 135 : self.map[j][i] = randint(135,136)
                if val == 138 : self.map[j][i] = randint(138,139)
                if val == 142 : self.map[j][i] = randint(142,144)
                if val == 145 : self.map[j][i] = randint(145,147)
                if val == 149 : self.map[j][i] = randint(149,150)
                if val == 151 : self.map[j][i] = choice([randint(151,155),randint(151,155), randint(151,155), randint(157,159)])
                if val == 174 : self.map[j][i] = randint(172,174)
                if val ==  11 or val == 43 or val == 41 : self.interact[(i,j)] =  val +1 
                if val == 56 : self.annim.append(((j,i, [d for d in range(56,64)] + [56], 80, True, False)))
                if val == 182 : self.annim.append(((j,i, [d for d in range(182,190)] + [182], 80, True, False)))
                if val == 190 : self.annim.append(((j,i, [d for d in range(190,198)] + [190], 80, True, False)))
                if val == 198 : self.annim.append(((j,i, [d for d in range(198,217)] + [198], 80, True, False)))
                if val == 221 : self.annim.append(((j,i, [d for d in range(221,239)] + [221], 80, True, False)))
                if val == 239 : self.annim.append(((j,i, [d for d in range(239,247)] + [239], 80, True, False)))
                if val == 247 : self.annim.append(((j,i, [d for d in range(247,253)] + [247], 80, True, False)))
                if val == 253 : self.annim.append(((j,i, [d for d in range(253,271)] + [253], 80, True, False)))
                if val == 271 : self.annim.append(((j,i, [d for d in range(271,284)] + [271], 80, True, False)))

class Tuto: #map du tutoriel
    def  __init__(self) -> None:
        load = load_object('data/tutorial/tutorial.data')
        self.ghost = []
        self.interact = {}
        self.annim = []
        self.spawn = 2.5,2.5
        self.mob_pos= load.mob_dict
        self.obj_handle = {elm: [(x/30+0.5,y/30+0.5) for x,y in load.objectsdict[elm]] for elm in load.objectsdict}
        self.salles = load.salles
        self.select = ['jour','gris']
        self.default_select = ['gris','grisfonce']
        self.map =  load.mapliste
        for j, col in enumerate(self.map) :
            for i, val in enumerate(col) :
                if val ==  1 or val ==2:self.map[j][i] = choice([ 1, 1, 1,2])
                if val ==  3 : self.map[j][i] = choice([ 3, 3, 3,4])
                if val == 5 : self.map[j][i] = choice([5,5,5,6,6])
                if val == 16 : self.map[j][i] = choice([randint(16,29),randint(16,29),randint(16,29),randint(47,48)])
                if val == 30 : self.map[j][i] = choice([randint(30,32), randint(30,32), randint(163,165)]) 
                if val == 33 : self.map[j][i] = randint(33,34)
                if val == 35 : self.map[j][i] = randint(35,38)
                if val == 64 : self.map[j][i] = randint(64,67)
                if val == 70 : self.map[j][i] = randint(70,73)
                if val == 81 : self.map[j][i] = randint(81,94)
                if val == 96 : self.map[j][i] = randint(96,109)
                if val == 115 : self.map[j][i] = choice([115,115,115,116])
                if val == 119 : self.map[j][i] = randint(119,124)
                if val == 127 : self.map[j][i] = randint(127,128)
                if val == 129 : self.map[j][i] = randint(129,130)
                if val == 131 : self.map[j][i] = randint(131,132)
                if val == 135 : self.map[j][i] = randint(135,136)
                if val == 138 : self.map[j][i] = randint(138,139)
                if val == 142 : self.map[j][i] = randint(142,144)
                if val == 145 : self.map[j][i] = randint(145,147)
                if val == 149 : self.map[j][i] = randint(149,150)
                if val == 151 : self.map[j][i] = choice([randint(151,155),randint(151,155), randint(151,155), randint(157,159)])
                if val == 174 : self.map[j][i] = randint(172,174)
                if val ==  11 or val == 43 or val == 41 : self.interact[(i,j)] =  val +1 
                if val == 56 : self.annim.append(((j,i, [d for d in range(56,64)] + [56], 80, True, False)))
                if val == 182 : self.annim.append(((j,i, [d for d in range(182,190)] + [182], 80, True, False)))
                if val == 190 : self.annim.append(((j,i, [d for d in range(190,198)] + [190], 80, True, False)))
                if val == 198 : self.annim.append(((j,i, [d for d in range(198,217)] + [198], 80, True, False)))
                if val == 221 : self.annim.append(((j,i, [d for d in range(221,239)] + [221], 80, True, False)))
                if val == 239 : self.annim.append(((j,i, [d for d in range(239,247)] + [239], 80, True, False)))
                if val == 247 : self.annim.append(((j,i, [d for d in range(247,253)] + [247], 80, True, False)))
                if val == 253 : self.annim.append(((j,i, [d for d in range(253,271)] + [253], 80, True, False)))
                if val == 271 : self.annim.append(((j,i, [d for d in range(271,284)] + [271], 80, True, False)))


        