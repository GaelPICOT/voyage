#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la création et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import dice
import model.temps
import math
from model.competance import Caracteristiques, Competances


class FatigueSegmet(object):
    """ modelise un segment de fatique
    """
    def __init__(self, size=5):
        """ initialisation
        """
        self._size = size
        self._used = 0


class FatigueCount(object):
    """ conteur de fatigue
    """
    def __init__(self):
        """ initialisation
        """
        self._segments = {0: [FatigueSegmet(2), FatigueSegmet(3),
                              FatigueSegmet(3)],
                          -1: [FatigueSegmet(2), FatigueSegmet(3),
                               FatigueSegmet(3)],
                          -2: FatigueSegmet(2),
                          -3: FatigueSegmet(3),
                          -4: FatigueSegmet(3),
                          -5: FatigueSegmet(2),
                          -6: FatigueSegmet(3),
                          -7: FatigueSegmet(3)
                          }
        self._malus = 0

    def recalculate_seg(self, endurence=15):
        """ (re)calculate segment
        """


class Personnage(object):
    """ objet permétant de créé un personnage.
    """
    def __init__(self):
        self._carac = Caracteristiques()
        self._competances = Competances()
        self._fatigue = FatigueCount()
        # points
        self._points = {}
        # seuils
        self._seuils = {}
        # ajout gestion vie est endurence
        self._carac["Taille"].value_changed.connect(self.calculate_vie)
        self._carac["Constitution"].value_changed.connect(self.calculate_vie)
        self._carac["Volonté"].value_changed.connect(self.calculate_vie)
        self.calculate_vie()
        # ajout gestion rêve
        self._carac["Rêve"].value_changed.connect(self.calculate_reve)
        self.calculate_reve()
        # + dom et enc
        self._carac["Taille"].value_changed.connect(self.calculate_p_dom)
        self._carac["Force"].value_changed.connect(self.calculate_p_dom)
        self.calculate_p_dom()
        # signe particulier
        # heure de naissance
        self._h_nais = model.temps.heures.vaisseau
        # age
        self._age = 18
        if dice.roll("1d12").pop() == 1:
            self._mainhand = "ambidextre"
        else:
            self._mainhand = "droite"

    def calculate_p_dom(self, _=None):
        """ (re)calculate +dom et encombrement
        """
        taille = self._carac["Taille"].valeur
        force = self._carac["Force"].valeur
        enc = (taille + force)/2
        # seuil d'encombrement
        self._seuils["Encombrement"] = enc
        # +dom
        if enc < 8:
            self._seuils["+dom"] = -1
        elif enc < 12:
            self._seuils["+dom"] = 0
        elif enc < 14:
            self._seuils["+dom"] = 1
        else:
            self._seuils["+dom"] = 2

    def calculate_reve(self, _=None):
        """ (re)calculate reve et seuil
        """
        if "Rêve" not in self._points.keys():
            # points de rêve
            self._points["Rêve"] = self._carac["Rêve"].valeur
            # seuil de rêve
            self._seuils["Rêve"] = self._points["Rêve"]
        else:
            if self._points["Rêve"] < self._carac["Rêve"].valeur:
                self._points["Rêve"] = self._carac["Rêve"].valeur
            if self._seuils["Rêve"] < self._carac["Rêve"].valeur:
                self._seuils["Rêve"] = self._carac["Rêve"].valeur

    def calculate_vie(self, _=None):
        """ (re)calcule la vie et la constitution et les seuilles en lien
        """
        # endurence potentiel 1
        const = self._carac["Constitution"].valeur
        taille = self._carac["Taille"].valeur
        end1 = taille + const
        # points de vie
        self._points["Vie"] = math.ceil(end1 / 2)
        # points d'endurence
        end2 = self._points["Vie"] + self._carac["Volonté"].valeur
        if end2 >= end1:
            self._points["Endurence"] = end2
        else:
            self._points["Endurence"] = end1
        self._fatigue.recalculate_seg(self._points["Endurence"])
        # seuil de constitution
        if const < 9:
            self._seuils["Constitution"] = 2
        elif const < 12:
            self._seuils["Constitution"] = 3
        elif const < 15:
            self._seuils["Constitution"] = 4
        else:
            self._seuils["Constitution"] = 5
        # seuil de sustentation
        if taille < 10:
            self._seuils["Sustentation"] = 2
        elif taille < 14:
            self._seuils["Sustentation"] = 3
        else:
            self._seuils["Sustentation"] = 4

    def passe_chateau_dormant(self):
        """ passage de chateau dormant
        """
        if self._points["Rêve"] > self._seuils["Rêve"]:
            self._points["Rêve"] -= 1

    @property
    def points(self):
        """ property to acces to points
        """
        return self._points

    @property
    def ceuils(self):
        """ property to acces to seuils
        """
        return self._seuils

    @property
    def main_principale(self):
        """ property pour la main principale
        """
        return self._mainhand

    @property
    def caracteristiques(self):
        """ property pour accédé aux caracteristiques
        """
        return self._carac

    @property
    def competances(self):
        """
        """
        return self._competances
