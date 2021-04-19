# coding: utf-8

from nourriture import *
import math


class Individu(Thing):
    poids_vitesse_energie_depensee = 0.
    poids_taille_energie_depensee = 0.
    coef_energie_depensee = 0.
    energie_depensee_plus = 0.
    coef_petit_mage_gros = 0.
    coef_vitesse_chasse = 0.
    duree_gestation_energie_totale = 0
    dic_caracteres_individus = {}

    def __init__(self, carte: Carte, carte_content: CarteContent, i: int, j: int, dic_variables: dict,
                 energie_init: float):
        self.dic_variables = dic_variables
        self.age = 0
        self.energie_init = energie_init
        self.vitesse = dic_variables[VITESSE_INDIVIDU]
        self.vitesse_chasse = self.vitesse * self.coef_vitesse_chasse
        self.direction = (random.random() * 2 - 1) * math.pi
        self.rayon = dic_variables[RAYON_INDIVIDU]
        self.dist_vision = dic_variables[RAYON_VISION_INDIVIDU]
        self.squared_dist_vision = dic_variables[RAYON_VISION_INDIVIDU] ** 2
        Thing.__init__(self, carte, carte_content, i, j, energie_init,
                       max(self.rayon, self.vitesse * SQUARED_DISTANCE_INDIVIDU_CONTACT_COEF_VITESSE))
        self.energie_depense = \
            self.coef_energie_depensee * (self.vitesse ** self.poids_vitesse_energie_depensee) * \
            (self.rayon ** self.poids_taille_energie_depensee) + self.energie_depensee_plus
        self.objectif: Thing or None = None
        self.rate_objectif = 0
        self.ennemi: Thing or None = None
        self.dic_variables_partenaire = None

        self.taille_max_individu_nourriture = self.rayon / self.coef_petit_mage_gros

        self.energie_min_new_individu = dic_variables[ENERGIE_MIN_NEW_INDIVIDU]
        self.energie_cout_new_individu = dic_variables[ENERGIE_COUT_NEW_INDIVIDU]
        self.duree_new_individu = dic_variables[DUREE_NEW_INDIVIDU]
        self.peut_se_reproduire = False
        self.compte_a_rebour_new_individu = 0
        self.new_individu = False

    def nouvelle_journee(self):
        self.age += 1

    def update(self):
        if not self.actif:
            return
        self.energie -= self.energie_depense * self.carte.liste_coefs_energie_depensee_i[int(self.i)]
        if self.energie <= 0:
            self.inactif()
            return
        self.peut_se_reproduire = False
        if self.compte_a_rebour_new_individu == 0:
            if self.age > 0 and self.energie > self.energie_min_new_individu:
                self.peut_se_reproduire = True
        else:
            self.compte_a_rebour_new_individu -= 1
            if self.compte_a_rebour_new_individu <= 0:
                self.new_individu = True
        for _ in range(NB_UPDATE_MAX_INDIVIDU_ORIENTATION):
            new_i = self.i + math.cos(self.direction) * self.vitesse
            new_j = self.j + math.sin(self.direction) * self.vitesse
            if int(new_i) == int(self.i) and int(new_j) == int(self.j):
                self.i, self.j = new_i, new_j
                # self.update_objectif()
                self.upadte_direction()
                break
            else:
                if self.carte.ij_altitude_positive(new_i, new_j):
                    self.carte_content.remove_grille_content(self, self.i, self.j)
                    self.i, self.j = new_i, new_j
                    self.carte_content.add_grille_content(self, self.i, self.j)
                    self.update_objectif()
                    # self.upadte_direction()
                    break
                else:
                    if self.direction > 0:
                        self.direction += VITESSE_ROTATION_INDIVIDU_OBSTACLE
                    else:
                        self.direction -= VITESSE_ROTATION_INDIVIDU_OBSTACLE

    def upadte_direction(self):
        if self.ennemi is None:
            if self.objectif is None:
                self.direction += random.random() * 0.5 - 0.25
            else:
                self.oriente_vers_objectif()
        else:
            self.oriente_vers_ennemi()

    def calcul_rate_objectif(self, thing: Thing, dist: float):
        if isinstance(thing, Individu):
            if self.vitesse > thing.vitesse_chasse:
                return thing.energie - self.energie_depense * dist / (self.vitesse - thing.vitesse_chasse)
            return 0
        return thing.energie - self.energie_depense * dist

    def thing_visible(self, thing: Thing, squared_rayon=None):
        if squared_rayon is None:
            squared_rayon = self.squared_dist_vision
        return (self.i - thing.i) ** 2 + (self.j - thing.j) ** 2 < squared_rayon

    def update_objectif(self):
        if self.ennemi is not None:
            if not self.ennemi.actif or (self.i - self.ennemi.i) ** 2 + (self.j - self.ennemi.j) ** 2 > \
                    min(self.squared_dist_vision, self.ennemi.squared_dist_vision):
                self.ennemi = None

        if self.objectif is not None:
            if not self.objectif.actif or (isinstance(self.objectif, Individu) and
                                           self.objectif.rayon < self.taille_max_individu_nourriture and
                                           self.rayon < self.objectif.taille_max_individu_nourriture and
                                           not (self.objectif.peut_se_reproduire and self.peut_se_reproduire)):
                self.objectif = None
            else:
                if (self.i - self.objectif.i) ** 2 + (self.j - self.objectif.j) ** 2 < \
                        (self.dist_contact_min + self.objectif.dist_contact_min) ** 2:
                    if isinstance(self.objectif, Individu):
                        if self.objectif.rayon < self.taille_max_individu_nourriture:
                            self.objectif.inactif()
                            self.energie += self.objectif.energie
                        elif self.rayon > self.objectif.taille_max_individu_nourriture and \
                                self.energie > self.energie_min_new_individu and \
                                self.objectif.energie > self.objectif.energie_min_new_individu:
                            self.compte_a_rebour_new_individu = self.duree_new_individu
                            self.dic_variables_partenaire = self.objectif.dic_variables
                            self.energie -= self.energie_cout_new_individu
                            self.objectif.energie -= self.objectif.energie_cout_new_individu
                    else:
                        self.objectif.inactif()
                        self.energie += self.objectif.energie
                    self.objectif = None

        # recherche_nourriture_individu = (self.objectif is None or isinstance(self.objectif, Nourriture) or
        #                                  (isinstance(self.objectif, Individu) and
        #                                   self.objectif.rayon < self.taille_max_individu_nourriture))

        recherche_nourriture_individu = (self.ennemi is None and not
                                         (isinstance(self.objectif, Individu) and
                                          self.objectif.rayon >= self.taille_max_individu_nourriture))

        for dist_max, list_things in self.carte_content.get_grille_content_dist_max_around_ij(self.i, self.j):
            for thing in list_things:
                if thing == self:
                    continue
                if isinstance(thing, Nourriture) or thing.rayon < self.taille_max_individu_nourriture:
                    if recherche_nourriture_individu:
                        if dist_max <= self.dist_vision or self.thing_visible(thing):
                            rate = self.calcul_rate_objectif(thing, dist_max)
                            if self.objectif is None or rate > self.rate_objectif:
                                self.objectif = thing
                                self.rate_objectif = rate
                elif self.rayon < thing.taille_max_individu_nourriture:
                    if self.thing_visible(thing, min(self.squared_dist_vision, thing.squared_dist_vision)):
                        self.objectif = None
                        self.ennemi = thing
                        return
                elif recherche_nourriture_individu and self.peut_se_reproduire and thing.peut_se_reproduire:
                    recherche_nourriture_individu = False
                    self.objectif = thing

    def oriente_vers_objectif(self):
        self.oriente_di_dj(self.objectif.i - self.i, self.objectif.j - self.j)

    def oriente_vers_ennemi(self):
        self.oriente_di_dj(self.i - self.ennemi.i, self.j - self.ennemi.j)

    def oriente_di_dj(self, di, dj):
        if di == 0:
            if dj > 0:
                self.direction = math.pi / 2
            else:
                self.direction = - math.pi / 2
        elif di > 0:
            self.direction = math.atan(dj / di)
        else:
            self.direction = math.atan(dj / di) + math.pi * random.choice([-1, 1])

    def get_couleur(self):
        if self.age == 0:
            return COULEUR_INDIVIDU_NAISSANCE
        if self.peut_se_reproduire:
            return COULEUR_INDIVIDU_PEUT_SE_REPRODUIRE
        if self.compte_a_rebour_new_individu == 0:
            return COULEUR_INDIVIDU_NORMAL
        return COULEUR_INDIVIDU_GESTANT

    def affiche(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.get_couleur(), self.carte.ij_carte_to_xy_ecran(self.i, self.j),
                           int(self.rayon * self.carte.echelle))
