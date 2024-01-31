from core.sprite_obj import *
from npc_files.NPC import *
import tkinter.messagebox as messagebox
import core.Carte as c

def random_coo(i,j):
    return (i+choice([-random()/2,random()/2]),j+choice([-random()/2,random()/2]))


class Objets: 
    def __init__(self, game) -> None:
        """initialisation de la class qui instancie les objets du jeu"""
        self.game = game
        self.obj_liste = []
        self.npc_liste = []
        self.processus_en_cours = []
        self.chemin_npc = 'media/npc'
        self.chemin_objets = 'media/objets'
        add = self.add_sprite
        addnpc = self.add_npc
        self.npc_positions = {}
        self.trigger = False
        self.annim = False
        self.temps_prev = pg.time.get_ticks()
        objshandler = game.niveau.obj_handle
        objs = game.objrendu.objects
        
        for object in objshandler : #on creer tout les objets (sans mauvais jeu de mot)
            if object == 'green' :
                for pos in objshandler[object] :
                    add(SpriteAnim(game, pos=pos, taille = objs[object][1], shift = objs[object][2]))
            else :
                for pos in objshandler[object] : 
                    add(Sprite(game, objs[object][0], pos, objs[object][1], objs[object][2]))


        for elm in game.niveau.mob_pos : #on creer tout les monstres
            if elm == 'bouler' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Bouler(game,pos=vals))
            if elm == 'golem' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Golem(game,pos=vals))
            if elm == 'golemglace' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(GolemGlace(game,pos=vals))
            if elm == 'mage' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Mage(game,pos=vals))
            if elm == 'metal' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Metal(game,pos=vals))
            if elm == 'metalb' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Metalb(game,pos=vals))
            if elm == 'metalg' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Metalg(game,pos=vals))
            if elm == 'metalw' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Metalw(game,pos=vals))
            if elm == 'oeil' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Oeil(game,pos=vals))
            if elm == 'robot' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Robot(game,pos=vals))
            if elm == '_' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(SoldierNPC(game,pos=vals))
            if elm == 'worm' :
                for vals in  game.niveau.mob_pos.get(elm, []) :
                    addnpc(Worm(game,pos=vals))
        
    def check_win(self):
        """Verification de si le joueur gagne la partie"""
        if self.game.level == 'i' or self.game.level == 't' :
            if not len(self.npc_positions):
                if self.game.level == 't':
                    self.game.objrendu.win() #affichage du message
                    pg.display.flip()
                    pg.time.delay(500)
                else :
                        pg.display.flip()
                        pg.time.delay(10)
                self.game.new_game(self.game.level) #lancement d'une nouvelle partie ou de la continuité du mode infini
        
    def update(self):
        """actualisation de tout les objets du jeu"""
        self.npc_positions = {npc.map_pos for npc in self.npc_liste if npc.en_vie }
        [sprite.update() for sprite in self.obj_liste]
        [npc.update() for npc in self.npc_liste]
        self.check_win()
    

    def add_sprite(self, sprite):
        """ajouter un objet"""
        self.obj_liste.append(sprite)

    def add_npc(self, npc):
        """ajouter un monstre"""
        self.npc_liste.append(npc)


        
    