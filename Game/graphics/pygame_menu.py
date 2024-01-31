from __future__ import annotations
import datetime
import time
import pygame as pg
from python_data.parametres import *


def get_texture(chemin: str, res=(TAILLE_TEXTURE,TAILLE_TEXTURE)):
        """Fonction qui prend en argument un chemin et une resolution
            et retourne une surface pygame composée de l'image"""
        texture = pg.image.load(chemin).convert_alpha()
        return pg.transform.scale(texture, res)

def get_texture_size(chemin: str, taille: float):
    """Fonction qui prend en argument un chemin et une taille
            et retourne une surface pygame composée de l'image aisi que la taille de chaque coté"""
    img = pg.image.load(chemin).convert_alpha()
    largeur,hauteur = img.get_size()
    img = pg.transform.scale(img, (largeur*taille, hauteur * taille))
    largeur,hauteur = img.get_size()
    return img,largeur,hauteur



class pygame_Button:
    """class qui instancie in bouton pygame"""
    def __init__(self,chemin_text, menu: Menu, pos: tuple,taille,commande, b_index: int, espacement=2, chemin: str = 'media/hud/btn.png',chemin_hover: str ='media/hud/btn_clic.png',text: list = []) -> None:
        """intialisation de la class, prend en argument :
            - un chemin pour l'image d'un texte
            - un menu 
            - une position
            - une taille
            - une commande a executer 
            - un index de position sur le menu
            - un espacement entre le boutton du bas et lui meme 
            - un chemin de l'image du boutton
            - un chemin pour lorsque la souris passe dessus 
            - une liste de texte remplace le texte losqu'il est remplis"""
        self.menu = menu
        self.game = menu.game
        self.pos = pos
        self.commande = commande
        self.screen = self.menu.game.screen

        self.image,self.largeur,self.hauteur = get_texture_size(chemin,taille)
        self.image_h = get_texture_size(chemin_hover,taille)[0]

        self.largeur,self.hauteur = self.largeur//2,self.hauteur//2
        self.pos = self.pos[0] - self.largeur , self.pos[1] - self.hauteur + (espacement*self.menu.agrandisement + self.hauteur*2) * b_index
        self.zone = (self.pos[0],self.pos[0] + self.largeur*2,self.pos[1],self.pos[1] + self.hauteur*2)

        if text == [] :
            self.text = [(get_texture_size(chemin_text,taille)[0],self.pos)]
        else :
            self.text = [(self.game.FONT2.render(text_v, True, (0,0,0)),(self.pos[0] + pos[0] ,self.pos[1] + pos[1])) for text_v,pos in text] + [(self.game.FONT2.render(text_v, True, (255,255,255)),(self.pos[0] + pos[0], self.pos [1] + pos[1] - self.menu.agrandisement +1)) for text_v,pos in text]

    def get_hover(self):
        """Méthode qui regarde qi la souris est sur le boutton, renvoie True si ou sinon Faux"""
        sx, sy = self.menu.game.mousepos
        if self.zone[0] < sx < self.zone[1] and self.zone[2] < sy < self.zone[3] :
            return True
        return False
    
    def get_clic(self):
        """Retourne True si on clic sur le boutton sinon False"""
        sx, sy = self.menu.game.clic
        if self.zone[0] < sx < self.zone[1] and self.zone[2] < sy < self.zone[3] :
            return True
        return False

    def update(self):
        """Actualise chaque élément du boutton"""
        v = self.get_hover()
        v2 = self.get_clic()
        if v2 :
            self.screen.blit(self.image_h,(self.pos))
            self.commande()
            self.menu.game.clic = (0,0)
        elif v :
            self.screen.blit(self.image_h,(self.pos))
        else :
            self.screen.blit(self.image,(self.pos))
        [self.screen.blit(text,(pos)) for text,pos in self.text]

