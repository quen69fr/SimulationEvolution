# coding: utf-8

import math
import random
import copy
import pygame
from constantes import *


class Carte:
    altitude_min_nour_abondante = 0.
    proba_modif_point_altitude_fixe = 0.
    valeur_modif_point_altitude_fixe = 0
    proba_modif_vitesse_point_altitude_fixe = 0.

    def __init__(self, largeur_carte: int, hauteur_carte: int):
        self.largeur_carte = largeur_carte
        self.hauteur_carte = hauteur_carte

        self.grille_altitude = []
        self.liste_altitudes_positives = []
        self.liste_altitudes_abondantes = []
        self.liste_altitudes_negatives = []
        self.liste_altitudes_fixes = []
        self.liste_valeurs_altitudes_fixes = []
        self.liste_coefs_energie_depensee_i = []

        self.largeur_ecran = 0
        self.hauteur_ecran = 0
        self.i_carte_camera = 0.
        self.j_carte_camera = 0.
        self.i_deplacement_camera = 0
        self.j_deplacement_camera = 0
        self.echelle_min = 0
        self.echelle_max = 0
        self.echelle = 0
        self.coef_zoom = 0.
        self.marge_bord_deplacement = 0
        self.vitesse_deplacement = 0
        self.ecran = None
        self.ecran_miniature = None
        self.liste_cases_affichage = []
        self.new_affichage = True
        self.coef_affichage_energie_depensee = 0

    def init_grille(self, nb_update_carte_init, altitude_max, altitude_min, altitude_globale_init, altitude_bord,
                    nb_altitudes_fixes_positives, nb_altitudes_fixes_negatives, coef_energie_depensee_gauche,
                    coef_energie_depensee_droite, proba_altitudes_negaties_vers_centre, tk_var_stop, tk_var_avancement):
        coef_dir = (coef_energie_depensee_droite - coef_energie_depensee_gauche) / self.largeur_carte
        self.liste_coefs_energie_depensee_i = [coef_energie_depensee_gauche + i * coef_dir
                                               for i in range(self.largeur_carte)]
        self.grille_altitude = [[altitude_bord if (i == 0 or j == 0 or i == self.largeur_carte - 1
                                                   or j == self.hauteur_carte - 1) else altitude_globale_init
                                 for i in range(self.largeur_carte)]
                                for j in range(self.hauteur_carte)]

        self.liste_altitudes_fixes = [(random.randint(MARGE_BORD_ALTITUDE_FIXE,
                                                      self.largeur_carte - MARGE_BORD_ALTITUDE_FIXE - 1),
                                       random.randint(MARGE_BORD_ALTITUDE_FIXE,
                                                      self.hauteur_carte - MARGE_BORD_ALTITUDE_FIXE - 1))
                                      for _ in range(nb_altitudes_fixes_negatives + nb_altitudes_fixes_positives)]
        for i in range(nb_altitudes_fixes_negatives):
            if random.random() < proba_altitudes_negaties_vers_centre:
                self.liste_altitudes_fixes[i] = int(proba_altitudes_negaties_vers_centre * self.largeur_carte / 2 +
                                                    (1 - proba_altitudes_negaties_vers_centre) *
                                                    self.liste_altitudes_fixes[i][0]), self.liste_altitudes_fixes[i][1]

        self.liste_valeurs_altitudes_fixes = ([(random.randint(0, self.valeur_modif_point_altitude_fixe * 2) -
                                                self.valeur_modif_point_altitude_fixe,
                                                random.randint(0, self.valeur_modif_point_altitude_fixe * 2) -
                                                self.valeur_modif_point_altitude_fixe,
                                                altitude_min)
                                               for _ in range(nb_altitudes_fixes_negatives)] +
                                              [(random.randint(0, self.valeur_modif_point_altitude_fixe * 2) -
                                                self.valeur_modif_point_altitude_fixe,
                                                random.randint(0, self.valeur_modif_point_altitude_fixe * 2) -
                                                self.valeur_modif_point_altitude_fixe,
                                                altitude_max)
                                               for _ in range(nb_altitudes_fixes_positives)])

        for n, (i, j) in enumerate(self.liste_altitudes_fixes):
            self.grille_altitude[j][i] = self.liste_valeurs_altitudes_fixes[n][2]

        for n in range(nb_update_carte_init):
            if tk_var_stop.get():
                break
            self.update_grille()
            tk_var_avancement.set(round(n / nb_update_carte_init, 2))

    def init_pygame(self, confs: dict):
        self.largeur_ecran = confs[LARGEUR_ECRAN]
        self.hauteur_ecran = confs[HAUTEUR_ECRAN]

        self.echelle_min = max(math.ceil(self.largeur_ecran / self.largeur_carte),
                               math.ceil(self.hauteur_ecran / self.hauteur_carte))
        self.echelle_max = confs[ECHELLE_MAX]
        self.echelle = self.echelle_min
        self.coef_zoom = confs[COEF_ZOOM]
        self.marge_bord_deplacement = confs[CARTE_MARGE_BORD_DEPLACEMENT]
        self.vitesse_deplacement = confs[CARTE_VITESSE_DEPLACEMENT]
        self.coef_affichage_energie_depensee = confs[COEF_AFFICHAGE_ENERGIE_DEPENSEE]

        self.ecran = pygame.Surface((self.largeur_ecran, self.hauteur_ecran))
        self.ecran_miniature = pygame.Surface((self.largeur_carte, self.hauteur_carte))
        self.liste_cases_affichage = []
        self.new_affichage = True

        self.i_carte_camera = 0.
        self.j_carte_camera = 0.
        self.i_deplacement_camera = 0
        self.j_deplacement_camera = 0

    def gere_clic(self, x_souris: int, y_souris: int):
        if 0 <= x_souris - X_MINIATURE_SUR_ECRAN <= self.largeur_carte and \
                0 <= y_souris - Y_MINIATURE_SUR_ECRAN <= self.hauteur_carte:
            self.set_i_carte_camera(x_souris - MARGE_BORD_ALTITUDE_FIXE - self.largeur_ecran / self.echelle / 2)
            self.set_j_carte_camera(y_souris - MARGE_BORD_ALTITUDE_FIXE - self.hauteur_ecran / self.echelle / 2)

    def gere_zoom(self, sens: bool, x_souris: int, y_souris: int):
        old_echelle = self.echelle
        i_souris, j_souris = self.xy_ecran_to_ij_carte(x_souris, y_souris)
        if sens:
            self.echelle = min(self.echelle + max(int(self.echelle * self.coef_zoom), 1), self.echelle_max)
        else:
            self.echelle = max(self.echelle - max(int(self.echelle * self.coef_zoom), 1), self.echelle_min)

        if old_echelle != self.echelle:
            self.new_affichage = True
            coef = old_echelle / self.echelle

            self.set_i_carte_camera(i_souris + coef * (self.i_carte_camera - i_souris))
            self.set_j_carte_camera(j_souris + coef * (self.j_carte_camera - j_souris))

    def update_deplacement_camera(self, x_souris: int, y_souris: int):
        self.i_deplacement_camera = 0
        dx = self.marge_bord_deplacement - x_souris
        if dx > 0:
            self.i_deplacement_camera = - dx / self.marge_bord_deplacement * self.vitesse_deplacement / self.echelle
        else:
            dx = self.marge_bord_deplacement - self.largeur_ecran + x_souris
            if dx > 0:
                self.i_deplacement_camera = dx / self.marge_bord_deplacement * self.vitesse_deplacement / self.echelle

        self.j_deplacement_camera = 0
        dy = self.marge_bord_deplacement - y_souris
        if dy > 0:
            self.j_deplacement_camera = - dy / self.marge_bord_deplacement * self.vitesse_deplacement / self.echelle
        else:
            dy = self.marge_bord_deplacement - self.hauteur_ecran + y_souris
            if dy > 0:
                self.j_deplacement_camera = dy / self.marge_bord_deplacement * self.vitesse_deplacement / self.echelle

    def set_i_carte_camera(self, i_carte_camera: float):
        # if i_carte_camera == self.i_carte_camera:
        #     return False
        old_i = self.i_carte_camera
        self.i_carte_camera = round(max(min(i_carte_camera, self.largeur_carte - self.largeur_ecran / self.echelle), 0),
                                    PRECISION_POSITION_CAMERA_CARTE)
        if old_i == self.i_carte_camera:
            return False

        self.new_affichage = True
        return True

    def set_j_carte_camera(self, j_carte_camera: float):
        # if j_carte_camera == self.j_carte_camera:
        #     return False
        old_j = self.j_carte_camera
        self.j_carte_camera = round(max(min(j_carte_camera, self.hauteur_carte - self.hauteur_ecran / self.echelle), 0),
                                    PRECISION_POSITION_CAMERA_CARTE)
        if old_j == self.j_carte_camera:
            return False

        self.new_affichage = True
        return True

    def update_position_camera(self):
        if not self.i_deplacement_camera == 0:
            if not self.set_i_carte_camera(self.i_carte_camera + self.i_deplacement_camera):
                self.i_deplacement_camera = 0
        if not self.j_deplacement_camera == 0:
            if not self.set_j_carte_camera(self.j_carte_camera + self.j_deplacement_camera):
                self.j_deplacement_camera = 0

    def update_grille(self):
        self.liste_altitudes_positives = []
        self.liste_altitudes_negatives = []
        self.liste_altitudes_abondantes = []

        for n, (i, j) in enumerate(self.liste_altitudes_fixes):
            if random.random() < self.proba_modif_point_altitude_fixe:
                old_i, old_j = i, j
                vx, vy, a = self.liste_valeurs_altitudes_fixes[n]
                if random.random() < self.proba_modif_point_altitude_fixe:
                    i += vx
                if random.random() < self.proba_modif_point_altitude_fixe:
                    j += vy
                if random.random() < self.proba_modif_vitesse_point_altitude_fixe:
                    vx = random.randint(0, self.valeur_modif_point_altitude_fixe * 2) - \
                         self.valeur_modif_point_altitude_fixe
                if random.random() < self.proba_modif_vitesse_point_altitude_fixe:
                    vy = random.randint(0, self.valeur_modif_point_altitude_fixe * 2) - \
                         self.valeur_modif_point_altitude_fixe

                if (old_i, old_j) == (i, j):
                    self.liste_valeurs_altitudes_fixes[n] = vx, vy, a
                    self.grille_altitude[j][i] = a
                else:
                    if MARGE_BORD_ALTITUDE_FIXE <= i < self.largeur_carte - MARGE_BORD_ALTITUDE_FIXE and \
                            MARGE_BORD_ALTITUDE_FIXE <= j < self.hauteur_carte - MARGE_BORD_ALTITUDE_FIXE:
                        self.liste_altitudes_fixes[n] = i, j
                        self.liste_valeurs_altitudes_fixes[n] = vx, vy, a
                        self.grille_altitude[j][i] = a

        copie_grille = copy.deepcopy(self.grille_altitude)
        for j, ligne in enumerate(copie_grille):
            if 0 < j < self.hauteur_carte - 1:
                for i, altitude in enumerate(ligne):
                    if 0 < i < self.largeur_carte - 1 and (i, j) not in self.liste_altitudes_fixes:
                        s = 0
                        for i2 in [i - 1, i, i + 1]:
                            for j2 in [j - 1, j, j + 1]:
                                if i2 == i and j2 == j:
                                    s += altitude
                                else:
                                    s += copie_grille[j2][i2]
                        self.grille_altitude[j][i] = round(s / 9, PRECISION_ALTITUDE_CARTE)
                    if altitude > 0:
                        self.liste_altitudes_positives.append((i, j))
                        if altitude > self.altitude_min_nour_abondante:
                            self.liste_altitudes_abondantes.append((i, j))
                    else:
                        self.liste_altitudes_negatives.append((i, j))
        self.new_affichage = True

    def update_ecran(self):
        self.update_position_camera()
        if self.new_affichage:
            self.new_affichage = False
            self.liste_cases_affichage = []
            i_min_camera_miniature = int(self.i_carte_camera)
            i_max_camera_miniature = i_min_camera_miniature + self.largeur_ecran // self.echelle
            j_min_camera_miniature = int(self.j_carte_camera)
            j_max_camera_miniature = j_min_camera_miniature + self.hauteur_ecran // self.echelle
            for j, ligne in enumerate(self.grille_altitude):
                for i, altitude in enumerate(ligne):
                    x, y = self.ij_carte_to_xy_ecran(i, j)
                    c = COULEUR_ALTITUDE(altitude, self.altitude_min_nour_abondante,
                                         self.liste_coefs_energie_depensee_i[i],
                                         self.coef_affichage_energie_depensee)
                    if - self.echelle < x < self.largeur_ecran and - self.echelle < y < self.hauteur_ecran:
                        self.ecran.fill(c, (x, y, self.echelle, self.echelle))
                        self.liste_cases_affichage.append((i, j))

                    if i_min_camera_miniature < i < i_max_camera_miniature and \
                            j_min_camera_miniature < j < j_max_camera_miniature:
                        self.ecran_miniature.set_at((i, j), c)
                    else:
                        self.ecran_miniature.set_at((i, j), (c[0] // COEF_COULEUR_MINIATURE_HORS_CAMERA,
                                                             c[1] // COEF_COULEUR_MINIATURE_HORS_CAMERA,
                                                             c[2] // COEF_COULEUR_MINIATURE_HORS_CAMERA))

            pygame.draw.rect(self.ecran_miniature, COULEUR_CADRE_CAMERA_MINIATURE,
                             (i_min_camera_miniature, j_min_camera_miniature,
                              i_max_camera_miniature - i_min_camera_miniature,
                              j_max_camera_miniature - j_min_camera_miniature), 1)

    def ecran_miniature_stats(self, coef_temperature):
        ecran_miniature = pygame.Surface((self.largeur_carte, self.hauteur_carte))
        for j, ligne in enumerate(self.grille_altitude):
            for i, altitude in enumerate(ligne):
                c = COULEUR_ALTITUDE(altitude, self.altitude_min_nour_abondante,
                                     self.liste_coefs_energie_depensee_i[i], coef_temperature)
                ecran_miniature.set_at((i, j), c)
        return ecran_miniature

    def xy_ecran_to_ij_carte(self, x: int, y: int):
        return self.i_carte_camera + x / self.echelle, self.j_carte_camera + y / self.echelle

    def ij_carte_to_xy_ecran(self, i: float, j: float):
        return int((i - self.i_carte_camera) * self.echelle), int((j - self.j_carte_camera) * self.echelle)

    def ij_altitude_positive(self, i: float, j: float):
        return (int(i), int(j)) in self.liste_altitudes_positives

    def affiche_miniature(self, chemin_image, taille, coef_temperature):
        image = pygame.image.load(chemin_image)
        if taille == 1:
            ecran_miniature = self.ecran_miniature_stats(coef_temperature)
        else:
            ecran_miniature = pygame.transform.rotozoom(self.ecran_miniature_stats(coef_temperature), 0, taille)
        image.blit(ecran_miniature, (X_MINIATURE_SUR_ECRAN,
                                     image.get_height() - Y_MINIATURE_SUR_ECRAN - ecran_miniature.get_height()))
        pygame.image.save(image, chemin_image)


class CarteContent:
    def __init__(self, largeur_carte: int, hauteur_carte: int):
        self._grille_content = [[[] for _ in range(largeur_carte)] for _ in range(hauteur_carte)]

    def add_grille_content(self, thing, i: float, j: float):
        self._grille_content[int(j)][int(i)].append(thing)

    def add_grille_content_int(self, thing, i: int, j: int):
        self._grille_content[j][i].append(thing)

    def remove_grille_content(self, thing, i: float, j: float):
        self._grille_content[int(j)][int(i)].remove(thing)

    def remove_grille_content_int(self, thing, i: int, j: int):
        self._grille_content[j][i].remove(thing)

    def get_grille_content_ij(self, i: int, j: int):
        return self._grille_content[j][i]

    def pop_grille_content_ij(self, i: int, j: int):
        content = self._grille_content[j][i]
        self._grille_content[j][i] = []
        return content

    def get_grille_content_dist_max_around_ij(self, i: float, j: float):
        i, j = int(i), int(j)
        liste_things = []
        for dist_max, list_indiv in LISTE_CASES_AUTOUR_INDIVIDU:
            for di, dj in list_indiv:
                liste_things.append((dist_max, self.get_grille_content_ij(i + di, j + dj)))
        return liste_things
