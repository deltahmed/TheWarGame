import os
import pygame as pg
from python_data.parametres import *


def get_texture(chemin: str, res=(TAILLE_TEXTURE,TAILLE_TEXTURE)):
        """Fonction qui prend en argument un chemin et une resolution
            et retourne une surface pygame composée de l'image"""
        texture = pg.image.load(chemin).convert_alpha()
        return pg.transform.scale(texture, res)

def flip(sequance: list,elm_actuelle):
    """fonction qui prend en entrée une liste non vide et un élément actuelle, elle renvoie le nouvelle élément choisit"""
    return sequance[sequance.index(elm_actuelle) -1]

def round_05(number):
    """fonction qui arrondit au 0,5 près"""
    return round(number * 2) / 2

pi = math.pi #calcule de variable pour ne pas a les recalculer
demi_pi = pi / 2
moins_demi_pi = -demi_pi
_3pisur2 = (3 * pi)/2

class Rendu_obj:
    """Géstion du rendu de tout les objets a l'écran"""
    def __init__(self, game, niveau) -> None:
        """initialisation des textures et des variables utiles"""
        self.game = game 
        self.screen = game.screen
        self.texture_mur = {} #on recupère les textures des murs dans un dictionnaire id: texture
        for file_name in os.listdir('media/textures/'):
            file_j = os.path.join('media/textures/', file_name)
            if os.path.isfile(file_j):
                num = int(''.join([c for c in file_name if isanumber(c)]))#on recupère l'id
                self.texture_mur[num] = get_texture(file_j) #on l'ajoute au dictionnaire
                #un id ne peu correspondre qu'a une seul texture
        self.objects = {
        'b1': ('media/objets/b1.png',0.5,0.5), 
         'b2': ('media/objets/b2.png',0.5,0.5), 
         'b3': ('media/objets/b3.png',0.5,0.5), 
         'b4': ('media/objets/b4.png',0.5,0.5), 
         'b5': ('media/objets/b5.png',0.5,0.5), 
         'bone': ('media/objets/bone.png',0.3,1.25), 
         'bone2': ('media/objets/bone2.png',0.3,1.25), 
         'brics': ('media/objets/brics.png',0.3,1.25), 
         'brics2': ('media/objets/brics2.png',0.3,1.25), 
         'chaise': ('media/objets/chaise.png',0.7,0.22), 
         'chaise2': ('media/objets/chaise2.png',0.7,0.22), 
         'coffin': ('media/objets/coffin.png',0.5,0.5), 
         'coffin2': ('media/objets/coffin2.png',0.5,0.5), 
         'cross0': ('media/objets/cross0.png',0.3,1.2), 
         'cross1': ('media/objets/cross1.png',0.3,1.2), 
         'cross2': ('media/objets/cross2.png',0.3,1.2), 
         'cross3': ('media/objets/cross3.png',0.3,1.2), 
         'GRASS_1': ('media/objets/GRASS_1.png',0.3,1.25), 
         'GRASS_2': ('media/objets/GRASS_2.png',0.3,1.25), 
         'GRASS_3': ('media/objets/GRASS_3.png',0.3,1.25), 
         'GRASS_4': ('media/objets/GRASS_4.png',0.3,1.25), 
         'GRASS_5': ('media/objets/GRASS_5.png',0.3,1.25), 
         'grave': ('media/objets/grave.png',0.3,1.2), 
         'grave2': ('media/objets/grave2.png',0.3,1.2), 
         'lampe1': ('media/objets/lampe1.png',0.4,-0.74), 
         'lampe2': ('media/objets/lampe2.png',0.4,-0.74), 
         'mush': ('media/objets/mush.png',0.3,1.2), 
         'plante': ('media/objets/plante.png',0.3,1.25), 
         'plante2': ('media/objets/plante2.png',0.3,1.25), 
         'ROCK_1': ('media/objets/ROCK_1.png',0.3,1.25), 
         'ROCK_2': ('media/objets/ROCK_2.png',0.3,1.25), 
         'skull2': ('media/objets/skull2.png',0.3,1.2), 
         'table': ('media/objets/table.png',0.6,0.5), 
         'z1': ('media/objets/z1.png',0.7,0.22), 
         'z2': ('media/objets/z2.png',0.7,0.22), 
         'z3': ('media/objets/z3.png',0.7,0.22), 
         'z4': ('media/objets/z4.png',0.2,-0.22), 
         'z5': ('media/objets/z5.png',0.7,0.22), 
         'z6': ('media/objets/z6.png',0.7,0.22), 
         'z7': ('media/objets/z7.png',0.7,0.22), 
         'z8': ('media/objets/z8.png',0.7,0.22),
         'z9': ('media/objets/z9.png',0.7,0.22),
         'zelda': ('media/objets/zelda.png',0.5,0.2),
         'green': ('media/objets/green/0.png',0.7,0.22)}


        
        self.selection = niveau.select #ciel et sol lors de l'apparition
        self.default_select = niveau.default_select #ciel et sol hors des salles
        self.salles = niveau.salles #salles
        #on définit un dictinaire pour les ciels/plafond et les ols
        self.image_ciel = {'jour': [get_texture('media/textures/ciel/ciel1.png', (LARGEUR, DEMI_HAUTEUR)),
                                    get_texture('media/textures/ciel/ciel2.png', (LARGEUR, DEMI_HAUTEUR)),
                                    get_texture('media/textures/ciel/ciel3.png', (LARGEUR, DEMI_HAUTEUR))],
                            'nuit': [get_texture('media/textures/ciel/ciel4.png', (LARGEUR, DEMI_HAUTEUR)),
                                    get_texture('media/textures/ciel/ciel5.png', (LARGEUR, DEMI_HAUTEUR)),
                                    get_texture('media/textures/ciel/ciel6.png', (LARGEUR, DEMI_HAUTEUR))],
                           'gris': (101, 101, 101),
                           }
        self.image_sol = {'gris': (99, 96, 94),
                          'grisfonce': (56, 63, 64),
                          'marron': (89, 47, 23),
                          'vert': (0, 89, 18)}
        self.ciel_off,self.ciel_off_2,self.ciel_off_3 = 0,0,0 #offset pour l'effet paralaxe 
        self.sol_off = 0 
        self.screen_img = get_texture('media/rouge.png', RES)

        self.taille_nombres = 90 # on deffinit unetaille 
        self.nombres_textures = [get_texture(f'media/textures/nb/{i}.png', [self.taille_nombres] * 2) for i in range(11)]
        self.nombes = dict(zip(map(str, range(11)), self.nombres_textures))
        #on charge d'autres images utile au jeu
        self.game_over_image = get_texture('media/game_over.png', RES)
        self.win_image = get_texture('media/win.png', RES)
        #liste des objet de type assets (ceux affiché surla carte)
        self.liste_obj_png = []
 
    def damage_joueur(self):
         """affiche un ecran rouge quand le joueur est touché"""
         self.screen.blit(self.screen_img, (0,0))

    def game_over(self):
         """affiche le game over"""
         self.screen.blit(self.game_over_image, (0,0))

    def win(self) :
        """affiche l'image quans on gagne"""
        self.screen.blit(self.win_image, (0,0))

    

    def draw_vie(self):
        """affichage de la vie sur l'ecran"""
        vie = str(self.game.joueur.vie)
        for i, char in enumerate(vie):
            self.screen.blit(self.nombes[char], (i * self.taille_nombres, 0))
        self.screen.blit(self.nombes['10'], ((i + 1) * self.taille_nombres, 0))
    
    def rendu_obj_du_jeu(self):
        """pour tout les objets a rendre"""
        liste_obj = sorted(self.game.raycast.obj_a_rendre, key=lambda x: x[0], reverse=True)
        for profondeur, image, pos in liste_obj :
            #si l'image est un objet de type assets
            if image in self.liste_obj_png :
                self.screen.blit(image, pos) #on affiche l'objet
            else : #sinon pour les murs
                couleur= (0,0,0,255 - 255/(1+profondeur**4.5*0.00002)) #on calcule la couleur en fonction de la profondeur
                self.screen.blit(image, pos) #on affiche l'image
                shape_surf = pg.Surface(image.get_size(), pg.SRCALPHA)
                pg.draw.rect(shape_surf, couleur, shape_surf.get_rect())  #on affiche la coupeur
                self.screen.blit(shape_surf, pos)

    def get_current_ciel_sol(self):
        """Séléction du ciel et du sol en temps reel"""
        pos = self.game.joueur.map_pos
        angle = self.game.joueur.angle
        l = []
        for salle in self.salles : #gestion des salles
            if pos in salle[1]:
                self.selection = salle[0]
            if salle[-1] == 'y' and pos == salle[2] :
                if salle[-2] == 'g' :
                    if 0 < angle < pi : #gestion des portes
                        self.selection = self.default_select
                    else :
                        self.selection = salle[0]
                else :
                    if 0 < angle < pi : #gestion des portes
                        self.selection = salle[0]
                    else :
                        self.selection = self.default_select

            if salle[-1] == 'x' and pos == salle[2] :
                if salle[-2] == 'h' :
                    if demi_pi < angle < _3pisur2 : #gestion des portes
                        self.selection = self.default_select
                    else :
                        self.selection = salle[0]
                else :
                    if demi_pi < angle < _3pisur2 : #gestion des portes
                        self.selection = salle[0]
                    else :
                        self.selection = self.default_select
            if pos not in salle[1] and pos != salle[2]:
                l.append(True)
        if len(self.salles) == len(l) and all(l) : #sinon on affiche le ciel de la carte
            self.selection = self.default_select
             

    def draw_ciel_sol(self):
        """fonction qui affiche le ciel et le sol"""
        ciel = self.image_ciel[self.selection[0]]
        if isinstance(ciel, list) : #si le ciel est en parlaxe il l'affiche 
            self.ciel_off = (self.ciel_off + 2.25 * self.game.joueur.pos_relative) % LARGEUR
            self.screen.blit(self.image_ciel[self.selection[0]][0], (-self.ciel_off, 0))
            self.screen.blit(self.image_ciel[self.selection[0]][0], (-self.ciel_off + LARGEUR, 0))
            self.ciel_off_2 = (self.ciel_off_2 + 3.5 * self.game.joueur.pos_relative) % LARGEUR
            self.screen.blit(self.image_ciel[self.selection[0]][1], (-self.ciel_off_2, 0))
            self.screen.blit(self.image_ciel[self.selection[0]][1], (-self.ciel_off_2 + LARGEUR, 0))
            self.ciel_off_3 = (self.ciel_off_3 + 4 * self.game.joueur.pos_relative) % LARGEUR
            self.screen.blit(self.image_ciel[self.selection[0]][2], (-self.ciel_off_3, 0))
            self.screen.blit(self.image_ciel[self.selection[0]][2], (-self.ciel_off_3 + LARGEUR, 0))
        elif isinstance(ciel, tuple) : #si c'est une couleur il l'affiche 
            pg.draw.rect(self.screen, ciel, (0,-DEMI_HAUTEUR, LARGEUR, HAUTEUR))
        else : #sinon (juste une image)
            self.ciel_off = (self.ciel_off + 5 * self.game.joueur.pos_relative) % LARGEUR
            self.screen.blit(self.image_ciel[ciel], (-self.ciel_off, 0))
            self.screen.blit(self.image_ciel[ciel], (-self.ciel_off + LARGEUR, 0))
        #sol self.texture_mur
        pg.draw.rect(self.screen, self.image_sol[self.selection[1]], (0,DEMI_HAUTEUR, LARGEUR, HAUTEUR))
    
    def draw_score(self):
        t = 'Score : ' + str(self.game.score)
        self.game.screen.blit(self.game.FONT.render(t, True, (0,0,0)),((20,HAUTEUR-50)))
        self.game.screen.blit(self.game.FONT.render(t, True, (215,0,0)),((20,HAUTEUR-49 - self.game.agrandissement )))         
    
    def draw(self):
        """affichage des différents éléments de l'écran"""
        self.get_current_ciel_sol()
        self.draw_ciel_sol()
        self.rendu_obj_du_jeu()
        self.draw_vie()
        if self.game.level == 'i' : self.draw_score()
         
    
def isanumber(char: str):
    """Fonction qui prend un charactère en entrée et qui renvoie si cecarractère est un nombre entier ou non"""
    try: 
        int(char)
        return True
    except: return False