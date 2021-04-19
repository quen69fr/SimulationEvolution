# TODO :
#  - TKINTER -> Config caractères individus : Forcer : min <= init <= max  &  griser init si aléatoire ...

# --------------------------------------- IMPORTS ---------------------------------------
# os
# Thread from threading
# tkinter (with messagebox, ttk, filedialog)
# pygame
# matplotlib.pyplot (with Axes3D from mpl_toolkits.mplot3d)
# moviepy.video.io.ImageSequenceClip
# numpy
# math
# random
# copy
# time


# --------------------------------------- SIMULATION ---------------------------------------
LISTE_CONFIGS = [DUREE_JOURNEE,
                 UPDATE_CARTE,
                 PERIODE_UPDATE_CARTE,
                 NB_NOURRITURES_PAR_JOUR,
                 NB_UPDATE_CARTE_INIT,
                 NB_INDIVIDUS_INIT,
                 NB_NOURRITURES_INIT,
                 COEF_ENERGIE_DEPENSEE_GAUCHE,
                 COEF_ENERGIE_DEPENSEE_DROITE,
                 ALTITUDE_MAX,
                 ALTITUDE_MIN,
                 ALTITUDE_GLOBALE_INIT,
                 ALTITUDE_BORD,
                 NB_ALTITUDES_FIXES_POSITIVES,
                 NB_ALTITUDES_FIXES_NEGATIVES,
                 PROBA_ALTITUDE_NEGATIVE_VERS_CENTRE,
                 COEF_PROBA_NOURRITURE_ABONDANTE,
                 ALTITUDE_MIN_NOURRITURE_ABONDANTE,
                 PROBA_NOURRITURE_1,
                 PROBA_NOURRITURE_2,
                 ENERGIE_NOURRITURE_1,
                 ENERGIE_NOURRITURE_2,
                 PROBA_MODIF_POINT_ALTITUDE_FIXE,
                 VALEUR_MODIF_POINT_ALTITUDE_FIXE,
                 PROBA_MODIF_POINT_ALTITUDE_FIXE_VITESSE,
                 LARGEUR_ENVIRONNEMENT,
                 HAUTEUR_ENVIRONNEMENT,
                 ENERGIE_DEPENSEE_MIN,
                 ENERGIE_DEPENSEE_MAX,
                 POIDS_VITESSE_ENERGIE_DEPENSEE,
                 POIDS_RAYON_ENERGIE_DEPENSEE,
                 COEF_PETIT_MANGE_GROS,
                 COEF_VITESSE_CHASSE,
                 DUREE_GESTATION_ENERGIE_TOTALE,
                 LARGEUR_ECRAN,
                 HAUTEUR_ECRAN,
                 ECHELLE_MAX,
                 COEF_ZOOM,
                 CARTE_MARGE_BORD_DEPLACEMENT,
                 CARTE_VITESSE_DEPLACEMENT,
                 PLEIN_ECRAN,
                 COEF_AFFICHAGE_ENERGIE_DEPENSEE] = list(range(42))

LISTE_CONFIGS_SIMULATION_ONLY = [DUREE_JOURNEE,
                                 UPDATE_CARTE,
                                 PERIODE_UPDATE_CARTE,
                                 NB_NOURRITURES_PAR_JOUR,
                                 NB_UPDATE_CARTE_INIT,
                                 NB_INDIVIDUS_INIT,
                                 NB_NOURRITURES_INIT,
                                 COEF_ENERGIE_DEPENSEE_GAUCHE,
                                 COEF_ENERGIE_DEPENSEE_DROITE,
                                 ALTITUDE_MAX,
                                 ALTITUDE_MIN,
                                 ALTITUDE_GLOBALE_INIT,
                                 ALTITUDE_BORD,
                                 NB_ALTITUDES_FIXES_POSITIVES,
                                 NB_ALTITUDES_FIXES_NEGATIVES,
                                 PROBA_ALTITUDE_NEGATIVE_VERS_CENTRE,
                                 COEF_PROBA_NOURRITURE_ABONDANTE,
                                 ALTITUDE_MIN_NOURRITURE_ABONDANTE,
                                 PROBA_NOURRITURE_1,
                                 PROBA_NOURRITURE_2,
                                 ENERGIE_NOURRITURE_1,
                                 ENERGIE_NOURRITURE_2,
                                 PROBA_MODIF_POINT_ALTITUDE_FIXE,
                                 VALEUR_MODIF_POINT_ALTITUDE_FIXE,
                                 PROBA_MODIF_POINT_ALTITUDE_FIXE_VITESSE,
                                 LARGEUR_ENVIRONNEMENT,
                                 HAUTEUR_ENVIRONNEMENT,
                                 ENERGIE_DEPENSEE_MIN,
                                 ENERGIE_DEPENSEE_MAX,
                                 POIDS_VITESSE_ENERGIE_DEPENSEE,
                                 POIDS_RAYON_ENERGIE_DEPENSEE,
                                 COEF_PETIT_MANGE_GROS,
                                 COEF_VITESSE_CHASSE,
                                 DUREE_GESTATION_ENERGIE_TOTALE]
LISTE_CONFIGS_PYGAME_ONLY = [LARGEUR_ECRAN,
                             HAUTEUR_ECRAN,
                             ECHELLE_MAX,
                             COEF_ZOOM,
                             CARTE_MARGE_BORD_DEPLACEMENT,
                             CARTE_VITESSE_DEPLACEMENT,
                             PLEIN_ECRAN,
                             COEF_AFFICHAGE_ENERGIE_DEPENSEE]

