#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour la création de personnage.

    :platform: Unix, Windows
    :synopsis: création de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from model.rules.rdd.voyageur import Personnage


class PersonnageCreateur(object):
    """ créateur de personnage
    """
    def __init__(self):
        """ init
        """
        self._personnage_courrant = Personnage()
        # point de carctéristique restant
        self._point_carac = 20
        # point d'expérience pour compétence restant
        self._point_comp = 3000
        # point de sort utilisé
        self._point_sort = 0
        # argent de départ en denier
        self._agent = 5000

    @property
    def personnage(self):
        """ renvoi le personnage
        """
        return self._personnage_courrant
