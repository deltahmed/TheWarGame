from importexport import *
class Data:
   """class qui permet d'enregistrer les information"""
   def __init__(self, score, time, killed ) -> None:
      '''class qui permet d'enregistrer les information, les element etrange permettes de brouiller les pistes'''
      self.ekzjnfj = 'sfndcuisbchjinsdchjbncshjc jnc djnc njsc'
      self.cnzsjcf = 'sncjdscnjkcjksncdjkncjkc n vh cj c canco'
      self.scnzsjd = score
      self.nmplplo = 'jdnsjcjisdncjdsj cjk  ns jsj  c dcnd scd'
      self.dckezdp = 'njdsnjkd sck ds c cnskd ckn sjkd ckc , d'
      self.tamjndj = time
      self.tueencc = killed
      self.floup = False
      self.djncshdchsc(5151,85181,8184)


   def djncshdchsc(self, c , jfnvj, djncj):
      """fonction qui ne sert a rien a part brouiller les pistes"""
      c
      jfnvj
      djncj
      self.ekzjnfj
      self.cnzsjcf
      self.scnzsjd
      self.nmplplo
      self.dckezdp
      self.tamjndj
      self.tueencc
      self.floup = True

class Gamesaves:
   '''class qui permet d'enregistrer les sauvegardes'''
   def __init__(self, time, level, life, started) -> None:
      self.time, self.level, self.life = time, level, life
      self.started = started


#AU LANCEMENT DE CE FICHIER TOUTE LES DONNE DU JEU SERRONS EFFACEE
d = Data(0,0,0)
g = Gamesaves(0,1,100,False)
save_object(d, 'data/anti_cheat_data/local.anti_cheat')
save_object(d, 'data/anti_cheat_data/stored.anti_cheat')
save_object(d, 'data/tempdata/local.temp')
save_object(d, 'data/player_data/player.data')
save_object(g,'data/player_data/gamesave1.save')
save_object(g,'data/player_data/gamesave2.save')
save_object(g,'data/player_data/gamesave3.save')