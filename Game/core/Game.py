from __future__ import annotations
import pygame as pg
import datetime
import time
import sys

from python_data.Niveau import *
from graphics.pygame_menu import *
from core.Carte import *
from player.Joueur import *
from graphics.moteur_graphique import *
from graphics.affichage_obj import *
from core.Objets import *
from player.Arme import *
from python_data.Sound import *
from npc_files.RechercheJoueur import *
from python_data.parametres import *



class Game:
    def __init__(self, niveau=0, agrandi = 6) -> None:
        '''initialisation de la class avec pygame'''
        pg.init()
        try: pg.mixer.init()
        except: pass
        self.FONT = pg.font.Font("media/pixelfont.ttf",int(5*agrandi))
        self.FONT2 = pg.font.Font("media/pixelfont.ttf",int(4*agrandi))
        self.screen = pg.display.set_mode(RES) # définition de la résolution 
        self.clock = pg.time.Clock() #on définini toute les variable nessessaire au fonctionnement du jeu
        self.compteurtemps = time.time()

        self.agrandissement = agrandi
        self.enemycount = 0
        self.score = 0
        self.scorelist = []
        self.scorelist.append(self.score)
        self.anciencompteurtemps = str(datetime.timedelta(seconds=0))
        self.save = 0
        #variable des sauvegardes
        self.savedata = {1: {'level': 1, 'vie': VIE_MAX, 'temps': 0, 'started': False},
                         2: {'level': 1, 'vie': VIE_MAX, 'temps': 0, 'started': False},
                         3: {'level': 1, 'vie': VIE_MAX, 'temps': 0, 'started': False}}
        
        self.getdata() #on recupère les info depuis les fichier

        self.level = 't'
        self.game_start = False
        self.delta_temps = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0

        pg.time.set_timer(self.global_event, 40)
        self.menu_v = 1
        self.mousepos = (0,0)
        self.rel_m = (0,0)
        self.clic =  (0,0)
        self.menu() #on creer et affiche le menu
        self.levels = [DebugMode(),Niveau1(),Niveau2()]

    def new_game(self, l, save = 0):
        '''Méthode qui creer une nouvelle partie'''
        self.game_start = True #on creer les differents objets utiles a la partie
        self.menu_v = 0
        pg.mouse.set_visible(False)
        self.level = l
        if save :
            self.save = save
        if isinstance(l, int) :
            self.niveau = self.levels[self.level]
        elif l == 't': self.niveau = Tuto()
        elif l == 'i' : self.niveau = choice([Niveauinf1(),Niveauinf2()]) 
        self.map = Carte(self, self.niveau)
        self.joueur = Joueur(self)
        self.objrendu = Rendu_obj(self,  self.niveau)
        self.raycast = RayCast(self)
        self.obj = Objets(self)
        self.arme = Arme(self)
        self.sound = Sound(self,  self.niveau)
        self.recherche_joueur = RechercheJoueur(self)
    
    def getdata(self):
        """recupère les variables stockée dans les fichier du jeu"""
        v1 = load_object('data/anti_cheat_data/local.anti_cheat') #donnée enregistrée dans plussieur fichier pour eviter les bidouillages
        v2 = load_object('data/anti_cheat_data/stored.anti_cheat') #donnée du score du temsp de jeu du score et des enemie tuee
        v3 = load_object('data/tempdata/local.temp')
        v4 = load_object('data/player_data/player.data')
        if all([v1.tueencc == v2.tueencc, v2.tueencc==v3.tueencc, v3.tueencc==v4.tueencc, v4.tueencc==v1.tueencc,
                v1.scnzsjd == v2.scnzsjd, v2.scnzsjd==v3.scnzsjd, v3.scnzsjd==v4.scnzsjd, v4.scnzsjd==v1.scnzsjd,
                v1.tamjndj == v2.tamjndj, v2.tamjndj==v3.tamjndj, v3.tamjndj==v4.tamjndj, v4.tamjndj==v1.tamjndj,
                  *list((v.floup for v in (v1,v2,v3,v4)))]) :
            self.anciencompteurtemps = str(datetime.timedelta(seconds=round(v1.tamjndj)))
            self.intanciencompteurtemps = v1.tamjndj
            self.ancienenemycount = v1.tueencc
            self.ancienscore = v1.scnzsjd

        s1 = load_object('data/player_data/gamesave1.save') #donnée des sauvegarde
        s2 = load_object('data/player_data/gamesave2.save')
        s3 = load_object('data/player_data/gamesave3.save')

        self.savedata = {1: {'level': s1.level, 'vie': s1.life, 'temps': s1.time, 'started': s1.started},
                         2: {'level': s2.level, 'vie': s2.life, 'temps': s2.time, 'started': s2.started},
                         3: {'level': s3.level, 'vie': s3.life, 'temps': s3.time, 'started': s3.started}}

    def update(self): #actualisation
        '''Méthode qui actualise la fenètre selon nos paramètres'''
        self.joueur.update()
        self.map.update()
        self.raycast.update()
        self.obj.update()
        self.arme.update()
        pg.display.flip()
        self.delta_temps = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self): #affichage
        '''Méthode qui dessine la fenètre'''
        self.objrendu.draw()
        self.arme.draw()
        #pour le debug uniquement :
        #self.map.draw()
        #self.joueur.draw()

    def check_event(self): #On regarde les action pour correctement fermer la fenetre quand on quite l'application
        '''Méthode qui ferme la fenètre proprement lorsqu'on l'a quite et qui verifie que les menu s'affiche bien ou non '''
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit()
            elif not self.menu_v :
                if event.type == self.global_event:
                    self.global_trigger = True
                self.joueur.tire(event)
            if self.menu_v and event.type == pg.MOUSEBUTTONDOWN :
                if event.button == 1:
                    self.clic = pg.mouse.get_pos()
        if self.menu_v :
            self.mousepos = pg.mouse.get_pos()
            self.rel_m = pg.mouse.get_rel()

    def quit(self):
        """Méthode qui permet de quitter la fenetre et d'enregistrer les informations"""
        timer = time.time() - self.compteurtemps #enregistrement
        self.scorelist.append(self.score)
        score = max(self.scorelist) if max(self.scorelist) > self.ancienscore else self.ancienscore
        data = Data(score,self.intanciencompteurtemps + timer,self.ancienenemycount+self.enemycount)
        if self.save : #enregistrement
            save_object(Gamesaves(timer,self.level,self.joueur.vie,True), f'data/player_data/gamesave{self.save}.save')
        #enregistrement
        save_object(data, 'data/anti_cheat_data/local.anti_cheat')
        save_object(data, 'data/anti_cheat_data/stored.anti_cheat')
        save_object(data, 'data/tempdata/local.temp')
        save_object(data, 'data/player_data/player.data')
        pg.quit() #on quitte la fenètre
        sys.exit()
    
    def menu(self) :
        """Méthode qui creer les différents menu"""
        self.menu_liste = [Menu_p(self,self.agrandissement),Menu_stats(self,self.agrandissement),Menu_saves(self,self.agrandissement)]
        self.menu_v = 1
        pg.mouse.set_visible(True)

    def change_menu(self, x: int):
        """Méthode qui permet de changer le menu actuel"""
        self.menu_v = x

    def run(self):
        '''Méthode qui permet de jouer le code a l'infinie'''
        while True:
            self.check_event()
            if self.menu_v :
                self.menu_liste[self.menu_v-1].menu_update()
                pg.display.flip()
            else :
                self.update()
                self.draw()

