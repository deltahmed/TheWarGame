from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from typing_extensions import Literal
import customtkinter as ctk
from PIL import Image,ImageTk

from typing import Any, List, Literal, Optional,Union,Tuple,Callable
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt

class Button(ctk.CTkButton):
    def __init__(self,master,text: str,command: Callable, side: str = tk.TOP, taille: Union[float,int]=18):
        super().__init__(master=master, text=text, command=command,font=('Arial', taille))
        self.pack(side=side, padx=5,pady=10,) #pack avec 10 de marge y et 20 de marge x

class ButtonPlage(ctk.CTkFrame) :
    def __init__(self,master,num: int, listtexts: List[str], listcmd: List[Callable]):
        super().__init__(master, fg_color="transparent")
        self.l = []
        for i in range(num): #pour chaque element de la liste creer des bouttons a gauche de frame
            x = Button(self,text=listtexts[i],command=listcmd[i], side=tk.LEFT)
            self.l.append(x)
        self.pack()

class Text(ctk.CTkLabel):
    def __init__(self, master, text: str, taille=18):
        self.text_var = tk.StringVar(value=text)
        super().__init__(master,textvariable= self.text_var,font=('Arial', taille))
        self.pack(padx=20,pady=10)


class Champs(ctk.CTkEntry):
    def __init__(self, master):
        super().__init__(master)

class Selection(ctk.CTkFrame):
    def __init__(self, master, Titre: str, values: list, default: str):
        super().__init__(master, fg_color="transparent")
        self.combobox_var = ctk.StringVar(value=default)  # valeur initials
        self.text_var = tk.StringVar(value=Titre) 
        self.label = ctk.CTkLabel(master=self,textvariable=self.text_var,font=('Arial', 18))
        self.label.pack(padx=5,pady=5,side= tk.LEFT) 
        self.select = ctk.CTkComboBox(master=self,values=values,state="readonly", variable=self.combobox_var) #combobox de etkinter
        self.select.pack(padx=20, pady=10, side = tk.LEFT)
        self.pack()

class ColorChooser(ctk.CTkFrame):
    def __init__(self,master,Titre:str, command: Callable, file: str ='images\colorw.png'):
        super().__init__(master, fg_color="transparent")
        try:
            self.text_var = tk.StringVar(value=Titre)
            self.label = ctk.CTkLabel(master=self,textvariable=self.text_var,font=('Arial', 18)) # création du texte 
            self.label.pack(padx=5,pady=5,side= tk.LEFT) 
            self.img = Image.open(file)  # on ouvre l'icone
            self.photo_image = ctk.CTkImage(light_image=self.img,dark_image=self.img,size=(15,15)) 
            self.b = ctk.CTkButton(master=self, command=command,text='', image=self.photo_image, width=16) #on crée un boutton avec cette icone
            self.b.pack(side= tk.LEFT) 
            self.pack() #on affiche le tout
        except : # si le programme echoue renvoyer une erreur
            raise FileNotFoundError(f'file {file} not found')

class CheckBox(ctk.CTkFrame):
    def __init__(self, master, Titre:str, command, on, off, defaultvar):
        super().__init__(master, fg_color="transparent")
        self.check_var = tk.BooleanVar(value=defaultvar)
        self.checkbox = ctk.CTkCheckBox(master=self, text=Titre, command=command,variable=self.check_var, onvalue=on, offvalue=off) #creation de la checkbox
        self.checkbox.pack(side= tk.LEFT)
        self.pack() #affichage du tout