class Menu:
    """class qui instancie un menu classique"""
    def __init__(self, game, taille, ciel = 0, hud = 'media/hud/hud.png') -> None:
        """Initialisation d'un menu, prend en argument:
            - le jeu
            - la taille
            - le ciel actel
            - l'image de fond du texte"""
        self.game = game
        self.agrandisement = taille

        self.image_menu,self.largeur,self.heuteur = get_texture_size(hud,self.agrandisement)
        #on definit les variables des differents ciel en paralaxe
        self.ciel_off,self.ciel_off_2,self.ciel_off_3 = 0,0,0
        self.ciel_off_4,self.ciel_off_5,self.ciel_off_6 = 0,0,0
        self.ciel_off_7,self.ciel_off_8,self.ciel_off_9,self.ciel_off_10 = 0,0,0,0
        self.image_ciel = [[get_texture('media/textures/ciel/ciel4.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel5.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel6.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel4.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel5.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel6.png', (LARGEUR, HAUTEUR))],
                            [get_texture('media/textures/ciel/ciel1.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel2.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel3.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel1.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel2.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel3.png', (LARGEUR, HAUTEUR))],
                            
                            [get_texture('media/textures/ciel/ciel7.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel8.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel9.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel10.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/ciel11.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel7.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel8.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel9.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel10.png', (LARGEUR, HAUTEUR)),
                            get_texture('media/textures/ciel/r_ciel11.png', (LARGEUR, HAUTEUR)),]]
        self.index_ciel = ciel
        self.sizes = [(size[0]//2,size[1]//2) for size in [image[self.index_ciel].get_size() for image in self.image_ciel]]
    
    def menu_update(self):
        """Méthode qui actualise la position du ciel en fonction de la souris"""
        ancien_4,ancien_5,ancien_6 = self.ciel_off_4,self.ciel_off_5,self.ciel_off_6
        ancien_8,ancien_10 = self.ciel_off_8,self.ciel_off_10
        if  1 < self.game.mousepos[0] < LARGEUR-1 and 1 < self.game.mousepos[1] < HAUTEUR-1 :
            self.game.screen.fill((0,0,0))
            #on calcul les valeur d'offsets
            self.ciel_off = (self.ciel_off + 0.2 * self.game.rel_m[0]) % LARGEUR 
            self.ciel_off_4 = (self.ciel_off_4 + 0.25 * self.game.rel_m[1]) % HAUTEUR

            self.ciel_off_2 = (self.ciel_off_2 + 0.3 * self.game.rel_m[0]) % LARGEUR
            self.ciel_off_5 = (self.ciel_off_5 + 0.5 * self.game.rel_m[1]) % HAUTEUR

            self.ciel_off_3 = (self.ciel_off_3 + 0.4 * self.game.rel_m[0]) % LARGEUR
            self.ciel_off_6 = (self.ciel_off_6 + 1 * self.game.rel_m[1]) % HAUTEUR

            self.ciel_off_7 = (self.ciel_off_7 + 0.5 * self.game.rel_m[0]) % LARGEUR
            self.ciel_off_8 = (self.ciel_off_8 + 1.25 * self.game.rel_m[1]) % HAUTEUR

            self.ciel_off_9 = (self.ciel_off_9 + 0.6 * self.game.rel_m[0]) % LARGEUR
            self.ciel_off_10 = (self.ciel_off_10 + 1.5 * self.game.rel_m[1]) % HAUTEUR

        #on verifie que le ciel ne bouge pas trop
        if -70 > self.ciel_off_4 - ancien_4 or 70 < self.ciel_off_4 - ancien_4 : self.ciel_off_4,self.ciel_off_5,self.ciel_off_6,self.ciel_off_8,self.ciel_off_10 = ancien_4,ancien_5,ancien_6,ancien_8,ancien_10
        if -70 > self.ciel_off_5 - ancien_5 or 70 < self.ciel_off_5- ancien_5 : self.ciel_off_4,self.ciel_off_5,self.ciel_off_6,self.ciel_off_8,self.ciel_off_10 = ancien_4,ancien_5,ancien_6,ancien_8,ancien_10
        if -70 > self.ciel_off_6 - ancien_6 or 70 < self.ciel_off_6 - ancien_6 : self.ciel_off_4,self.ciel_off_5,self.ciel_off_6,self.ciel_off_8,self.ciel_off_10 = ancien_4,ancien_5,ancien_6,ancien_8,ancien_10
        if -70 > self.ciel_off_8 - ancien_8 or 70 < self.ciel_off_8 - ancien_8 : self.ciel_off_4,self.ciel_off_5,self.ciel_off_6,self.ciel_off_8,self.ciel_off_10 = ancien_4,ancien_5,ancien_6,ancien_8,ancien_10
        if -70 > self.ciel_off_10 - ancien_10 or 70 < self.ciel_off_10- ancien_10 : self.ciel_off_4,self.ciel_off_5,self.ciel_off_6,self.ciel_off_8,self.ciel_off_10 = ancien_4,ancien_5,ancien_6,ancien_8,ancien_10

        if len(self.image_ciel[self.index_ciel]) == 6 : #on affiche les ciel 
            self.game.screen.blit(self.image_ciel[self.index_ciel][0], (-self.ciel_off, -self.ciel_off_4//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][0], (-self.ciel_off + LARGEUR, -self.ciel_off_4//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][1], (-self.ciel_off_2, -self.ciel_off_5//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][1], (-self.ciel_off_2 + LARGEUR,-self.ciel_off_5//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][2], (-self.ciel_off_3, -self.ciel_off_6//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][2], (-self.ciel_off_3 + LARGEUR, -self.ciel_off_6//6))

            self.game.screen.blit(self.image_ciel[self.index_ciel][3], (-self.ciel_off, -self.ciel_off_4//6 + HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][3], (-self.ciel_off + LARGEUR, -self.ciel_off_4//6 + HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][4], (-self.ciel_off_2, -self.ciel_off_5//6 + HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][4], (-self.ciel_off_2 + LARGEUR,-self.ciel_off_5//6 + HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][5], (-self.ciel_off_3, -self.ciel_off_6//6 + HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][5], (-self.ciel_off_3 + LARGEUR, -self.ciel_off_6//6 + HAUTEUR))

        if len(self.image_ciel[self.index_ciel]) == 10 :

            self.game.screen.blit(self.image_ciel[self.index_ciel][0], (-self.ciel_off, -self.ciel_off_4//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][0], (-self.ciel_off + LARGEUR, -self.ciel_off_4//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][1], (-self.ciel_off_2, -self.ciel_off_5//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][1], (-self.ciel_off_2 + LARGEUR,-self.ciel_off_5//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][2], (-self.ciel_off_3, -self.ciel_off_6//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][2], (-self.ciel_off_3 + LARGEUR, -self.ciel_off_6//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][3], (-self.ciel_off_7, -self.ciel_off_8//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][3], (-self.ciel_off_7 + LARGEUR, -self.ciel_off_8//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][4], (-self.ciel_off_9, -self.ciel_off_10//6))
            self.game.screen.blit(self.image_ciel[self.index_ciel][4], (-self.ciel_off_9 + LARGEUR, -self.ciel_off_10//6))

            self.game.screen.blit(self.image_ciel[self.index_ciel][5], (-self.ciel_off, -self.ciel_off_4//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][5], (-self.ciel_off + LARGEUR, -self.ciel_off_4//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][6], (-self.ciel_off_2, -self.ciel_off_5//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][6], (-self.ciel_off_2 + LARGEUR,-self.ciel_off_5//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][7], (-self.ciel_off_3, -self.ciel_off_6//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][7], (-self.ciel_off_3 + LARGEUR, -self.ciel_off_6//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][8], (-self.ciel_off_7, -self.ciel_off_8//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][8], (-self.ciel_off_7 + LARGEUR, -self.ciel_off_8//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][9], (-self.ciel_off_9, -self.ciel_off_10//6+ HAUTEUR))
            self.game.screen.blit(self.image_ciel[self.index_ciel][9], (-self.ciel_off_9 + LARGEUR, -self.ciel_off_10//6+ HAUTEUR))

        
        self.game.screen.blit(self.image_menu,(DEMI_LARGEUR-self.largeur//2,DEMI_HAUTEUR-self.heuteur//2))  

class Menu_p(Menu):
    """Menu principal"""
    def __init__(self, game, taille) -> None:
        super().__init__(game,taille,0)
        #on creer les bouttons utiles 
        self.b_list = [pygame_Button('media/hud/1.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//6 ),self.agrandisement,lambda: self.game.new_game('t'),0),
                       pygame_Button('media/hud/2.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//6 ),self.agrandisement,lambda: self.game.change_menu(3),1),
                       pygame_Button('media/hud/3.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//6 ),self.agrandisement,lambda: self.game.new_game('i'),2),
                       pygame_Button('media/hud/4.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//6 ),self.agrandisement,lambda: self.game.change_menu(2),3),
                       pygame_Button('media/hud/5.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//6 ),self.agrandisement,lambda: self.game.quit(),4.5)]
    def menu_update(self):
        """Méthode qui actualise le menu"""
        super().menu_update()
        [b.update() for b in self.b_list]

class Menu_stats(Menu):
    """Menu des Statitistiques """
    def __init__(self, game, taille) -> None:
        """intialisation de la class"""
        super().__init__(game,taille,2)
        self.pos = (DEMI_LARGEUR,DEMI_HAUTEUR)
        #on recupère les valeur dynamiquement
        text = [(f'{self.game.ancienscore}',(-40,-15)),(f'{self.game.ancienenemycount}',(-40,60)),(f'{self.game.anciencompteurtemps}',(-40,100))] 
        self.texts = [[self.game.FONT.render(text_v, True, (0,0,0)),None] for text_v,pos in text] + [[self.game.FONT.render(text_v, True, (255,255,255)),None] for text_v,pos in text]
        espacement = 0
        for i in range(len(self.texts)//2): #on calcule toute les positions des textes en fonction de la taille du menu
            text_width = self.texts[i][0].get_width()
            text_height = self.texts[i][0].get_height()
            self.texts[i][1] = (DEMI_LARGEUR - text_width/2,DEMI_HAUTEUR/1.35 + espacement*self.agrandisement)
            espacement += 13.5
        espacement = 0
        for i in range(len(self.texts)//2,len(self.texts)):
            text_width = self.texts[i][0].get_width()
            text_height = self.texts[i][0].get_height()
            self.texts[i][1] = (DEMI_LARGEUR - text_width/2,DEMI_HAUTEUR/1.35 + espacement*self.agrandisement - self.agrandisement)
            espacement += 13.5
        print(self.texts)
        self.text = get_texture_size('media/hud/hud2.png',self.agrandisement)[0]
        self.b_list = [pygame_Button('media/hud/6.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//6 ),self.agrandisement,lambda: self.game.change_menu(1),4.5)]

    def menu_update(self):
        """Méthode qui actualise le menu"""
        super().menu_update()
        self.game.screen.blit(self.text,(DEMI_LARGEUR-self.largeur//2,DEMI_HAUTEUR-self.heuteur//2))  
        [b.update() for b in self.b_list]
        [self.game.screen.blit(self.texts[i][0],(self.texts[i][1])) for i in range(len(self.texts)) if i != 5 and i != 2]
        t = str(datetime.timedelta(seconds=round(self.game.intanciencompteurtemps + time.time()- self.game.compteurtemps)))
        self.game.screen.blit(self.game.FONT.render(t, True, (0,0,0)),(self.texts[2][1]))
        self.game.screen.blit(self.game.FONT.render(t, True, (255,255,255)),(self.texts[5][1]))


class Menu_saves(Menu):
    """Menu de selection de sauvegarde"""
    def __init__(self, game, taille) -> None:
        super().__init__(game,taille,1,'media/hud/hud3.png')
        self.data = game.savedata #on recupère les info
        t1,t2,t3 = self.data[1]['temps'],self.data[2]['temps'],self.data[3]['temps']
        l1,l2,l3 = self.data[1]['level'],self.data[2]['level'],self.data[3]['level']
        print(self.data)
        v1,v2,v3 = self.data[1]['vie'],self.data[2]['vie'],self.data[3]['vie']
        liste1 = [(f'Sauvegarde 1 : {str(datetime.timedelta(seconds=round(t1)))}',(20,2.5*self.agrandisement)),(f'Niveau : {l1}',(20,8.3*self.agrandisement)),(f'Vie : {v1}',(20,14.16*self.agrandisement))] if self.data[1]['started'] else []
        liste2 = [(f'Sauvegarde 2 : {str(datetime.timedelta(seconds=round(t2)))}',(20,2.5*self.agrandisement)),(f'Niveau : {l2}',(20,8.3*self.agrandisement)),(f'Vie : {v2}',(20,14.16*self.agrandisement))] if self.data[2]['started']  else []
        liste3 = [(f'Sauvegarde 3 : {str(datetime.timedelta(seconds=round(t3)))}',(20,2.5*self.agrandisement)),(f'Niveau : {l3}',(20,8.3*self.agrandisement)),(f'Vie : {v3}',(20,14.16*self.agrandisement))] if self.data[3]['started']  else []
        c1 = lambda: self.game.new_game(l1, 1)
        c2 = lambda: self.game.new_game(l2, 2)
        c3 = lambda: self.game.new_game(l3, 3) #onaffiche les bouttons en questions
        self.b_list = [pygame_Button('media/hud/8.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//2.8 ),
                                     self.agrandisement,
                                     c1,1,3,'media/hud/btn2.png','media/hud/btn2_clic.png',
                                     liste1),
                        pygame_Button('media/hud/8.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//2.8 ),
                                      self.agrandisement,
                                      c2,2,3,'media/hud/btn2.png','media/hud/btn2_clic.png',
                                      liste2),
                        pygame_Button('media/hud/8.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//2.8 ),
                                      self.agrandisement,
                                      c3,3,3,'media/hud/btn2.png','media/hud/btn2_clic.png',
                                      liste3),
                        pygame_Button('media/hud/6.png',self,(DEMI_LARGEUR,DEMI_HAUTEUR- self.heuteur//6 ),
                                      self.agrandisement,
                                      lambda: self.game.change_menu(1),4.25,3,'media/hud/btn3.png','media/hud/btn3_clic.png')]
    def menu_update(self):
        """Méthode qui actualise le menu"""
        super().menu_update()
        [b.update() for b in self.b_list]