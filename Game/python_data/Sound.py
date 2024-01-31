import pygame as pg


class Sound:
    """class qui stock les variable relative au son du jeu"""
    def __init__(self, game, niveau) -> None:
        
        self.game = game 
        try : #si l'utilisateur n'a pas de periferique audio on ne fait rien
            self.chemin = 'media/son/'
            self.pompe = pg.mixer.Sound(self.chemin + 'shotgun.wav')
            self.pompe.set_volume(0.1)
            self.joueur_douleur_s = pg.mixer.Sound(self.chemin + 'player_pain.wav')
            self.theme = pg.mixer.music.load(self.chemin + 'theme.mp3') #la musique du jeu n'est pas encore implémenté en jeu
            pg.mixer.music.set_volume(0.1)
        except : 
            self.chemin = 'media/son/'
            self.pompe = Sound_error()
            self.joueur_douleur_s = Sound_error()
            self.theme = Sound_error()


class Sound_error: #permet d'eviter les erreurs
    def __init__(self) -> None:
        pass
    def play(self):
        print('erreur son')