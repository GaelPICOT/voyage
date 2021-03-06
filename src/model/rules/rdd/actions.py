#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion des actions. ainsi que point de tâches et de
qualités.

    :platform: Unix, Windows
    :synopsis: gestion des actions

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import math
import dice
from model.rules.rdd.temps import DateTime, ureg


class Action(object):
    """ resultat d'une action
    """
    def __init__(self, personnage, carac=10, competence=0, ajustement=0,
                 lancer=None, debut=DateTime(), duree=1*ureg.minute,
                 ignore_etat_g=False):
        """ init
        """
        if isinstance(carac, str):
            self._carac_name = carac
            carac = personnage.caracteristiques[carac].valeur
        else:
            self._carac_name = ""
        if isinstance(competence, str):
            self._cmp_name = competence
            carac = personnage.competances[competence].valeur
        else:
            self._cmp_name = ""
        self._pc_reussit = 0
        # competance
        self._carac = carac
        # ajustement
        if personnage is not None and not ignore_etat_g:
            self._ajst = ajustement + competence + personnage.etat_general
        else:
            self._ajst = ajustement + competence
        # roll
        self.roll(lancer)
        # time to start
        self._debut = debut
        # durée de l'action
        self._duree = duree
        # save the personnage
        self._personnage = personnage
        if personnage is not None:
            personnage.add_event(self)

    def roll(self, lancer=None):
        """ roll dice again
        """
        if lancer is None:
            self._lancer = dice.roll("1d100+0")
        else:
            self._lancer = lancer
        if self._ajst >= -8:
            self._pc_reussit = (self._carac * (self._ajst + 10)) // 2
        elif self._ajst >= -10:
            self._pc_reussit = self._carac // (self._ajst * 2)
        elif self._ajst > -17:
            self._pc_reussit = 1
        else:
            self._pc_reussit = 0
        self._reusite = self._pc_reussit >= self._lancer
        if self._pc_reussit >= 100:
            self._reusite = self._lancer == 100
        # réussite particulière
        self._r_part = self._lancer <= math.ceil(self._pc_reussit*0.2)
        # réussite significative
        self._r_sign = self._lancer <= math.floor(self._pc_reussit*0.5)
        # échec particulière
        self._e_part = self._lancer >= 100 - math.floor((100-self._pc_reussit)
                                                        * 0.2)
        # échec total
        self._e_tot = self._lancer > 100 - math.floor((100-self._pc_reussit) *
                                                      0.1)
        if self._ajst <= -11:
            self._r_part = False
            self._r_sign = False
            self._e_part = not self._reusite
            if self._ajst == -11:
                self._e_tot = self._lancer >= 90
            elif self._ajst == -12:
                self._e_tot = self._lancer >= 70
            elif self._ajst == -13:
                self._e_tot = self._lancer >= 50
            elif self._ajst == -14:
                self._e_tot = self._lancer >= 30
            elif self._ajst == -15:
                self._e_tot = self._lancer >= 10
            elif self._ajst == -16:
                self._e_tot = self._lancer >= 2
            else:
                self._e_tot = self._lancer >= 1

    @property
    def duree(self):
        """ durée de l'action
        """
        return self._duree

    @property
    def carac_name(self):
        """ carcteristique name
        """
        return self._carac_name

    @property
    def cmp_name(self):
        """ competence name
        """
        return self._cmp_name

    @property
    def p_qualite(self):
        """ return nombre de point de qualité
        """
        if self._e_tot:
            return -6
        elif self._e_part:
            return -4
        elif not self._reusite:
            return -2
        elif self._r_part:
            return 2
        elif self._r_sign:
            return 1
        else:
            return 0

    @property
    def p_tache(self):
        """ return nombre de point de qualité
        """
        if self._e_tot:
            return -4
        elif self._e_part:
            return -2
        elif not self._reusite:
            return 0
        elif self._r_part:
            return 3
        elif self._r_sign:
            return 2
        else:
            return 1

    @property
    def lancer(self):
        """ property for roll result
        """
        return self._lancer

    @property
    def reussite(self):
        """ property pour accédé à la réussi ou non de l'action
        """
        return self._reusite

    @property
    def r_part(self):
        """ property pour accédé à la réussi particulière de l'action
        """
        return self._r_part

    @property
    def r_sign(self):
        """ property pour accédé à la réussi sgnificative de l'action
        """
        return self._r_sign

    @property
    def e_part(self):
        """ property pour accédé à l'échec particulier de l'action
        """
        return self._e_part

    @property
    def e_tot(self):
        """ property pour accédé à à l'échec total de l'action
        """
        return self._e_tot

    @property
    def debut(self):
        """ return début de l'action
        """
        return self._debut