PARAM_DEFAULT_VALUE = PARAM_VALUE = 0
PARAM_MIN_VALUE = 1
PARAM_MAX_VALUE = 2
PARAM_STEP = 3
PARAM_LABEL = 4
PARAM_TYPE = 5

DIC_CONFIGURATIONS = {
    DUREE_JOURNEE: {
        PARAM_DEFAULT_VALUE: 50,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 200,
        PARAM_STEP: 1,
        PARAM_LABEL: "Durée d'une journée",
        PARAM_TYPE: int
    },
    UPDATE_CARTE: {
        PARAM_DEFAULT_VALUE: True,
        PARAM_LABEL: "Evolution de la carte",
        PARAM_TYPE: bool
    },
    PERIODE_UPDATE_CARTE: {
        PARAM_DEFAULT_VALUE: 1,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 30,
        PARAM_STEP: 1,
        PARAM_LABEL: "Période d'évolution de la carte",
        PARAM_TYPE: int
    },
    NB_NOURRITURES_PAR_JOUR: {
        PARAM_DEFAULT_VALUE: 70,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 800,
        PARAM_STEP: 1,
        PARAM_LABEL: "Nombre de nourritures par jour",
        PARAM_TYPE: int
    },
    NB_INDIVIDUS_INIT: {
        PARAM_DEFAULT_VALUE: 100,
        PARAM_MIN_VALUE: 10,
        PARAM_MAX_VALUE: 500,
        PARAM_STEP: 10,
        PARAM_LABEL: "Nombre d'individus au départ",
        PARAM_TYPE: int
    },
    NB_NOURRITURES_INIT: {
        PARAM_DEFAULT_VALUE: 100,
        PARAM_MIN_VALUE: 10,
        PARAM_MAX_VALUE: 1000,
        PARAM_STEP: 10,
        PARAM_LABEL: "Nombre de nourritures au départ",
        PARAM_TYPE: int
    },
    NB_UPDATE_CARTE_INIT: {
        PARAM_DEFAULT_VALUE: 20,
        PARAM_MIN_VALUE: 2,
        PARAM_MAX_VALUE: 1000,
        PARAM_STEP: 2,
        PARAM_LABEL: "Nombre d'étape d'évolution de la carte",
        PARAM_TYPE: int
    },
    COEF_ENERGIE_DEPENSEE_GAUCHE: {
        PARAM_DEFAULT_VALUE: 1.,
        PARAM_MIN_VALUE: 1.,
        PARAM_MAX_VALUE: 10.,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Cout en énergie à gauche",
        PARAM_TYPE: float
    },
    COEF_ENERGIE_DEPENSEE_DROITE: {
        PARAM_DEFAULT_VALUE: 5.,
        PARAM_MIN_VALUE: 1.,
        PARAM_MAX_VALUE: 20.,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Cout en énergie à droite",
        PARAM_TYPE: float
    },
    ALTITUDE_MAX: {
        PARAM_DEFAULT_VALUE: 4,
        PARAM_MIN_VALUE: 0.5,
        PARAM_MAX_VALUE: 6,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Altitude maximale",
        PARAM_TYPE: float
    },
    ALTITUDE_MIN: {
        PARAM_DEFAULT_VALUE: -1,
        PARAM_MIN_VALUE: -4,
        PARAM_MAX_VALUE: -0.5,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Altitude minimale",
        PARAM_TYPE: float
    },
    ALTITUDE_GLOBALE_INIT: {
        PARAM_DEFAULT_VALUE: 0.2,
        PARAM_MIN_VALUE: -1,
        PARAM_MAX_VALUE: 3,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Altitude globale initiale",
        PARAM_TYPE: float
    },
    ALTITUDE_BORD: {
        PARAM_DEFAULT_VALUE: -1,
        PARAM_MIN_VALUE: -5,
        PARAM_MAX_VALUE: -0.5,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Altitude au niveau des bords de la carte",
        PARAM_TYPE: float
    },
    NB_ALTITUDES_FIXES_POSITIVES: {
        PARAM_DEFAULT_VALUE: 20,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 120,
        PARAM_STEP: 1,
        PARAM_LABEL: "Nombre de points hauts sur la carte",
        PARAM_TYPE: int
    },
    NB_ALTITUDES_FIXES_NEGATIVES: {
        PARAM_DEFAULT_VALUE: 50,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 120,
        PARAM_STEP: 1,
        PARAM_LABEL: "Nombre de points bas sur la carte",
        PARAM_TYPE: int
    },
    PROBA_ALTITUDE_NEGATIVE_VERS_CENTRE: {
        PARAM_DEFAULT_VALUE: 0.7,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 1,
        PARAM_STEP: 0.01,
        PARAM_LABEL: "Proba séparation droite/gauche",
        PARAM_TYPE: int
    },
    COEF_PROBA_NOURRITURE_ABONDANTE: {
        PARAM_DEFAULT_VALUE: 3,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 8,
        PARAM_STEP: 1,
        PARAM_LABEL: "Poids des zones abondantes (nourriture)",
        PARAM_TYPE: int
    },
    ALTITUDE_MIN_NOURRITURE_ABONDANTE: {
        PARAM_DEFAULT_VALUE: 0.6,
        PARAM_MIN_VALUE: 0.1,
        PARAM_MAX_VALUE: 5,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Altitude minimale des zones abondantes",
        PARAM_TYPE: float
    },
    PROBA_NOURRITURE_1: {
        PARAM_DEFAULT_VALUE: 0.7,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 1,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Proportion de nourriture de type 1",
        PARAM_TYPE: float
    },
    PROBA_NOURRITURE_2: {
        PARAM_DEFAULT_VALUE: 0.3,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 1,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Proportion de nourriture de type 2",
        PARAM_TYPE: float
    },
    ENERGIE_NOURRITURE_1: {
        PARAM_DEFAULT_VALUE: 50,
        PARAM_MIN_VALUE: 5,
        PARAM_MAX_VALUE: 150,
        PARAM_STEP: 2,
        PARAM_LABEL: "Energie d'une nourriture de type 1",
        PARAM_TYPE: float
    },
    ENERGIE_NOURRITURE_2: {
        PARAM_DEFAULT_VALUE: 80,
        PARAM_MIN_VALUE: 5,
        PARAM_MAX_VALUE: 120,
        PARAM_STEP: 2,
        PARAM_LABEL: "Energie d'une nourriture de type 2",
        PARAM_TYPE: float
    },
    PROBA_MODIF_POINT_ALTITUDE_FIXE: {
        PARAM_DEFAULT_VALUE: 0.5,
        PARAM_MIN_VALUE: 0.05,
        PARAM_MAX_VALUE: 1,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Fréquence mouvement carte",
        PARAM_TYPE: float
    },
    VALEUR_MODIF_POINT_ALTITUDE_FIXE: {
        PARAM_DEFAULT_VALUE: 1,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 8,
        PARAM_STEP: 1,
        PARAM_LABEL: "Vitesse mouvement carte",
        PARAM_TYPE: int
    },
    PROBA_MODIF_POINT_ALTITUDE_FIXE_VITESSE: {
        PARAM_DEFAULT_VALUE: 0.1,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 1,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Fréquence changement mouvement carte",
        PARAM_TYPE: float
    },
    LARGEUR_ENVIRONNEMENT: {
        PARAM_DEFAULT_VALUE: 150,
        PARAM_MIN_VALUE: 20,
        PARAM_MAX_VALUE: 500,
        PARAM_STEP: 10,
        PARAM_LABEL: "Largeur de la carte",
        PARAM_TYPE: int
    },
    HAUTEUR_ENVIRONNEMENT: {
        PARAM_DEFAULT_VALUE: 100,
        PARAM_MIN_VALUE: 20,
        PARAM_MAX_VALUE: 500,
        PARAM_STEP: 10,
        PARAM_LABEL: "Hauteur de la carte",
        PARAM_TYPE: int
    },
    ENERGIE_DEPENSEE_MIN: {
        PARAM_DEFAULT_VALUE: 5,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 50,
        PARAM_STEP: 1,
        PARAM_LABEL: "Energie dépensée min",
        PARAM_TYPE: float
    },
    ENERGIE_DEPENSEE_MAX: {
        PARAM_DEFAULT_VALUE: 500,
        PARAM_MIN_VALUE: 50,
        PARAM_MAX_VALUE: 4000,
        PARAM_STEP: 50,
        PARAM_LABEL: "Energie dépensée max",
        PARAM_TYPE: float
    },
    POIDS_VITESSE_ENERGIE_DEPENSEE: {
        PARAM_DEFAULT_VALUE: 2,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 5,
        PARAM_STEP: 0.5,
        PARAM_LABEL: "Poids vitesse énergie dépensée",
        PARAM_TYPE: float
    },
    POIDS_RAYON_ENERGIE_DEPENSEE: {
        PARAM_DEFAULT_VALUE: 3,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 5,
        PARAM_STEP: 0.5,
        PARAM_LABEL: "Poids taille énergie dépensée",
        PARAM_TYPE: float
    },
    COEF_PETIT_MANGE_GROS: {
        PARAM_DEFAULT_VALUE: 1.3,
        PARAM_MIN_VALUE: 1.05,
        PARAM_MAX_VALUE: 2.5,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Coef taille manger plus petit",
        PARAM_TYPE: float
    },
    COEF_VITESSE_CHASSE: {
        PARAM_DEFAULT_VALUE: 0.85,
        PARAM_MIN_VALUE: 0.5,
        PARAM_MAX_VALUE: 1.2,
        PARAM_STEP: 0.01,
        PARAM_LABEL: "Non optimisme chasse des individus",
        PARAM_TYPE: float
    },
    DUREE_GESTATION_ENERGIE_TOTALE: {
        PARAM_DEFAULT_VALUE: 200,
        PARAM_MIN_VALUE: 50,
        PARAM_MAX_VALUE: 400,
        PARAM_STEP: 5,
        PARAM_LABEL: "Durée de gestation énergie totale",
        PARAM_TYPE: float
    },

    LARGEUR_ECRAN: {
        PARAM_DEFAULT_VALUE: 900,
        PARAM_MIN_VALUE: 200,
        PARAM_MAX_VALUE: 1200,
        PARAM_STEP: 5,
        PARAM_LABEL: "Largeur de l'écran (pixels)",
        PARAM_TYPE: int
    },
    HAUTEUR_ECRAN: {
        PARAM_DEFAULT_VALUE: 600,
        PARAM_MIN_VALUE: 200,
        PARAM_MAX_VALUE: 1200,
        PARAM_STEP: 5,
        PARAM_LABEL: "Hauteur de l'écran (pixels)",
        PARAM_TYPE: int
    },
    COEF_ZOOM: {
        PARAM_DEFAULT_VALUE: 0.15,
        PARAM_MIN_VALUE: 0.05,
        PARAM_MAX_VALUE: 1.,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Sensibilité du zoom",
        PARAM_TYPE: float
    },
    CARTE_VITESSE_DEPLACEMENT: {
        PARAM_DEFAULT_VALUE: 25,
        PARAM_MIN_VALUE: 2,
        PARAM_MAX_VALUE: 50,
        PARAM_STEP: 1,
        PARAM_LABEL: "Sensibilité déplacement",
        PARAM_TYPE: int
    },
    CARTE_MARGE_BORD_DEPLACEMENT: {
        PARAM_DEFAULT_VALUE: 30,
        PARAM_MIN_VALUE: 2,
        PARAM_MAX_VALUE: 50,
        PARAM_STEP: 1,
        PARAM_LABEL: "Bordure déplacement",
        PARAM_TYPE: int
    },
    ECHELLE_MAX: {
        PARAM_DEFAULT_VALUE: 80,
        PARAM_MAX_VALUE: 50,
        PARAM_MIN_VALUE: 200,
        PARAM_STEP: 5,
        PARAM_LABEL: "Echelle maximale",
        PARAM_TYPE: int
    },
    PLEIN_ECRAN: {
        PARAM_DEFAULT_VALUE: False,
        PARAM_LABEL: "Plein écran",
        PARAM_TYPE: bool
    },
    COEF_AFFICHAGE_ENERGIE_DEPENSEE: {
        PARAM_DEFAULT_VALUE: 50,
        PARAM_MAX_VALUE: 100,
        PARAM_MIN_VALUE: 0,
        PARAM_STEP: 5,
        PARAM_LABEL: "Contraste température",
        PARAM_TYPE: int
    }
}

