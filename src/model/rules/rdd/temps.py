#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion du temps.

    :platform: Unix, Windows
    :synopsis: gestion du temps

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from enum import Enum
from pint import UnitRegistry

ureg = UnitRegistry()
ureg.load_definitions('unit_reg.txt')


class heures(Enum):
    """ enumeration des heures de reve de dragon
    """
    vaisseau = 1
    sirene = 2
    faucon = 3
    couronne = 4
    dragon = 5
    epee = 6
    lyre = 7
    serpent = 8
    poisson_ac = 9
    araigne = 10
    roseau = 11
    chateau_dormant = 12


class tache(object):
    """ action sur la durée
    """
    def __init__(self, pt_tache, difficulte, periodicite):
        """ initialisation
        """
        self._pt_tache = pt_tache
        self._pt_effectue = 0
        self._difficulte = difficulte
        self._periodicite = periodicite

    def add_action(self, action):
        """ ajouté une action sur la tache
        """
        self._pt_effectue += action.p_tache

    @property
    def finish(self):
        return self._pt_effectue >= self._pt_tache

    @property
    def periodicite(self):
        return self._periodicite

    @property
    def difficulte(self):
        return self._difficulte
