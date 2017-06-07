#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la création et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import dice
import math
from model.competance import Caracteristiques, Competances


class Personnage(object):
    """ objet permétant de créé un personnage.
    """
    def __init__(self):
        self._caracteristiques = Caracteristiques()
        self._competances = Competances()
        # points
        self._points = {}
        # points de rêve
        self._points["Rêve"] = self._caracteristiques["Rêve"].valeur
        self.calculate_vie_const()
        # seuils
        self._seuils = {}
        # seuil d'encombrement
        self._seuils["Encombrement"] = 0
        # seuil de sustentation
        self._seuils["Sustentation"] = 0
        # seuil de constitution
        self._seuils["Constitution"] = 0
        # seuil de rêve
        self._seuils["Rêve"] = self._points["Rêve"]
        # +dom
        self._seuils["+dom"] = 0
        # signe particulier
        # heure de naissance
        self._h_nais = 0
        # age
        self._age = 18
        if dice.roll("1d12").pop() == 1:
            self._mainhand = "ambidextre"
        else:
            self._mainhand = "droite"

    def calculate_vie_const(self, _=None):
        """ re calcule la vie et la constitution
        """
        # endurence potentiel 1
        end1 = (self._caracteristiques["Taille"].valeur +
                self._caracteristiques["Constitution"].valeur)
        # points de vie
        self._points["Vie"] = end1 / 2
        self._points["Vie"] = math.ceil(self._points["Vie"])
        # points d'endurence
        end2 = self._points["Vie"] + self._caracteristiques["Volonté"].valeur
        if end2 >= end1:
            self._points["Endurence"] = end2
        else:
            self._points["Endurence"] = end1

    def passe_chateau_dormant(self):
        """ passage de chateau dormant
        """
        if self._points["Rêve"] > self._seuils["Rêve"]:
            self._points["Rêve"] -= 1

    @property
    def main_principale(self):
        """ property pour la main principale
        """
        return self._mainhand

    @property
    def caracteristiques(self):
        """ property pour accédé aux caracteristiques
        """
        return self._caracteristiques

    @property
    def competances(self):
        """
        """
        return self._competances