LISTE_CARACTERES_INDIVIDU = [VITESSE_INDIVIDU,
                             RAYON_VISION_INDIVIDU,
                             RAYON_INDIVIDU,
                             ENERGIE_MIN_NEW_INDIVIDU,
                             ENERGIE_COUT_NEW_INDIVIDU,
                             DUREE_NEW_INDIVIDU] = list(range(6))
LISTE_CARACTERES_INDIVIDU_SECONDAIRES = [AGE, ENERGIE_DEPENSEE, ENERGIE_INIT] = [6, 7, 8]

PARAM_PROBA_MUTATION_DEFAULT = PARAM_PROBA_MUTATION = 6
PARAM_DEGRE_MUTATION_DEFAULT = PARAM_DEGRE_MUTATION = 7
PARAM_DEGRE_MUTATION_MIN = 8
PARAM_DEGRE_MUTATION_MAX = 9
PARAM_DEGRE_MUTATION_STEP = 10
PARAM_ALEATOIRE_DEFAULT = PARAM_ALEATOIRE = 11

DIC_CARACTERES_INDIVIDU = {
    VITESSE_INDIVIDU: {
        PARAM_DEFAULT_VALUE: 0.3,
        PARAM_MIN_VALUE: 0.05,
        PARAM_MAX_VALUE: 1.,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Vitesse de déplacement",
        PARAM_TYPE: float,
        PARAM_PROBA_MUTATION_DEFAULT: 0.1,
        PARAM_DEGRE_MUTATION_DEFAULT: 0.08,
        PARAM_DEGRE_MUTATION_MIN: 0.005,
        PARAM_DEGRE_MUTATION_MAX: 0.2,
        PARAM_DEGRE_MUTATION_STEP: 0.005,
        PARAM_ALEATOIRE_DEFAULT: False
    },
    RAYON_VISION_INDIVIDU: {
        PARAM_DEFAULT_VALUE: 1.,
        PARAM_MIN_VALUE: 0.2,
        PARAM_MAX_VALUE: 2.5,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Vision (distance)",
        PARAM_TYPE: float,
        PARAM_PROBA_MUTATION_DEFAULT: 0.1,
        PARAM_DEGRE_MUTATION_DEFAULT: 0.1,
        PARAM_DEGRE_MUTATION_MIN: 0.05,
        PARAM_DEGRE_MUTATION_MAX: 0.2,
        PARAM_DEGRE_MUTATION_STEP: 0.005,
        PARAM_ALEATOIRE_DEFAULT: False
    },
    RAYON_INDIVIDU: {
        PARAM_DEFAULT_VALUE: 0.3,
        PARAM_MIN_VALUE: 0.1,
        PARAM_MAX_VALUE: 1,
        PARAM_STEP: 0.02,
        PARAM_LABEL: "Taille (rayon)",
        PARAM_TYPE: float,
        PARAM_PROBA_MUTATION_DEFAULT: 0.1,
        PARAM_DEGRE_MUTATION_DEFAULT: 0.08,
        PARAM_DEGRE_MUTATION_MIN: 0.005,
        PARAM_DEGRE_MUTATION_MAX: 0.2,
        PARAM_DEGRE_MUTATION_STEP: 0.005,
        PARAM_ALEATOIRE_DEFAULT: False
    },
    ENERGIE_MIN_NEW_INDIVIDU: {
        PARAM_DEFAULT_VALUE: 300,
        PARAM_MIN_VALUE: 50,
        PARAM_MAX_VALUE: 500,
        PARAM_STEP: 5,
        PARAM_LABEL: "Energie pour se reproduire",
        PARAM_TYPE: float,
        PARAM_PROBA_MUTATION_DEFAULT: 0.1,
        PARAM_DEGRE_MUTATION_DEFAULT: 5,
        PARAM_DEGRE_MUTATION_MIN: 1,
        PARAM_DEGRE_MUTATION_MAX: 30,
        PARAM_DEGRE_MUTATION_STEP: 0.5,
        PARAM_ALEATOIRE_DEFAULT: False
    },
    ENERGIE_COUT_NEW_INDIVIDU: {
        PARAM_DEFAULT_VALUE: 200,
        PARAM_MIN_VALUE: 20,
        PARAM_MAX_VALUE: 450,
        PARAM_STEP: 5,
        PARAM_LABEL: "Coup de reproduction",
        PARAM_TYPE: float,
        PARAM_PROBA_MUTATION_DEFAULT: 0.1,
        PARAM_DEGRE_MUTATION_DEFAULT: 5,
        PARAM_DEGRE_MUTATION_MIN: 1,
        PARAM_DEGRE_MUTATION_MAX: 30,
        PARAM_DEGRE_MUTATION_STEP: 0.5,
        PARAM_ALEATOIRE_DEFAULT: False
    },
    DUREE_NEW_INDIVIDU: {
        PARAM_DEFAULT_VALUE: 100,
        PARAM_MIN_VALUE: 5,
        PARAM_MAX_VALUE: 400,
        PARAM_STEP: 5,
        PARAM_LABEL: "Durée de gestation",
        PARAM_TYPE: int,
        PARAM_PROBA_MUTATION_DEFAULT: 0.1,
        PARAM_DEGRE_MUTATION_DEFAULT: 3,
        PARAM_DEGRE_MUTATION_MIN: 1,
        PARAM_DEGRE_MUTATION_MAX: 20,
        PARAM_DEGRE_MUTATION_STEP: 1,
        PARAM_ALEATOIRE_DEFAULT: True
    },

    AGE: {
        PARAM_LABEL: "Age (en jours)"
    },
    ENERGIE_DEPENSEE: {
        PARAM_LABEL: "Energie dépensée"
    },
    ENERGIE_INIT: {
        PARAM_LABEL: "Energie à la naissance"
    }
}

