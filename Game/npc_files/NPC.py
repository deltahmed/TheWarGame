from core.sprite_obj import * 
from random import randint, random, choice 

class NPC(SpriteAnim):
    """class qui instancie les monstre"""
    def __init__(self, game, chemin='media/npc/soldier/0.png', pos=(10.5, 5.5), taille=0.6, shift=0.38, temps_anim=180, ranged=0):
        """initialisation de la class parent et des variables utile au programme"""
        super().__init__(game, chemin, pos, taille, shift, temps_anim)
        self.attaque_images = self.get_image(self.chemin + '/attack')
        self.mort_images = self.get_image(self.chemin + '/death')
        self.idle_images = self.get_image(self.chemin + '/idle')
        self.mal_images = self.get_image(self.chemin + '/pain')
        self.marche_images = self.get_image(self.chemin + '/walk')

        try :
            c = chemin[0:len(chemin)-5]
            self.npc_douleur = pg.mixer.Sound(c + 'npc_pain.wav')
            self.npc_douleur.set_volume(0.1)
            self.npc_mort = pg.mixer.Sound(c + 'npc_death.wav')
            self.npc_mort.set_volume(0.1)
            self.npc_tire = pg.mixer.Sound(c + 'npc_attack.wav')
            self.npc_tire.set_volume(0.1)
        except : pass

        self.pts = 10
        self.attaque_dist = randint(3,6)
        self.vitesse = 0.03
        self.taille = 10
        self.vie = 100
        self.attaque_v = 10
        self.visee = 0.15
        self.en_vie = True
        self.douleur = False
        self.raycast_v = False
        self.frame_count = 0
        self.vuejoueur = False
        self.ranged = ranged
        self.sc = False

    def update(self):
        """actualisation du programme"""
        self.check_temps()
        self.get()
        self.run()
    
    def not_est_mur(self,x,y) :
        """on regarde si c'est un mur ou non"""
        if (x,y) in self.game.map.gost_blocs: 
            return True
        return (x,y) not in self.game.map.map_monde

    def collision_mur(self, dx, dy):
        """on gère les collision entre le NPC et les murs"""
        #on verifie que le joueur n'est pas sur un mur, si non il se deplace
        if self.not_est_mur(int(self.x + dx * self.taille), int(self.y)):
            self.x += dx #on change les coordonnée du joueur
        if self.not_est_mur(int(self.x), int(self.y + dy* self.taille)):
            self.y += dy #on change les coordonnée du joueur

    def movement(self):
        """on deplace le NPC grace a l'algorithme de BFS"""
        next_pos = self.game.recherche_joueur.get_chemin(self.map_pos, self.game.joueur.map_pos, self)
        if next_pos == None :
            self.vuejoueur = False
            return
        next_x, next_y = next_pos
        #debug uniquement :
        # pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.obj.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.vitesse
            dy = math.sin(angle) * self.vitesse
            self.collision_mur(dx, dy)

    def attaque(self):
        """méthode qui permet a l'NPC d'attaquer le joueur"""
        if self.trigger:
            try : self.npc_tire.play()
            except : pass
            if random() < self.visee :
                self.game.joueur.get_damage(self.attaque_v)
            
    
    def annimer_mort(self):
        """annimation de la mort du NPC"""
        if not self.en_vie:
            if self.game.global_trigger and self.frame_count < len(self.mort_images)-1 :
                self.mort_images.rotate(-1)
                self.image = self.mort_images[0]
                self.frame_count += 1

    def annimer_douleur(self):
        """annimation de la douleur du NPC"""
        self.annimer(self.mal_images)
        if self.trigger:
            self.douleur = False 

    def check_coups(self):
        """Verification de si le joueur touche le NPC"""
        if self.raycast_v and self.game.joueur.tire_variable:
            if DEMI_LARGEUR - self.image_demi_largeur * self.taille//6 * self.ranged < self.screen_x < DEMI_LARGEUR + self.image_demi_largeur * self.taille//6 * self.ranged :
                try : self.npc_douleur.play()
                except: pass
                self.game.joueur.tire_variable = False
                self.douleur = True
                self.vie -= self.game.arme.damage
                self.check_vie()

    def check_vie(self):
        """On verifie la vie du NPC ainsi que s'il est mort ou non"""
        if self.vie < 1 :
            self.en_vie = False
            try: self.npc_mort.play()
            except: pass
            if self.game.level == 'i' and not self.sc :
                self.sc = True
                self.game.score += self.pts
                self.game.enemycount += 1


    def run(self):
        """on execute les elment tel que le NPC puisse faire tout ce qui lui ai demandé"""
        if self.en_vie:
            self.raycast_v = self.raycast_npc()
            self.check_coups()
            if self.douleur:
                self.annimer_douleur()
            elif self.raycast_v :
                if len(self.game.obj.processus_en_cours) <= 5 :
                    self.game.obj.processus_en_cours.append(self) #on gère le nombre de personne entrain d'utiliser le DFS pour les problème de performances
                self.vuejoueur = True
                if self.dist < self.attaque_dist:
                    self.annimer(self.attaque_images)
                    self.attaque()
                else :
                    self.annimer(self.marche_images)
                    self.movement()
            elif self.vuejoueur : 
                self.annimer(self.marche_images)
                self.movement()
            else:
                try : self.game.obj.processus_en_cours.remove(self)
                except : pass
                self.annimer(self.idle_images)

        else :
            try: self.game.obj.processus_en_cours.remove(self)
            except : pass
            self.annimer_mort()
    @property #propriéter pareil que dans le fichier joueur.py
    def map_pos(self):
        return int(self.x), int(self.y)

    def raycast_npc(self):
        """Calcul du champs de vision de notre NPC, pour savoir si il nous vois ou non """
        if self.game.joueur.map_pos == self.map_pos:
            return True
        
        distance_mur_v,distance_mur_h = 0,0
        distance_joueur_v,distance_joueur_h = 0,0
        
        #on recupère les valeurs utile pour le calcul
        ox, oy = self.game.joueur.pos # coordonnée du joueur
        x_map, y_map = self.game.joueur.map_pos #case du joueur

        angles_rayon = self.theta

        
        sin_angle = math.sin(angles_rayon) + 0.00001
        cos_angle = math.cos(angles_rayon) + 0.00001

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
            if case_hor == self.map_pos:
                distance_joueur_h = profondeur_horizontal
                break
            if case_hor in self.game.map.map_monde : #si la case est un mur on casse la boucle
                distance_mur_h = profondeur_horizontal
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
            if case_vert == self.map_pos :
                distance_joueur_v = profondeur_vertical
                break
            if case_vert in self.game.map.map_monde : #si la case est un mur on casse la boucle
                distance_mur_v = profondeur_vertical
                break 
            x_vert += dx
            y_vert += dy 
            profondeur_vertical += delta_profondeur #on change la case séléctionnée
        
        distance_joueur = max(distance_joueur_h, distance_joueur_v)
        distance_mur = max(distance_mur_h, distance_mur_v)

        if 0 < distance_joueur < distance_mur or not distance_mur:
            return True
        return False 
    

