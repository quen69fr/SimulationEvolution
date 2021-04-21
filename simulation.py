# coding: utf-8

from environnement import *
from threading import Thread
import tkinter
from tkinter import messagebox, ttk, filedialog
import os
import moviepy.video.io.ImageSequenceClip as Movieclip
# import gc --> gc.collect()


def new_label_frame(master_frame, title: str, weight_rows: list, weight_columns: list):
    frame = tkinter.LabelFrame(master_frame,
                               text=title,
                               font=TK_FRAME_FONT)

    for row, weight in enumerate(weight_rows):
        frame.rowconfigure(row, weight=weight)

    for column, weight in enumerate(weight_columns):
        frame.columnconfigure(column, weight=weight)

    return frame


def new_top_frame(master_frame, size, caption, title, weight_rows: list, weight_columns: list):
    frame = tkinter.Toplevel(master_frame)
    frame.geometry(size)
    frame.title(caption)

    titre = tkinter.Label(frame,
                          text=title,
                          font=TK_TITLE_2_FONT)

    for row, weight in enumerate(weight_rows):
        frame.rowconfigure(row, weight=weight)

    for column, weight in enumerate(weight_columns):
        frame.columnconfigure(column, weight=weight)

    titre.grid(column=0, row=0, columnspan=len(weight_columns), sticky="nsew")

    return frame


def new_scale_config(master_frame, config, variable):
    return tkinter.Scale(master_frame,
                         orient="horizontal",
                         from_=DIC_CONFIGURATIONS[config][PARAM_MIN_VALUE],
                         to=DIC_CONFIGURATIONS[config][PARAM_MAX_VALUE],
                         resolution=DIC_CONFIGURATIONS[config][PARAM_STEP],
                         font=TK_LABEL_FONT,
                         label=DIC_CONFIGURATIONS[config][PARAM_LABEL],
                         variable=variable)