PROBA_MUTATION_MIN = 0.
PROBA_MUTATION_MAX = 1.
PROBA_MUTATION_STEP = 0.01

LISTE_CASES_AUTOUR_INDIVIDU = [(1/(2 ** (1/2)), [(0, 0)]),
                               (5 ** (1/2) / 2, [(-1, 0), (1, 0), (0, 1), (0, -1)]),
                               (3 / (2 ** (1/2)), [(-1, 1), (1, 1), (-1, -1), (1, -1)]),
                               ((13 / 2) ** (1/2), [(-2, 0), (0, 2), (2, 0), (0, -2)]),
                               ((17 / 2) ** (1/2), [(-1, 2), (1, 2), (-1, -2), (1, -2),
                                                    (-2, 1), (2, 1), (-2, -1), (2, -1)]),
                               (5 / (2 ** (1/2)), [(-2, 2), (2, 2), (-2, -2), (2, -2)])]

SQUARED_DISTANCE_INDIVIDU_CONTACT_COEF_VITESSE = 0.55
VITESSE_ROTATION_INDIVIDU_OBSTACLE = 0.6
NB_UPDATE_MAX_INDIVIDU_ORIENTATION = 10

TYPE_NOUR_1 = 1
TYPE_NOUR_2 = 2

PARAM_NOUR_ENERGIE = 0
PARAM_NOUR_PROBA = 1
PARAM_NOUR_RAYON = 2
PARAM_NOUR_COULEUR = 3