class MenuBox(ctk.CTkScrollableFrame):
    def __init__(self, master, Titre: str, desc: str, anchor='ne', *args: Tuple[str,Callable]):
        super().__init__(master=master,border_color=('#000000','#FFFFFF'),height=450,width=300,border_width=4,corner_radius=20)
        self.anchor_v = anchor
        self.menu = False
        self.l = []
        self.textliste = []
        if Titre != None: #on crée le Titre si il est différent de None
            self.Titre = Text(self,Titre,25)
        if desc != None: #on crée la description si il est différent de None
            self.desc = Text(self,desc,12)
        for texte,command in args: # pour chaque texte et chaque commande si elle n'est pas egal a None on crée le bouton approprié
            if command != None :
                b = ctk.CTkButton(master=self, text=texte, command=command,font=('Arial', 18)) # bouton de la bibliothèque customtkinter
                self.l.append(b)
                b.pack(side=tk.TOP, padx=5,pady=5,) #pack avec 10 de marge y et 20 de marge x
            else : # sinon on ecrit juste un texte
                t = Text(self,texte,18)
                self.textliste.append(t)
        self.pack() #on affiche le menu
        self.place(relx=-1, rely=-1, anchor=self.anchor_v) #on place le menu en dehors de la fenètre

    def flip(self):
        """affichage du menu déroulant"""
        if self.menu :
            self.menu = False
            self.place(relx=-1, rely=-1, anchor=self.anchor_v)
        else :
            self.menu = True
            self.place(relx=1, rely=0.1, anchor=self.anchor_v)
    
    def cacher(self) :
        self.menu = False
        self.place(relx=-1, rely=-1, anchor=self.anchor_v)
    
    def afficher(self) :
        self.menu = True
        self.place(relx=1, rely=0.1, anchor=self.anchor_v)

class ImageButton(ctk.CTkButton):
    def __init__(self,master,image: str,command: Callable, side: str = tk.TOP, taille: Tuple[int,int]=(50,50)):
        img = Image.open(image)  # on ouvre l'icone
        photo_image = ctk.CTkImage(light_image=img,dark_image=img,size=taille) 
        super().__init__(master=master, image=photo_image, command=command, width=taille[0], height=taille[1], fg_color="transparent", border_width=0, border_spacing=0, text ='')
        self.pack(side=side, padx=0,pady=0) #pack avec 10 de marge y et 20 de marge x

class ImageButtonPlage(ctk.CTkFrame) :
    def __init__(self, master, listbutton: List[Tuple[str,Callable]], taille: Tuple[int,int] = (50,50)):
        super().__init__(master, fg_color="transparent")
        self.masterh = master
        self.l = []
        for nom, commande in listbutton: #pour chaque element de la liste creer des bouttons a gauche de frame
            x = ImageButton(self,nom,commande,tk.LEFT,taille)
            self.l.append(x)
        self.pack(side=tk.TOP, padx=0,pady=0)

class ImagesButtonGrid(ctk.CTkFrame):
    def __init__(self, master, listeimages: List[List[Tuple[str,Callable]]],taille: Tuple[int,int] = (50,50)):
        super().__init__(master, fg_color="transparent")
        self.masterh = master
        self.l = []
        for listes in listeimages:
            x = ImageButtonPlage(self,listes,taille)
            self.l.append(x)
        self.pack(padx=0,pady=0)

    def __getitem__(self, key: Tuple[int,int]) -> Any:
        return self.l[key[1]].l[key[0]]

class IDImagesMenuBox(ctk.CTkScrollableFrame):
    def __init__(self, master, Titre: str, desc: str, listeimages: List[List[Tuple[str,Callable]]], taille=(30,30), anchor='ne'):
        super().__init__(master=master,border_color=('#000000','#FFFFFF'),height=450,width=300,border_width=4,corner_radius=20)
        self.masterh = master
        self.anchor_v = anchor
        self.menu = False
        if Titre != None: #on crée le Titre si il est différent de None
            self.titre = Text(self,Titre,25)
        if desc != None: #on crée la description si il est différent de None
            self.desc = Text(self,desc,12)

        self.gridimg = ImagesButtonGrid(self, listeimages,taille)

        self.pack() #on affiche le menu
        self.place(relx=-1, rely=-1, anchor=self.anchor_v) #on place le menu en dehors de la fenètre


    def flip(self):
        """affichage du menu déroulant"""
        if self.menu :
            self.menu = False
            self.place(relx=-1, rely=-1, anchor=self.anchor_v)
        else :
            self.menu = True
            self.place(relx=1, rely=0.1, anchor=self.anchor_v)
    
    def cacher(self) :
        self.menu = False
        self.place(relx=-1, rely=-1, anchor=self.anchor_v)
    
    def afficher(self) :
        self.menu = True
        self.place(relx=1, rely=0.1, anchor=self.anchor_v)

def isanumber(char):
    try: 
        int(char)
        return True
    except: return False