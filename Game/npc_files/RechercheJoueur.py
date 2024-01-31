from random import choice
from tools.Graph import *



class RechercheJoueur:
    """class qui permet de faire du PathFinding"""
    def __init__(self,game) -> None:
        self.game = game
        self.map = self.game.map.mini_map
        self.chemins_possibles = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = Graph()
        self.graph2 = Graph()
        self.graph3 = Graph()
        self.graph4 = Graph()
        self.m = len(self.map)//2
        self.m2 = len(self.map[0])//2


        self.get_graph() #on recupère les graphs correspondant a la carte
        

    def get_chemin(self, debut, fin, obj):
        """donne le chemin le environnant le plus rapide entre un debut et une fin avec l'algorithme de BFS"""
        try:
            if obj in self.game.obj.processus_en_cours : #on rend inteligent que 5 enemie pour eviter les surcharge 
                if debut in self.graph and fin in self.graph : solution = self.graph.solution(fin,self.graph.parcours_largeur_dict_avec_liste_de_noeud_interdit(debut, self.game.obj.npc_positions))
                elif debut in self.graph2 and fin in self.graph2 : solution = self.graph2.solution(fin,self.graph2.parcours_largeur_dict_avec_liste_de_noeud_interdit(debut, self.game.obj.npc_positions))
                elif debut in self.graph3 and fin in self.graph3 : solution = self.graph3.solution(fin,self.graph3.parcours_largeur_dict_avec_liste_de_noeud_interdit(debut, self.game.obj.npc_positions))
                elif debut in self.graph4 and fin in self.graph4 : solution = self.graph4.solution(fin,self.graph4.parcours_largeur_dict_avec_liste_de_noeud_interdit(debut, self.game.obj.npc_positions))
            else : solution = [fin]

            if len(solution) >= 2 : 
                return solution[1]
            else : 
                return solution[0]
            
        except : return fin
        
    def get_next_nodes(self, x, y):
        """retourne la prochaine case ou il faut aller"""
        return [(x + dx, y + dy) for dx, dy in self.chemins_possibles if (x + dx, y + dy) not in self.game.map.map_monde]

    def get_graph(self):
        """Méthode qui creer 4 graph de la map pour permettre de faire des algorithme sur ces dit graph"""
        m = self.m
        m2 = self.m2

        for y, ligne in enumerate(self.map):
            for x, colone in enumerate(ligne):
                if not colone or (x, y) in self.game.map.gost_blocs:
                    if 0 <= y <= m and 0 <= x <= m2 :
                        self.graph.add_sommet((x, y))
                        self.graph.add_liste_voisin((x, y),self.get_next_nodes(x, y))
                    if 0 <= y <= m and m <= x <= len(self.map[0]) :
                        self.graph2.add_sommet((x, y))
                        self.graph2.add_liste_voisin((x, y),self.get_next_nodes(x, y))
                    if m <= y <= len(self.map) and 0 <= x <= m2 :
                        self.graph3.add_sommet((x, y))
                        self.graph3.add_liste_voisin((x, y),self.get_next_nodes(x, y))
                    if m <= y <= len(self.map) and m <= x <= len(self.map[0]) :
                        self.graph4.add_sommet((x, y))
                        self.graph4.add_liste_voisin((x, y),self.get_next_nodes(x, y))


    