DIC_NOURRITURE = {TYPE_NOUR_1: {PARAM_NOUR_RAYON: 0.1,
                                PARAM_NOUR_COULEUR: (255, 0, 0)},
                  TYPE_NOUR_2: {PARAM_NOUR_RAYON: 0.2,
                                PARAM_NOUR_COULEUR: (255, 100, 100)}
                  }


# --------------------------------------- TKINTER ---------------------------------------
TK_APP_SIZE = "630x480"
TK_CONFIG_FRAME_SIZE = "520x650"
TK_CONFIG_AVANCEES_FRAME_SIZE = "1070x720"
TK_CONFIG_INDIVIDUS_FRAME_SIZE = "390x660"
TK_CONFIG_CARACTERES_FRAME_SIZE = "1300x550"
TK_MATPLOTLIB_FRAME_SIZE = "400x430"
TK_PYGAME_FRAME_SIZE = "350x480"
TK_PYGAME_FRAME_AVANCEE_SIZE = "350x490"
TK_MOVIEPY_FRAME_SIZE = "500x700"
TK_MOVIEPY_ENREGISTREMENT_FRAME_SIZE = ""

TK_TITLE_FONT = None, 30
TK_TITLE_2_FONT = None, 22
TK_FRAME_FONT = None, 15
TK_BUTTON_FONT = None, 14
TK_LABEL_FONT = None, 12
TK_JOUR_LABEL_FONT = None, 15

TK_MARGE_WIDGET = 9
FRAME_GENERAL = 0
FRAME_DEPART = 1
FRAME_AVANCEES_CARTE = 2
FRAME_AVANCEES_CARTE_ALTITUDES = 3
FRAME_AVANCEES_NOURRITURE = 4
FRAME_AVANCEES_INDIVIDUS = 5
FRAME_PYGAME_GENERAL = 6
FRAME_PYGAME_AVANCEES = 7

PARAM_TITRE = 0
PARAM_LISTE_CONFIG = 1

