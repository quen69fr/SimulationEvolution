# coding: utf-8

import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
from individu import *


def couleur_rgb_to_matplotlib(couleur):
    return couleur[0] / 255, couleur[1] / 255, couleur[2] / 255


class Stats:
    id_axs = 0
    tk_jour = None
    tk_nb_individus = None
    tk_nb_jours_par_min = None

    def __init__(self, carte: Carte):
        self.jour = 0

        self.nb_individus = numpy.array([0])
        self.nb_individus_naissance = numpy.array([0])
        self.nb_individus_peut_se_reproduire = numpy.array([0])
        self.nb_individus_gestants = numpy.array([0])
        self.nb_morts = numpy.array([0])
        self.time = 0

        self.dic_individus_new = []
        self.dic_individus_gestant = []
        self.dic_individus_peut_se_reproduire = []
        self.dic_individus_autre = []

        self.dic_id_figs = {}

        self.tk_jour.set(0)
        self.tk_nb_individus.set(0)
        self.tk_nb_jours_par_min.set(0.)

        self.dic_figures_enregistrement = {}

        self.carte = carte

    def nouvelle_journee(self, liste_individus: list):
        self.dic_individus_new = []
        self.dic_individus_gestant = []
        self.dic_individus_peut_se_reproduire = []
        self.dic_individus_autre = []

        nb_individus = 0
        nb_individus_naissance = 0
        nb_individus_peut_se_reproduire = 0
        nb_individus_gestants = 0

        for individu in liste_individus:
            nb_individus += 1
            dic_caractere = copy.deepcopy(individu.dic_variables)
            # LISTE_CARACTERES_INDIVIDU_SECONDAIRES :
            dic_caractere[AGE] = individu.age
            dic_caractere[ENERGIE_DEPENSEE] = individu.energie_depense
            dic_caractere[ENERGIE_INIT] = individu.energie_init
            if individu.age == 0:
                nb_individus_naissance += 1
                self.dic_individus_new.append(dic_caractere)
            elif individu.peut_se_reproduire:
                nb_individus_peut_se_reproduire += 1
                self.dic_individus_peut_se_reproduire.append(dic_caractere)
            elif individu.compte_a_rebour_new_individu > 0:
                nb_individus_gestants += 1
                self.dic_individus_gestant.append(dic_caractere)
            else:
                self.dic_individus_autre.append(dic_caractere)

        self.nb_individus = numpy.append(self.nb_individus, [nb_individus])
        self.nb_individus_naissance = numpy.append(self.nb_individus_naissance, [nb_individus_naissance])
        self.nb_individus_peut_se_reproduire = numpy.append(self.nb_individus_peut_se_reproduire,
                                                            [nb_individus_peut_se_reproduire])
        self.nb_individus_gestants = numpy.append(self.nb_individus_gestants, [nb_individus_gestants])
        if self.jour == 0:
            nb_morts = 0
        else:
            nb_morts = self.nb_individus[self.jour] - nb_individus + nb_individus_naissance
        self.nb_morts = numpy.append(self.nb_morts, [nb_morts])

        self.jour += 1
        self.tk_jour.set(self.jour)
        self.tk_nb_individus.set(nb_individus)
        if time.time() == self.time:
            self.tk_nb_jours_par_min.set(math.inf)
        else:
            self.tk_nb_jours_par_min.set(round(60 / (time.time() - self.time), 1))
        self.time = time.time()
        for id_fig in self.dic_id_figs:
            self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_NEW_AFFICHAGE] = True

        try:
            self.update_enregistrements()
        except:
            print("Oups !")

    def new_enregistrement(self, id_fig, tk_var_nb_jours, nom_dossier, periode, type_resolution, afficher_miniature,
                           taille_miniature, coef_temperature_miniature):
        plt.ioff()
        id_fig2 = self.init_graph_matplotlib(self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_CARACTERES_3D],
                                             self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_VITESSE_ROTATION],
                                             self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_HAUTEUR_Z_AXIS])
        if not afficher_miniature:
            taille_miniature = 0
            coef_temperature_miniature = 0
        self.dic_figures_enregistrement[id_fig2] = {PARAM_MATPLOTLIB_TK_VAR_NB_JOURS: tk_var_nb_jours,
                                                    PARAM_MATPLOTLIB_NOM_DOSSIER: nom_dossier,
                                                    PARAM_MATPLOTLIB_PERIODE_IMAGE: [0, periode],
                                                    PARAM_TAILLE_MINIATURE: taille_miniature,
                                                    PARAM_COEF_TEMPERATURE_MINIATURE: coef_temperature_miniature}
        size = DIC_SIZE_ENREGISTREMENT[type_resolution][PARAM_ENR_SIZE]
        if size is None:
            size = self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].get_size_inches()
        self.dic_id_figs[id_fig2][PARAM_MATPLOTLIB_FIG].set_size_inches(*size)
        return id_fig2

    def update_enregistrements(self):
        for id_fig, dic_fig in self.dic_figures_enregistrement.items():
            dic_fig[PARAM_MATPLOTLIB_PERIODE_IMAGE][0] -= 1
            if dic_fig[PARAM_MATPLOTLIB_PERIODE_IMAGE][0] <= 0:
                dic_fig[PARAM_MATPLOTLIB_PERIODE_IMAGE][0] = dic_fig[PARAM_MATPLOTLIB_PERIODE_IMAGE][1]
                num_jour = dic_fig[PARAM_MATPLOTLIB_TK_VAR_NB_JOURS].get() + 1
                self.update_graph_matplotlib(id_fig, True)
                self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].savefig(
                    f"{dic_fig[PARAM_MATPLOTLIB_NOM_DOSSIER]}/{num_jour}.png")
                if not dic_fig[PARAM_TAILLE_MINIATURE] == 0:
                    self.carte.affiche_miniature(f"{dic_fig[PARAM_MATPLOTLIB_NOM_DOSSIER]}/{num_jour}.png",
                                                 dic_fig[PARAM_TAILLE_MINIATURE],
                                                 dic_fig[PARAM_COEF_TEMPERATURE_MINIATURE])
                dic_fig[PARAM_MATPLOTLIB_TK_VAR_NB_JOURS].set(num_jour)

    def init_graph_matplotlib(self, caractere_3D, vitesse_rotate, hauteur_z):
        self.id_axs += 1
        if caractere_3D is not None:
            self.init_graph_matplotlib_caracteres_population(self.id_axs, caractere_3D, vitesse_rotate, hauteur_z)
        else:
            self.init_graph_matplotlib_taille_population(self.id_axs)
        return self.id_axs

    def init_graph_matplotlib_taille_population(self, id_fig):
        fig = plt.figure(id_fig)
        ax = fig.add_subplot()
        fig.suptitle("Evolution de la population",
                     fontsize=fig.get_size_inches()[1] * MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_TITLE)
        self.dic_id_figs[id_fig] = {PARAM_MATPLOTLIB_FIG: fig,
                                    PARAM_MATPLOTLIB_AX: ax,
                                    PARAM_MATPLOTLIB_NEW_AFFICHAGE: True,
                                    PARAM_MATPLOTLIB_CARACTERES_3D: None,
                                    PARAM_MATPLOTLIB_VITESSE_ROTATION: None,
                                    PARAM_MATPLOTLIB_HAUTEUR_Z_AXIS: None}

    def init_graph_matplotlib_caracteres_population(self, id_fig, caractere_3D, vitesse_rotate, hauteur_z):
        fig = plt.figure(id_fig)
        ax = Axes3D(fig)
        if not vitesse_rotate == 0:
            ax.view_init(elev=hauteur_z, azim=vitesse_rotate * self.jour % int(360 / vitesse_rotate))
        else:
            ax.view_init(elev=hauteur_z)
        self.dic_id_figs[id_fig] = {PARAM_MATPLOTLIB_FIG: fig,
                                    PARAM_MATPLOTLIB_AX: ax,
                                    PARAM_MATPLOTLIB_NEW_AFFICHAGE: True,
                                    PARAM_MATPLOTLIB_CARACTERES_3D: caractere_3D,
                                    PARAM_MATPLOTLIB_VITESSE_ROTATION: vitesse_rotate,
                                    PARAM_MATPLOTLIB_HAUTEUR_Z_AXIS: hauteur_z}

    def update_graph_matplotlib(self, id_fig, update_if_new_affichage_is_false=False):
        if update_if_new_affichage_is_false or self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_NEW_AFFICHAGE]:
            self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_NEW_AFFICHAGE] = False
            if self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_CARACTERES_3D] is not None:
                self.update_graph_caracteres_population(id_fig)
            else:
                self.update_graph_taille_population(id_fig)
            return True
        return False

    def update_graph_taille_population(self, id_fig):
        fig = self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG]
        fig.suptitle(MATPLOTLIB_EVOLUTION_POPULATION_TITLE,
                     fontsize=fig.get_size_inches()[1] * MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_TITLE)
        ax = self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_AX]
        fontsize = (self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].get_size_inches()[1] *
                    MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_LEGENDE)
        labelpad = (self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].get_size_inches()[1] *
                    MATPLOTLIB_COEF_HEIGHT_FONT_DIST_AXES_LABELS)
        ax.clear()
        x = numpy.append(numpy.append([0], numpy.arange(0, self.jour)), [self.jour - 1])
        y1 = self.nb_individus
        y2 = y1 - self.nb_individus_naissance
        y3 = y2 - self.nb_individus_gestants
        y4 = y3 - self.nb_individus_peut_se_reproduire
        y5 = - self.nb_morts
        for y, color in [(y1, COULEUR_INDIVIDU_NAISSANCE),
                         (y2, COULEUR_INDIVIDU_GESTANT),
                         (y3, COULEUR_INDIVIDU_PEUT_SE_REPRODUIRE),
                         (y4, COULEUR_INDIVIDU_NORMAL),
                         (y5, COULEUR_INDIVIDU_MORT)]:
            ax.fill(x, numpy.append(y, [0]), color=couleur_rgb_to_matplotlib(color))

        ax.set_xlabel(MATPLOTLIB_LEGENDE_AXES_EVOLUTION_POPULATION[0], fontsize=fontsize, labelpad=labelpad)
        ax.set_ylabel(MATPLOTLIB_LEGENDE_AXES_EVOLUTION_POPULATION[1], fontsize=fontsize, labelpad=labelpad)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize)
        ax.legend(MATPLOTLIB_LEGENDE_EVOLUTION_POPULATION_TITLE, loc=MATPLOTLIB_POSITION_LEGENDE_EVOLUTION_POPULATION,
                  fontsize=fontsize)
        ax.grid()

    def update_graph_caracteres_population(self, id_fig):
        fig = self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG]
        fig.suptitle(MATPLOTLIB_GRAPH_3D_TITLE,
                     fontsize=fig.get_size_inches()[1] * MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_TITLE)
        caractere_3D = self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_CARACTERES_3D]
        ax = self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_AX]
        fontsize = (self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].get_size_inches()[1] *
                    MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_LEGENDE)
        pointsize = (self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].get_size_inches()[1] *
                     MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_POINTS_3D)
        labelpad = (self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].get_size_inches()[1] *
                    MATPLOTLIB_COEF_HEIGHT_FONT_DIST_AXES_LABELS)
        ax.clear()
        vitesse_rotate = self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_VITESSE_ROTATION]
        if not vitesse_rotate == 0:
            ax.view_init(elev=self.dic_id_figs[id_fig][PARAM_MATPLOTLIB_HAUTEUR_Z_AXIS],
                         azim=vitesse_rotate * self.jour % int(360 / vitesse_rotate))
        for liste_dics_individus, color in [(self.dic_individus_autre, COULEUR_INDIVIDU_NORMAL),
                                            (self.dic_individus_new, COULEUR_INDIVIDU_NAISSANCE),
                                            (self.dic_individus_peut_se_reproduire,
                                             COULEUR_INDIVIDU_PEUT_SE_REPRODUIRE),
                                            (self.dic_individus_gestant, COULEUR_INDIVIDU_GESTANT)]:
            x = []
            y = []
            z = []
            for individu in liste_dics_individus:
                x.append(individu[caractere_3D[0]])
                y.append(individu[caractere_3D[1]])
                z.append(individu[caractere_3D[2]])

            ax.scatter(x, y, z, color=couleur_rgb_to_matplotlib(color), marker="o", alpha=0.8, s=pointsize)

        ax.set_xlabel(DIC_CARACTERES_INDIVIDU[caractere_3D[0]][PARAM_LABEL], fontsize=fontsize, labelpad=labelpad)
        ax.set_ylabel(DIC_CARACTERES_INDIVIDU[caractere_3D[1]][PARAM_LABEL], fontsize=fontsize, labelpad=labelpad)
        ax.set_zlabel(DIC_CARACTERES_INDIVIDU[caractere_3D[2]][PARAM_LABEL], fontsize=fontsize, labelpad=labelpad)

        ax.set_xlim3d(Individu.dic_caracteres_individus[caractere_3D[0]][PARAM_MIN_VALUE],
                      Individu.dic_caracteres_individus[caractere_3D[0]][PARAM_MAX_VALUE])
        ax.set_ylim3d(Individu.dic_caracteres_individus[caractere_3D[1]][PARAM_MIN_VALUE],
                      Individu.dic_caracteres_individus[caractere_3D[1]][PARAM_MAX_VALUE])
        ax.set_zlim3d(Individu.dic_caracteres_individus[caractere_3D[2]][PARAM_MIN_VALUE],
                      Individu.dic_caracteres_individus[caractere_3D[2]][PARAM_MAX_VALUE])
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize)
        for tick in ax.zaxis.get_major_ticks():
            tick.label.set_fontsize(fontsize)
        ax.legend(MATPLOTLIB_LEGENDE_GRAPH_3D, loc=MATPLOTLIB_POSITION_LEGENDE_GRAPH_3D, fontsize=fontsize)