def new_config_label_frame(master_frame, dic_tkvar: dict, type_frame: int):
    liste_config = DIC_LABEL_FRAME_CONFIGURATIONS[type_frame][PARAM_LISTE_CONFIG]
    frame = new_label_frame(master_frame, DIC_LABEL_FRAME_CONFIGURATIONS[type_frame][PARAM_TITRE],
                            [1] * len(liste_config), [1])
    for i, config in enumerate(liste_config):
        if DIC_CONFIGURATIONS[config][PARAM_TYPE] == bool:
            check_button = tkinter.Checkbutton(frame,
                                               text=DIC_CONFIGURATIONS[config][PARAM_LABEL],
                                               font=TK_LABEL_FONT,
                                               variable=dic_tkvar[config])
            check_button.grid(row=i, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsw")
        else:
            scale = new_scale_config(frame, config, dic_tkvar[config])
            scale.grid(row=i, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
    return frame


def new_scale(master_frame, type_scale, variable):
    return tkinter.Scale(master_frame,
                         orient="horizontal",
                         from_=DIC_SCALE[type_scale][PARAM_MIN_VALUE],
                         to=DIC_SCALE[type_scale][PARAM_MAX_VALUE],
                         resolution=DIC_SCALE[type_scale][PARAM_STEP],
                         variable=variable,
                         font=TK_LABEL_FONT,
                         label=DIC_SCALE[type_scale][PARAM_LABEL])


def clear_images_moviepy(nom_dossier: str, nb_images):
    for i in range(1, nb_images + 2):
        chemin = f"{nom_dossier}/{i}{FORMAT_IMAGES}"
        if os.path.exists(chemin):
            os.remove(chemin)
    os.rmdir(nom_dossier)


class Simulation:
    def __init__(self):
        self.app = tkinter.Tk()
        self.num_simulation = 0
        self.environnement = None
        self.list_id_figs_matplotlib = []

        self.running_simu = False
        self.running_pygame = False
        self.running_matplotbil = False
        self.stop_enregistrement = tkinter.BooleanVar(self.app, value=False)
        self.tk_var_stop_init_new_environnement = None

        self.tk_valeurs_configurations = {conf: DIC_CONFIGURATIONS[conf][PARAM_DEFAULT_VALUE]
                                          for conf in LISTE_CONFIGS}

        self.tk_valeurs_caracteres_individus = {caractere: {param: DIC_CARACTERES_INDIVIDU[caractere][param]
                                                            for param in [PARAM_VALUE, PARAM_MIN_VALUE, PARAM_MAX_VALUE,
                                                                          PARAM_PROBA_MUTATION, PARAM_DEGRE_MUTATION,
                                                                          PARAM_ALEATOIRE]}
                                                for caractere in LISTE_CARACTERES_INDIVIDU}

        self.delay_simulation = tkinter.DoubleVar(value=DIC_SCALE[SCALE_SIMULATION_FPS][PARAM_DEFAULT_VALUE])
        self.var_fps_pygame = tkinter.IntVar(value=DIC_SCALE[SCALE_PYGAME_FPS][PARAM_DEFAULT_VALUE])
        self.var_fps_matplotlib = tkinter.IntVar(value=DIC_SCALE[SCALE_MATPLOTLIB_FPS][PARAM_DEFAULT_VALUE])

        self.tk_buttons_simulation = {}
        self.tk_buttons_pygame = {}
        self.tk_buttons_matplotbil = {}
        self.tk_nb_figs_matplotlib = tkinter.IntVar(self.app, 0)

        self.chemin_videos = ""

        self.init_tkinter_app()

        self.new_environnement({conf: self.tk_valeurs_configurations[conf] for conf in LISTE_CONFIGS_SIMULATION_ONLY},
                               self.tk_valeurs_caracteres_individus)

    # Tkinter
    def init_tkinter_app(self):
        self.app.geometry(TK_APP_SIZE)
        self.app.title(TK_CAPTION_TEXT)
        self.app.option_add("*TCombobox*Listbox.font", TK_LABEL_FONT)

        self.app.protocol("WM_DELETE_WINDOW", self.quitter)

        title = tkinter.Label(self.app,
                              text=TK_TITLE_TEXT,
                              font=TK_TITLE_FONT)

        simulation_frame = new_label_frame(self.app, TK_SIMULATION_TEXT, [1, 1, 1, 1], [1, 1])
        pygame_frame = new_label_frame(self.app, TK_PYGAME_TEXT, [1, 1], [1, 1])
        matplotlib_frame = new_label_frame(self.app, TK_MATPLOTLIB_TEXT, [1, 1, 1], [1, 1])

        def init_tkinter_simulation_frame():
            start_button = tkinter.Button(simulation_frame,
                                          text=TK_START_BUTTON_TEXT,
                                          font=TK_BUTTON_FONT,
                                          command=self.start_simulation)

            stop_button = tkinter.Button(simulation_frame,
                                         text=TK_STOP_BUTTON_TEXT,
                                         font=TK_BUTTON_FONT,
                                         command=self.stop_simulation,
                                         state="disabled")

            delay_scale = new_scale(simulation_frame, SCALE_SIMULATION_FPS, self.delay_simulation)

            # --------------------------------------------------------
            info_frame = new_label_frame(simulation_frame, "Informations", [1, 1], [1, 1, 1, 1])

            Stats.tk_jour = tkinter.IntVar()
            Stats.tk_nb_individus = tkinter.IntVar()
            Stats.tk_nb_jours_par_min = tkinter.DoubleVar()

            num_jour_label = tkinter.Label(info_frame,
                                           textvariable=Stats.tk_jour,
                                           width=4,
                                           anchor="w",
                                           font=TK_JOUR_LABEL_FONT)
            jour_label = tkinter.Label(info_frame,
                                       text=TK_JOUR_NUM_LABEL_TEXT,
                                       font=TK_JOUR_LABEL_FONT)
            jour_label.grid(row=0, column=0, rowspan=2, sticky="e")
            num_jour_label.grid(row=0, column=1, rowspan=2, sticky="ew")

            for j, (var, text) in enumerate([(Stats.tk_nb_individus, TK_LABEL_I_NB_INDIVIDUS),
                                             (Stats.tk_nb_jours_par_min, TK_LABEL_I_NB_JOURS_PAR_MIN)]):
                var_label = tkinter.Label(info_frame,
                                          width=4,
                                          anchor="e",
                                          textvariable=var,
                                          font=TK_LABEL_FONT)
                label = tkinter.Label(info_frame,
                                      text=text,
                                      font=TK_LABEL_FONT)
                var_label.grid(row=j, column=2, padx=TK_MARGE_WIDGET, sticky="ew")
                label.grid(row=j, column=3, sticky="w")
            # --------------------------------------------------------

            new_button = tkinter.Button(simulation_frame,
                                        text=TK_NEW_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=self.new_simulation_frame)

            # config_button = tkinter.Button(simulation_frame,
            #                                text=TK_CONFIG_BUTTON_TEXT,
            #                                font=TK_BUTTON_FONT,
            #                                command=self.configurations_button_action)

            new_button.grid(row=3, column=0, columnspan=4, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

            start_button.grid(row=0, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
            stop_button.grid(row=0, column=1, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
            delay_scale.grid(row=1, column=0, columnspan=2, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="ew")
            info_frame.grid(row=2, column=0, columnspan=2, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

            self.tk_buttons_simulation = {START_BUTTON: start_button,
                                          NEW_BUTTON: new_button,
                                          STOP_BUTTON: stop_button}

        def init_tkinter_pygame_frame():
            new_button = tkinter.Button(pygame_frame,
                                        text=TK_NEW_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=self.new_pygame_fame)

            stop_button = tkinter.Button(pygame_frame,
                                         text=TK_STOP_BUTTON_TEXT,
                                         font=TK_BUTTON_FONT,
                                         command=self.stop_pygame,
                                         state="disabled")

            delay_scale = new_scale(pygame_frame, SCALE_PYGAME_FPS, self.var_fps_pygame)

            new_button.grid(row=0, column=0, sticky="nsew", padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET)
            stop_button.grid(row=0, column=1, sticky="nsew", padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET)
            delay_scale.grid(row=1, column=0, columnspan=2, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="ew")

            self.tk_buttons_pygame = {NEW_BUTTON: new_button,
                                      STOP_BUTTON: stop_button}

        def init_tkinter_matplotlib_frame():
            start_button = tkinter.Button(matplotlib_frame,
                                          text=TK_NEW_BUTTON_TEXT,
                                          font=TK_BUTTON_FONT,
                                          command=self.new_matplotlib_fame)

            stop_button = tkinter.Button(matplotlib_frame,
                                         text=TK_STOP_BUTTON_TEXT,
                                         font=TK_BUTTON_FONT,
                                         command=self.stop_matplotlib,
                                         state="disabled")

            delay_scale = new_scale(matplotlib_frame, SCALE_MATPLOTLIB_FPS, self.var_fps_matplotlib)

            new_moviepy_button = tkinter.Button(matplotlib_frame,
                                                text=TK_NEW_MOVIEPY_BUTTON_TEXT,
                                                font=TK_BUTTON_FONT,
                                                command=self.new_moviepy_frame,
                                                state="disabled")

            start_button.grid(row=0, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
            stop_button.grid(row=0, column=1, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
            delay_scale.grid(row=1, column=0, columnspan=2, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="ew")
            new_moviepy_button.grid(row=2, column=0, columnspan=2, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET,
                                    sticky="nsew")

            self.tk_buttons_matplotbil = {START_BUTTON: start_button,
                                          STOP_BUTTON: stop_button,
                                          NEW_BUTTON: new_moviepy_button}

        init_tkinter_simulation_frame()
        init_tkinter_pygame_frame()
        init_tkinter_matplotlib_frame()

        button_quitter = tkinter.Button(self.app,
                                        text=TK_QUITTER_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=self.quitter)

        for i, weight in enumerate([1, 5]):
            self.app.columnconfigure(i, weight=weight)
        for i, weight in enumerate([1, 20, 19, 1]):
            self.app.rowconfigure(i, weight=weight)

        title.grid(row=0, column=0, columnspan=2, sticky="nsew")
        simulation_frame.grid(row=1, column=0, rowspan=2, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
        pygame_frame.grid(row=1, column=1, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
        matplotlib_frame.grid(row=2, column=1, rowspan=2, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
        button_quitter.grid(row=3, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

    def run(self):
        self.app.mainloop()

    def quitter(self):
        self.stop_simulation()
        self.stop_pygame()
        self.stop_matplotlib()

        message_confirmation = messagebox.askyesno(*TK_MESSAGE_BOX_QUITTER)
        if message_confirmation:
            self.stop_enregistrement.set(True)
            self.app.quit()
            self.app = None

    # Tkinter function : Pour les configurations => new_simulation_frame() et new_pygame_fame()
    def tk_conf_frame(self, master_frame, command_valider, list_configs: list, list_type_label_frame: list,
                      frame_size: str, title: str, buttons_frame_weights: list, configs_caracteres: bool = False,
                      button_master=None):
        dic_tkvar = {
            conf: tkinter.IntVar(value=self.tk_valeurs_configurations[conf])
            if DIC_CONFIGURATIONS[conf][PARAM_TYPE] == int
            else (tkinter.BooleanVar(value=self.tk_valeurs_configurations[conf])
                  if DIC_CONFIGURATIONS[conf][PARAM_TYPE] == bool
                  else tkinter.DoubleVar(value=self.tk_valeurs_configurations[conf]))
            for conf in list_configs}

        dic_tkvar_caractere = {}
        if configs_caracteres:
            dic_tkvar_caractere = {
                caractere: {
                    param: tkinter.IntVar(value=value) if DIC_CARACTERES_INDIVIDU[caractere][PARAM_TYPE] == int
                    else (tkinter.BooleanVar(value=value)
                          if param == PARAM_ALEATOIRE else tkinter.DoubleVar(value=value))
                    for param, value in dic_params.items()}
                for caractere, dic_params in self.tk_valeurs_caracteres_individus.items()}

        def command_button_valider():
            if check_value.get():
                for conf, var in dic_tkvar.items():
                    self.tk_valeurs_configurations[conf] = var.get()
                if configs_caracteres:
                    for car, dic in dic_tkvar_caractere.items():
                        for param, var in dic.items():
                            self.tk_valeurs_caracteres_individus[car][param] = var.get()
            if button_master is not None:
                button_master["state"] = "normal"
            frame.destroy()
            if configs_caracteres:
                command_valider({conf: var.get() for conf, var in dic_tkvar.items()},
                                {car: {conf: var.get() for conf, var in dic.items()}
                                 for car, dic in dic_tkvar_caractere.items()})
            else:
                command_valider({conf: var.get() for conf, var in dic_tkvar.items()})

        def command_button_reset():
            for conf, var in dic_tkvar.items():
                var.set(DIC_CONFIGURATIONS[conf][PARAM_DEFAULT_VALUE])
            if configs_caracteres:
                for car, dic in dic_tkvar_caractere.items():
                    for param, var in dic.items():
                        var.set(DIC_CARACTERES_INDIVIDU[car][param])

        def command_quitter():
            frame.destroy()
            if button_master is not None:
                button_master["state"] = "normal"

        if button_master is not None:
            button_master["state"] = "disabled"

        nb_rows = (4 + len(list_type_label_frame))
        frame = new_top_frame(master_frame, frame_size, TK_CAPTION_TEXT, title, [1] * nb_rows, [1, 1, 1])

        frame.protocol("WM_DELETE_WINDOW", command_quitter)

        for i, type_label_frame in enumerate(list_type_label_frame):
            label_frame = new_config_label_frame(frame, dic_tkvar, type_label_frame)
            label_frame.grid(row=1 + i, column=0, columnspan=3,
                             padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

        buttons_frame = new_label_frame(frame, TK_CONFIG_AVANCES_TEXT, *buttons_frame_weights)

        check_value = tkinter.BooleanVar()
        check_value.set(True)
        check_button = tkinter.Checkbutton(frame,
                                           text=TK_CHECKBUTTON_KEEP_CONF,
                                           font=TK_LABEL_FONT,
                                           variable=check_value)
        button_valider = tkinter.Button(frame,
                                        text=TK_VALIDER_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=command_button_valider)
        button_reset = tkinter.Button(frame,
                                      text=TK_RESET_BUTTON_TEXT,
                                      font=TK_BUTTON_FONT,
                                      command=command_button_reset)
        button_annuler = tkinter.Button(frame,
                                        text=TK_ANNULER_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=command_quitter)

        buttons_frame.grid(row=nb_rows - 3, column=0, columnspan=3, pady=TK_MARGE_WIDGET,
                           padx=TK_MARGE_WIDGET, sticky="nsew")
        check_button.grid(row=nb_rows - 2, column=0, columnspan=3, padx=TK_MARGE_WIDGET, sticky="nsw")
        button_annuler.grid(row=nb_rows - 1, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")
        button_reset.grid(row=nb_rows - 1, column=1, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")
        button_valider.grid(row=nb_rows - 1, column=2, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")

        if configs_caracteres:
            return buttons_frame, dic_tkvar, dic_tkvar_caractere
        return buttons_frame, dic_tkvar

    # Simulation
    def new_simulation_frame(self):
        avancees_frame_configurations, dic_tkvar, dic_tkvar_caracteres = \
            self.tk_conf_frame(self.app, self.new_simulation, LISTE_CONFIGS_SIMULATION_ONLY,
                               [FRAME_GENERAL, FRAME_DEPART], TK_CONFIG_FRAME_SIZE, TK_TITLE_CONF_TEXT,
                               [[1], [1, 1, 1]], True, self.tk_buttons_simulation[NEW_BUTTON])

        def fame_conf_avancees():
            def quitte_fame_conf_avancees():
                frame_conf_avancees.destroy()
                button_avancees["state"] = "normal"

            button_avancees["state"] = "disabled"
            frame_conf_avancees = new_top_frame(avancees_frame_configurations, TK_CONFIG_AVANCEES_FRAME_SIZE,
                                                TK_CAPTION_TEXT, TK_TITLE_CONF_TEXT, [1, 6], [1, 1, 1])

            frame_conf_avancees.protocol("WM_DELETE_WINDOW", quitte_fame_conf_avancees)

            for i, type_frame in enumerate([FRAME_AVANCEES_CARTE,
                                            FRAME_AVANCEES_CARTE_ALTITUDES,
                                            FRAME_AVANCEES_NOURRITURE]):
                label_frame = new_config_label_frame(frame_conf_avancees, dic_tkvar, type_frame)
                label_frame.grid(column=i, row=1, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

        def fame_conf_caracteres():
            def quitte_fame_conf_avancees():
                frame_conf_caractere.destroy()
                button_caracteres["state"] = "normal"

            button_caracteres["state"] = "disabled"
            frame_conf_caractere = new_top_frame(avancees_frame_configurations, TK_CONFIG_CARACTERES_FRAME_SIZE,
                                                 TK_CAPTION_TEXT, TK_TITLE_CONF_TEXT, [1, 6],
                                                 [1] * len(LISTE_PARAM_CARACTERES_INDIVIDUS_TITLE))

            frame_conf_caractere.protocol("WM_DELETE_WINDOW", quitte_fame_conf_avancees)

            for i, (param, title) in enumerate(LISTE_PARAM_CARACTERES_INDIVIDUS_TITLE):
                if param == PARAM_VALUE:
                    frame = new_label_frame(frame_conf_caractere, title, [1] * len(LISTE_CARACTERES_INDIVIDU), [1, 2])
                else:
                    frame = new_label_frame(frame_conf_caractere, title, [1] * len(LISTE_CARACTERES_INDIVIDU), [1])
                for j, caractere in enumerate(LISTE_CARACTERES_INDIVIDU):
                    if param == PARAM_LABEL:
                        label = tkinter.Label(frame,
                                              text=DIC_CARACTERES_INDIVIDU[caractere][PARAM_LABEL],
                                              font=TK_LABEL_FONT)
                        label.grid(column=0, row=j)
                    else:
                        if param in [PARAM_VALUE, PARAM_MIN_VALUE, PARAM_MAX_VALUE]:
                            from_ = DIC_CARACTERES_INDIVIDU[caractere][PARAM_MIN_VALUE]
                            to = DIC_CARACTERES_INDIVIDU[caractere][PARAM_MAX_VALUE]
                            resolution = DIC_CARACTERES_INDIVIDU[caractere][PARAM_STEP]
                        elif param == PARAM_DEGRE_MUTATION:
                            from_ = DIC_CARACTERES_INDIVIDU[caractere][PARAM_DEGRE_MUTATION_MIN]
                            to = DIC_CARACTERES_INDIVIDU[caractere][PARAM_DEGRE_MUTATION_MAX]
                            resolution = DIC_CARACTERES_INDIVIDU[caractere][PARAM_DEGRE_MUTATION_STEP]
                        else:
                            from_ = PROBA_MUTATION_MIN
                            to = PROBA_MUTATION_MAX
                            resolution = PROBA_MUTATION_STEP
                        scale = tkinter.Scale(frame,
                                              orient="horizontal",
                                              from_=from_,
                                              to=to,
                                              resolution=resolution,
                                              font=TK_LABEL_FONT,
                                              variable=dic_tkvar_caracteres[caractere][param])
                        if param == PARAM_VALUE:
                            checkbutton = tkinter.Checkbutton(frame,
                                                              variable=dic_tkvar_caracteres[caractere][PARAM_ALEATOIRE])
                            checkbutton.grid(column=0, row=j, padx=TK_MARGE_WIDGET // 2, pady=TK_MARGE_WIDGET,
                                             sticky="nsew")
                            scale.grid(column=1, row=j, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
                        else:
                            scale.grid(column=0, row=j, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
                frame.grid(column=i, row=1, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

        def fame_conf_individu():
            def quitte_fame_conf_avancees():
                frame_conf_individus.destroy()
                button_individus["state"] = "normal"

            button_individus["state"] = "disabled"
            frame_conf_individus = new_top_frame(avancees_frame_configurations, TK_CONFIG_INDIVIDUS_FRAME_SIZE,
                                                 TK_CAPTION_TEXT, TK_TITLE_CONF_TEXT, [1, 6], [1])

            frame_conf_individus.protocol("WM_DELETE_WINDOW", quitte_fame_conf_avancees)

            label_frame = new_config_label_frame(frame_conf_individus, dic_tkvar, FRAME_AVANCEES_INDIVIDUS)
            label_frame.grid(column=0, row=1, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

        button_avancees = tkinter.Button(avancees_frame_configurations,
                                         text=TK_CONFIG_AVANCEES_BUTTON_TEXT,
                                         font=TK_BUTTON_FONT,
                                         command=fame_conf_avancees)
        button_individus = tkinter.Button(avancees_frame_configurations,
                                          text=TK_CONFIG_INDIVIDUS_BUTTON_TEXT,
                                          font=TK_BUTTON_FONT,
                                          command=fame_conf_individu)
        button_caracteres = tkinter.Button(avancees_frame_configurations,
                                           text=TK_CONFIG_CARACTERE_BUTTON_TEXT,
                                           font=TK_BUTTON_FONT,
                                           command=fame_conf_caracteres)

        button_avancees.grid(column=0, row=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
        button_individus.grid(column=1, row=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
        button_caracteres.grid(column=2, row=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

    def new_simulation(self, dic_configurations: dict, dic_conf_caracteres: dict):
        self.stop_simulation()
        self.stop_pygame()
        self.stop_matplotlib()

        message_confirmation = messagebox.askyesno(*TK_MESSAGE_BOX_NOUVEAU)
        if message_confirmation:
            thread_new_environnement = Thread(target=self.new_environnement, args=[dic_configurations,
                                                                                   dic_conf_caracteres])
            thread_new_environnement.start()

    def start_simulation(self):
        if not self.running_simu:
            self.running_simu = True
            thread_simu = Thread(target=self.run_simulation)
            thread_simu.start()
        self.tk_buttons_simulation[START_BUTTON]["state"] = "disabled"
        self.tk_buttons_simulation[STOP_BUTTON]["state"] = "normal"

    def stop_simulation(self):
        if self.tk_var_stop_init_new_environnement is not None:
            self.tk_var_stop_init_new_environnement.set(True)
        if self.running_simu:
            self.running_simu = False
        self.tk_buttons_simulation[START_BUTTON]["state"] = "normal"
        self.tk_buttons_simulation[STOP_BUTTON]["state"] = "disabled"

    # Pygame
    def new_pygame_fame(self):
        avancees_frame_new_pygame, dic_tkvar = self.tk_conf_frame(self.app, self.new_pygame, LISTE_CONFIGS_PYGAME_ONLY,
                                                                  [FRAME_PYGAME_GENERAL], TK_PYGAME_FRAME_SIZE,
                                                                  TK_TITLE_PYGAME_TEXT, [[1], [1]],
                                                                  button_master=self.tk_buttons_pygame[NEW_BUTTON])

        def pygame_fame_conf_avancees():
            def quitte_fame_conf_avancees():
                frame_new_pygame_avancees.destroy()
                button_avancees["state"] = "normal"

            button_avancees["state"] = "disabled"
            frame_new_pygame_avancees = new_top_frame(avancees_frame_new_pygame, TK_PYGAME_FRAME_AVANCEE_SIZE,
                                                      TK_CAPTION_TEXT, TK_TITLE_PYGAME_TEXT, [1, 1], [1])

            frame_new_pygame_avancees.protocol("WM_DELETE_WINDOW", quitte_fame_conf_avancees)

            avancees_frame = new_config_label_frame(frame_new_pygame_avancees, dic_tkvar, FRAME_PYGAME_AVANCEES)
            avancees_frame.grid(row=1, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

        button_avancees = tkinter.Button(avancees_frame_new_pygame,
                                         text=TK_CONFIG_AVANCEES_BUTTON_TEXT,
                                         font=TK_BUTTON_FONT,
                                         command=pygame_fame_conf_avancees)
        button_avancees.grid(row=2, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")

    def new_pygame(self, dic_configurations):
        if not self.running_pygame:
            self.running_pygame = True
            thread_pygame = Thread(target=self.run_affichage_pygame, args=[dic_configurations])
            thread_pygame.start()
        self.tk_buttons_pygame[NEW_BUTTON]["state"] = "disabled"
        self.tk_buttons_pygame[STOP_BUTTON]["state"] = "normal"

    def stop_pygame(self):
        if self.running_pygame:
            self.running_pygame = False
        self.tk_buttons_pygame[NEW_BUTTON]["state"] = "normal"
        self.tk_buttons_pygame[STOP_BUTTON]["state"] = "disabled"

    # Matplotlib
    def new_matplotlib_fame(self):
        def observeur_radiobutton_graph(*_):
            if var_graph.get():
                for child in frame_3D.winfo_children():
                    child.configure(state="disable")
            else:
                for child in frame_3D.winfo_children():
                    if child.winfo_class() == "TCombobox":
                        child.configure(state="readonly")
                    else:
                        child.configure(state="normal")

        def command_button_valider():
            self.new_matplotlib(var_graph.get(),
                                [(LISTE_CARACTERES_INDIVIDU + LISTE_CARACTERES_INDIVIDU_SECONDAIRES)[ld.current()]
                                 for ld in liste_listes_deroulantes], tk_var_vitesse_rotation.get(),
                                tk_var_hauteur_z.get())
            frame_new_matplotlib.destroy()

        frame_new_matplotlib = new_top_frame(self.app, TK_MATPLOTLIB_FRAME_SIZE, TK_CAPTION_TEXT, TK_TITLE_MATPLOT_TEXT,
                                             [1, 1, 1, 1], [1, 1, 1])

        frame_new_matplotlib.protocol("WM_DELETE_WINDOW", frame_new_matplotlib.destroy)

        var_graph = tkinter.BooleanVar(frame_new_matplotlib, value=False)
        var_graph.trace("w", observeur_radiobutton_graph)
        graph_pop = tkinter.Radiobutton(frame_new_matplotlib,
                                        text=TK_MATPLOT_RADIOBUTTON_POPULATION_TEXT,
                                        font=TK_LABEL_FONT,
                                        value=True,
                                        variable=var_graph)
        graph_3D = tkinter.Radiobutton(frame_new_matplotlib,
                                       text=TK_MATPLOT_RADIOBUTTON_3D_TEXT,
                                       font=TK_LABEL_FONT,
                                       value=False,
                                       variable=var_graph)
        button_valider = tkinter.Button(frame_new_matplotlib,
                                        text=TK_VALIDER_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=command_button_valider)
        button_annuler = tkinter.Button(frame_new_matplotlib,
                                        text=TK_ANNULER_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=frame_new_matplotlib.destroy)

        frame_3D = new_label_frame(frame_new_matplotlib, "", [1] * 5, [1, 1])
        list_caracteres = [DIC_CARACTERES_INDIVIDU[caractere][PARAM_LABEL]
                           for caractere in LISTE_CARACTERES_INDIVIDU + LISTE_CARACTERES_INDIVIDU_SECONDAIRES]
        liste_listes_deroulantes = []
        for i, title in enumerate(TK_LABELS_MATPLOT_AXES):
            text_label = tkinter.Label(frame_3D,
                                       text=title,
                                       font=TK_LABEL_FONT)
            text_label.grid(row=i,
                            column=0,
                            sticky="nsew")
            liste_deroulante = ttk.Combobox(frame_3D,
                                            values=list_caracteres,
                                            state="readonly",
                                            font=TK_LABEL_FONT)
            liste_deroulante.current(i)
            liste_deroulante.grid(row=i, column=1, sticky="nsew", pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET)
            liste_listes_deroulantes.append(liste_deroulante)

        tk_var_vitesse_rotation = tkinter.DoubleVar(frame_3D)
        tk_var_hauteur_z = tkinter.IntVar(frame_3D)

        for row, variable, type_scale in [(3, tk_var_vitesse_rotation, SCALE_MATPLOTLIB_3D_VITESSE_ROTATION),
                                          (4, tk_var_hauteur_z, SCALE_MATPLOTLIB_3D_HAUTEUR_Z)]:
            scale = new_scale(frame_3D, type_scale, variable)
            variable.set(DIC_SCALE[type_scale][PARAM_DEFAULT_VALUE])
            scale.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=TK_MARGE_WIDGET)

        graph_pop.grid(row=1, column=0, columnspan=3, sticky="nsw", pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET)
        graph_3D.grid(row=2, column=0, sticky="nw", pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET)
        button_annuler.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET)
        button_valider.grid(row=3, column=2, sticky="nsew", pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET)

        frame_3D.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET)

        var_graph.set(True)

    def new_matplotlib(self, graph: bool, caractere_3D: list, vitesse_rotate: float, hauteur_z: int):
        if not self.running_matplotbil:
            self.running_matplotbil = True
        thread_matplotbil = Thread(target=self.run_graphs_matplotlib,
                                   args=[graph, caractere_3D, vitesse_rotate, hauteur_z])
        thread_matplotbil.start()
        self.tk_buttons_matplotbil[STOP_BUTTON]["state"] = "normal"
        self.tk_buttons_matplotbil[NEW_BUTTON]["state"] = "normal"

    def stop_matplotlib(self):
        if self.running_matplotbil:
            self.running_matplotbil = False
        self.tk_buttons_matplotbil[STOP_BUTTON]["state"] = "disabled"
        self.tk_buttons_matplotbil[NEW_BUTTON]["state"] = "disabled"

    # Moviepy
    def new_moviepy_frame(self):
        id_dossier_fig = []

        def liste_figures_matplotlib():
            return [f"Figure {id_f}" for id_f in self.list_id_figs_matplotlib]

        def observeur_nb_figures_matplotlib(*_):
            liste = liste_figures_matplotlib()
            if len(liste) == 0:
                quitter()
            else:
                liste_deroulante["values"] = liste

        def observeur_nb_jours(*_):
            label_nb_images["text"] = TK_LABEL_MOVIEPY_NB_IMAGES + str(var_nb_jours.get())
            label_duree["text"] = (TK_LABEL_MOVIEPY_DUREE_ENREGISTREMENT[0] +
                                   str(round(var_nb_jours.get() / tk_fps_moviepy.get(), 2)) +
                                   TK_LABEL_MOVIEPY_DUREE_ENREGISTREMENT[1])
            button_sss["state"] = "normal"

        def observateur_affiche_miniature(*_):
            if tk_affiche_miniature.get():
                scale_size_miniature["state"] = "normal"
                scale_coef_froid["state"] = "normal"
            else:
                scale_size_miniature["state"] = "disabled"
                scale_coef_froid["state"] = "disabled"

        def command_button_sss():
            if len(id_dossier_fig) == 0:
                for child in frame_images.winfo_children():
                    if child in [frame_radiobuttons, frame_miniature]:
                        for child_child in child.winfo_children():
                            child_child.configure(state="disable")
                    else:
                        child.configure(state="disable")
                button_sss.config(text=TK_STOP_BUTTON_TEXT, state="disabled")
                self.tk_nb_figs_matplotlib.trace_remove("write", cbname_observeur)
                tk_affiche_miniature.trace_remove("write", cbname_observeur_miniature)
                id_fig = self.new_moviepy(self.list_id_figs_matplotlib[liste_deroulante.current()],
                                          tk_periode_image.get(), var_nb_jours, tk_resolution.get(),
                                          tk_affiche_miniature.get(), scale_size_miniature.get(),
                                          scale_coef_froid.get())
                id_dossier_fig.append(id_fig)
            elif len(id_dossier_fig) == 1:
                nom_dossier = self.stop_moviepy(id_dossier_fig[0])
                button_sss["text"] = TK_SAUVER_BUTTON_TEXT
                id_dossier_fig.append(nom_dossier)
            else:
                nom_fichier = id_dossier_fig[1].split("/")[-1]
                emplacement_fichier_mp3 = filedialog.asksaveasfile(parent=frame_new_moviepy,
                                                                   defaultextension=FORMAT_VIDEOS,
                                                                   initialdir=id_dossier_fig[1][:-len(nom_fichier)],
                                                                   initialfile=f"{nom_fichier}{FORMAT_VIDEOS}",
                                                                   title=TK_TITLE_MOVIEPY_ENREGISTREMENT_BROWSE_TEXT,
                                                                   filetypes=TK_FILESTYPES_BROWSE_SAVE_VIDEO)

                if emplacement_fichier_mp3 is not None:
                    thread_save_moviepy = Thread(target=self.save_moviepy, args=[emplacement_fichier_mp3.name,
                                                                                 id_dossier_fig[1],
                                                                                 tk_fps_moviepy.get(),
                                                                                 var_nb_jours.get(),
                                                                                 keep_images.get()])
                    thread_save_moviepy.start()
                    frame_new_moviepy.destroy()
                    self.stop_enregistrement.trace_remove("write", observeur_stop_enregistrement)

        def stop_enregistrement(*_):
            if self.stop_enregistrement.get():
                quitter(True)

        def quitter(forcer=False):
            if len(id_dossier_fig) == 0:
                frame_new_moviepy.destroy()
                self.tk_nb_figs_matplotlib.trace_remove("write", cbname_observeur)
                self.stop_enregistrement.trace_remove("write", observeur_stop_enregistrement)
            else:
                stop = False
                if forcer:
                    stop = True
                else:
                    message_confirmation = messagebox.askyesno(*TK_MESSAGE_BOX_ENREGISTEMENT, parent=frame_new_moviepy)
                    if message_confirmation:
                        stop = True
                if stop:
                    if len(id_dossier_fig) == 1:
                        nom_dossier = self.stop_moviepy(id_dossier_fig[0])
                        clear_images_moviepy(nom_dossier, var_nb_jours.get())
                    elif len(id_dossier_fig) == 2:
                        clear_images_moviepy(id_dossier_fig[1], var_nb_jours.get())
                    frame_new_moviepy.destroy()
                    self.stop_enregistrement.trace_remove("write", observeur_stop_enregistrement)

        frame_new_moviepy = new_top_frame(self.app, TK_MOVIEPY_FRAME_SIZE, TK_CAPTION_TEXT, TK_TITLE_MOVIEPY_TEXT,
                                          [1] * 5, [1, 1])

        cbname_observeur = self.tk_nb_figs_matplotlib.trace_add("write", observeur_nb_figures_matplotlib)
        observeur_stop_enregistrement = self.stop_enregistrement.trace_add("write", stop_enregistrement)

        frame_new_moviepy.protocol("WM_DELETE_WINDOW", quitter)

        tk_fps_moviepy = tkinter.IntVar(frame_new_moviepy, DIC_SCALE[SCALE_MOVIEPY_FPS][PARAM_DEFAULT_VALUE])
        keep_images = tkinter.BooleanVar(frame_new_moviepy, False)
        var_nb_jours = tkinter.IntVar(frame_new_moviepy, -1)

        button_sss = tkinter.Button(frame_new_moviepy,
                                    text=TK_VALIDER_BUTTON_TEXT,
                                    font=TK_BUTTON_FONT,
                                    command=command_button_sss)

        tk_fps_moviepy.trace_add("write", observeur_nb_jours)
        var_nb_jours.trace_add("write", observeur_nb_jours)

        # --------------------------------------------------------
        frame_images = new_label_frame(frame_new_moviepy, TK_LISTE_TITLE_MOVIEPY_FRAMES_TEXT[0], [1, 1, 1], [1, 1])
        tk_periode_image = tkinter.IntVar(frame_images, DIC_SCALE[SCALE_MOVIEPY_PERIODE][PARAM_DEFAULT_VALUE])
        tk_resolution = tkinter.IntVar(frame_images)
        liste_deroulante = ttk.Combobox(frame_images,
                                        values=liste_figures_matplotlib(),
                                        state="readonly",
                                        font=TK_LABEL_FONT)
        liste_deroulante.current(0)
        periode_scale = new_scale(frame_images, SCALE_MOVIEPY_PERIODE, tk_periode_image)

        frame_radiobuttons = new_label_frame(frame_images, TK_LISTE_TITLE_MOVIEPY_FRAMES_TEXT[1],
                                             [1] * len(LISTE_SIZE_ENREGISTREMENT), [1])
        liste_radiobuttons = []
        for type_size in LISTE_SIZE_ENREGISTREMENT:
            liste_radiobuttons.append(tkinter.Radiobutton(frame_radiobuttons,
                                                          text=DIC_SIZE_ENREGISTREMENT[type_size][PARAM_ENR_LABEL],
                                                          font=TK_LABEL_FONT,
                                                          value=type_size,
                                                          variable=tk_resolution))
        frame_miniature = new_label_frame(frame_images, TK_LISTE_TITLE_MOVIEPY_FRAMES_TEXT[2], [1, 1, 1], [1])
        tk_affiche_miniature = tkinter.BooleanVar(frame_miniature, True)
        cbname_observeur_miniature = tk_affiche_miniature.trace_add("write", observateur_affiche_miniature)
        check_button_miniature = tkinter.Checkbutton(frame_miniature,
                                                     text=TK_CHECKBUTTON_MOVIEPY_AFFICHER_MINIATURE,
                                                     font=TK_LABEL_FONT,
                                                     variable=tk_affiche_miniature)
        scale_size_miniature = \
            new_scale(frame_miniature, SCALE_MOVIEPY_SIZE_MINIATURE,
                      tkinter.DoubleVar(frame_miniature,
                                        value=DIC_SCALE[SCALE_MOVIEPY_SIZE_MINIATURE][PARAM_DEFAULT_VALUE]))
        scale_coef_froid = \
            new_scale_config(frame_miniature, COEF_AFFICHAGE_ENERGIE_DEPENSEE,
                             tkinter.DoubleVar(frame_miniature, value=DIC_CONFIGURATIONS[
                                 COEF_AFFICHAGE_ENERGIE_DEPENSEE][PARAM_DEFAULT_VALUE]))

        check_button_miniature.grid(row=0, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsw")
        scale_size_miniature.grid(row=1, column=0, padx=TK_MARGE_WIDGET, sticky="nsew")
        scale_coef_froid.grid(row=2, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")

        liste_deroulante.grid(row=0, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="sew")
        periode_scale.grid(row=2, column=0, columnspan=2, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")
        frame_radiobuttons.grid(row=1, column=0, padx=TK_MARGE_WIDGET, pady=TK_MARGE_WIDGET, sticky="nsew")
        for i, radiobutton in enumerate(liste_radiobuttons):
            radiobutton.grid(row=i, column=0, padx=TK_MARGE_WIDGET, sticky="nsw")
        frame_miniature.grid(row=0, column=1, rowspan=2, padx=TK_MARGE_WIDGET, sticky="nsew")

        tk_resolution.set(SIZE_ENREGISTREMENT_DEFAULT)

        # --------------------------------------------------------
        frame_videos = new_label_frame(frame_new_moviepy, TK_LISTE_TITLE_MOVIEPY_FRAMES_TEXT[3], [1] * 3, [1])
        label_nb_images = tkinter.Label(frame_videos,
                                        font=TK_LABEL_FONT)
        fps_scale = new_scale(frame_videos, SCALE_MOVIEPY_FPS, tk_fps_moviepy)
        label_duree = tkinter.Label(frame_videos,
                                    font=TK_LABEL_FONT)
        var_nb_jours.set(0)
        label_nb_images.grid(row=0, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsw")
        fps_scale.grid(row=1, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")
        label_duree.grid(row=2, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsw")

        # --------------------------------------------------------
        check_button = tkinter.Checkbutton(frame_new_moviepy,
                                           text=TK_CHECKBUTTON_ENR_KEEP_IMAGES,
                                           font=TK_LABEL_FONT,
                                           variable=keep_images)
        button_annuler = tkinter.Button(frame_new_moviepy,
                                        text=TK_ANNULER_BUTTON_TEXT,
                                        font=TK_BUTTON_FONT,
                                        command=quitter)

        frame_images.grid(row=1, column=0, columnspan=2, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")
        frame_videos.grid(row=2, column=0, columnspan=2, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")
        check_button.grid(row=3, column=0, columnspan=2, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsw")
        button_sss.grid(row=4, column=1, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")
        button_annuler.grid(row=4, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")

    def init_chemins_videos(self):
        self.chemin_videos = f"{CHEMIN_SAUVEGARDE_VIDEO}"

        if not os.path.exists(self.chemin_videos):
            os.makedirs(self.chemin_videos)

        while os.path.exists(self.chemin_videos):
            self.num_simulation += 1
            self.chemin_videos = f"{CHEMIN_SAUVEGARDE_VIDEO}/{SIMULATION_NOM_DOSSIER}{self.num_simulation}"
        os.makedirs(self.chemin_videos)

    def new_moviepy(self, id_fig: int, periode: int, var_nb_jours: tkinter.IntVar, type_resolution: int,
                    afficher_miniature, taille_miniature, coef_temperature_miniature):
        if self.chemin_videos == "":
            self.init_chemins_videos()
        nom_dossier = f"{self.chemin_videos}/{FIGURE_NOM_DOSSIER}{id_fig}"
        n = 1
        while os.path.exists(nom_dossier) or os.path.exists(f"{os.path.exists(nom_dossier)}{FORMAT_VIDEOS}"):
            n += 1
            nom_dossier = f"{self.chemin_videos}/{FIGURE_NOM_DOSSIER}{id_fig}_{n}"
        os.makedirs(nom_dossier)
        return self.environnement.stats.new_enregistrement(id_fig, var_nb_jours, nom_dossier, periode, type_resolution,
                                                           afficher_miniature, taille_miniature,
                                                           coef_temperature_miniature)

    def stop_moviepy(self, id_fig: int):
        nom_dossier = self.environnement.stats.dic_figures_enregistrement[id_fig][PARAM_MATPLOTLIB_NOM_DOSSIER]
        del self.environnement.stats.dic_id_figs[id_fig]
        del self.environnement.stats.dic_figures_enregistrement[id_fig]
        return nom_dossier

    # Threading
    def new_environnement(self, dic_configurations: dict, dic_conf_caracteres: dict):
        tk_var_stop_init_new_environnement = tkinter.BooleanVar(self.app, value=False)
        self.tk_var_stop_init_new_environnement = tk_var_stop_init_new_environnement
        self.stop_enregistrement.set(True)
        self.tk_buttons_simulation[START_BUTTON].config(text=TK_START_BUTTON_PLEASE_WAIT_TEXT, state="disabled")
        self.tk_buttons_simulation[STOP_BUTTON]["state"] = "normal"
        self.tk_buttons_pygame[NEW_BUTTON]["state"] = "disabled"
        self.tk_buttons_matplotbil[START_BUTTON]["state"] = "disabled"

        def observateur_avancement(*_):
            self.tk_buttons_simulation[START_BUTTON]["text"] = f"{int(100 * tk_var_avancement.get())} %"

        tk_var_avancement = tkinter.DoubleVar(self.app, value=0.)
        cbname_observeur_avancement = tk_var_avancement.trace_add("write", observateur_avancement)

        environnement = Environnement(dic_configurations, dic_conf_caracteres, tk_var_stop_init_new_environnement,
                                      tk_var_avancement)

        tk_var_avancement.trace_remove("write", cbname_observeur_avancement)
        if self.tk_var_stop_init_new_environnement == tk_var_stop_init_new_environnement:
            self.tk_var_stop_init_new_environnement = None
            if environnement.init_terminee:
                self.environnement = environnement
            self.stop_enregistrement.set(False)
            self.tk_buttons_simulation[START_BUTTON].config(text=TK_START_BUTTON_TEXT, state="normal")
            self.tk_buttons_simulation[STOP_BUTTON]["state"] = "disabled"
            self.tk_buttons_pygame[NEW_BUTTON]["state"] = "normal"
            self.tk_buttons_matplotbil[START_BUTTON]["state"] = "normal"

    def save_moviepy(self, emplacement_fichier_mp3, nom_dossier: str, fps: int, nb_images: int, keep_images: bool):
        frame_saving = new_top_frame(self.app, TK_MOVIEPY_ENREGISTREMENT_FRAME_SIZE, TK_CAPTION_TEXT,
                                     TK_TITLE_MOVIEPY_ENREGISTREMENT_TEXT, [1, 1], [1])
        text = tkinter.Label(frame_saving,
                             text=emplacement_fichier_mp3,
                             font=TK_LABEL_FONT)
        text.grid(row=1, column=0, pady=TK_MARGE_WIDGET, padx=TK_MARGE_WIDGET, sticky="nsew")

        frame_saving.protocol("WM_DELETE_WINDOW", lambda *_: None)

        # os.remove(emplacement_fichier_mp3)
        clip = Movieclip.ImageSequenceClip([f"{nom_dossier}/{i}{FORMAT_IMAGES}" for i in range(1, nb_images + 1)
                                            if os.path.exists(f"{nom_dossier}/{i}{FORMAT_IMAGES}")],
                                           fps=fps)
        clip.write_videofile(emplacement_fichier_mp3, verbose=False, logger=None, audio=False)

        if not keep_images:
            clear_images_moviepy(nom_dossier, nb_images)

        frame_saving.destroy()

    def run_simulation(self):
        while self.running_simu:
            self.environnement.update()
            time.sleep(self.delay_simulation.get())

    def run_affichage_pygame(self, dic_configurations):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        if dic_configurations[PLEIN_ECRAN]:
            screen = pygame.display.set_mode((dic_configurations[LARGEUR_ECRAN],
                                              dic_configurations[HAUTEUR_ECRAN]), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((dic_configurations[LARGEUR_ECRAN],
                                              dic_configurations[HAUTEUR_ECRAN]))
        self.environnement.init_pygame(dic_configurations)

        while self.running_pygame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_pygame()
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.environnement.gere_clic(*pygame.mouse.get_pos())
                    elif event.button == 4:
                        self.environnement.gere_zoom(True, *pygame.mouse.get_pos())
                    elif event.button == 5:
                        self.environnement.gere_zoom(False, *pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEMOTION:
                    self.environnement.gere_deplacement_souris(*pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop_pygame()
                        break

            try:
                self.environnement.affiche(screen)
            except:
                print("Oups !")

            pygame.display.update()
            pygame.time.Clock().tick(self.var_fps_pygame.get())

        self.environnement.carte.ecran = None
        pygame.quit()
        return

    def run_graphs_matplotlib(self, garph: bool, caractere_3D: list = None, vitesse_rotate=None, hauteur_z=None):
        if garph:
            caractere_3D = None

        plt.ion()

        id_fig = self.environnement.stats.init_graph_matplotlib(caractere_3D, vitesse_rotate, hauteur_z)

        self.list_id_figs_matplotlib.append(id_fig)
        self.tk_nb_figs_matplotlib.set(self.tk_nb_figs_matplotlib.get() + 1)

        while self.running_matplotbil:
            self.environnement.stats.update_graph_matplotlib(id_fig)
            self.environnement.stats.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].canvas.draw_idle()
            try:
                self.environnement.stats.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].canvas.flush_events()
            except tkinter.TclError:
                if len(self.list_id_figs_matplotlib) == 1:
                    self.stop_matplotlib()
                break
            time.sleep(1 / self.var_fps_matplotlib.get())

        plt.close(id_fig)

        # C'est pas très propre (pas du tout !) mais ça marche...
        try:
            self.environnement.stats.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].canvas.draw_idle()
            self.environnement.stats.dic_id_figs[id_fig][PARAM_MATPLOTLIB_FIG].canvas.flush_events()
        except tkinter.TclError:
            pass  # Ca devrait tout le temps faire cette erreur et arrêter je ne sais quoi de Matplotlib...

        del self.environnement.stats.dic_id_figs[id_fig]
        self.list_id_figs_matplotlib.remove(id_fig)
        self.tk_nb_figs_matplotlib.set(self.tk_nb_figs_matplotlib.get() - 1)
        return