DIC_LABEL_FRAME_CONFIGURATIONS = {
    FRAME_GENERAL: {
        PARAM_TITRE: "Général",
        PARAM_LISTE_CONFIG: [DUREE_JOURNEE,
                             NB_NOURRITURES_PAR_JOUR]
    },
    FRAME_DEPART: {
        PARAM_TITRE: "Départ",
        PARAM_LISTE_CONFIG: [NB_INDIVIDUS_INIT,
                             NB_NOURRITURES_INIT]
    },
    FRAME_AVANCEES_CARTE: {
        PARAM_TITRE: "Carte général",
        PARAM_LISTE_CONFIG: [LARGEUR_ENVIRONNEMENT,
                             HAUTEUR_ENVIRONNEMENT,
                             NB_UPDATE_CARTE_INIT,
                             UPDATE_CARTE,
                             PERIODE_UPDATE_CARTE,
                             PROBA_MODIF_POINT_ALTITUDE_FIXE,
                             VALEUR_MODIF_POINT_ALTITUDE_FIXE,
                             PROBA_MODIF_POINT_ALTITUDE_FIXE_VITESSE]
    },
    FRAME_AVANCEES_CARTE_ALTITUDES: {
        PARAM_TITRE: "Carte altitudes",
        PARAM_LISTE_CONFIG: [ALTITUDE_MAX,
                             ALTITUDE_MIN,
                             ALTITUDE_GLOBALE_INIT,
                             ALTITUDE_BORD,
                             PROBA_ALTITUDE_NEGATIVE_VERS_CENTRE,
                             NB_ALTITUDES_FIXES_POSITIVES,
                             NB_ALTITUDES_FIXES_NEGATIVES]
    },
    FRAME_AVANCEES_NOURRITURE: {
        PARAM_TITRE: "Energie",
        PARAM_LISTE_CONFIG: [COEF_ENERGIE_DEPENSEE_GAUCHE,
                             COEF_ENERGIE_DEPENSEE_DROITE,
                             COEF_PROBA_NOURRITURE_ABONDANTE,
                             ALTITUDE_MIN_NOURRITURE_ABONDANTE,
                             PROBA_NOURRITURE_1,
                             PROBA_NOURRITURE_2,
                             ENERGIE_NOURRITURE_1,
                             ENERGIE_NOURRITURE_2]
    },
    FRAME_AVANCEES_INDIVIDUS: {
        PARAM_TITRE: "Individus",
        PARAM_LISTE_CONFIG: [ENERGIE_DEPENSEE_MIN,
                             ENERGIE_DEPENSEE_MAX,
                             POIDS_VITESSE_ENERGIE_DEPENSEE,
                             POIDS_RAYON_ENERGIE_DEPENSEE,
                             COEF_PETIT_MANGE_GROS,
                             COEF_VITESSE_CHASSE,
                             DUREE_GESTATION_ENERGIE_TOTALE]
    },
    FRAME_PYGAME_GENERAL: {
        PARAM_TITRE: "Général",
        PARAM_LISTE_CONFIG: [LARGEUR_ECRAN,
                             HAUTEUR_ECRAN,
                             PLEIN_ECRAN]
    },
    FRAME_PYGAME_AVANCEES: {
        PARAM_TITRE: "Avancés",
        PARAM_LISTE_CONFIG: [COEF_AFFICHAGE_ENERGIE_DEPENSEE,
                             COEF_ZOOM,
                             CARTE_VITESSE_DEPLACEMENT,
                             CARTE_MARGE_BORD_DEPLACEMENT,
                             ECHELLE_MAX]

    }
}

LISTE_PARAM_CARACTERES_INDIVIDUS_TITLE = [
    (PARAM_LABEL, "Caractère"),
    (PARAM_VALUE, "Valeur initiale   "),
    (PARAM_MIN_VALUE, "Valeur minimale"),
    (PARAM_MAX_VALUE, "Valeur maximale"),
    (PARAM_PROBA_MUTATION, "Proba de mutation"),
    (PARAM_DEGRE_MUTATION, "Valeur mutation")
]

SCALE_SIMULATION_FPS = 0
SCALE_PYGAME_FPS = 1
SCALE_MATPLOTLIB_FPS = 2
SCALE_MOVIEPY_FPS = 3
SCALE_MOVIEPY_PERIODE = 4
SCALE_MATPLOTLIB_3D_VITESSE_ROTATION = 5
SCALE_MATPLOTLIB_3D_HAUTEUR_Z = 6
SCALE_MOVIEPY_SIZE_MINIATURE = 7

DIC_SCALE = {
    SCALE_SIMULATION_FPS: {
        PARAM_DEFAULT_VALUE: 0.03,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 0.2,
        PARAM_STEP: 0.002,
        PARAM_LABEL: "Delay minimum (vitesse smulation)"
    },
    SCALE_PYGAME_FPS: {
        PARAM_DEFAULT_VALUE: 20,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 40,
        PARAM_STEP: 1,
        PARAM_LABEL: "Nombre d'images par seconde"
    },
    SCALE_MATPLOTLIB_FPS: {
        PARAM_DEFAULT_VALUE: 20,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 40,
        PARAM_STEP: 1,
        PARAM_LABEL: "Nombre d'images par seconde"
    },
    SCALE_MOVIEPY_FPS: {
        PARAM_DEFAULT_VALUE: 20,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 40,
        PARAM_STEP: 1,
        PARAM_LABEL: "Nombre d'images par seconde"
    },
    SCALE_MOVIEPY_PERIODE: {
        PARAM_DEFAULT_VALUE: 2,
        PARAM_MIN_VALUE: 1,
        PARAM_MAX_VALUE: 40,
        PARAM_STEP: 1,
        PARAM_LABEL: "Période prises en jours"
    },
    SCALE_MATPLOTLIB_3D_VITESSE_ROTATION: {
        PARAM_DEFAULT_VALUE: 0,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 4,
        PARAM_STEP: 0.05,
        PARAM_LABEL: "Vitesse de rotation de la caméra"
    },
    SCALE_MATPLOTLIB_3D_HAUTEUR_Z: {
        PARAM_DEFAULT_VALUE: 15,
        PARAM_MIN_VALUE: 0,
        PARAM_MAX_VALUE: 90,
        PARAM_STEP: 1,
        PARAM_LABEL: "Hauteur de la caméra"
    },
    SCALE_MOVIEPY_SIZE_MINIATURE: {
        PARAM_DEFAULT_VALUE: 1,
        PARAM_MIN_VALUE: 0.2,
        PARAM_MAX_VALUE: 5,
        PARAM_STEP: 0.1,
        PARAM_LABEL: "Taille de la miniature"
    }
}


