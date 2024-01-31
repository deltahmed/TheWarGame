from __future__ import annotations
import pygame as pg
import math 
from python_data.parametres import *


to_plane_dist=int((LARGEUR/2)/math.tan(math.radians(FOV/2)))
class RayCast:
    def __init__(self, game) -> None:
        '''initialisation de la classe raycast'''
        self.game = game
        self.resultat = []
        self.obj_a_rendre = []
        self.textures = self.game.objrendu.texture_mur
        self.diag = []

    def rendre_obj(self):
        """met tout les objets a rendre dans la liste des objets a rendre sous forme de surface pygame"""
        self.game.objrendu.liste_obj_png = []
        self.obj_a_rendre = [] #on recreer la liste des objet a rendre
        for rayon, valeur in enumerate(self.resultat): #pour chaque rayon 
            profondeur,hauteur_projection, texture, aff = valeur #on prend la valeur
        
            if hauteur_projection >= 0 :
                if hauteur_projection < HAUTEUR : #evite les bug de rendu en dehors de l'image, on affiche chaque mur
                    collone_mur = self.textures[texture].subsurface(aff * (TAILLE_TEXTURE - ECHELLE), 0, ECHELLE, TAILLE_TEXTURE)
                    collone_mur = pg.transform.scale(collone_mur, (ECHELLE, hauteur_projection))
                    mur_pos = (rayon * ECHELLE, DEMI_HAUTEUR - hauteur_projection // 2)
                else :
                    hauteur_texture = TAILLE_TEXTURE * HAUTEUR / hauteur_projection
                    collone_mur = self.textures[texture].subsurface( aff * (TAILLE_TEXTURE - ECHELLE), DEMI_TAILLE_TEXTURE - hauteur_texture // 2, ECHELLE, hauteur_texture)
                    collone_mur = pg.transform.scale(collone_mur, (ECHELLE, HAUTEUR))
                    mur_pos = (rayon * ECHELLE, 0)
                self.obj_a_rendre.append((profondeur, collone_mur, mur_pos))
    
    def rayons(self):
        '''Méthode créant les rayons pour le raycasting'''
        self.resultat = [] #on vide les resultats
        #on recupère les valeurs utile pour le calcul
        ox, oy = self.game.joueur.pos # coordonnée du joueur
        x_map, y_map = self.game.joueur.map_pos #case du joueur

        #on defini les paramètre de textures 
        texture_vert, texture_hor = 1,1
        #calcul de l'angle entre chaque rayon
        angles_rayon = self.game.joueur.angle - DEMI_FOV + 0.0001 #permet d'eviter des division par 0
        for rayon in range(NB_RAYONS):
            sin_angle = math.sin(angles_rayon)
            cos_angle = math.cos(angles_rayon)

            #calcule des intersections avec les ligne horizontal de la grille
            if sin_angle > 0 :
                y_hor, dy = y_map+1, 1 
            else :
                y_hor, dy = y_map - 1e-6, -1

            profondeur_horizontal = (y_hor - oy) / sin_angle
            x_hor = ox + profondeur_horizontal * cos_angle

            delta_profondeur = dy / sin_angle
            dx = delta_profondeur * cos_angle

            for _ in range(PROFONDEUR_MAX) : #on envoie les rayons profondeurmax fois
                case_hor = int(x_hor), int(y_hor) #coordonnée de la case
                if case_hor in self.game.map.map_monde : #si la case est un mur on casse la boucle
                    texture_hor = self.game.map.map_monde[case_hor]
                    break 
                x_hor += dx
                y_hor += dy 
                profondeur_horizontal += delta_profondeur #on change la case séléctionnée

            #calcule des intersections avec les ligne verticals de la grille
            if cos_angle > 0 :
                x_vert, dx = x_map+1, 1 
            else :
                x_vert, dx = x_map - 1e-6, -1
                
            profondeur_vertical = (x_vert - ox) / cos_angle
            y_vert = oy + profondeur_vertical * sin_angle
            
            delta_profondeur = dx / cos_angle
            dy = delta_profondeur * sin_angle

            for _ in range(PROFONDEUR_MAX) : #on envoie les rayons profondeurmax fois
                case_vert = int(x_vert), int(y_vert) #coordonnée de la case
                if case_vert in self.game.map.map_monde : #si la case est un mur on casse la boucle
                    texture_vert = self.game.map.map_monde[case_vert]
                    break 
                x_vert += dx
                y_vert += dy 
                profondeur_vertical += delta_profondeur #on change la case séléctionnée

            #on calcule la profondeur entre le joueur et le mur
            if profondeur_vertical < profondeur_horizontal :
                profondeur,texture = profondeur_vertical, texture_vert
                y_vert %= 1
                if cos_angle > 0 :
                    aff = y_vert
                else :
                    aff = 1 - y_vert
            else :
                profondeur,texture = profondeur_horizontal, texture_hor
                x_hor %= 1 
                if sin_angle > 0 :
                    aff = 1 - x_hor
                else :
                    aff = x_hor
            

            #on enlève l'effect de courbes du a l'utilisation des cosinus et sinus 
            profondeur *= math.cos(self.game.joueur.angle - angles_rayon)

            # debug -----------------------------------------------------
            #on affiche le tout pour debuger le programme
            #pg.draw.line(self.game.screen, "yellow", (100 * ox, 100 * oy),
            #             (100*ox + 100 * profondeur * cos_angle, 100 * oy + 100 * profondeur * sin_angle),
            #            2 )
            # fin debug -------------------------------------------------

            #Projection de l'environnement
            hauteur_projection = DISTANCE_RENDU / (profondeur + 0.0001) #pour eviter les division par 0
            #resultat du raycasting
            



            # debug -----------------------------------------------------
            #on affiche des rectangle pour chaque rayon pour dessiner les murs
            #on calcule l'assombrissement du mur en fonction de la distance

            #couleur= [255/(1+profondeur**5*0.00002)] * 3
            #pg.draw.rect(self.game.screen, couleur, 
            #             (rayon * ECHELLE, DEMI_HAUTEUR - hauteur_projection // 2, ECHELLE, hauteur_projection))
            # fin debug -------------------------------------------------
            
            self.resultat.append((profondeur,hauteur_projection, texture, aff))
            angles_rayon += DELTA_ANGLE

    def update(self):
        """actualisation du moteur graphique"""
        self.rayons()
        self.rendre_obj()