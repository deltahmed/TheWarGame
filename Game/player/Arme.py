from core.sprite_obj import *

class Arme(SpriteAnim):
    """Class correspondant a l'arme du joueur, elle herite de la class Sprite annim"""
    def __init__(self, game, chemin='media/objets/armes/pompe/0.png', taille=0.6, temps_anim=90):
        """definition des variable utile au programme"""
        super().__init__(game=game, chemin=chemin, taille=taille, temps_anim=temps_anim)
        #chargement des images de l'annimation dans une queue
        self.images = deque([pg.transform.smoothscale(img, (self.image.get_width()* taille, self.image.get_height() * taille)) for img in self.images])
        self.arme_pos = (DEMI_LARGEUR - self.images[0].get_width() // 2, HAUTEUR - self.images[0].get_height())
        self.recharge = False
        self.num_images = len(self.images)
        self.frame_count = 0
        self.damage = 50

    def animation(self):
        """annime l'arme losque la variable recharge est sur true"""
        if self.recharge :
            self.game.joueur.tire_variable = False
            if self.trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_count += 1
                if self.frame_count == self.num_images:
                    self.recharge = False
                    self.frame_count = 0


    def draw(self):
        """Dessine l'arme a l'ecran"""
        self.game.screen.blit(self.images[0], self.arme_pos)
    
    def update(self):
        """rafrachissemnt de l'annimation"""
        self.check_temps()
        self.animation()