START_BUTTON = 0
STOP_BUTTON = 1
NEW_BUTTON = 2

TK_MESSAGE_BOX_NOUVEAU = ("Nouvelle simulation ?", "Vous allez perdre la simulation en cours.\n"
                                                   "Et tous les enregistrements en cours associés\n"
                                                   "Êtes vous sûr de vouloir en lancer une autre ?")
TK_MESSAGE_BOX_QUITTER = ("Fermer le programme ?",
                          "Vous allez perdre la simulation et\n"
                          "tous les enregistrements en cours.\n"
                          "Êtes vous sûr de vouloir quitter ?")
TK_MESSAGE_BOX_ENREGISTEMENT = ("Abandonner l'enregistrement ?",
                                "Êtes vous sûr de vouloir arrêter cet enregistrement ?\n"
                                "Toutes les images seront suprimées !",)

TK_CAPTION_TEXT = "Gestion : Simulation et évolution"

TK_TITLE_TEXT = "Simulation de l'évolution"
TK_TITLE_CONF_TEXT = "Configuration simulation"
TK_TITLE_MATPLOT_TEXT = "Nouveau graphique"
TK_TITLE_PYGAME_TEXT = "Paramètres d'affichage"
TK_TITLE_MOVIEPY_TEXT = "Nouvel enregistrement"
TK_TITLE_MOVIEPY_ENREGISTREMENT_TEXT = "Enregistrement"
TK_TITLE_MOVIEPY_ENREGISTREMENT_BROWSE_TEXT = "Enregistrer la vidéo"
TK_LISTE_TITLE_MOVIEPY_FRAMES_TEXT = "Images", "Résolution", "Miniature", "Vidéos"

TK_SIMULATION_TEXT = "Simulation"
TK_PYGAME_TEXT = "Affichage"
TK_MATPLOTLIB_TEXT = "Graphiques"
TK_CONFIG_AVANCES_TEXT = "Avancés"

TK_NEW_BUTTON_TEXT = "Nouveau"
TK_START_BUTTON_TEXT = "Start"
TK_STOP_BUTTON_TEXT = "Stop"
TK_START_BUTTON_PLEASE_WAIT_TEXT = "Quelques instants ..."
TK_QUITTER_BUTTON_TEXT = "Quitter"
TK_VALIDER_BUTTON_TEXT = "Valider"
TK_RESET_BUTTON_TEXT = "Reset"
TK_ANNULER_BUTTON_TEXT = "Annuler"
TK_CONFIG_AVANCEES_BUTTON_TEXT = "Paramètres avancés"
TK_CONFIG_INDIVIDUS_BUTTON_TEXT = "Individus"
TK_CONFIG_CARACTERE_BUTTON_TEXT = "Caractères"
TK_MATPLOT_RADIOBUTTON_POPULATION_TEXT = "Population"
TK_MATPLOT_RADIOBUTTON_3D_TEXT = "3D"
TK_NEW_MOVIEPY_BUTTON_TEXT = "Nouvel enregistrement"
TK_SAUVER_BUTTON_TEXT = "Sauver"

TK_JOUR_NUM_LABEL_TEXT = "Jour n°"
TK_LABEL_I_NB_INDIVIDUS = "individus"
TK_LABEL_I_NB_JOURS_PAR_MIN = "jours par minute"
TK_LABELS_MATPLOT_AXES = ["Axe X", "Axe Y", "Axe Z"]
TK_CHECKBUTTON_KEEP_CONF = "Garder ces configurations"
TK_CHECKBUTTON_ENR_KEEP_IMAGES = "Garder les images"
TK_LABEL_VIDEO_SAVING = "La vidéo est en train de s'enregistrer :\n\n"
TK_LABEL_MOVIEPY_NB_IMAGES = "Nombre d'images : "
TK_LABEL_MOVIEPY_DUREE_ENREGISTREMENT = "Durée de l'enrgistrement : ", " sec"
TK_CHECKBUTTON_MOVIEPY_AFFICHER_MINIATURE = "Afficher la miniature"


# --------------------------------------- PYGAME ---------------------------------------
CAPTION = "Evolution"

X_MINIATURE_SUR_ECRAN = 10
Y_MINIATURE_SUR_ECRAN = 10
COULEUR_CADRE_CAMERA_MINIATURE = 255, 255, 255
COEF_COULEUR_MINIATURE_HORS_CAMERA = 2
PRECISION_ALTITUDE_CARTE = 3
PRECISION_POSITION_CAMERA_CARTE = 4
MARGE_BORD_ALTITUDE_FIXE = 9


