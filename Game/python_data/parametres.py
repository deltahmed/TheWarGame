import math

#Parametre général du projet
RES = LARGEUR, HAUTEUR = 1920,1080
DEMI_LARGEUR = LARGEUR // 2
DEMI_HAUTEUR = HAUTEUR // 2
FPS = 0

#Paramètre du joueur 
JOUEUR_POS = 2.5, 5.5 #sur la mini map
JOUEUR_ANGLE = 0 #angle de vue
JOUEUR_VITESSE = 0.006 #vitesse du joueure
JOUEUR_VITESSE_ROT = 0.002 #vitesse de rotation
JOUEUR_X_TAILLE = 60 #grosseur du joueur
VIE_MAX = 100

#paramètre du raycast
FOV = math.pi / 3 #champs de vision
DEMI_FOV = FOV / 2
NB_RAYONS = LARGEUR // 2# nombre de rayon pour le raycast
DEMI_NB_RAYON = NB_RAYONS // 2
DELTA_ANGLE = FOV / NB_RAYONS #angle entre chaque rayon
PROFONDEUR_MAX = 30 #profondeur maximum
PROFONDEUR_MAX_OBJ = 20 #profondeur maximum

#Paramètre de projection
DISTANCE_RENDU = DEMI_LARGEUR / math.tan(DEMI_FOV)
ECHELLE = LARGEUR // NB_RAYONS

#textures 
TAILLE_TEXTURE = 256
DEMI_TAILLE_TEXTURE = TAILLE_TEXTURE // 2

#paramètre de la souris
S_SENSI = 0.00015
S_MAX_REL = 40 #mouvement relatif de la souris maximum
S_BORD_GAUCHE = 100
S_BORD_DROIT = LARGEUR - S_BORD_GAUCHE


DISTANCE_FOCAL = 100
ECHELLE_MODE7 = 100
