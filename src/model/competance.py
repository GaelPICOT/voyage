#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la gestion des compétance.

    :platform: Unix, Windows
    :synopsis: gestion des compétance

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import model.observer as obs


class Experience(object):
    """ représente l'expérience gagné dans une caractéristique ou une
    compétance.
    """
    def __init__(self, element, xp_tab):
        """ initialization

        :param element: élément à augmenté (caractéristique ou compétance)
        """
        self._element = element
        self._xp_tab = xp_tab
        self._valeur = 0

    def __iadd__(self, valeur):
        """ incrémente la valeur
        """
        self._valeur += valeur
        while (self._valeur >= self._xp_tab[int(self._element)+1]):
            self._valeur -= self._xp_tab[int(self._element)+1]
            self._element.valeur = self._element.valeur + 1
        return self

    def __int__(self):
        """ retourn la valeur
        """
        return self._valeur

    @property
    def valeur(self):
        self._valeur


class XpTab(object):
    """ list de valeur pour l'augmentation par l'expérience
    """
    def __init__(self, base_list, evolution_func):
        """ initialization

        :param base_list: list d'évolution basique
        :param evolution_fun: fonction pour le calcul des element exterieur
        """
        self._base_list = base_list
        self._evolution_func = evolution_func

    def __getitem__(self, key):
        if key in list(self._base_list.keys()):
            return self._base_list[key]
        else:
            return self._evolution_func(key)


class OptionEvolutive(object):
    """ représente tout option pouvant évoluer avec l'expertience
    """

    def __init__(self, name, valeur=10, max_=None, experience=None):
        """ initialization
        """
        self.value_changed = obs.Observable()
        #: nom de l'option
        self._name = name
        #: valeur de la option
        self._valeur = valeur
        #: expérinece dans la option
        if experience is None:
            self._exp = Experience(self, self.xp_tab)
        else:
            self._exp = experience
        #: si l'option à une limite
        self._max = max_

    def __int__(self):
        return self._valeur

    def __iadd__(self, valeur):
        self._valeur += valeur
        self.value_changed.emit(self._name)
        return self

    def __add__(self, valeur):
        return self._valeur + valeur

    @property
    def valeur(self):
        return self._valeur

    @valeur.setter
    def valeur(self, valeur):
        if self._max is not None:
            if valeur <= self._max:
                self._valeur = valeur
        else:
            self._valeur = valeur
        self.value_changed.emit(self._name)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        if self.valeur > value:
            self.valeur = value
        self._max = value

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, exp):
        self._exp = exp


class Caracteristique(OptionEvolutive):
    """ représente une caracteristique
    """

    base_tab = {7: 6, 8: 6, 9: 7, 10: 7, 11: 8, 12: 8, 13: 9, 14: 9, 15: 10,
                16: 20}

    xp_tab = XpTab(base_tab, lambda x: (x - 14) * 10)

    def __init__(self, name, valeur=10, max_=None, experience=None):
        """ initialization
        """
        OptionEvolutive.__init__(self, name, valeur, max_, experience)


class Caracteristiques(object):
    """ classe gérant l'ensemble des caractéristiques d'un personnage (*le
    controller et la vue doivent géré les XP dans les dériver.
    """

    def __init__(self):
        """ initialization
        """
        # force < taill + 4 géré par controleur
        # taille exp = None géré par controleur
        self._tab = {"Taille": Caracteristique("Taille", 10, 15),
                     "Apparence": Caracteristique("Apparence"),
                     "Constitution": Caracteristique("Constitution", 10, 20),
                     "Force": Caracteristique("Force", 10, 14),
                     "Agilité": Caracteristique("Agilité", 10, 20),
                     "Dextérité": Caracteristique("Dextérité", 10, 20),
                     "Perception": Caracteristique("Perception", 10, 20),
                     "Vue": Caracteristique("Vue", 10, 20),
                     "Ouïe": Caracteristique("Ouïe", 10, 20),
                     "Odorat-Gout": Caracteristique("Odorat-Gout", 10, 20),
                     "Volonté": Caracteristique("Volonté"),
                     "Itellect": Caracteristique("Itellect"),
                     "Empathie": Caracteristique("Empathie"),
                     "Rêve": Caracteristique("Rêve"),
                     "Chance": Caracteristique("Chance")}
        self._tab["Taille"].value_changed.connect(self.caracteristique_changed)

    def caracteristique_changed(self, name):
        """ slot pour changement de caractéristique.
        """
        if name == "Taille":
            self._tab["Force"].max = self._tab["Taille"] + 4

    def __getitem__(self, key):
        if key == "Mêlée":
            return (int(self["Force"]) + int(self["Agilité"])) // 2
        elif key == "Tir":
            return (int(self["Vue"]) + int(self["Dextérité"])) // 2
        elif key == "Lancer":
            return (int(self["Tir"]) + int(self["Force"])) // 2
        elif key == "Dérobée":
            return (int(self["Agilité"]) + (21 - int(self["Taille"]))) // 2
        else:
            return self._tab[key]


