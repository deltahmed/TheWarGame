#all the code in this repository are under BSD 2-Clause License

from __future__ import annotations

import os
import time
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from typing import List, Union
from PIL import Image,ImageTk
from pathvalidate import sanitize_filepath

import customtkinter as ctk
import numpy as np

from AffichageGraphique import *
from importexport import *


class Windows(ctk.CTk):
    def __init__(self):
        """ fenètre de base de l'application """
        super().__init__()
        self.geometry('1000x1000') #on definie la taille de la fenètre
        self.taille = '1000x1000' 
        self.title('Générateur de Map') #on definie le titre de la fenètre
        self.protocol("WM_DELETE_WINDOW", self.quitw) #le protocol de fermeture de la fnètre
        self.wm_title("Générateur de Map") #on definie le titre de la fenètre tkinter
        try:
            self.iconbitmap('Creatormedia\\icone.ico') #on définie l'icone de la fenètre
        except:
            pass # si une erreur survient lors de l'import de l'icone on ne change pas l'icone, ce sera celle de base
        self.framemain = MainTK(self) # on gènre les diférentes frames de notre application
        self.framegen = GenererTK(self)
        self.framecrea = Creator(self)
        self.framemain.pack(fill='both', expand=True) #on affiche la fenètre principal framemain
        

    def changeframe(self,frame):
        """fonction qui change la frame affichée"""
        self.framemain.pack_forget()
        self.framecrea.pack_forget()
        self.framegen.pack_forget()
        frame.pack(side="top", fill="both", expand=True)

    def changewithclear(self, frame):
        """fonction qui change la frame affichée en supprimant les élément de la frame du graph et du labyrinthe"""
        self.framemain.pack_forget()
        self.framecrea.pack_forget()
        self.framegen.pack_forget()
        for widgets in self.framemain.winfo_children():
            widgets.destroy()
        for widgets in self.framecrea.winfo_children():
            widgets.destroy()
        for widgets in self.framegen.winfo_children():
            widgets.destroy()
        self.framemain.initialisation()
        self.framegen.initialisation()
        frame.pack(side="top", fill="both", expand=True)

    def quitw(self):
        """méthode qui quitte le code"""
        plt.close('all') 
        plt.ioff()
        self.quit()
        self.destroy()
        quit()

class MainTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """Frame de la page principal"""
        super().__init__(parent)
        self.parent = parent
        self.initialisation()

    def initialisation(self):
        #affichage et assignations des éléments de la fenètre
        Text(self,'Map Creator', 50)
        Button(self,'Creer une Map',lambda : self.parent.changeframe(self.parent.framegen))
        Button(self,'Importer une Map (a venir)',self.fonctionalit)
        Button(self,'Paramètres (a venir)',self.fonctionalit)
        Button(self,'Quitter',self.parent.quit)

    def fonctionalit(self):
        messagebox.showinfo('Fonctionnalité', 'Fonctionnalité a venir')


class GenererTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """Frame de la page principal"""
        super().__init__(parent)
        self.parent = parent
        self.initialisation()

    def initialisation(self):
        #affichage et assignations des éléments de la fenètre
        Text(self, 'Générer une Map', 50)
        Text(self, 'Nom :')
        self.nom = Champs(self)
        self.nom.pack()
        Text(self, 'Hauteur :')
        self.e_hauteur = Champs(self)
        self.e_hauteur.pack()
        Text(self, 'Longueur :')
        self.e_longueur = Champs(self)
        self.e_longueur.pack()
        Button(self, 'Générer', lambda: self.parent.framecrea.initialisation(self.e_hauteur.get(),self.e_longueur.get(),self.nom.get()))
        ButtonPlage(self,2, ['Menu Principal','Reset'], [self.menuprincipal, self.reset])

    def menuprincipal(self):
        self.reset()
        self.parent.changeframe(self.parent.framemain)
    def reset(self):
        """fonction qui reset la page"""
        for widgets in self.winfo_children():
            widgets.destroy()
        self.initialisation()


