# coding: utf-8

from carte import *


class Thing:
    def __init__(self, carte: Carte, carte_content: CarteContent, i: int, j: int, energie: float,
                 dist_contact_min: float):
        self.carte = carte
        self.carte_content = carte_content
        self.i, self.j = i, j
        self.carte_content.add_grille_content_int(self, self.i, self.j)
        self.i += random.random()
        self.j += random.random()
        self.energie = energie
        self.dist_contact_min = dist_contact_min
        self.actif = True

    def inactif(self):
        self.actif = False
        self.carte_content.remove_grille_content(self, self.i, self.j)

    def update(self):
        pass

    def affiche(self, screen: pygame.Surface):
        pass
