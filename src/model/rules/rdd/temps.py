#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion du temps.

    :platform: Unix, Windows
    :synopsis: gestion du temps

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from enum import Enum
from pint import UnitRegistry
import os


current_rep = os.path.abspath(os.path.split(__file__)[0])

ureg = UnitRegistry()
ureg.load_definitions(current_rep + '/unit_reg.txt')


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


class DateTime(object):
    """ moment precis
    """
    def __init__(self, moi=heures.vaisseau, heure=heures.vaisseau, minutes=0,
                 annee=1000):
        """ init
        """
        self._moi = moi
        self._heure = heure
        self._minutes = minutes
        self._annee = annee  # année depuits début 3ième age
        self._timestamp = self._heure.value * ureg.heure
        self._timestamp += self._minutes * ureg.minute
        self._timestamp += self._moi.value * ureg.moi
        self._timestamp += self._annee * ureg.annee

    @property
    def saison(self):
        """ return season
        """
        if self._moi in [heures.vaisseau, heures.sirene, heures.faucon]:
            return "printemps"
        elif self._moi in [heures.couronne, heures.dragon, heures.epee]:
            return "été"
        elif self._moi in [heures.lyre, heures.serpent, heures.poisson_ac]:
            return "automne"
        elif self._moi in [heures.araigne, heures.roseau,
                           heures.chateau_dormant]:
            return "hiver"
        else:
            raise TypeError("le moi n'est pas exprimer correctement")


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
        self._nb_periodes = 0

    def add_action(self, action):
        """ ajouté une action sur la tache
        """
        if not self.finish:
            self._nb_periodes += 1
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