class Creator(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """Frame de la page principal"""
        super().__init__(parent)
        self.parent = parent

    def initialisation(self,h,l,name):

        self.nom = name
        try: 
            h,l = int(h),int(l)
            if h < 2 or h > 60 or l > 60 or l < 9 :
                raise ValueError()
        except: 
            messagebox.showerror('Erreur','Un entier Naturel superieur entre 9 et 60 est Requis')
            self.parent.changewithclear(self.parent.framegen)
            return
        self.maptaille = (l,h)
        self.etapes = 0
        self.selected = 1
        self.start = (2.5, 5.5)
        self.roomselected = None
        self.sky_selected = ['jour','gris']
        self.salles = []
        self.textures = {}
        self.texturesplacements = {}
        self.objectsplacements = {}
        self.drawings = []
        self.objects = {}
        self.buttons = ButtonPlage(self, 4, ['Menu principal', 'Clear', 'Textures', 'Passer Au Menu Suivant'],[self.clear,self.reset,self.fliptextmenu, self.fliproommenu])
        self.canvas = tk.Canvas(self, width=self.maptaille[0]*30, height=self.maptaille[1]*30)
        self.canvas.bind('<Button-1>',self.get_x_y)
        self.canvas.bind('<B1-Motion>',self.get_x_y_motion)
        self.canvas.bind('<Button-3>',self.get_x_y_2)
        self.canvas.bind('<Button-2>',self.adddoor)
        self.canvas.bind('<Double-Button-2>',self.addspawn)
        for x in range(0, self.maptaille[0]*30, 30):
            for y in range(0, self.maptaille[1]*30, 30):
                self.canvas.create_rectangle(x, y, x+30, y+30, outline='black',fill='white')
        self.canvas.pack()
        try:
            liste = []
            sublist = []
            for file_name in os.listdir('Creatormedia/Textures/'):
                file_j = os.path.join('Creatormedia/Textures/', file_name)
                if os.path.isfile(file_j):
                    num = int(''.join([c for c in file_name if isanumber(c)]))
                    self.textures[num] = ImageTk.PhotoImage(Image.open(file_j).resize((30,30), Image.LANCZOS),master=self)
                    self.texturesplacements[num] = []
                    sublist.append((file_j, lambda x= num: self.change_selected(x)))
                if len(sublist) == 6 :
                    liste.append(sublist)
                    sublist = []
            if sublist != [] :
                liste.append(sublist)

            liste2 = []
            sublist2 = []
            for file_name in os.listdir('Creatormedia/Entitee/'):
                file_j = os.path.join('Creatormedia/Entitee/', file_name)
                if os.path.isfile(file_j):
                    name = os.path.basename(os.path.splitext(file_j)[0])
                    self.textures[name] = ImageTk.PhotoImage(Image.open(file_j).resize((30,30), Image.LANCZOS),master=self)
                    self.objectsplacements[name] = []
                    sublist2.append((file_j, lambda x= name: self.change_selected(x)))
                if len(sublist2) == 2 :
                    liste2.append(sublist2)
                    sublist2 = []
            if sublist2 != [] :
                liste2.append(sublist2)
        

            self.textures[0] = ImageTk.PhotoImage(Image.open('Creatormedia/c.png').resize((30,30), Image.LANCZOS),master=self)
        except: 
            messagebox.showerror('Erreur Fatal', "Une erreur fatal s'est produite le programme ne peut pas fonctionner correctement")
            self.parent.quit()
        self.textmenu = IDImagesMenuBox(self, 'Textures', f'Choisir un element : {self.selected}', liste)
        self.entitiesmenu = IDImagesMenuBox(self, 'Entitée', 'Choisir un element', liste2, (100,100))
        self.roommenu = MenuBox(self, 'Room selector', 'ciel/plafond', 'ne', 
                                (f'Ajouter une room : {len(self.salles)}', self.addroom),
                                (f'Changer de room : {self.roomselected}', self.changeroom),
                                ('supprimer une room', self.delroom),
                                (f'{self.roomselected}:{None}', None),
                                ('Ciel/Plafond:', None),
                                (f'selected: {self.sky_selected}', None),
                                ('jour', lambda: self.sky_change_selected('jour', 0)),
                                ('gris', lambda: self.sky_change_selected('gris', 0)),
                                ('Sol:', None),
                                ('gris', lambda: self.sky_change_selected('gris', 1)),
                                ('gris foncé', lambda: self.sky_change_selected('grisfonce', 1)),
                                ('marron', lambda: self.sky_change_selected('marron', 1)))
        self.parent.changeframe(self)

    def addspawn(self, event):
        if self.etapes == 2 :
            self.start = (round_to_multiple(event.x-15,15)/30, round_to_multiple(event.y-15,15)/30)
            messagebox.showinfo('Point de spawn', f'point de spawn modifié en {self.start}')
    def clear(self):
        msg = messagebox.askokcancel('Attention !',"Vous etes sur le points tout effacer, voulez vous continuer")
        if msg :
            self.textmenu.cacher()
            self.entitiesmenu.cacher()
            self.roommenu.cacher()
            self.selected = 1
            self.parent.changewithclear(self.parent.framemain)
    def fliptextmenu(self):
        if self.entitiesmenu.menu :
            self.entitiesmenu.cacher()
        if self.roommenu.menu :
            self.roommenu.cacher()
        if self.etapes == 0 :
            self.textmenu.flip()
        if self.etapes != 0 :
            messagebox.showerror('Erreur','impossible de revenir en arrière')
    
    def fliproommenu(self):
        if self.textmenu.menu :
            self.textmenu.cacher()
        if self.entitiesmenu.menu :
            self.entitiesmenu.cacher()
        if self.etapes == 2 :
            messagebox.showerror('Erreur','impossible de revenir en arrière')
        if self.etapes == 0 :
            msg = messagebox.askokcancel('Attention !','Vous etes sur le points de passer au mode room, Les modifications sur les textures et les entitée ne serons plus possible, la possiblité de retour est prevu dans le developpement, voulez vous continuer')
            if msg :
                self.entitiesmenu.cacher()
                self.etapes = 1
                self.selected = 0
                self.buttons.l[2].configure(text="Rooms",command= self.fliproommenu)
                self.buttons.l[3].configure(command= self.flipentitiemenu)
        if self.etapes == 1 :
            self.roommenu.flip()

    def flipentitiemenu(self):
        if self.textmenu.menu :
            self.textmenu.cacher()
        if self.roommenu.menu :
            self.roommenu.cacher()
        if self.etapes == 0 :
            messagebox.showerror('Erreur',"impossible ! passez par l'etape 'room'")
        if self.etapes == 1 :
            msg = messagebox.askokcancel('Attention !',"Vous etes sur le points de passer au mode entité, Les modifications sur les textures ne serons plus possible, la possiblité de retour est prevu dans le developpement mais pour l'instant la possiblité de retour en arrière est impossible, voulez vous continuer")
            if msg :
                self.textmenu.cacher()
                self.etapes = 2
                self.selected = 'a'
                self.buttons.l[2].configure(text="Entitée",command= self.flipentitiemenu)
                self.buttons.l[3].configure(text="Save",command= self.save)
        if self.etapes == 2 :
            self.entitiesmenu.flip()

    def reset(self):
        """fonction qui reset la page"""
        for widgets in self.winfo_children():
            widgets.destroy()
        self.initialisation(self.maptaille[0],self.maptaille[1],self.nom)

    def change_selected(self, num):
        self.selected = num
        self.textmenu.desc.text_var.set(f'Choisir un element : {self.selected}')

    def changeroom(self):
        if len(self.salles) != 0 :
            if len(self.salles) == 1 or self.roomselected+1 == len(self.salles)+1:
                self.roomselected = 1
            else :
                self.roomselected += 1
            self.roommenu.l[0].configure(text=f'Ajouter une room : {len(self.salles)}')
            self.roommenu.l[1].configure(text=f'Changer de room : {self.roomselected}')
            self.roommenu.textliste[0].text_var.set(f'{self.roomselected}:{self.salles[self.roomselected-1][0]}')

    def addroom(self) :
        self.salles.append([self.sky_selected.copy(),[],(0,0)])
        self.roomselected = 1
        self.roommenu.l[0].configure(text=f'Ajouter une room : {len(self.salles)}')
        self.roommenu.l[1].configure(text=f'Changer de room : {self.roomselected}')
        self.roommenu.textliste[0].text_var.set(f'{self.roomselected}:{self.salles[self.roomselected-1][0]}')

    def delroom(self) :
        if self.salles != [] :
            for pos in self.salles[-1][1] :
                self.drawings.remove((pos[0]*30,pos[1]*30))
                self.erase(pos[0]*30,pos[1]*30)
            self.salles.pop()
            self.roomselected = 1 if self.salles != [] else None
            self.roommenu.l[0].configure(text=f'Ajouter une room : {len(self.salles)}')
            self.roommenu.l[1].configure(text=f'Changer de room : {self.roomselected}')
            if self.roomselected != None :
                self.roommenu.textliste[0].text_var.set(f'{self.roomselected}:{self.salles[self.roomselected-1][0]}')
            else : 
                self.roommenu.textliste[0].text_var.set(f'{self.roomselected}:{None}')

    def sky_change_selected(self, sky: str, index: int):
        self.sky_selected[index] = sky
        self.selected = 0
        self.roommenu.textliste[2].text_var.set(f'selected: {self.sky_selected}')

    def adddoor(self,event):
        if self.selected == 0 :
            x, y = round_to_multiple(event.x-15,30), round_to_multiple(event.y-15,30)
            self.salles[self.roomselected-1][2] = (int(x/30), int(y/30))
            messagebox.showinfo('Passage', f'point de passage modifié en {(int(x/30), int(y/30))}')

    def get_x_y(self, event):
        if isinstance(self.selected,int) :
            x, y = round_to_multiple(event.x-15,30), round_to_multiple(event.y-15,30)
            if (x, y) not in self.drawings:
                if self.selected == 0 and self.salles!= []: self.salles[self.roomselected-1][1].append((int(x/30), int(y/30)))
                elif self.selected !=0 : self.texturesplacements[self.selected].append((x, y))
                if self.salles!= [] or self.selected !=0:
                    self.drawings.append((x, y))
                    self.draw_b(x, y)
        else :
            x, y = round_to_multiple(event.x-15,5), round_to_multiple(event.y-15,5)
            if (x, y) not in self.objects:
                self.objectsplacements[self.selected].append((x, y))
                self.draw_b(x, y, True)


    def get_x_y_motion(self, event):
        if isinstance(self.selected,int) :
            ox, oy = round_to_multiple(event.x-15,30), round_to_multiple(event.y-15,30)
            if (ox, oy) not in self.drawings:
                if self.selected == 0 and self.salles!= []: self.salles[self.roomselected-1][1].append((int(ox/30), int(oy/30)))
                elif self.selected !=0 : self.texturesplacements[self.selected].append((ox, oy))
                if self.salles!= [] or self.selected !=0: 
                    self.drawings.append((ox, oy))
                    self.draw_b(ox, oy)
        

    def get_x_y_2(self, event):
        if isinstance(self.selected,int) :
            x2, y2 = round_to_multiple(event.x-15,30), round_to_multiple(event.y-15,30)
            if (x2, y2) in self.drawings and self.selected == 0 :
                self.salles[self.roomselected-1][1].remove((int(x2/30), int(y2/30)))
                self.drawings.remove((x2, y2))
                self.erase(x2, y2)
            elif (x2, y2) in self.drawings and (x2, y2) in self.texturesplacements[self.selected]:
                self.drawings.remove((x2, y2))
                self.texturesplacements[self.selected].remove((x2, y2))
                self.erase(x2, y2)
            
        else:
            x2, y2 = round_to_multiple(event.x-15, 5), round_to_multiple(event.y-15, 5)
            if (x2, y2) in self.objectsplacements[self.selected] and  (x2, y2) in self.objects :
                self.objectsplacements[self.selected].remove((x2, y2))
                self.canvas.delete(self.objects[(x2,y2)])
                self.objects.pop((x2, y2))
            if (x2+5, y2) in self.objectsplacements[self.selected] and  (x2+5, y2) in self.objects :
                self.objectsplacements[self.selected].remove((x2+5, y2))
                self.canvas.delete(self.objects[(x2+5,y2)])
                self.objects.pop((x2+5, y2))
            if (x2, y2+5) in self.objectsplacements[self.selected] and  (x2, y2+5) in self.objects :
                self.objectsplacements[self.selected].remove((x2, y2+5))
                self.canvas.delete(self.objects[(x2,y2+5)])
                self.objects.pop((x2, y2+5))
            if (x2-5, y2) in self.objectsplacements[self.selected] and  (x2-5, y2) in self.objects :
                self.objectsplacements[self.selected].remove((x2-5, y2))
                self.canvas.delete(self.objects[(x2-5,y2)])
                self.objects.pop((x2-5, y2))
            if (x2, y2-5) in self.objectsplacements[self.selected] and  (x2, y2-5) in self.objects :
                self.objectsplacements[self.selected].remove((x2, y2-5))
                self.canvas.delete(self.objects[(x2,y2-5)])
                self.objects.pop((x2, y2-5))
            if (x2+5, y2+5) in self.objectsplacements[self.selected] and  (x2+5, y2+5) in self.objects :
                self.objectsplacements[self.selected].remove((x2+5, y2+5))
                self.canvas.delete(self.objects[(x2+5,y2+5)])
                self.objects.pop((x2+5, y2+5))
            if (x2-5, y2-5) in self.objectsplacements[self.selected] and  (x2-5, y2-5) in self.objects :
                self.objectsplacements[self.selected].remove((x2-5, y2-5))
                self.canvas.delete(self.objects[(x2-5,y2-5)])
                self.objects.pop((x2-5, y2-5))
            if (x2+5, y2-5) in self.objectsplacements[self.selected] and  (x2+5, y2-5) in self.objects :
                self.objectsplacements[self.selected].remove((x2+5, y2-5))
                self.canvas.delete(self.objects[(x2+5,y2-5)])
                self.objects.pop((x2+5, y2-5))
            if (x2-5, y2+5) in self.objectsplacements[self.selected] and  (x2-5, y2+5) in self.objects :
                self.objectsplacements[self.selected].remove((x2-5, y2+5))
                self.canvas.delete(self.objects[(x2-5,y2+5)])
                self.objects.pop((x2-5, y2+5))

        
        
    

    def erase(self,x,y) :
        print('e')
        self.canvas.create_rectangle(x, y, x+30, y+30, outline=None,fill='white')

    def draw_b(self,x,y, m = False):
        id = self.canvas.create_image(x, y,anchor=tk.NW, image=self.textures.get(self.selected))
        if m :
            self.objects[(x,y)] = id
        

    def save(self):
        try :
            listofnums = []
            try : 
                for file_name in os.listdir('Creatorsaves/'):
                    file_j = os.path.join('Creatorsaves/', file_name)
                    if os.path.isfile(file_j):
                        num = int(''.join([c for c in file_name if isanumber(c)]))
                        listofnums.append(num)
            except: pass
            filetypes = (('data files', '*.data'),) #définition des type de fichier acceptée
            try: 
                defaultfilename = sanitize_filepath(self.nom)
                if defaultfilename == '' :
                    defaultfilename = 'newproject'
            except: defaultfilename = 'newproject'
            try : nom = fd.asksaveasfilename(initialfile=f'{defaultfilename}{max(listofnums,default=0)+1}',initialdir = "Creatorsaves/",title='Enregistrer un fichier',filetypes=filetypes,defaultextension="*.data") #nom prend la valeur du chemin d'accès du fichier
            except: nom = fd.asksaveasfilename(initialfile=f'{defaultfilename}{max(listofnums,default=0)+1}',title='Enregistrer un fichier',filetypes=filetypes,defaultextension="*.data")
            if nom == '':
                return
            liste = [[0 for _ in range(self.maptaille[0])] for _ in range(self.maptaille[1])]
            for elem in self.texturesplacements :
                for x,y in self.texturesplacements[elem] :
                    try:
                        if elem != 0 and isinstance(elem, int): liste[int(y/30)][int(x/30)] = elem
                    except: pass
            object_handler = {}
            mob_pos= {}
            for obj in self.objectsplacements :
                if obj[0] == '!' and obj[1] == '!':
                    mob_pos[obj[2:len(obj)]] = [(pos[0]/30,pos[1]/30) for pos in self.objectsplacements[obj]]
                else :
                    if obj[0] == '!' and obj[1] != '!':
                        object_handler[obj[1:len(obj)]] = self.objectsplacements[obj]
                    else :
                        object_handler[obj] = self.objectsplacements[obj]
            for salle in self.salles :
                x_, y_ = (salle[2])
                salle.append('')
                salle.append('')
                if (x_+1,y_) in salle[1] :
                    salle[3] = 'h'
                    salle[4] = 'x'
                if (x_-1,y_) in salle[1] :
                    salle[3] = 'b'
                    salle[4] = 'x'
                if (x_,y_+1) in salle[1] :
                    salle[3] = 'd'
                    salle[4] = 'y'
                if (x_,y_-1) in salle[1] :
                    salle[3] = 'g'
                    salle[4] = 'y'
        
            save_object(Save(liste, object_handler, mob_pos, self.salles, self.sky_selected,self.start), nom)
        except : messagebox.showerror('Erreur', "Erreur dans l'enregistement")


def round_to_multiple(num, multiple):
    return multiple * round(num/multiple) 


class Save:
    def __init__(self, mapliste, objectsdict, mob_dict, salles, select, start) -> None:
        self.mapliste = mapliste
        self.objectsdict = objectsdict
        self.mob_dict = mob_dict
        self.salles = salles
        self.select = select
        self.start = start

if __name__ == "__main__":
    root = Windows() #on lance l'application
    root.mainloop() #on lance la boucle tkinter