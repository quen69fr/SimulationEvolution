# coding: utf-8

from stats import *


class Environnement:
    def __init__(self, dic_params: dict, dic_caracteres_individus: dict, tk_var_stop, tk_var_avancement):
        self.init_terminee = True
        self.liste_nourriture = []
        self.liste_individus = []
        self.t = 0
        self.duree_journee = dic_params[DUREE_JOURNEE]
        self.periode_update_carte = dic_params[PERIODE_UPDATE_CARTE] if dic_params[UPDATE_CARTE] else 0

        self.carte = Carte(dic_params[LARGEUR_ENVIRONNEMENT], dic_params[HAUTEUR_ENVIRONNEMENT])
        self.carte.init_grille(dic_params[NB_UPDATE_CARTE_INIT], dic_params[ALTITUDE_MAX], dic_params[ALTITUDE_MIN],
                               dic_params[ALTITUDE_GLOBALE_INIT], dic_params[ALTITUDE_BORD],
                               dic_params[NB_ALTITUDES_FIXES_POSITIVES], dic_params[NB_ALTITUDES_FIXES_NEGATIVES],
                               dic_params[COEF_ENERGIE_DEPENSEE_GAUCHE], dic_params[COEF_ENERGIE_DEPENSEE_DROITE],
                               dic_params[PROBA_ALTITUDE_NEGATIVE_VERS_CENTRE], tk_var_stop, tk_var_avancement)
        if tk_var_stop.get():
            self.init_terminee = False
            return
        self.carte_content = CarteContent(dic_params[LARGEUR_ENVIRONNEMENT], dic_params[HAUTEUR_ENVIRONNEMENT])
        self.stats = Stats(self.carte)

        Nourriture.nb_nourritures_par_jour = dic_params[NB_NOURRITURES_PAR_JOUR]
        Nourriture.dic_type_nourriture = {
            TYPE_NOUR_1: {
                PARAM_NOUR_PROBA: dic_params[PROBA_NOURRITURE_1],
                PARAM_NOUR_ENERGIE: dic_params[ENERGIE_NOURRITURE_1]},
            TYPE_NOUR_2: {
                PARAM_NOUR_PROBA: dic_params[PROBA_NOURRITURE_2],
                PARAM_NOUR_ENERGIE: dic_params[ENERGIE_NOURRITURE_2]}
        }
        Nourriture.coef_proba_nour_abondante = dic_params[COEF_PROBA_NOURRITURE_ABONDANTE]
        Carte.altitude_min_nour_abondante = dic_params[ALTITUDE_MIN_NOURRITURE_ABONDANTE]
        Carte.proba_modif_point_altitude_fixe = dic_params[PROBA_MODIF_POINT_ALTITUDE_FIXE]
        Carte.valeur_modif_point_altitude_fixe = dic_params[VALEUR_MODIF_POINT_ALTITUDE_FIXE]
        Carte.proba_modif_vitesse_point_altitude_fixe = dic_params[PROBA_MODIF_POINT_ALTITUDE_FIXE_VITESSE]
        Individu.poids_vitesse_energie_depensee = dic_params[POIDS_VITESSE_ENERGIE_DEPENSEE]
        Individu.poids_taille_energie_depensee = dic_params[POIDS_RAYON_ENERGIE_DEPENSEE]
        energie_depensee_min = dic_params[ENERGIE_DEPENSEE_MIN] / self.duree_journee
        energie_depensee_max = dic_params[ENERGIE_DEPENSEE_MAX] / self.duree_journee
        Individu.coef_energie_depensee = (energie_depensee_max - energie_depensee_min) / \
                                         (((dic_caracteres_individus[VITESSE_INDIVIDU][PARAM_MAX_VALUE] **
                                            Individu.poids_vitesse_energie_depensee) *
                                           (dic_caracteres_individus[RAYON_INDIVIDU][PARAM_MAX_VALUE] **
                                            Individu.poids_taille_energie_depensee)) -
                                          ((dic_caracteres_individus[VITESSE_INDIVIDU][PARAM_MIN_VALUE] **
                                            Individu.poids_vitesse_energie_depensee) *
                                           (dic_caracteres_individus[RAYON_INDIVIDU][PARAM_MIN_VALUE] **
                                            Individu.poids_taille_energie_depensee)))
        Individu.energie_depensee_plus = (energie_depensee_min -
                                          (Individu.coef_energie_depensee *
                                           (dic_caracteres_individus[VITESSE_INDIVIDU][PARAM_MIN_VALUE] **
                                            Individu.poids_vitesse_energie_depensee) *
                                           (dic_caracteres_individus[RAYON_INDIVIDU][PARAM_MIN_VALUE] **
                                            Individu.poids_taille_energie_depensee)))
        Individu.coef_petit_mage_gros = dic_params[COEF_PETIT_MANGE_GROS]
        Individu.coef_vitesse_chasse = dic_params[COEF_VITESSE_CHASSE]
        Individu.duree_gestation_energie_totale = dic_params[DUREE_GESTATION_ENERGIE_TOTALE]

        Individu.dic_caracteres_individus = {}
        dic_caracteres_individus_init = {}
        for caractere, dic in dic_caracteres_individus.items():
            dic_params_caractere = {}
            for param, value in dic.items():
                if param == PARAM_VALUE:
                    dic_caracteres_individus_init[caractere] = value
                else:
                    dic_params_caractere[param] = value
            Individu.dic_caracteres_individus[caractere] = dic_params_caractere

        # LISTE_CARACTERES_INDIVIDU_SECONDAIRES :
        Individu.dic_caracteres_individus[AGE] = {PARAM_MIN_VALUE: 0,
                                                  PARAM_MAX_VALUE: AGE_MAXIMUM_AFFICHAGE_GRAPH_3D}
        Individu.dic_caracteres_individus[ENERGIE_DEPENSEE] = {PARAM_MIN_VALUE: energie_depensee_min,
                                                               PARAM_MAX_VALUE: energie_depensee_max}
        Individu.dic_caracteres_individus[ENERGIE_INIT] = {
            PARAM_MIN_VALUE: (dic_caracteres_individus[ENERGIE_COUT_NEW_INDIVIDU][PARAM_MIN_VALUE] *
                              dic_caracteres_individus[DUREE_NEW_INDIVIDU][PARAM_MIN_VALUE] /
                              Individu.duree_gestation_energie_totale),
            PARAM_MAX_VALUE: (dic_caracteres_individus[ENERGIE_COUT_NEW_INDIVIDU][PARAM_MAX_VALUE] *
                              dic_caracteres_individus[DUREE_NEW_INDIVIDU][PARAM_MAX_VALUE] /
                              Individu.duree_gestation_energie_totale)}

        for _ in range(dic_params[NB_INDIVIDUS_INIT]):
            i, j = random.choice(self.carte.liste_altitudes_positives)
            for caractere in dic_caracteres_individus_init.keys():
                if not dic_caracteres_individus[caractere][PARAM_ALEATOIRE]:
                    dic_caracteres_individus_init[caractere] = (dic_caracteres_individus[caractere][PARAM_MIN_VALUE] +
                                                                random.random() *
                                                                (dic_caracteres_individus[caractere][PARAM_MAX_VALUE] -
                                                                 dic_caracteres_individus[caractere][PARAM_MIN_VALUE]))
                    if DIC_CARACTERES_INDIVIDU[caractere][PARAM_TYPE] == int:
                        dic_caracteres_individus_init[caractere] = int(dic_caracteres_individus_init[caractere])
            self.new_individu(i, j, copy.deepcopy(dic_caracteres_individus_init))

        self.add_nourritures(dic_params[NB_NOURRITURES_INIT])

        self.nouvelle_journee()

    def new_individu(self, i: int, j: int, dic_variables: dict, dic_variables_partenaires: dict = None):
        energie_init = dic_variables[ENERGIE_COUT_NEW_INDIVIDU] * \
                       dic_variables[DUREE_NEW_INDIVIDU] / Individu.duree_gestation_energie_totale
        for caractere in LISTE_CARACTERES_INDIVIDU:
            dic = Individu.dic_caracteres_individus[caractere]
            if dic_variables_partenaires is not None and random.random() > 0.5:
                dic_variables[caractere] = dic_variables_partenaires[caractere]
            if random.random() < dic[PARAM_PROBA_MUTATION]:
                if random.random() > 0.5:
                    dic_variables[caractere] += random.random() * dic[PARAM_DEGRE_MUTATION]
                    if DIC_CARACTERES_INDIVIDU[caractere][PARAM_TYPE] == int:
                        dic_variables[caractere] = int(dic_variables[caractere])
                    if dic_variables[caractere] > dic[PARAM_MAX_VALUE]:
                        dic_variables[caractere] = dic[PARAM_MAX_VALUE]
                else:
                    dic_variables[caractere] -= random.random() * dic[PARAM_DEGRE_MUTATION]
                    if DIC_CARACTERES_INDIVIDU[caractere][PARAM_TYPE] == int:
                        dic_variables[caractere] = int(dic_variables[caractere])
                    if dic_variables[caractere] < dic[PARAM_MIN_VALUE]:
                        dic_variables[caractere] = dic[PARAM_MIN_VALUE]
        self.liste_individus.append(Individu(self.carte, self.carte_content, i, j, dic_variables, energie_init))

    def new_nourriture(self, i: int, j: int, type_nour: int):
        nourriture = Nourriture(self.carte, self.carte_content, type_nour, i, j)
        self.liste_nourriture.append(nourriture)

    def add_nourritures(self, nb: int):
        liste_cases = (self.carte.liste_altitudes_positives +
                       Nourriture.coef_proba_nour_abondante * self.carte.liste_altitudes_abondantes)
        for type_nour, dic_nour in Nourriture.dic_type_nourriture.items():
            for _ in range(round(nb * dic_nour[PARAM_NOUR_PROBA])):
                self.new_nourriture(*random.choice(liste_cases), type_nour)

    def gere_clic(self, x_souris: int, y_souris: int):
        self.carte.gere_clic(x_souris, y_souris)

    def gere_zoom(self, sens: bool, x_souris: int, y_souris: int):
        self.carte.gere_zoom(sens, x_souris, y_souris)

    def gere_deplacement_souris(self, x_souris: int, y_souris: int):
        self.carte.update_deplacement_camera(x_souris, y_souris)

    def nouvelle_journee(self):
        self.stats.nouvelle_journee(self.liste_individus)
        self.t = 0
        if not self.periode_update_carte == 0 and self.stats.jour % self.periode_update_carte == 0:
            self.carte.update_grille()

        for i, j in self.carte.liste_altitudes_negatives:
            for thing in self.carte_content.pop_grille_content_ij(i, j):
                thing.actif = False
                if isinstance(thing, Nourriture):
                    self.liste_nourriture.remove(thing)
                else:
                    self.liste_individus.remove(thing)

        self.add_nourritures(Nourriture.nb_nourritures_par_jour)

        for individu in self.liste_individus:
            individu.nouvelle_journee()

    def update(self):
        self.t += 1
        for individu in self.liste_individus:
            individu.update_objectif()
            # individu.update()
            if not individu.actif:
                self.liste_individus.remove(individu)
            if individu.new_individu:
                self.new_individu(int(individu.i), int(individu.j), copy.deepcopy(individu.dic_variables),
                                  individu.dic_variables_partenaire)
                individu.new_individu = False
                individu.dic_variables_partenaire = None
        for individu in self.liste_individus:
            individu.update()

        for nourriture in self.liste_nourriture:
            nourriture.update()
            if not nourriture.actif:
                self.liste_nourriture.remove(nourriture)

        if self.t >= self.duree_journee:
            self.nouvelle_journee()

    def init_pygame(self, confs: dict):
        self.carte.init_pygame(confs)

    def affiche(self, screen: pygame.Surface):
        self.carte.update_ecran()
        screen.blit(self.carte.ecran, (0, 0))
        for case in self.carte.liste_cases_affichage:
            for thing in self.carte_content.get_grille_content_ij(*case):
                thing.affiche(screen)
        screen.blit(self.carte.ecran_miniature, (X_MINIATURE_SUR_ECRAN, Y_MINIATURE_SUR_ECRAN))
