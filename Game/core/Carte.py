from __future__ import annotations
from typing import List
import pygame as pg
from python_data.parametres import *


class Carte:
    """Class qui permet la gestion de la carte"""
    def __init__(self,game, niveau) -> None:
        '''initialisation de la class carte avec des recuperations de valeurs depuis le niveau'''
        self.game = game #on recup^ère les valeurs utiles 
        self.niveau = niveau
        self.gost_blocs = self.niveau.ghost
        self.interact = self.niveau.interact
        self.mini_map = self.niveau.map
        self.annim_b = self.niveau.annim
        self.map_monde = {}
        self.map_monde_2 = []
        self.blocdict = {}
        self.get_map() #on lance les fonction utile au programme
        self.get_bloc()

    def update(self):
        """fonction qui rafraichis la map"""
        if self.blocdict != {}: #on rafraichit les bloc annimé
            [self.blocdict[bloc].update() for bloc in self.blocdict]
        self.get_map() #on récupère la map

    def get_bloc(self):
        """fonction qui ajoute des bloc annimé"""
        for i,j,liste, temps, inf, trig in self.annim_b :
            self.blocdict[(i,j)] = Bloc_Annime_Carte(self.game, self, temps, i, j, liste, inf, trig)

    def get_map(self,t=True):
        '''remplit le dictionnaire map_monde avec les coordonnée de chaque bloc en clé
            et les valeur de chaque bloc en valeur'''
        for j, colone in enumerate(self.mini_map) :
            for i, valeur in enumerate(colone) :
                if valeur:
                    self.map_monde[(i,j)] = valeur
                if valeur == 12 or valeur == 42 or valeur == 44 :
                    self.gost_blocs.append((i,j))
                else :
                    self.map_monde_2.append((i,j))
        self.map_monde[(12.5,2.5)] = 1

    def draw(self):
        '''cette méthode n'est conçe que pour le débug, méthode utilisé pour le test de la carte, dessine en 2d des carré gris pour les valeur True de map_monde '''
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1]*100,100,100), 2) for pos in self.map_monde]


class Bloc_Annime_Carte:
    """class qui correspond aux blocs annimée"""
    def __init__(self, game, carte: Carte, temps: int, i: int, j: int, liste: List[int], infinit: bool = False, trigered: bool = True) -> None:
        """initialisation de la class avec 
            - le jeu en question, 
            - la carte de type carte 
            - le temps d'annimation 
            - les coordonnée i,j du bloc 
            - la liste des identifiants des blocs
            - deux bool i l'annimation est infini ou non et si elle doit etre activé par le joueur ou non"""
        self.game, self.map, self.temps, self.inf, self.trig  = game, carte, temps, infinit, trigered
        self.temps_prev = pg.time.get_ticks()
        self.trigger,self.annim,self.counter = False,False,0
        if infinit :
            self.annim = True
        self.i, self.j, self.liste = i,j,liste

    def check_temps(self,temps_anim):
        """verification du respect du temps d'annimation"""
        self.trigger = False
        temps_actuelle = pg.time.get_ticks()
        if temps_actuelle - self.temps_prev > temps_anim :
            self.temps_prev = temps_actuelle
            self.trigger = True
    
    def annimate_map(self, i, j, liste):
        """changement des valeurs dans la map"""
        self.annim = True
        if self.trigger:
            self.map.mini_map[i][j] = liste[self.counter]
            self.counter += 1
        if self.counter >= len(liste)-1 :
            self.counter = 0
            if not self.inf :
                self.annim = False

    def annimer(self):
        """déclanchement de l'annimation"""
        self.annim = True

    def update(self) :
        """actualisation du bloc"""
        self.check_temps(self.temps)
        if self.trig or self.annim :
            self.annimate_map(self.i, self.j, self.liste)




    