def COULEUR_ALTITUDE(altitude: float, altitude_min_nour_abondante: float, coef_froid: float, coef_couleur_froid: int):
    if altitude <= 0:
        return 0, 0, min(10 + int(- altitude * 20), 20)
    if coef_couleur_froid == 0:
        if altitude > altitude_min_nour_abondante:
            return 60, 125, 30
        c = min(0.4 + 1.2 * altitude, 0.9)
        return int(60 * c), int(125 * c), int(30 * c)
    add = (coef_froid - 1.1) * (altitude ** 0.1) * coef_couleur_froid
    if altitude > altitude_min_nour_abondante:
        return (min(int(60 + add), 255),
                min(int(125 + add), 255),
                min(int(30 + add), 255))
    c = min(0.4 + 1.2 * altitude, 0.9)
    return (min(int(60 * c + add), 255),
            min(int(125 * c + add), 255),
            min(int(30 * c + add), 255))

    # if altitude > ATITUDE_MIN_NOURITURE_ABONDANTE:
    #     d = 0.5
    #     if altitude > ATITUDE_MIN_NOURITURE_ABONDANTE + d:
    #         return 60, 125, 30
    #     # c = min(0.4 + 1.2 * altitude, 0.9)
    #     return (int(10 / d * (altitude - ATITUDE_MIN_NOURITURE_ABONDANTE) + 50),
    #             int(95 / d * (altitude - ATITUDE_MIN_NOURITURE_ABONDANTE) + 30),
    #             int(15 / d * (altitude - ATITUDE_MIN_NOURITURE_ABONDANTE) + 15))
    # c = min(0.4 + 1.2 * altitude, 0.9)
    # return int(50 * c), int(30 * c), int(15 * c)


COULEUR_INDIVIDU_NORMAL = 80, 80, 255
COULEUR_INDIVIDU_PEUT_SE_REPRODUIRE = 170, 80, 255
COULEUR_INDIVIDU_GESTANT = 255, 80, 255
COULEUR_INDIVIDU_MORT = 150, 0, 0
COULEUR_INDIVIDU_NAISSANCE = 80, 80, 80

# --------------------------------------- MATPLOTLIB ---------------------------------------
AGE_MAXIMUM_AFFICHAGE_GRAPH_3D = 100

PARAM_MATPLOTLIB_FIG, PARAM_MATPLOTLIB_AX, PARAM_MATPLOTLIB_NEW_AFFICHAGE, PARAM_MATPLOTLIB_CARACTERES_3D, \
    PARAM_MATPLOTLIB_VITESSE_ROTATION, PARAM_MATPLOTLIB_HAUTEUR_Z_AXIS = list(range(6))
PARAM_MATPLOTLIB_TK_VAR_NB_JOURS, PARAM_MATPLOTLIB_NOM_DOSSIER, PARAM_MATPLOTLIB_PERIODE_IMAGE, \
    PARAM_TAILLE_MINIATURE, PARAM_COEF_TEMPERATURE_MINIATURE = list(range(5))

MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_TITLE = 4
MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_LEGENDE = 1.9
MATPLOTLIB_COEF_HEIGHT_FONT_SIZE_POINTS_3D = 4.5
MATPLOTLIB_COEF_HEIGHT_FONT_DIST_AXES_LABELS = 1.2

MATPLOTLIB_EVOLUTION_POPULATION_TITLE = "Evolution de la population"
MATPLOTLIB_GRAPH_3D_TITLE = "Evolution des caractères"
MATPLOTLIB_LEGENDE_EVOLUTION_POPULATION_TITLE = ["Nombre de naissances",
                                                 "Nombre d'individus gestants",
                                                 "Nombre d'individus féconds",
                                                 "Nombre d'individus non féconds",
                                                 "Nombre d'individus morts"]
MATPLOTLIB_LEGENDE_AXES_EVOLUTION_POPULATION = ["Nombre de jours", "Nombre d'individus"]
MATPLOTLIB_LEGENDE_GRAPH_3D = ["Individus non féconds",
                               "Nouveaux individus (naissance)",
                               "Individus féconds",
                               "Individus gestants"]
MATPLOTLIB_POSITION_LEGENDE_EVOLUTION_POPULATION = "upper left"
MATPLOTLIB_POSITION_LEGENDE_GRAPH_3D = "upper right"


# --------------------------------------- MOVIEPY ---------------------------------------
CHEMIN_SAUVEGARDE_VIDEO = "Videos"
FIGURE_NOM_DOSSIER = "Figure_"
SIMULATION_NOM_DOSSIER = "Simulation_"
FORMAT_IMAGES = ".png"
FORMAT_VIDEOS = ".mp4"
TK_FILESTYPES_BROWSE_SAVE_VIDEO = (("Fichiers vidéos MP4 (*.mp4)", "*.mp4*"), ("Tous les fichiers (*)", "*.*"))

LISTE_SIZE_ENREGISTREMENT = [ENR_AUTO, ENR_480P, ENR_720P, ENR_1080P] = range(4)

PARAM_ENR_SIZE = 0
PARAM_ENR_LABEL = 1

DIC_SIZE_ENREGISTREMENT = {
    ENR_480P: {
        PARAM_ENR_SIZE: (7.20, 4.80),
        PARAM_ENR_LABEL: "SD : 480p"
    },
    ENR_720P: {
        PARAM_ENR_SIZE: (12.80, 7.20),
        PARAM_ENR_LABEL: "HD : 720p"
    },
    ENR_1080P: {
        PARAM_ENR_SIZE: (19.20, 10.80),
        PARAM_ENR_LABEL: "Full HD : 1080p"
    },
    ENR_AUTO: {
        PARAM_ENR_SIZE: None,
        PARAM_ENR_LABEL: "Taille de la figure actuelle"
    }
}
SIZE_ENREGISTREMENT_DEFAULT = ENR_AUTO