class Competance(OptionEvolutive):

    base_tab = {-10: 5, -9: 5, -8: 5, -7: 10, -6: 10, -5: 10, -4: 10, -3: 15,
                -2: 15, -1: 15, 0: 15, 1: 20, 2: 20, 3: 20, 4: 20, 5: 30,
                6: 30, 7: 40, 8: 40, 9: 60, 10: 60}

    xp_tab = XpTab(base_tab, lambda x: 100)

    def __init__(self, name, valeur=0, max_=None, experience=None):
        """ initialisation
        """
        OptionEvolutive.__init__(self, name, valeur, max_, experience)


class CompetanceTron(Competance):
    """ représente une compétance liée à une, ou plus, autre.
    """

    def __init__(self, name, competance_lier, limite_lien=0):
        """ initialisation
        """
        self._limite_lien = limite_lien
        self._competance_lier = competance_lier
        Competance.__init__(self, name, competance_lier.valeur,
                            competance_lier.max, None)
        self.value_changed.connect(self.self_modifier)
        self._competance_lier.value_changed.connect(self.lien_modifier)

    def lien_modifier(self, _):
        """
        """
        if self._competance_lier.valeur <= self._limite_lien:
            self._valeur = self._competance_lier.valeur
        elif self.valeur < self._limite_lien:
            self._valeur = self._limite_lien

    def self_modifier(self, _):
        """
        """
        if (self.valeur <= self._limite_lien and
                self._competance_lier.valeur < self.valeur):
            self._competance_lier.valeur = self.valeur
        elif self._competance_lier.valeur < self.valeur:
            self._competance_lier.valeur = self._limite_lien


class CompetanceLimitee(Competance):
    """ représente une compétance limité par une autre.
    """
    def __init__(self, name, competance_limitante, valeur=-8, max_=None,
                 limite_lien=0):
        """ initialisation
        """
        self._limite_lien = limite_lien
        self._competance_limitante = competance_limitante
        Competance.__init__(self, name, valeur, max_, None)
        self.value_changed.connect(self.self_modifier)

    def self_modifier(self, _):
        """
        """
        if self._valeur >= self._limite_lien:
            self.value_changed.observer = []
        if self._valeur >= self._competance_limitante.valeur:
            self._valeur = self._competance_limitante.valeur


