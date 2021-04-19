# coding: utf-8

from thing import *


class Nourriture(Thing):
    nb_nourritures_par_jour = 0
    dic_type_nourriture = {
        TYPE_NOUR_1: {
            PARAM_NOUR_PROBA: 0,
            PARAM_NOUR_ENERGIE: 0},
        TYPE_NOUR_2: {
            PARAM_NOUR_PROBA: 0,
            PARAM_NOUR_ENERGIE: 0}
    }
    coef_proba_nour_abondante = 0

    def __init__(self, carte: Carte, carte_content: CarteContent, type_nourriture: int, i: int, j: int):
        self.type = type_nourriture
        self.rayon = DIC_NOURRITURE[type_nourriture][PARAM_NOUR_RAYON]
        Thing.__init__(self, carte, carte_content, i, j, self.dic_type_nourriture[type_nourriture][PARAM_NOUR_ENERGIE],
                       self.rayon)
        self.couleur = DIC_NOURRITURE[type_nourriture][PARAM_NOUR_COULEUR]

    def affiche(self, screen):
        pygame.draw.circle(screen, self.couleur, self.carte.ij_carte_to_xy_ecran(self.i, self.j),
                           int(self.rayon * self.carte.echelle))