#class enfants pour chaque enemi différent :
class SoldierNPC(NPC):
    def __init__(self, game, path='media/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=120):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50


class Bouler(NPC):
    def __init__(self, game, path='media/npc/bouler/0.png', pos=(10.5, 5.5),
                 scale=1.2, shift=-0.055, animation_time=120):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.attaque_dist = 1
        self.vitesse = 0.05
        self.taille = 20
        self.vie = 200
        self.attaque_v = 10
        self.visee = 1
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50

class Mage(NPC):
    def __init__(self, game, path='media/npc/mage/0.png', pos=(10.5, 5.5),
                 scale=1.2, shift=-0.055, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time, 0.35)
        self.pts = 70
        self.attaque_dist = 5
        self.vitesse = 0.02
        self.taille = 10
        self.vie = 200
        self.attaque_v = 30
        self.visee = 0.08
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50

class Robot(NPC):
    def __init__(self, game, path='media/npc/robot/0.png', pos=(10.5, 5.5),
                 scale=1.2, shift=-0.046, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time, 0.35)
        self.pts = 50
        self.attaque_dist = 3
        self.vitesse = 0.05
        self.taille = 15
        self.vie = 200
        self.attaque_v = 5
        self.visee = 0.1
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50

class Worm(NPC):
    def __init__(self, game, path='media/npc/worm/0.png', pos=(10.5, 5.5),
                 scale=1.4, shift=0.22, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 5
        self.attaque_dist = 1
        self.vitesse = 0.04
        self.taille = 15
        self.vie = 50
        self.attaque_v = 5
        self.visee = 0.1
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50


class Golem(NPC):
    def __init__(self, game, path='media/npc/golem/0.png', pos=(10.5, 5.5),
                 scale=1.4, shift=-0.05, animation_time=220):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 100
        self.attaque_dist = 1.5
        self.vitesse = 0.01
        self.taille = 15
        self.vie = 500
        self.attaque_v = 50
        self.visee = 0.5
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50


class GolemGlace(NPC):
    def __init__(self, game, path='media/npc/golemglace/0.png', pos=(10.5, 5.5),
                 scale=1, shift=0.17, animation_time=220):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 100
        self.attaque_dist = 1.5
        self.vitesse = 0.01
        self.taille = 15
        self.vie = 500
        self.attaque_v = 50
        self.visee = 0.5

        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50



class Metal(NPC):
    def __init__(self, game, path='media/npc/metal/0.png', pos=(10.5, 5.5),
                 scale=1.4, shift=0.001, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 20
        self.attaque_dist = 1.2
        self.vitesse = 0.04
        self.taille = 15
        self.vie = 100
        self.attaque_v = 10
        self.visee = 0.2
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50


class Metalb(NPC):
    def __init__(self, game, path='media/npc/metalb/0.png', pos=(10.5, 5.5),
                 scale=1.4, shift=0.001, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 20
        self.attaque_dist = 1.2
        self.vitesse = 0.04
        self.taille = 15
        self.vie = 100
        self.attaque_v = 10
        self.visee = 0.2
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50


class Metalg(NPC):
    def __init__(self, game, path='media/npc/metalg/0.png', pos=(10.5, 5.5),
                 scale=1.4, shift=0.001, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 20
        self.attaque_dist = 1.2
        self.vitesse = 0.04
        self.taille = 15
        self.vie = 100
        self.attaque_v = 10
        self.visee = 0.2
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50

class Metalw(NPC):
    def __init__(self, game, path='media/npc/metalw/0.png', pos=(10.5, 5.5),
                 scale=1.4, shift=0.001, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 20
        self.attaque_dist = 1.2
        self.vitesse = 0.04
        self.taille = 15
        self.vie = 100
        self.attaque_v = 10
        self.visee = 0.2
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50

class Oeil(NPC):
    def __init__(self, game, path='media/npc/oeil/0.png', pos=(10.5, 5.5),
                 scale=0.7, shift=0.2, animation_time=120):
        super().__init__(game, path, pos, scale, shift, animation_time, 1)
        self.pts = 5
        self.attaque_dist = 1
        self.vitesse = 0.05
        self.taille = 20
        self.vie = 50
        self.attaque_v = 10
        self.visee = 1
        if self.game.level == 0 :
            self.attaque_dist = 1
            self.vitesse = 0
            self.attaque_v = 0
            self.vie = 50
