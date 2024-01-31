#all the code in this repository are under BSD 2-Clause License

import math
import requests
import webbrowser
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

import python_data.parametres as p
from graphics.tkinter_graphique import *

version = 1
global ok 
ok = False
global a 
a = 6
class Windows(tk.Tk):
    def __init__(self):
        """ fenètre de lancement du jeu """
        super().__init__()
        self.geometry('500x500') #on definie la taille de la fenètre
        self.title('The War launcher') #on definie le titre de la fenètre
        self.protocol("WM_DELETE_WINDOW", self.quitw) #le protocol de fermeture de la fnètre
        self.wm_title("The War launcher") #on definie le titre de la fenètre tkinter
        try:
            self.iconbitmap('media\\icone.ico') #on définie l'icone de la fenètre
        except:
            pass # si une erreur survient lors de l'import de l'icone on ne change pas l'icone, ce sera celle de base
        titre(self, 'Game Launcher')
        titre(self, 'Paramètres :',15)
        self.taille = selection_ttk(self,'Taille de la fenètre :', ['1920 x 1080','1900 x 1000','1000 x 600','900 x 600'],'1900 x 1000')
        self.texture = selection_ttk(self,'Qualité des textures :', ['Ultra','Haute','Moyenne','Basse'],'Moyenne')
        self.proj = selection_ttk(self,'Qualité de la projection 3d :', ['Ultra','Haute','Moyenne','Basse'],'Moyenne')
        self.fov = selection_ttk(self,'Champs de vision FOV :', ["Grand (déformation possible)",'Normal','Bas'],'Normal')
        self.fps = selection_ttk(self,'Blocage des FPS :', ['Pas de Blocage','60','30'],'Pas de Blocage')
        button_ttk(self,'ok',self.quittrue)
    
    def quitw(self):
        """méthode qui quitte le code"""
        self.quit()
        self.destroy()
    
    def quittrue(self):
        """méthode qui quitte le code mais qui lance le jeu"""
        #on definit les variable en fonction de ce que l'on choisit
        global a
        global ok
        c = {'1920 x 1080':(1920,1080),'1900 x 1000':(1900,1000),'1000 x 600':(1000,600),'900 x 600':(900,600)}
        c1 = {'Ultra':2048,'Haute':1024,'Moyenne':512,'Basse':256}
        c2 = {'Ultra':1,'Haute':2,'Moyenne':4,'Basse':6}
        c3 = {"Grand (déformation possible)":2,'Normal':3,'Bas':4}
        c4 = {'Pas de Blocage':0,'60':60,'30':30}
        p.RES = p.LARGEUR, p.HAUTEUR = c.get(self.taille.get(),(1900,1000))
        p.DEMI_LARGEUR = p.LARGEUR // 2
        p.DEMI_HAUTEUR = p.HAUTEUR // 2
        p.FPS = c4.get(self.fps.get(), 0)
        #paramètre du raycast
        p.FOV = math.pi / c3.get(self.fov.get(),3) #champs de vision
        p.DEMI_FOV = p.FOV / 2
        p.NB_RAYONS = p.LARGEUR // c2.get(self.proj.get(),2)# nombre de rayon pour le raycast
        p.DEMI_NB_RAYON = p.NB_RAYONS // 2
        p.DELTA_ANGLE = p.FOV / p.NB_RAYONS #angle entre chaque rayon

        #Paramètre de projection
        p.DISTANCE_RENDU = p.DEMI_LARGEUR / math.tan(p.DEMI_FOV)
        p.ECHELLE = p.LARGEUR // p.NB_RAYONS

        #textures 
        p.TAILLE_TEXTURE = c1.get(self.texture.get(),512)
        p.DEMI_TAILLE_TEXTURE = p.TAILLE_TEXTURE // 2
        p.S_BORD_DROIT = 100
        p.S_BORD_GAUCHE = p.LARGEUR - p.S_BORD_DROIT

        if p.RES == (1920,1080) :
            p.S_SENSI = 0.00012
            a = 6
        if p.RES == (1900,1000) :
            p.S_SENSI = 0.00015
            a = 5.5
        if p.RES == (1000,600) :
            p.S_SENSI = 0.0004
            a = 3.5
        if p.RES == (900,600) :
            p.S_SENSI = 0.0006
            a = 3.5
        ok = True
        self.quit()
        self.destroy()

if __name__ == '__main__' :
    try: 
        url = 'https://raw.githubusercontent.com/ahmedmathsinfo/TheWarGame-main/main/Media/version.txt'
        page = requests.get(url)
        if int(page.text) != version :
            messagebox.showwarning('Mise a jour', 'Une Nouvelle mise a jour est disponible ! (vous pouvez quand meme acceder au jeu) : \n {}')
            webbrowser.open('amimiprojects.studio')
    except: pass

    root = Windows() #on lance l'application
    root.mainloop() #on lance la boucle tkinter
    if ok : 
        from core.Game import *
        game = Game(1,a) #on lance le jeu en fonction de la fenètre
        game.run()