class Competances():
    def __init__(self):
        """ initialisation
        """
        self._c_generales = {"Bricollage": Competance("Bricollage", -4),
                             "Chant": Competance("Chant", -4),
                             "Course": Competance("Course", -4),
                             "Cuisine": Competance("Cuisine", -4),
                             "Danse": Competance("Danse", -4),
                             "Dessin": Competance("Dessin", -4),
                             "Discretion": Competance("Discretion", -4),
                             "Escalade": Competance("Escalade", -4),
                             "Saut": Competance("Saut", -4),
                             "Séduction": Competance("Séduction", -4),
                             "Vigilance": Competance("Vigilance", -4)}
        srv = "Survie en "
        srv_ext = Competance(srv + "Extérieur", -8)
        self._c_particulieres = {"Charpenterie": Competance("Charpenterie",
                                                            -8),
                                 "Comédie": Competance("Comédie", -8),
                                 "Commerce": Competance("Commerce", -8),
                                 "Equitation": Competance("Equitation", -8),
                                 "Maçonnerie": Competance("Maçonnerie", -8),
                                 "Pickpocket": Competance("Pickpocket", -8),
                                 srv + "Cité": Competance(srv + "Cité", -8),
                                 srv + "Extérieur": srv_ext,
                                 srv + "Désert":
                                 CompetanceLimitee(srv + "Désert", srv_ext),
                                 srv + "Forêt":
                                 CompetanceLimitee(srv + "Forêt", srv_ext),
                                 srv + "Glaces":
                                 CompetanceLimitee(srv + "Glaces", srv_ext),
                                 srv + "Marais":
                                 CompetanceLimitee(srv + "Marais", srv_ext),
                                 srv + "Montagne":
                                 CompetanceLimitee(srv + "Montagne", srv_ext),
                                 srv + "Sous-sols":
                                 CompetanceLimitee(srv + "Sous-sols", srv_ext),
                                 "Travestissement":
                                 Competance("Travestissement", -8)}
        self._c_specialse = {"Acrobatie": Competance("Acrobatie", -11),
                             "Chirurgie": Competance("Chirurgie", -11),
                             "Jeu": Competance("Jeu", -11),
                             "Jonglerie": Competance("Jonglerie", -11),
                             "Maroquinerie": Competance("Maroquinerie", -11),
                             "Métallurgie": Competance("Métallurgie", -11),
                             "Natation": Competance("Natation", -11),
                             "Navigation": Competance("Navigation", -11),
                             "Orfèvrerie": Competance("Orfèvrerie", -11),
                             "Serrurerie": Competance("Serrurerie", -11)}
        self._connaissances = {"Alchimie": Competance("Alchimie", -11),
                               "Astrologie": Competance("Astrologie", -11),
                               "Botanique": Competance("Botanique", -11),
                               "Écriture": Competance("Écriture", -11),
                               "Légendes": Competance("Légendes", -11),
                               "Médecine": Competance("Médecine", -11),
                               "Zoologie": Competance("Zoologie", -11)}
        self._draconic = {"Oniros": Competance("Oniros", -11),
                          "Hypnos": Competance("Hypnos", -11),
                          "Narcos": Competance("Narcos", -11),
                          "Thanatos": Competance("Thanatos", -11)}
        epee = Competance("Epée 1 main", -6)
        dague = Competance("Dague de mélée", -6)
        hache = Competance("Hache 1 main", -6)
        masse = Competance("Masse 1 main", -6)
        self._c_combat = {"Armes d’hast": Competance("Armes d’hast", -6),
                          "Bouclier": Competance("Bouclier", -6),
                          "Dague de mélée": dague,
                          "Corp à corp": CompetanceTron("Corp à corp", dague),
                          "Esquive": CompetanceTron("Esquive", dague),
                          "Epée 1 main": epee,
                          "Epée 2 main": CompetanceTron("Epée 2 main", epee),
                          "Hache 1 main": hache,
                          "Hache 2 main": CompetanceTron("Hache 2 main",
                                                         hache),
                          "Lance": Competance("Lance", -6),
                          "Masse 1 main": masse,
                          "Masse 2 main": CompetanceTron("Masse 2 main", masse)
                          }
        self._c_tir_lance = {"Arbalète": Competance("Arbalète", -8),
                             "Arc": Competance("Arc", -8),
                             "Fronde": Competance("Fronde", -8),
                             "Hache de lancer": Competance("Hache de lancer",
                                                           -8),
                             "Fouet": Competance("Fouet", -8),
                             "Dague de jets": Competance("Dague de jets", -8)}
        self._all = {**self._c_generales, **self._c_particulieres,
                     **self._c_specialse, **self._connaissances,
                     **self._draconic, **self._c_combat, **self._c_tir_lance}

    def __getitem__(self, key):
        """ get a competence by name
        """
        return self._all[key]

    def __setitem__(self, key, value):
        """ get a competence by name
        """
        self._all[key] = value
