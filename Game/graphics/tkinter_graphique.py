import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable,List,Union

#on reprend ce fichier fait pour un ancien projet

#on reprend les fonctions tkinter crée pour le projet 4 en les adaptant a ttk
def titre(master,text: str,taille=18) : #affiche un titre sur la fenetre
    '''Prend une frame ou une fenetre master ainsi qu'un texte en paramètre et creer un titre sur la fenètre'''
    label = ttk.Label(master=master,text=text,font=('Helvetica',taille)) #texte
    label.pack(padx=5,pady=5) #pack avec 10 de marge y et 20 de marge x
def selection_ttk(master,Titre: str,values: list, default: Union[int,str]):
    '''prend en paramètre une fenetre ou une frame, un titre, une liste de valeurs et une valeur par default et renvoie un boite de séléction'''
    combobox_var = tk.StringVar(value=default)  # valeur initials
    keepvalue = combobox_var.get()
    frame = tk.Frame(master) #on creer une nouvelle frame
    text_var = tk.StringVar(value=Titre) 
    label = tk.Label(master=frame,textvariable=text_var)
    label.pack(padx=5,pady=5,side= tk.LEFT) 
    select = ttk.Combobox(master=frame,values=values,state="readonly", textvariable=keepvalue) #combobox de tkinter
    if isinstance(default,int) :
        select.current(default)
    else :
        select.current(values.index(default))
    select.pack(padx=3, pady=4, side = tk.LEFT)
    frame.pack()
    return select #on retourne la boite de selection pour pouvoir la manipuler plus tard

def button_ttk(master, text: str, command: Callable) : #creer un bouton sur la fenetre ou la frame master
    '''Prend une frame ou une fenetre master, un texte et une commande en paramètre et creer un boutton'''
    b = ttk.Button(master=master, text=text, command=command) # bouton de la bibliothèque customtkinter
    
    b.pack(side=tk.TOP, padx=20,pady=10,) #pack avec 10 de marge y et 20 de marge x

def button_left_ttk(master, text: str, command: Callable) : #creer un bouton sur la gauche sur la fenetre ou la frame master
    '''Prend une frame ou une fenetre, un texte et une commande en paramètre et creer un boutton qui sera pack a gauche'''
    b = ttk.Button(master=master, text=text, command=command,font=('Arial', 18)) # bouton de la bibliothèque customtkinter
    b.pack(side=tk.LEFT, padx=2,pady=10,) #pack avec 10 de marge y et 2 de marge x
    return b #on retourne le bouton en question pour pouvoir le manipuler plus tard

def multiple_button_ttk(master,num: int,listtexts: List[str], listcmd: List[Callable]): #creer plusieurs bouttons allignée
    '''Prend une frame ou une fenetre master,un nombre n de boutton, une liste de n textes et une liste de n commandes en paramètre et creer plusieurs boutton alignée sur master'''
    frame = tk.Frame(master, fg_color="transparent") # on inistialise une frame
    l = []
    for i in range(num): #pour chaque element de la liste creer des bouttons a gauche de frame
        x = button_left_ttk(frame,text=listtexts[i],command=listcmd[i])
        l.append(x)
    frame.pack()
    return l #on retourne tout les boutons dans une liste pour pouvoir les manipuler plus tard