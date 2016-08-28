#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la gestion des compétance.

    :platform: Unix, Windows
    :synopsis: gestion des compétance

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import dice
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


class Caracteristique(object):
    """ représente une caracteristique
    """

    value_changed = obs.Observable()

    base_tab = {7: 6, 8: 6, 9: 7, 10: 7, 11: 8, 12: 8, 13: 9, 14: 9, 15: 10,
                16: 20}

    xp_tab = XpTab(base_tab, lambda x: (x - 14) * 10)

    def __init__(self, name, valeur=10, max_=None, experience=None):
        """ initialization
        """
        #: nom caracteristique
        self._name = name
        #: valeur de la caractéristique
        self._valeur = valeur
        #: expérinece dans la caractéristique
        if experience is None:
            self._exp = Experience(self, Caracteristique.xp_tab)
        else:
            self._exp = experience
        #: si la caractéristique et physique (limité à 20)
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


class Competance(object):
    base_tab = {-10: 5, -9: 5, -8: 5, -7: 10, -6: 10, -5: 10, -4: 10, -3: 15,
                -2: 15, -1: 15, 0: 15, 1: 20, 2: 20, 3: 20, 4: 20, 5: 30,
                6: 30, 7: 40, 8: 40, 9: 60, 10: 60}

    xp_tab = XpTab(base_tab, lambda x: 100)

    def __init__(self, name, valeur=0):
        self._name = name
        self._valeur = valeur
