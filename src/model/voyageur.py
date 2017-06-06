#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la création et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import dice
from model.competance import Caracteristiques, Competances


class Personnage(object):
    """ objet permétant de créé un personnage.
    """
    def __init__(self):
        self._caracteristiques = Caracteristiques()
        self._competances = Competances()
        if dice.roll("d12").pop() == 1:
            self._mainhand = "ambidextre"
        else:
            self._mainhand = "droite"

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
