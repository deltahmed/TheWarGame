import pygame as pg
import math
import os
from collections import deque
from python_data.parametres import * 
from graphics.pygame_menu import get_texture_size

class Sprite:
    """Class qui correspond a un objet statique du jeu"""
    def __init__(self, game, chemin='media/objets/table.png',
                 pos=(10.5, 3.5), taille=0.7, shift=0.27):
        self.game = game
        self.joueur = game.joueur
        self.x, self.y = pos
        self.image = pg.image.load(chemin).convert_alpha()
        self.image_largeur = self.image.get_width()
        self.image_demi_largeur = self.image.get_width() // 2
        self.ratio = self.image_largeur / self.image.get_height()
        self.demi_proj_largeur, self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 0, 1, 1
        self.sprite_taille = taille
        self.demi_taille_sprite = shift

    def get_projection(self):
        """Méthode qui affiche l'image sur l'écran"""
        proj = DISTANCE_RENDU / self.norm_dist * self.sprite_taille
        proj_largeur, proj_hauteur = proj * self.ratio, proj

        image = pg.transform.scale(self.image, (proj_largeur, proj_hauteur))

        self.demi_proj_largeur = proj_largeur // 2
        hauteur_shift = proj_hauteur * self.demi_taille_sprite
        pos = self.screen_x - self.demi_proj_largeur, DEMI_HAUTEUR - proj_hauteur // 2 + hauteur_shift
        self.game.objrendu.liste_obj_png.append(image)
        self.game.raycast.obj_a_rendre.append((self.norm_dist, image, pos))

    def get(self):
        """Méthode qui calcule l'image affiché sur l'ecran de l'objet"""
        dx = self.x - self.joueur.x
        dy = self.y - self.joueur.y
        
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.joueur.angle
        if (dx > 0 and self.joueur.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rayons = delta / DELTA_ANGLE
        self.screen_x = (DEMI_NB_RAYON + delta_rayons) * ECHELLE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.image_demi_largeur < self.screen_x < (LARGEUR + self.image_demi_largeur) and PROFONDEUR_MAX_OBJ > self.norm_dist > 0.5:
            self.get_projection()

    def update(self):
        """Méthode qui actualise le sprite"""
        self.get()

class SpriteAnim(Sprite):
    """Class qui correspond a un objet annimé du jeu"""
    def __init__(self, game, chemin='media/objets/green/0.png', pos=(11.5, 3.5), taille=0.8, shift=0.15, temps_anim=120, agrandi = 1):
        super().__init__(game, chemin, pos, taille, shift)
        self.temps_anim = temps_anim
        self.chemin = chemin.rsplit('/', 1)[0]
        self.agrandi = agrandi
        self.images = self.get_image(self.chemin)
        self.temps_prev = pg.time.get_ticks()
        self.trigger = False
    
    def check_temps(self):
        """On verifie que l'annimation respecte bien le temps demandé"""
        self.trigger = False
        temps_actuelle = pg.time.get_ticks()
        if temps_actuelle - self.temps_prev > self.temps_anim :
            self.temps_prev = temps_actuelle
            self.trigger = True

    def get_image(self, chemin):
        """Recuperation des image depuis le fichier de l'objet"""
        images = deque()
        for file_name in os.listdir(chemin):
            if os.path.isfile(os.path.join(chemin, file_name)):
                if file_name.split('.')[-1] == 'png':
                    img = get_texture_size(chemin + '/' + file_name, self.agrandi)[0]
                    images.append(img)
        return images
    
    def annimer(self, images: deque):
        """annimation de l'objet"""
        if self.trigger:
            images.rotate(-1)
            self.image = images[0]

    def update(self):
        """Actualisation du Sprite annimé"""
        super().update()
        self.check_temps()
        self.annimer(self.images)


