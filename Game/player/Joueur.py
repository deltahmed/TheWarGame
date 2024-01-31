from __future__ import annotations
import pygame as pg
import math
from python_data.parametres import * 
import core.Carte as c


class Joueur:
    def __init__(self, game) -> None:
        '''initialisation de la classe Joueur'''
        self.game = game 
        self.x, self.y = self.game.niveau.spawn #position du joueur
        self.angle = JOUEUR_ANGLE # angle du joueur
        self.tire_variable = False
        self.vie = self.game.savedata[self.game.save]['vie'] if self.game.save else VIE_MAX
        self.pos_relative = 0
        self.vie_delay = 700
        self.temps_prev = pg.time.get_ticks()
        # correction mouvement diagonal
        self.diag_corr = 1 / math.sqrt(2)

    def check_vie_delay(self):
        """Methode qui permet de calculer le temps avant le quel le joueur commence a reganier de la vie"""
        temps_actuel = pg.time.get_ticks()
        if temps_actuel - self.temps_prev > self.vie_delay:
            self.temps_prev = temps_actuel
            return True

    def tire(self, event):
        """Methode qui permet au joueur de tirer"""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.tire_variable and not self.game.arme.recharge:
                self.game.sound.pompe.play()
                self.tire_variable = True
                self.game.arme.recharge = True

    def vie_recover(self):
        """Méthode qui permet de faire regagner de la vie au joueuer"""
        if self.check_vie_delay() and self.vie < VIE_MAX:
            self.vie += 1
    
    def get_damage(self, a_retirer):
        """retire de la vie au joueur lorsqu'il est touché"""
        self.vie -= a_retirer
        self.game.objrendu.damage_joueur()
        self.game.sound.joueur_douleur_s.play()
        self.check_game_over() #on verifie que le joueur n'a pas perdu

    def check_game_over(self):
        """on verifie que la vie du joueur est toujours positive sinon il a perdu"""
        if self.vie < 1 :
            self.game.objrendu.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.scorelist.append( self.game.score) 
            self.game.score = 0
            self.game.new_game(self.game.level) #on recomence le jeu



    def mouvement(self):
        '''méthode qui deplace le joueur '''
        # on calcule en fonction de l'angle de vision la direction pour pourvoir avancer
        sin_a = math.sin(self.angle) 
        cos_a = math.cos(self.angle) 
        dx,dy = 0,0
        #on calcule la vitesse reel du joueur pour que cela ne depende pas du nombre de fps par seconde
        vitesse = JOUEUR_VITESSE * self.game.delta_temps
        v_sin = vitesse * sin_a #on calcule le produit du sinus et du cosinus de notre angle
        v_cos = vitesse * cos_a # pour pouvoir ajouter a notre mouvement la vitesse demandé
        keys = pg.key.get_pressed() # ajouter la bonne vitesse pour chaque touche
        nb_touches = 0
        if keys[pg.K_z] or keys[pg.K_w] or keys[pg.K_UP]:
            nb_touches += 1
            dx += v_cos
            dy += v_sin
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            nb_touches += 1
            dx += -v_cos
            dy += -v_sin
        if keys[pg.K_q] or keys[pg.K_a] or keys[pg.K_LEFT]:
            nb_touches += 1
            dx += v_sin
            dy += -v_cos
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            nb_touches += 1
            dx += -v_sin
            dy += v_cos
        if keys[pg.K_e] : #verification pour interagire avec les portes
            if (self.map_pos[0]+1,self.map_pos[1]) in self.game.map.interact: self.game.map.mini_map[self.map_pos[1]][self.map_pos[0]+1] = self.game.map.interact[(self.map_pos[0]+1,self.map_pos[1])]
            if (self.map_pos[0]-1,self.map_pos[1]) in self.game.map.interact: self.game.map.mini_map[self.map_pos[1]][self.map_pos[0]-1] = self.game.map.interact[(self.map_pos[0]-1,self.map_pos[1])]
            if (self.map_pos[0],self.map_pos[1]+1) in self.game.map.interact: self.game.map.mini_map[self.map_pos[1]+1][self.map_pos[0]] = self.game.map.interact[(self.map_pos[0],self.map_pos[1]+1)] 
            if (self.map_pos[0],self.map_pos[1]-1) in self.game.map.interact: self.game.map.mini_map[self.map_pos[1]-1][self.map_pos[0]] = self.game.map.interact[(self.map_pos[0],self.map_pos[1]-1)]
                

        if nb_touches >= 2: #on corrige le mouement diagonal saccadé
            dx *= self.diag_corr
            dy *= self.diag_corr
        

        self.collision_mur(dx,dy) #o regarde si il n'ya pas de mur et on deplace le joueur

        if keys[pg.K_1] : #on change la valeur de l'angle de vision
            self.angle -= JOUEUR_VITESSE_ROT * self.game.delta_temps
        if keys[pg.K_2] :
            self.angle += JOUEUR_VITESSE_ROT * self.game.delta_temps

        self.angle %= math.tau

    def draw(self):
        """methode qui permet de dessiner la carte pour le debug"""
        #pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #             (self.x * 100 + LARGEUR * math.cos(self.angle),
        #            self.y * 100 + LARGEUR * math.sin(self.angle)), 2 )
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def not_est_mur(self,x,y) :
        """methode qui verifie que le bloc est un mur"""
        if (x,y) in self.game.map.gost_blocs: 
            return True
        return (x,y) not in self.game.map.map_monde

    def collision_mur(self, dx, dy):
        """verifications des collisions entre le joueur et le mur"""
        taille = JOUEUR_X_TAILLE / self.game.delta_temps #le joueur n'est plus definie par un point mais par une sphère
        #on verifie que le joueur n'est pas sur un mur, si non il se deplace
        if self.not_est_mur(int(self.x + dx * taille), int(self.y)):
            self.x += dx #on change les coordonnée du joueur
        if self.not_est_mur(int(self.x), int(self.y + dy* taille)):
            self.y += dy #on change les coordonnée du joueur
        if self.x > len(self.game.map.mini_map[0]) or self.y > len(self.game.map.mini_map) or self.x < 0 or self.y < 0 :
            self.x, self.y = self.game.niveau.spawn #position du joueur

    def souris(self):
        """gestion le mouvement de la souris """
        sx, sy = pg.mouse.get_pos()
        if sx < S_BORD_GAUCHE or sx > S_BORD_DROIT :
            pg.mouse.set_pos([DEMI_LARGEUR,DEMI_HAUTEUR])
        self.pos_relative = pg.mouse.get_rel()[0]
        self.pos_relative = max(-S_MAX_REL, min(S_MAX_REL, self.pos_relative))
        self.angle += self.pos_relative * S_SENSI  * self.game.delta_temps
    def update(self):
        '''méthode qui met a jour le joueur'''
        if self.game.game_start :
            self.mouvement()
            self.souris()
            self.vie_recover()
    #création de deux propriété du joueur
    @property # décorateur qui permet de declarer simplement une propriété pour pouvoir utiliser des getter et des setter
    def pos(self):
        '''accede aux coordonnée x et y du joueur'''
        return self.x, self.y
    @property
    def map_pos(self):
        '''accede aux coordonnée x et y de la case ou le joueur se trouve'''
        return int(self.x),int(self.y)
    