class Data:
   """class qui permet d'enregistrer les information"""
   def __init__(self, score, time, killed ) -> None:
      '''class qui permet d'enregistrer les information, les element etrange permettes de brouiller les pistes'''
      self.ekzjnfj = 'sfndcuisbchjinsdchjbncshjc jnc djnc njsc'
      self.cnzsjcf = 'sncjdscnjkcjksncdjkncjkc n vh cj c canco'
      self.scnzsjd = score
      self.nmplplo = 'jdnsjcjisdncjdsj cjk  ns jsj  c dcnd scd'
      self.dckezdp = 'njdsnjkd sck ds c cnskd ckn sjkd ckc , d'
      self.tamjndj = time
      self.tueencc = killed
      self.floup = False
      self.djncshdchsc(5151,85181,8184)


   def djncshdchsc(self, c , jfnvj, djncj):
      """fonction qui ne sert a rien a part brouiller les pistes"""
      c
      jfnvj
      djncj
      self.ekzjnfj
      self.cnzsjcf
      self.scnzsjd
      self.nmplplo
      self.dckezdp
      self.tamjndj
      self.tueencc
      self.floup = True

class Gamesaves:
   '''class qui permet d'enregistrer les sauvegardes'''
   def __init__(self, time, level, life, started) -> None:
      self.time, self.level, self.life = time, level, life
      self.started = started
